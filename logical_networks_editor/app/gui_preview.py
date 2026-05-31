# gui_preview.py

import dearpygui.dearpygui as dpg
import tools
import os


class GUIPreview:

    ## ------------------------------ Preview Callbacks --------------------------------

    def update_preview(self):
        self.save_snapshot(None, None)
        path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        # path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.json"
        
        if not os.path.exists(path):
            dpg.delete_item("preview_text", children_only=True)
            dpg.add_text("Preview not available.", parent="preview_text")
            return 1
        
        with open(path) as f:
            preview = f.read()
        
        self._render_lp_preview(preview)
        return 0

    def _render_lp_preview(self, lp_text):
        dpg.delete_item("preview_text", children_only=True)
        
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
            elif stripped.endswith("."):
                color = (220, 220, 220, 255)      # facts - white
            else:
                color = (160, 160, 160, 255)      # everything else - dim

            dpg.add_text(line if line else " ", parent="preview_text", color=color)
    
    def update_input_template(self):
        input_nodes = [nid for nid, n in self.NETWORK.nodes.items() if n["name"] == "INPUT"]
        lines = ["inputs = ["]
        
        for nid in input_nodes:
            val = self.NETWORK.nodes[nid]["val"]
            lines.append(f"    {val},  # {nid}")
        lines.append("]")
        
        dpg.set_value("input_script", "\n".join(lines))
        return 0
    
    def apply_inputs(self, sender, app_data):
        script = dpg.get_value("input_script")
        local = {}
        try:
            exec(script, {}, local)
            values = local.get("inputs", [])
        except Exception as e:
            print(f"Input script error: {e}")
            return 1
        
        input_nodes = [nid for nid, n in self.NETWORK.nodes.items() if n["name"] == "INPUT"]
        
        if len(values) != len(input_nodes):
            print(f"Expected {len(input_nodes)} inputs, got {len(values)}")
            return 1
        if any(v is None for v in values):
            print("All inputs must be set.")
            return 1
        
        for node_id, val in zip(input_nodes, values):
            self.NETWORK.nodes[node_id]["val"] = val
        
        self.update_preview()
        return 0
