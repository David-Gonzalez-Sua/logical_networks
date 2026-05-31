# gui_files.py

import dearpygui.dearpygui as dpg
import tools


class GUIFiles:

    ## ------------------------------ File Callbacks ------------------------------
    
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
            with dpg.window(label="Save Network", modal=True, tag="save_popup", no_resize=True):
                dpg.add_text("Enter network name:")
                dpg.add_input_text(tag="save_name_input")
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
        self.NETWORK.export_to_json(f"{path}/json/{name}.json")
        self.NETWORK.export_to_lp(f"{path}/{name}.lp")
        self.last_save_name = name
        dpg.delete_item("save_popup")
        return 0
    
    def load_network(self, sender, app_data):
        folder = tools.resource_path(self.CONFIG["paths"]["networks_folder"]) + "/json"
        if not os.path.exists(folder):
            print("No saved networks found.")
            return 1
        
        files = [f[:-5] for f in os.listdir(folder) if f.endswith(".json")]
        print(f"Available networks: {files}")
        
        with dpg.window(label="Load Network", modal=True, tag="load_popup", no_resize=True):
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
        return 0
    
    def save_gate(self, sender, app_data):
        if not hasattr(self, 'current_gate_in_editor') or self.current_gate_in_editor is None:
            print("No gate selected.")
            return
        name = self.current_gate_in_editor
        DEFAULT_GATES = {"INPUT", "OUTPUT"}
        if name in DEFAULT_GATES:
            print(f"Cannot save default gate {name}.")
            return
        content = dpg.get_value("gate_editor_box")
        path = self.REGISTRY[name]["file"]
        with open(path, "w") as f:
            f.write(content)
        dpg.configure_item("gate_editor_box", enabled=False)
        dpg.set_item_label("gate_edit_toggle", "Edit")
        return 0
