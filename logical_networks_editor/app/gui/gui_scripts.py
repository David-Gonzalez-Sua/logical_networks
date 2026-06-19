# gui_scripts.py

import dearpygui.dearpygui as dpg
import tools
import os


class GUIScripts:

    ## ------------------------- Input Scripts -------------------------

    def save_input_script_as(self, sender, app_data):
        pos = dpg.get_mouse_pos(local=False)
        try:
            if dpg.does_item_exist("save_input_script_popup"):
                dpg.delete_item("save_input_script_popup")
            with dpg.window(label="Save Input Script", modal=True, tag="save_input_script_popup", no_resize=True, pos=pos):
                dpg.add_text("Enter script name:")
                dpg.add_input_text(tag="save_input_script_name", default_value=getattr(self, 'current_input_script', '') or "")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save", callback=self._confirm_save_input_script)
                    dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("save_input_script_popup"))
        except Exception as e:
            print(f"Error with save dialog: {e}")
        return 0

    def _confirm_save_input_script(self, sender, app_data):
        name = dpg.get_value("save_input_script_name")
        if not name:
            return 1
        folder = tools.resource_path(self.CONFIG["paths"]["input_scripts_folder"])
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{name}.py")
        content = dpg.get_value("input_script")
        with open(path, "w") as f:
            f.write(content)
        self.current_input_script = name
        dpg.delete_item("save_input_script_popup")
        return 0

    def load_input_script_popup(self, sender, app_data):
        pos = dpg.get_mouse_pos(local=False)
        folder = tools.resource_path(self.CONFIG["paths"]["input_scripts_folder"])
        os.makedirs(folder, exist_ok=True)
        if dpg.does_item_exist("load_input_script_popup"):
            dpg.delete_item("load_input_script_popup")
        
        files = [f[:-3] for f in os.listdir(folder) if f.endswith(".py")]
        
        with dpg.window(label="Load Input Script", modal=True, tag="load_input_script_popup", no_resize=True, pos=pos):
            dpg.add_text("Select a script:")
            dpg.add_listbox(items=files, tag="load_input_script_listbox", num_items=min(len(files), 6) if files else 1)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Load", callback=self._confirm_load_input_script)
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("load_input_script_popup"))
        return 0

    def _confirm_load_input_script(self, sender, app_data):
        name = dpg.get_value("load_input_script_listbox")
        if not name:
            return 1
        
        folder = tools.resource_path(self.CONFIG["paths"]["input_scripts_folder"])
        path = os.path.join(folder, f"{name}.py")
        if not os.path.exists(path):
            dpg.delete_item("load_input_script_popup")
            return 1
        
        with open(path) as f:
            dpg.set_value("input_script", f.read())
        self.current_input_script = name
        dpg.delete_item("load_input_script_popup")
        self.apply_inputs(None, None)
        return 0

    def revert_input_script(self, sender, app_data):
        if self.current_input_script:
            folder = tools.resource_path(self.CONFIG["paths"]["input_scripts_folder"])
            path = os.path.join(folder, f"{self.current_input_script}.py")
            if os.path.exists(path):
                with open(path) as f:
                    dpg.set_value("input_script", f.read())
                self.apply_inputs(None, None)
                return 0
            else:
                self.current_input_script = None  # stale reference, fall through
        
        # fallback to the network's saved input script
        dpg.set_value("input_script", self.NETWORK.input_script)
        self.apply_inputs(None, None)
        return 0

    ## ------------------------- Output Scripts -------------------------

    def save_output_script_as(self, sender, app_data):
        pos = dpg.get_mouse_pos(local=False)
        try:
            if dpg.does_item_exist("save_output_script_popup"):
                dpg.delete_item("save_output_script_popup")
            current = self.NETWORK.output_script if hasattr(self.NETWORK, 'output_script') else "default"
            with dpg.window(label="Save Output Script", modal=True, tag="save_output_script_popup", no_resize=True, pos=pos):
                dpg.add_text("Enter script name:")
                dpg.add_input_text(tag="save_output_script_name", default_value=current)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save", callback=self._confirm_save_output_script)
                    dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("save_output_script_popup"))
        except Exception as e:
            print(f"Error with save dialog: {e}")
        return 0

    def _confirm_save_output_script(self, sender, app_data):
        name = dpg.get_value("save_output_script_name")
        if not name:
            return 1
        folder = tools.resource_path(self.CONFIG["paths"]["output_scripts_folder"])
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{name}.py")
        content = dpg.get_value("output_script_editor")
        with open(path, "w") as f:
            f.write(content)
        self.NETWORK.output_script = name
        dpg.delete_item("save_output_script_popup")
        return 0

    def load_output_script_popup(self, sender, app_data):
        pos = dpg.get_mouse_pos(local=False)
        folder = tools.resource_path(self.CONFIG["paths"]["output_scripts_folder"])
        os.makedirs(folder, exist_ok=True)
        if dpg.does_item_exist("load_output_script_popup"):
            dpg.delete_item("load_output_script_popup")
        
        files = [f[:-3] for f in os.listdir(folder) if f.endswith(".py")]
        
        with dpg.window(label="Load Output Script", modal=True, tag="load_output_script_popup", no_resize=True, pos=pos):
            dpg.add_text("Select a script:")
            dpg.add_listbox(items=files, tag="load_output_script_listbox", num_items=min(len(files), 6) if files else 1)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Load", callback=self._confirm_load_output_script)
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("load_output_script_popup"))
        return 0

    def _confirm_load_output_script(self, sender, app_data):
        name = dpg.get_value("load_output_script_listbox")
        if not name:
            return 1
        folder = tools.resource_path(self.CONFIG["paths"]["output_scripts_folder"])
        path = os.path.join(folder, f"{name}.py")
        if not os.path.exists(path):
            dpg.delete_item("load_output_script_popup")
            return 1
        with open(path) as f:
            dpg.set_value("output_script_editor", f.read())
        self.NETWORK.output_script = name
        dpg.delete_item("load_output_script_popup")
        return 0

    def revert_output_script(self, sender, app_data):
        name = self.NETWORK.output_script if hasattr(self.NETWORK, 'output_script') else "default"
        folder = tools.resource_path(self.CONFIG["paths"]["output_scripts_folder"])
        path = os.path.join(folder, f"{name}.py")
        if os.path.exists(path):
            with open(path) as f:
                dpg.set_value("output_script_editor", f.read())
        return 0
    