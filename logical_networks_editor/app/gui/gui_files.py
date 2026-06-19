# gui_files.py

import dearpygui.dearpygui as dpg
import importlib
import tools
import sys
import os


class GUIFiles:

    ## ------------------------------ Network Callbacks ------------------------------
    
    def save_snapshot(self, sender, app_data):
        path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"])
        self.NETWORK.export_to_json(f"{path}/preview.json")
        self.NETWORK.export_to_lp(f"{path}/preview.lp")
        return 0
    
    def quick_save(self, sender, app_data):
        if self.last_save_name:
            path = tools.resource_path(self.CONFIG["paths"]["networks_folder"])
            self.NETWORK.export_to_json(f"{path}/json/{self.last_save_name}.json")
            self.NETWORK.export_to_lp(f"{path}/{self.last_save_name}.lp")
        else:
            self.save_snapshot(sender, app_data)
        return 0
    
    def save_network_as(self, sender, app_data):
        try:
            pos = dpg.get_mouse_pos()
            if dpg.does_item_exist("save_popup"):
                dpg.delete_item("save_popup")

            with dpg.window(label="Save Network", modal=True, tag="save_popup", no_resize=True, pos=pos):
                dpg.add_text("Enter network name:")
                dpg.add_input_text(tag="save_name_input", default_value=self.last_save_name if self.last_save_name else "")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save", callback=self._confirm_save)
                    dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("save_popup"))
        except Exception as e:
            print(f"Error with save dialog: {e}")
        return 0

    def _confirm_save(self, sender, app_data):
        name = dpg.get_value("save_name_input")
        if not name:
            return 1
        path = tools.resource_path(self.CONFIG["paths"]["networks_folder"])
        self.NETWORK.input_script = dpg.get_value("input_script")

        self.NETWORK.export_to_json(f"{path}/json/{name}.json")
        self.NETWORK.export_to_lp(f"{path}/{name}.lp")
        self.last_save_name = name
        dpg.delete_item("save_popup")
        return 0
    
    def load_network(self, sender, app_data):
        pos = dpg.get_mouse_pos()
        folder = tools.resource_path(self.CONFIG["paths"]["networks_folder"]) + "/json"
        if not os.path.exists(folder):
            print("No saved networks found.")
            return 1
        if dpg.does_item_exist("load_popup"):
            dpg.delete_item("load_popup")
        
        files = [f[:-5] for f in os.listdir(folder) if f.endswith(".json")]
        # print(f"Available networks: {files}")
        
        with dpg.window(label="Load Network", modal=True, tag="load_popup", no_resize=True, pos=pos):
            dpg.add_text("Select a network:")
            dpg.add_listbox(items=files, tag="load_listbox", num_items=min(len(files), 6))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Load", callback=self._confirm_load)
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("load_popup"))
        return 0

    def _confirm_load(self, sender, app_data):
        name = dpg.get_value("load_listbox")
        if not name:
            return 1
        
        path = tools.resource_path(self.CONFIG["paths"]["networks_folder"]) + f"/json/{name}.json"
        self.NETWORK.load_from_json(path)
        self.last_save_name = name
        self.rebuild_from_network()
        dpg.delete_item("load_popup")
        
        dpg.set_value("input_script", self.NETWORK.input_script)
        self.apply_inputs(None, None)
        return 0
    
    ## ------------------------------ Gate Callbacks ------------------------------

    def save_gate(self, sender, app_data):
        gate_type = dpg.get_value("gate_editor_box").splitlines()[0].strip()[9:]
        DEFAULT_GATES = set(self.CONFIG["defaults"]["DEFAULT_GATES"])
        if gate_type in DEFAULT_GATES:
            self.show_error_popup(f"Cannot save a gate named '{gate_type}' — reserved default gate name.")
            return 1
        gate_type = gate_type.lower()
        
        content = dpg.get_value("gate_editor_box")
        path = tools.resource_path(self.CONFIG["paths"]["gates_folder"]) + f"/{gate_type}.lp"

        with open(path, "w") as f:
            f.write(content)
        
        # reload registry and rebuild gate list
        self.REGISTRY = tools.load_gates(self.CONFIG)
        dpg.delete_item("gate_list", children_only=True)
        self.build_gate_list()
        
        self.current_gate_in_editor = gate_type.upper()
        self._show_gate_readonly(content)
        return 0
    
    def delete_gate(self, sender, app_data, user_data):
        gate_type = self.current_gate_in_editor
        if gate_type is None:
            self.show_error_popup("No gate selected.")
            return 1

        DEFAULT_GATES = set(self.CONFIG["defaults"]["DEFAULT_GATES"])
        if gate_type in DEFAULT_GATES:
            self.show_error_popup(f"Cannot delete default gate '{gate_type}'.")
            return 1
        
        path = tools.resource_path(self.REGISTRY[gate_type]["file"])
        os.remove(path)
        
        # reload registry and rebuild gate list
        self.REGISTRY = tools.load_gates(self.CONFIG)
        dpg.delete_item("gate_list", children_only=True)
        self.build_gate_list()
        return 0

    ## ------------------------------ Preview Callbacks ------------------------------

    def save_preview_file(self, sender, app_data):
        selected = dpg.get_value("preview_selector")
        content = dpg.get_value("preview_editor")
        
        if selected == "LP":
            path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        elif selected == "JSON":
            path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.json"
        elif selected == "main.lp":
            path = tools.resource_path(self.CONFIG["paths"]["base_folder"]) + "/main.lp"
        
        with open(path, "w") as f:
            f.write(content)
        
        # back to readonly
        dpg.configure_item("preview_editor", enabled=False)
        dpg.hide_item("preview_save_btn")
        dpg.show_item("preview_edit_btn")
        self._show_preview_readonly(content)
        return 0
    
    ## ------------------------------ Output Script Callbacks ------------------------------

    def run_output_script(self, sender, app_data):
        output_script_name = self.NETWORK.output_script if hasattr(self.NETWORK, 'output_script') else "default"
        script_path = tools.resource_path(self.CONFIG["paths"]["output_scripts_folder"])
        if script_path not in sys.path:
            sys.path.insert(0, script_path)

        try:
            formatter = importlib.import_module(output_script_name)
            importlib.reload(formatter)  # reload in case of edits
            return formatter
        except Exception as e:
            print(f"[ERROR] Could not load output script: {e}")
            return None
