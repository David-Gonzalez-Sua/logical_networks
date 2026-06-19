# network_serializer.py
# Holds the Network class

'''Example of network organization: 
self.nodes = {
    "INPUT_1": {
        "type": "INPUT",
        "dpg_id": None,
        "inputs": None,          # no inputs, source node
        "outputs": [],           # list of (target_id, index)
        "val": None              # set by user before run
    },
    "NOT_1": {
        "type": "NOT",
        "dpg_id": None,
        "inputs": [None],        # fixed size, filled with source_id or None
        "outputs": [],           # list of (target_id, index)
        "val": None              # computed by Clingo, None until run
    },
    "OUTPUT_1": {
        "type": "OUTPUT",
        "dpg_id": None,
        "inputs": [None],        # single input
        "outputs": None,         # no outputs, sink node
        "val": None              # read from Clingo after run
    }
}

self.links = {
    dpg_link_id: (source_id, target_id, target_input_index)
    # e.g. 123:   ("INPUT_1", "NOT_1", 0)
    # e.g. 124:   ("NOT_1",   "OUTPUT_1", 0)
}'''

import json


class Network:
    def __init__(self):
        self.nodes = {}
        self.links = {}
        self.input_nodes = []  # list of node_ids that are inputs
        self.counts = {}  # for generating unique node IDs of each type
        self.output_script = "default"
        self.input_script = "inputs = [\n    # Inputs\n]"

    def add_node(self, node_id, node_type, max_inputs, dpg_id=None):
        try:
            if node_id in self.nodes:
                raise ValueError(f"Node ID {node_id} already exists.")
            
            self.nodes[node_id] = {
                "type": node_type,
                "dpg_id": dpg_id,
                "inputs": [None] * max_inputs,  # list of (source_id)
                "outputs": [],                  # list of (target_id)
                "val": None                     # computed value, None until run
            }

            if node_type == "INPUT":
                self.input_nodes.append(node_id)
        
        except Exception as e:
            print(f"Error adding node: {e}")
            return 1
        return 0
    
    def add_link(self, dpg_link_id, source_id, target_id, target_input_index):
        try:
            if source_id not in self.nodes:
                raise ValueError(f"Source node {source_id} does not exist.")
            if target_id not in self.nodes:
                raise ValueError(f"Target node {target_id} does not exist.")
            if target_input_index >= len(self.nodes[target_id]["inputs"]):
                raise ValueError(f"Target node {target_id} does not have input index {target_input_index}.")
            if self.nodes[target_id]["inputs"][target_input_index] is not None:
                raise ValueError(f"Target node {target_id} input index {target_input_index} is already occupied.")
            
            self.links[dpg_link_id] = (source_id, target_id, target_input_index)
            self.nodes[source_id]["outputs"].append(target_id)
            self.nodes[target_id]["inputs"][target_input_index] = source_id
        
        except Exception as e:
            print(f"Error adding link: {e}")
            return 1
        return 0

    def delete_link(self, dpg_link_id):
        try:
            if dpg_link_id not in self.links:
                raise ValueError(f"Link ID {dpg_link_id} does not exist.")
            
            source_id, target_id, _ = self.links[dpg_link_id]
            del self.links[dpg_link_id]
            self.nodes[source_id]["outputs"] = [out for out in self.nodes[source_id]["outputs"] if out != target_id]
            
            idx = self.nodes[target_id]["inputs"].index(source_id)
            self.nodes[target_id]["inputs"][idx] = None
        
        except Exception as e:
            print(f"Error deleting link: {e}")
            return 1
        return 0
        
    def delete_node(self, node_id):
        try:
            if node_id not in self.nodes:
                raise ValueError(f"Node ID {node_id} does not exist.")
            
            # Remove all links associated with this node using delete_link
            for link_id, (src, tgt, _) in list(self.links.items()):
                if src == node_id or tgt == node_id:
                    self.delete_link(link_id)

            if node_id in self.input_nodes:
                self.input_nodes.remove(node_id)

            del self.nodes[node_id]
        except Exception as e:
            print(f"Error deleting node: {e}")
            return 1
        return 0

    def export_to_json(self, path):
        try:
            export = {
                "nodes": {
                    node_id: {
                        "type": node["type"],
                        "inputs": node["inputs"],
                        "outputs": node["outputs"],
                        "val": node["val"]
                    }
                    for node_id, node in self.nodes.items()
                },
                "links": [
                    {"source": src, "target": tgt, "target_input_index": idx}
                    for src, tgt, idx in self.links.values()
                ],
                "output_script": self.output_script,
                "input_script": self.input_script
            }
            with open(path, "w") as f:
                json.dump(export, f, indent=2)
        
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return 1
        return 0

    def load_from_json(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            self.nodes = {}
            self.counts = {}
            self.links = {}
            self.input_nodes = []

            # rebuild nodes
            for node_id, node in data["nodes"].items():
                self.nodes[node_id] = {
                    "type": node["type"],
                    "dpg_id": None,
                    "inputs": node["inputs"],
                    "outputs": node["outputs"],
                    "val": node["val"]
                }

                # rebuild counts
                type = node["type"]
                parts = node_id.split("_", 1)
                if len(parts) == 2 and parts[-1].isdigit():
                    self.counts[type] = max(self.counts.get(type, 0), int(parts[1]))
                # num = int(node_id.split("_")[-1]) if "_" in node_id else 1
                # self.counts[type] = max(self.counts.get(type, 0), num)
            
            # rebuild links
            for i, link in enumerate(data["links"]):
                self.links[i] = (link["source"], link["target"], link["target_input_index"])

            # rebuild input nodes list
            self.input_nodes = [nid for nid, n in self.nodes.items() if n["type"] == "INPUT"]

            self.output_script = data.get("output_script", "default")
            self.input_script = data.get("input_script", "inputs = [\n    # Inputs\n]")
        
        except Exception as e:
            print(f"Error loading from JSON: {e}")
            return 1
        return 0

    def export_to_lp(self, path):
        try:
            with open(path, "w") as f:
                f.write("%% Network Structure""\n")
                
                f.write("%% Neurons:\n")
                f.write("% neuron(type, unique_id)\n")
                for node_id, node in self.nodes.items():
                    f.write(f'''neuron(\"{node['type']}\", \"{node_id}\").\n''')
                
                f.write("\n\n%% Edges:\n")
                f.write("% edge(source_id, target_id)\n")
                for src, tgt, idx in self.links.values():
                    f.write(f"edge(\"{src}\", \"{tgt}\").\n")

                f.write("\n\n%% Cardinality constraints:\n")
                f.write("% { edge(source_id, target_id) : neuron(type, target_id) } max_inputs.\n")
                for node_id, node in self.nodes.items():
                    max_inputs = len(node["inputs"])
                    if max_inputs > 0:
                        f.write(f"{{ edge(src, \"{node_id}\") : neuron(\"{node['type']}\", \"{node_id}\") }} {max_inputs}.\n")
                
                f.write("\n\n%% Values:\n")
                f.write("% val(neuron_id, value).\n")
                for node_id, node in self.nodes.items():
                    if node["val"] is not None:
                        f.write(f"val(\"{node_id}\", {node['val']}).\n")

        except Exception as e:
            print(f"Error exporting to LP: {e}")
            return 1
        return 0