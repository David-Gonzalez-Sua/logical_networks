# Tools for building the GUI using DearPyGui.
#

import dearpygui.dearpygui as dpg
import tomllib
import os

import network_serializer as network


class GUI:
    def __init__(self, CONFIG, REGISTRY, NETWORK):
        self.CONFIG = CONFIG
        self.REGISTRY = REGISTRY
        self.NETWORK = NETWORK

        # self.preview_path = self.CONFIG["paths"]["networks_folder"] + "/working_network.lp"
        # self.preview_path = "app/snapshots/preview.json"
        # self.preview_path = "app/snapshots/preview.lp"
        self.app_folder_path = "app/"

    def build_gui(self):
        CONFIG = self.CONFIG
        REGISTRY = self.REGISTRY
        # T = CONFIG["window"]["title"]
        W = CONFIG["window"]["width"]
        H = CONFIG["window"]["height"]

        with dpg.window(label="Gates", width=200, height=H-20, pos=(0,0), tag="sidebar"):
            dpg.add_text("Controls:\n- Click and drag to create links\n- Select and press Delete/Backspace to delete\n- Use arrow keys to pan\n- Click 'Recenter' to reset view")
            # dpg.add_button(label="Recenter", callback=self.recenter)
            dpg.add_button(label="Reorganize", callback=self.reorganize)

            dpg.add_text("Gates:")
            dpg.add_separator()
            for name, gate in REGISTRY.items():
                dpg.add_button(label=name, callback=self.add_gate_node, user_data=gate)
        
        with dpg.window(label="Canvas", width=W-400, height=H-20, pos=(200,0), tag="canvas"):
            with dpg.node_editor(
                tag="node_editor",
                callback=self.on_link_created,
                delink_callback=self.on_link_deleted):
                pass

        with dpg.window(label="Preview", width=200, height=H-20, pos=(W-200,0), tag="preview"):
            dpg.add_text("Logical Network Preview:")
            dpg.add_separator()
            dpg.add_text("", tag="preview_text")
            self.update_preview()
        return 0

    ## ------------------------------ Main Callbacks ------------------------------

    def add_gate_node(self, sender, app_data, user_data):
        gate = user_data
        name = gate["name"]
        
        self.NETWORK.counts[name] = self.NETWORK.counts.get(name, 0) + 1
        node_id = f"{name}_{self.NETWORK.counts[name]}"
        uid = dpg.generate_uuid()
        
        with dpg.node(label=node_id, parent="node_editor", tag=uid):
            for i in range(gate["inputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                    dpg.add_text("in")
            for i in range(gate["outputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text("out")
        
        self.NETWORK.add_node(node_id, name, gate["inputs"], uid)
        pos = self.get_free_position()
        dpg.set_item_pos(uid, pos)

        self.update_preview()
        return 0

    def on_link_created(self, sender, app_data):
        source_pin = app_data[0]
        target_pin = app_data[1]
        
        source_id = None
        target_id = None
        target_input_index = None

        for node_id, node in self.NETWORK.nodes.items():
            children = dpg.get_item_children(node["dpg_id"], slot=1)
            if source_pin in children:
                source_id = node_id
            if target_pin in children:
                target_id = node_id
                target_input_index = children.index(target_pin)

        link_uid = dpg.generate_uuid()
        dpg.add_node_link(source_pin, target_pin, parent="node_editor", tag=link_uid)
        self.NETWORK.add_link(link_uid, source_id, target_id, target_input_index)
        self.update_preview()
        return 0

    def on_link_deleted(self, sender, app_data):
        self.NETWORK.delete_link(app_data)
        dpg.delete_item(app_data)
        self.update_preview()
        return 0

    ## ------------------------------ Other Callbacks ------------------------------

    def delete_selected(self, sender, app_data):
        selected_nodes = dpg.get_selected_nodes("node_editor")
        selected_links = dpg.get_selected_links("node_editor")
        
        for node in selected_nodes:
            node_id = next(k for k, v in self.NETWORK.nodes.items() if v["dpg_id"] == node)
            self.NETWORK.delete_node(node_id)
            dpg.delete_item(node)
        
        for link in selected_links:
            self.NETWORK.delete_link(link)
            dpg.delete_item(link)
        
        self.update_preview()
        return 0
    
    def save_snapshot(self, sender, app_data):
        path = self.app_folder_path + "snapshots/"
        self.NETWORK.export_to_json(path + "preview.json")
        self.NETWORK.export_to_lp(path + "preview.lp")
        return 0
    
    ## ------------------------------ Utility Functions ------------------------------

    def update_preview(self):
        # path = self.CONFIG["paths"]["networks_folder"] + "/working_network.lp"
        self.save_snapshot(None, None)
        # path = self.app_folder_path + "snapshots/preview.json"
        path = self.app_folder_path + "snapshots/preview.lp"
        
        if not os.path.exists(path):
            dpg.set_value("preview_text", "Preview not available.")
            return 1
        
        with open(path) as f:
            preview = f.read()
        
        dpg.set_value("preview_text", preview)
        return 0
    
    def pan(self, dx, dy):
        for node_id, node in self.NETWORK.nodes.items():
            pos = dpg.get_item_pos(node["dpg_id"])
            dpg.set_item_pos(node["dpg_id"], [pos[0]+dx, pos[1]+dy])
        return 0

    def recenter(self):
        for node_id, node in self.NETWORK.nodes.items():
            dpg.set_item_pos(node["dpg_id"], [0, 0])
        return 0

    def reorganize(self):
        '''Longest path layering — Sugiyama et al. (1981)
           assigns each node to the layer of its furthest predecessor + 1'''
        if not self.NETWORK.nodes:
            return

        # step 1 - longest path layering
        layers = {}

        def get_layer(node_id):
            if node_id in layers:
                return layers[node_id]
            
            node = self.NETWORK.nodes[node_id]
            predecessors = [src for src in node["inputs"] if src is not None]
            
            if not predecessors:
                layers[node_id] = 0
            else:
                layers[node_id] = max(get_layer(p) for p in predecessors) + 1
            
            return layers[node_id]

        for node_id in self.NETWORK.nodes:
            get_layer(node_id)

        # step 2 - group by layer
        layer_groups = {}
        for node_id, layer in layers.items():
            layer_groups.setdefault(layer, []).append(node_id)

        # step 3 - position
        x_start = 50
        x_spacing = 200
        y_spacing = 150
        y_start = 50

        for layer, node_ids in sorted(layer_groups.items()):
            x = x_start + layer * x_spacing
            for i, node_id in enumerate(node_ids):
                y = y_start + i * y_spacing
                dpg.set_item_pos(self.NETWORK.nodes[node_id]["dpg_id"], [x, y])
        return 0

    def get_free_position(self):
        x_spacing = 150
        y_spacing = 100
        x_start = 20
        y_start = 20
        max_cols = 8

        occupied = set()
        for node in self.NETWORK.nodes.values():
            pos = dpg.get_item_pos(node["dpg_id"])
            if pos == [0, 0]:
                continue
            col = max(0, round((pos[0] - x_start) / x_spacing))
            row = max(0, round((pos[1] - y_start) / y_spacing))
            if 0 <= col < max_cols:
                occupied.add((col, row))

        row = 0
        while True:
            for col in range(max_cols):
                if (col, row) not in occupied:
                    return [x_start + col * x_spacing, y_start + row * y_spacing]
            row += 1

    def rebuild_from_network(self):
        try:
            dpg.delete_item("node_editor", children_only=True)
            
            # pass 1 - rebuild nodes
            for node_id, node in self.NETWORK.nodes.items():
                gate = self.REGISTRY[node["name"]]
                uid = dpg.generate_uuid()
                
                with dpg.node(label=node_id, parent="node_editor", tag=uid):
                    for i in range(gate["inputs"]):
                        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                            dpg.add_text("in")
                    for i in range(gate["outputs"]):
                        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                            dpg.add_text("out")
                
                self.NETWORK.nodes[node_id]["dpg_id"] = uid
            
            # pass 2 - rebuild links
            new_links = {}
            for _, (source_id, target_id, target_input_index) in self.NETWORK.links.items():
                source_uid = self.NETWORK.nodes[source_id]["dpg_id"]
                target_uid = self.NETWORK.nodes[target_id]["dpg_id"]
                
                source_children = dpg.get_item_children(source_uid, slot=1)
                target_children = dpg.get_item_children(target_uid, slot=1)
                
                source_out_pin = source_children[-1]
                target_in_pin = target_children[target_input_index]
                
                link_uid = dpg.generate_uuid()
                dpg.add_node_link(source_out_pin, target_in_pin, parent="node_editor", tag=link_uid)
                new_links[link_uid] = (source_id, target_id, target_input_index)
            
            self.NETWORK.links = new_links
            self.update_lp_preview()
            return 0
        
        except Exception as e:
            print(f"Error rebuilding from network: {e}")
