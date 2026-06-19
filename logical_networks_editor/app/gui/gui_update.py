# gui_updatepy

import dearpygui.dearpygui as dpg
import tools
import os


class GUIUpdate:

    ## ------------------------------ Preview Callbacks --------------------------------

    def update_preview(self):
        if dpg.does_item_exist("preview_selector") and dpg.get_value("preview_selector") != "LP":
            return 1
        
        self.save_snapshot(None, None)
        path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"

        if not os.path.exists(path):
            self._show_preview_readonly("Preview not available.")
            return 1
        with open(path) as f:
            content = f.read()

        if dpg.is_item_enabled("preview_editor"):
            dpg.set_value("preview_editor", content)
        else:
            self._show_preview_readonly(content)
        return 0
    
    def _show_preview_readonly(self, content):
        dpg.set_value("preview_editor", "")
        dpg.hide_item("preview_editor")
        dpg.delete_item("preview_colored", children_only=True)
        dpg.show_item("preview_colored")
        self._render_lp_preview(content)
        return 0

    def _render_lp_preview(self, lp_text):
        parent = "preview_colored" if dpg.does_item_exist("preview_colored") else "preview_text"
        dpg.delete_item(parent, children_only=True)
        
        for line in lp_text.split("\n"):
            stripped = line.strip()
            
            if stripped.startswith("%"):
                color = (120, 120, 120, 255)      # comments - gray
            elif ":-" in stripped:
                color = (100, 180, 255, 255)      # rules - blue
            elif stripped.startswith(":~"):
                color = (255, 180, 80, 255)       # weak constraints - orange
            elif stripped.startswith("#"):
                color = (255, 220, 50, 255)       # directives - yellow
            elif stripped.endswith(".") or stripped.endswith(","):
                color = (220, 220, 220, 255)      # facts - white
            else:
                color = (160, 160, 160, 255)      # everything else - dim

            dpg.add_text(line if line else " ", parent=parent, color=color)
        return 0
    
    ## ------------------------------ Input/Output Callbacks --------------------------------
    
    def update_input_template(self, sender=None, app_data=None):
        # reset all node vals first
        for node in self.NETWORK.nodes.values():
            node["val"] = None
        
        input_nodes = self.NETWORK.input_nodes
        lines = ["inputs = ["]
        for nid in input_nodes:
            lines.append(f"    None,  # {nid}")
        lines.append("]")
        template = "\n".join(lines)
        dpg.set_value("input_script", template)
        self.NETWORK.input_script = template
        self.current_input_script = None
        
        # update displays so pins go back to "in"/"out"
        for node_id in self.NETWORK.nodes:
            self.update_node_display(node_id)
        
        return 0
    
    def apply_inputs(self, sender, app_data):
        script = dpg.get_value("input_script")
        local = {}
        try:
            exec(script, {}, local)
            values = local.get("inputs", [])
        except Exception as e:
            self._log_error(f"Input script error: {e}")
            return 1
        
        input_nodes = self.NETWORK.input_nodes
        
        if len(values) != len(input_nodes):
            self._log_error(f"Expected {len(input_nodes)} inputs, got {len(values)}")
            return 1
        if any(v is None for v in values):
            self._log_error("All inputs must be set.")
        #     # return 1
        
        # reset all node values first
        for node_id in self.NETWORK.nodes:
            self.NETWORK.nodes[node_id]["val"] = None
        
        # apply new input values
        for node_id, val in zip(input_nodes, values):
            self.NETWORK.nodes[node_id]["val"] = val
        
        # update displays
        for node_id in self.NETWORK.nodes:
            self.update_node_display(node_id)

        self.update_preview()
        return 0

    def load_default_output_script(self, sender, app_data):
        try:
            default_output_path = tools.resource_path(self.CONFIG["paths"]["output_scripts_folder"]) + "/default.py"
            if os.path.exists(default_output_path):
                self.NETWORK.output_script = "default"
                with open(default_output_path) as f:
                    dpg.set_value("output_script_editor", f.read())
            return 0
        except Exception as e:
            print(f"Error loading default output script: {e}")
            return 1

    def _log_error(self, message):
        if dpg.does_item_exist("run_scripting"):
            dpg.add_text(message, parent="run_scripting", color=(255, 80, 80, 255), wrap=dpg.get_viewport_width() - 20)
            dpg.set_y_scroll("run_scripting", 99999)
        else:
            print(message)

    ## ------------------------------ Node Display Update --------------------------------

    def update_node_display(self, node_id):
        node = self.NETWORK.nodes[node_id]
        uid = node["dpg_id"]
        children = dpg.get_item_children(uid, slot=1)
        
        # update input pin labels
        for i, pin_id in enumerate(children[:-1]):  # all but last (output)
            src = node["inputs"][i]
            if src and self.NETWORK.nodes[src]["val"] is not None:
                val = self.NETWORK.nodes[src]["val"]
            else:
                val = "in"
            pin_children = dpg.get_item_children(pin_id, slot=1)
            if pin_children:
                dpg.set_value(pin_children[0], str(val))
        
        # update output pin label
        out_pin = children[-1]
        out_children = dpg.get_item_children(out_pin, slot=1)
        if out_children:
            val = ("    " + str(node["val"])) if node["val"] is not None else "  out"
            dpg.set_value(out_children[0], str(val))
