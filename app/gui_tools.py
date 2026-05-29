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
        self.PAN_MODE = False

        # self.preview_path = self.CONFIG["paths"]["networks_folder"] + "/working_network.lp"
        self.preview_path = "app/snapshots/preview.json"

    def build_gui(self):
        CONFIG = self.CONFIG
        REGISTRY = self.REGISTRY
        # T = CONFIG["window"]["title"]
        W = CONFIG["window"]["width"]
        H = CONFIG["window"]["height"]

        with dpg.window(label="Gates", width=200, height=H-20, pos=(0,0), tag="sidebar"):
            dpg.add_button(label="Pan Mode: OFF", tag="pan_button", callback=self.toggle_pan_mode)
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

    # def add_gate_node(self, sender, app_data, user_data):
    #     gate = user_data
    #     with dpg.node(label=gate["name"], parent="node_editor"):
    #         for i in range(gate["inputs"]):
    #             with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
    #                 dpg.add_text("in")
    #         for i in range(gate["outputs"]):
    #             with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
    #                 dpg.add_text("out")
    #         self.NETWORK.add_node(gate["name"] + "_" + str(len(self.NETWORK.nodes)), gate, gate["inputs"])
    #     return 0

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
        self.update_preview()
        return 0

    # def on_link_created(self, sender, app_data):
    #     dpg.add_node_link(app_data[0], app_data[1], parent="node_editor")
    #     self.update_preview()
    #     return 0

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
        dpg.delete_item(app_data)
        self.update_preview()
        return 0

    def update_preview(self):
        # path = self.CONFIG["paths"]["networks_folder"] + "/working_network.lp"
        self.save_snapshot(None, None)
        path = self.preview_path
        
        if not os.path.exists(path):
            dpg.set_value("preview_text", "Preview not available.")
            return 1
        with open(path) as f:
            preview = f.read()
        dpg.set_value("preview_text", preview)


        return 0
    
    def save_snapshot(self, sender, app_data):
        path = "app/snapshots/preview.json"
        self.NETWORK.export_to_json(path)
        return 0

    def delete_selected(self, sender, app_data):
        selected_nodes = dpg.get_selected_nodes("node_editor")
        selected_links = dpg.get_selected_links("node_editor")
        for node in selected_nodes:
            dpg.delete_item(node)
        for link in selected_links:
            dpg.delete_item(link)
        self.update_preview()
        return 0
    
    def toggle_pan_mode(self, sender, app_data):
        self.PAN_MODE = not self.PAN_MODE
        label = "Pan Mode: ON" if self.PAN_MODE else "Pan Mode: OFF"
        dpg.set_item_label("pan_button", label)
        return 0
    
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
