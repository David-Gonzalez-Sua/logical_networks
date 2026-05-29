# Example of organization: 
# self.nodes = {
#     "INPUT_1": {
#         "name": "INPUT",
#         "dpg_id": None,
#         "inputs": None,          # no inputs, source node
#         "outputs": [],           # list of (target_id, index)
#         "val": None              # set by user before run
#     },
#     "NOT_1": {
#         "name": "NOT",
#         "dpg_id": None,
#         "inputs": [None],        # fixed size, filled with source_id or None
#         "outputs": [],           # list of (target_id, index)
#         "val": None              # computed by Clingo, None until run
#     },
#     "OUTPUT_1": {
#         "name": "OUTPUT",
#         "dpg_id": None,
#         "inputs": [None],        # single input
#         "outputs": None,         # no outputs, sink node
#         "val": None              # read from Clingo after run
#     }
# }

# self.links = {
#     dpg_link_id: (source_id, target_id, target_input_index)
#     # e.g. 123:   ("INPUT_1", "NOT_1", 0)
#     # e.g. 124:   ("NOT_1",   "OUTPUT_1", 0)
# }

import json


class Network:
    def __init__(self):
        self.nodes = {}
        self.links = {}
        self.counts = {}  # for generating unique node IDs of each type

    def add_node(self, node_id, node_type, max_inputs, dpg_id=None):
        try:
            if node_id in self.nodes:
                raise ValueError(f"Node ID {node_id} already exists.")
            
            self.nodes[node_id] = {
                "name": node_type,
                "dpg_id": dpg_id,
                "inputs": [None] * max_inputs,  # list of (source_id)
                "outputs": [],                  # list of (target_id)
                "val": None                     # computed value, None until run
            }
        
        except Exception as e:
            print(f"Error adding node: {e}")
    
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

    def delete_node(self, node_id):
        try:
            if node_id not in self.nodes:
                raise ValueError(f"Node ID {node_id} does not exist.")
            
            # Remove all links associated with this node using delete_link
            for link_id, (src, tgt, _) in list(self.links.items()):
                if src == node_id or tgt == node_id:
                    self.delete_link(link_id)

            del self.nodes[node_id]
        
        except Exception as e:
            print(f"Error deleting node: {e}")

    def export_to_json(self, path):
        try:
            export = {
                "nodes": {
                    node_id: {
                        "name": node["name"],
                        "inputs": node["inputs"],
                        "outputs": node["outputs"],
                        "val": node["val"]
                    }
                    for node_id, node in self.nodes.items()
                },
                "links": [
                    {"source": src, "target": tgt, "target_input_index": idx}
                    for src, tgt, idx in self.links.values()
                ]
            }
            with open(path, "w") as f:
                json.dump(export, f, indent=2)
        
        except Exception as e:
            print(f"Error exporting to JSON: {e}")

    def load_from_json(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            self.nodes = {}
            self.links = {}

            for node_id, node in data["nodes"].items():
                self.nodes[node_id] = {
                    "name": node["name"],
                    "dpg_id": None,
                    "inputs": node["inputs"],
                    "outputs": node["outputs"],
                    "val": node["val"]
                }
            
            for i, link in enumerate(data["links"]):
                self.links[i] = (link["source"], link["target"], link["target_input_index"])
        
        except Exception as e:
            print(f"Error loading from JSON: {e}")