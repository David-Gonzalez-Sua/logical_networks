# Tools for building the GUI using DearPyGui.
import dearpygui.dearpygui as dpg
import tomllib
import os


class GUI:
    CONFIG = None
    REGISTRY = {}
    PAN_MODE = False

    def __init__(self, CONFIG, REGISTRY):
        self.CONFIG = CONFIG
        self.REGISTRY = REGISTRY

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
            self.update_lp_preview()
        return 0

    def add_gate_node(self, sender, app_data, user_data):
        gate = user_data
        with dpg.node(label=gate["name"], parent="node_editor"):
            for i in range(gate["inputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                    dpg.add_text("in")
            for i in range(gate["outputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text("out")
        return 0

    def on_link_created(self, sender, app_data):
        dpg.add_node_link(app_data[0], app_data[1], parent="node_editor")
        self.update_lp_preview()
        return 0

    def on_link_deleted(self, sender, app_data):
        dpg.delete_item(app_data)
        self.update_lp_preview()
        return 0

    def update_lp_preview(self):
        path = self.CONFIG["paths"]["networks_folder"] + "/working_network.lp"
        if not os.path.exists(path):
            dpg.set_value("preview_text", "Preview not available.")
            return 1
        with open(path) as f:
            preview = f.read()
        dpg.set_value("preview_text", preview)
        return 0

    def delete_selected(self, sender, app_data):
        selected_nodes = dpg.get_selected_nodes("node_editor")
        selected_links = dpg.get_selected_links("node_editor")
        for node in selected_nodes:
            dpg.delete_item(node)
        for link in selected_links:
            dpg.delete_item(link)
        self.update_lp_preview()
        return 0
    
    def toggle_pan_mode(self, sender, app_data):
        global PAN_MODE
        PAN_MODE = not PAN_MODE
        label = "Pan Mode: ON" if PAN_MODE else "Pan Mode: OFF"
        dpg.set_item_label("pan_button", label)
        return 0
