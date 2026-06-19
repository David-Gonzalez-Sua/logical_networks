# gui_window.py

import dearpygui.dearpygui as dpg
import sys
import os
import re

import tools


class GUIWindow:

    ## ------------------------ Window Utility Functions ---------------------------

    def on_viewport_resize(self):
        W = dpg.get_viewport_width()
        H = dpg.get_viewport_height()
        
        # Adjust Sidebar
        sidebar_w = self.CONFIG["window"]["sidebar_width"]
        input_script_h = self.CONFIG["window"]["input_script_height"]
        
        sidebar_content_h = H - 35
        min_gate_list_h = 150
        controls_text_h = 50
        input_section_h = input_script_h + 320
        
        gate_list_h = max(min_gate_list_h, sidebar_content_h - controls_text_h - input_section_h - 60)
        dpg.configure_item("gate_list", height=gate_list_h)

        output_buttons_width = 160 + 100 + 60 + 75 + 75 + 140 + 140 + 5 # rough estimate of all items in output header
        if dpg.does_item_exist("output_spacer"):
            dpg.configure_item("output_spacer", width=W - output_buttons_width)
        
        preview_w = self.CONFIG["window"]["preview_width"]
        sidebar_w = self.CONFIG["window"]["sidebar_width"]
        dpg.configure_item("toolbar", width=W)
        self._resize_for_output(W, H, self.output_shown)
        dpg.configure_item("sidebar", width=sidebar_w)
        dpg.configure_item("preview", width=preview_w, pos=(W-preview_w, 35))
        dpg.configure_item("canvas", width=W-sidebar_w-preview_w)
        return 0

    def show_error_popup(self, message):
        if dpg.does_item_exist("error_popup"):
            dpg.delete_item("error_popup")
        pos = dpg.get_mouse_pos(local=False)
        with dpg.window(label="Error", modal=True, tag="error_popup", no_resize=True, pos=pos):
            dpg.add_text(message, color=(255, 80, 80, 255), wrap=300)
            dpg.add_separator()
            dpg.add_button(label="Okay", width=80, callback=lambda: dpg.delete_item("error_popup"))
        return 0  

    def open_settings(self, sender, app_data):
        if dpg.does_item_exist("settings_popup"):
            dpg.delete_item("settings_popup")
        pos = dpg.get_mouse_pos(local=False)
        
        with dpg.window(label="Settings", modal=True, tag="settings_popup", no_resize=True, pos=pos, width=400, height=400):
            with dpg.tab_bar():
                with dpg.tab(label="Window"):
                    dpg.add_checkbox(label="Default to Formatted Output", tag="settings_default_formatted",
                                    default_value=self.CONFIG["extra"]["default_to_formatted_output"])
                    dpg.add_separator()
                    dpg.add_input_int(label="Preview Width", tag="settings_preview_width", default_value=self.CONFIG["window"]["preview_width"])
                    dpg.add_input_int(label="Sidebar Width", tag="settings_sidebar_width", default_value=self.CONFIG["window"]["sidebar_width"])
                    dpg.add_input_int(label="Output Height", tag="settings_output_height", default_value=self.CONFIG["window"]["output_height"])
                    dpg.add_input_int(label="Gate Editor Height", tag="settings_gate_editor_height", default_value=self.CONFIG["window"]["gate_editor_height"])
                    dpg.add_input_int(label="Input Script Height", tag="settings_input_script_height", default_value=self.CONFIG["window"]["input_script_height"])
                    dpg.add_input_int(label="Output Script Height", tag="settings_output_script_height", default_value=self.CONFIG["window"]["output_script_height"])
                    dpg.add_separator()
                    dpg.add_checkbox(label="Warn Before Editing Base Files", tag="settings_warn_base", default_value=self.CONFIG["window"]["warn_on_base_edit"])
                    dpg.add_checkbox(label="Warn Before Clearing Canvas", tag="settings_warn_clear", default_value=self.CONFIG["window"]["warn_on_clear_canvas"])
                
                with dpg.tab(label="Clingo"):
                    dpg.add_input_int(label="Max Solutions", tag="settings_max_solutions", default_value=self.CONFIG["clingo"]["max_solutions"])
                    dpg.add_input_int(label="Timeout (s)", tag="settings_timeout", default_value=self.CONFIG["clingo"]["timeout"])
                    dpg.add_text("Extra Files (one per line):")
                    dpg.add_input_text(tag="settings_extra_files", multiline=True, height=80, default_value="\n".join(self.CONFIG["clingo"].get("extra_files", [])))

            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Apply", callback=self._apply_settings, width=80)
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("settings_popup"), width=80)
        return 0

    def _apply_settings(self, sender, app_data):
        layout_changed = False
    
        layout_fields = {
            "preview_width": "settings_preview_width",
            "sidebar_width": "settings_sidebar_width",
            "output_height": "settings_output_height",
            "output_script_height": "settings_output_script_height",
            "gate_editor_height": "settings_gate_editor_height",
            "input_script_height": "settings_input_script_height",
        }
        
        for config_key, widget_tag in layout_fields.items():
            new_value = dpg.get_value(widget_tag)
            if self.CONFIG["window"][config_key] != new_value:
                layout_changed = True
            self.CONFIG["window"][config_key] = new_value

        self.CONFIG["clingo"]["max_solutions"] = dpg.get_value("settings_max_solutions")
        self.CONFIG["clingo"]["timeout"] = dpg.get_value("settings_timeout")
        extra_files_raw = dpg.get_value("settings_extra_files")
        self.CONFIG["clingo"]["extra_files"] = [f.strip() for f in extra_files_raw.split("\n") if f.strip()]
        
        self.CONFIG["extra"]["default_to_formatted_output"] = dpg.get_value("settings_default_formatted")
        self.CONFIG["window"]["warn_on_base_edit"] = dpg.get_value("settings_warn_base")
        self.CONFIG["window"]["warn_on_clear_canvas"] = dpg.get_value("settings_warn_clear")
        
        self._write_config_to_disk()
        dpg.delete_item("settings_popup")

        if layout_changed:
            dpg.set_frame_callback(dpg.get_frame_count() + 2, lambda: self._show_restart_required_popup(None, None))
        return 0

    def _write_config_to_disk(self):
        config_path = tools.resource_path("app/config.toml")
        with open(config_path, "r") as f:
            content = f.read()
        
        def replace_value(content, key, value):
            if isinstance(value, bool):
                value_str = "true" if value else "false"
            elif isinstance(value, str):
                value_str = f'"{value}"'
            else:
                value_str = str(value)
            pattern = rf"^{key}\s*=.*$"
            return re.sub(pattern, f"{key} = {value_str}", content, flags=re.MULTILINE)
        
        content = replace_value(content, "max_solutions", self.CONFIG["clingo"]["max_solutions"])
        content = replace_value(content, "timeout", self.CONFIG["clingo"]["timeout"])
        
        extra_files_list = self.CONFIG["clingo"].get("extra_files", [])
        extra_files_str = "[" + ", ".join(f'"{f}"' for f in extra_files_list) + "]"
        content = re.sub(r"^extra_files\s*=.*$", f"extra_files = {extra_files_str}", content, flags=re.MULTILINE)
        
        content = replace_value(content, "default_to_formatted_output", self.CONFIG["extra"]["default_to_formatted_output"])
        content = replace_value(content, "preview_width", self.CONFIG["window"]["preview_width"])
        content = replace_value(content, "sidebar_width", self.CONFIG["window"]["sidebar_width"])
        content = replace_value(content, "output_height", self.CONFIG["window"]["output_height"])
        content = replace_value(content, "gate_editor_height", self.CONFIG["window"]["gate_editor_height"])
        content = replace_value(content, "input_script_height", self.CONFIG["window"]["input_script_height"])
        content = replace_value(content, "output_script_height", self.CONFIG["window"]["output_script_height"])
        content = replace_value(content, "warn_on_base_edit", self.CONFIG["window"]["warn_on_base_edit"])
        content = replace_value(content, "warn_on_clear_canvas", self.CONFIG["window"]["warn_on_clear_canvas"])
        
        with open(config_path, "w") as f:
            f.write(content)
        return 0
    
    def _show_restart_required_popup(self, sender, app_data):
        print("Made it into _show_restart_required_popup.")
        pos = dpg.get_mouse_pos(local=False)
        if dpg.does_item_exist("restart_popup"):
            dpg.delete_item("restart_popup")
        
        with dpg.window(label="Restart Required", modal=True, tag="restart_popup", no_resize=True, pos=pos):
            print(f"popup pos: {pos}, viewport: {dpg.get_viewport_width()}x{dpg.get_viewport_height()}")
            dpg.add_text("Layout changes require a restart to take effect.", color=(255, 180, 80, 255))
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Restart Now", width=100, callback=self._restart_app)
                dpg.add_button(label="Later", width=80, callback=lambda: dpg.delete_item("restart_popup"))
        print("Exiting _show_restart_required_popup.")
        return 0
    
    def _restart_app(self, sender, app_data):
        dpg.stop_dearpygui()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def show_help_popup(self, sender, app_data):
        if dpg.does_item_exist("help_popup"):
            dpg.delete_item("help_popup")
        pos = dpg.get_mouse_pos(local=False)
        
        with dpg.window(label="Help", modal=True, tag="help_popup", no_resize=True, pos=pos, width=550, height=500):
            with dpg.tab_bar():
                with dpg.tab(label="Controls"):
                    dpg.add_text(
                        "Canvas Controls:\n\n"
                        "- Click and drag to create links between gate pins\n"
                        "- Select a node/link and press Delete or Backspace to remove it\n"
                        "- Use arrow keys to pan the canvas\n"
                        "- Click 'Reload Canvas' if the view gets lost or stuck\n"
                        "- Click 'Reorganize' to auto-layout the network\n"
                        "- Double click a gate node to rename it\n"
                        "- C / V to copy and paste selected nodes\n\n"
                        "Gate Editor:\n\n"
                        "- Click a gate button to add it to the canvas\n"
                        "- Click the gate editor to view or edit a gate's logic\n"
                        "- Close the gate editor to draw gates with a single click\n",
                        wrap=500
                    )
                
                with dpg.tab(label="Gates"):
                    dpg.add_text(
                        "Gates are defined as .lp (Answer Set Programming) files in the gates folder.\n\n"
                        "Each gate file has a header declaring its type and pin count:\n\n"
                        "  %% gate: AND\n"
                        "  %% inputs: 2\n"
                        "  %% outputs: 1\n\n"
                        "IMPORTANT: If you create a gate with more than 2 inputs, you must also "
                        "update main.lp to support that many inputs - the base propagation rules "
                        "are written for a fixed number of input slots. Adding a gate with 3+ inputs "
                        "without updating main.lp will cause it to be ignored or error during solving.\n\n"
                        "Similarly, the only values currently supported (e.g. 0 and 1) are defined in "
                        "main.lp under the 'values' facts. If you need more than binary values, "
                        "you'll need to expand that definition too.\n\n"
                        "Default gates (INPUT, OUTPUT, AND, OR, NOT, XOR) cannot be edited or deleted, "
                        "but you can create new custom gates from the '+ New Custom Gate' button.",
                        wrap=500
                    )
                
                with dpg.tab(label="Input Scripts"):
                    dpg.add_text(
                        "Input scripts are short Python snippets that define values for your network's "
                        "INPUT nodes. They must define a dictionary called 'inputs', keyed by node ID:\n\n"
                        "  inputs = {\n"
                        '      "INPUT_1": 1,\n'
                        '      "INPUT_2": 0,\n'
                        "  }\n\n"
                        "The script re-runs automatically as you type, or you can click 'Update' to "
                        "force a re-run (useful if your script uses randomness).\n\n"
                        "'Refresh Template' regenerates a blank template matching the network's current "
                        "INPUT nodes, resetting all values to None.\n\n"
                        "'Save As' / 'Load' let you store reusable input scripts independent of any "
                        "single network. 'Revert' restores the script that was last loaded, or the "
                        "one saved with the current network if none was explicitly loaded.\n\n"
                        "The input script you're using is saved as part of the network file itself, "
                        "so it travels with your saved network.",
                        wrap=500
                    )
                
                with dpg.tab(label="Output Scripts"):
                    dpg.add_text(
                        "Output scripts are Python files that format Clingo's solved results into "
                        "readable text. Each must define a function:\n\n"
                        "  def format(facts, values):\n"
                        "      return \"some readable string\"\n\n"
                        "'facts' is a list of raw val(...) ASP facts (quoted, Clingo-ready).\n"
                        "'values' is a dictionary of {node_id: value} with clean Python string keys.\n\n"
                        "The 'default' output script cannot be overwritten silently - saving over it "
                        "is allowed, but only intentionally.\n\n"
                        "Output script selection is saved with the network (by name), so make sure "
                        "to save any custom script before saving your network if you want it referenced "
                        "correctly later.",
                        wrap=500
                    )
                
                with dpg.tab(label="Saving & Files"):
                    dpg.add_text(
                        "Saving a network creates two files:\n\n"
                        "  .json - the full network structure (nodes, links, input/output script refs)\n"
                        "  .lp   - the generated Answer Set Program for that network's topology\n\n"
                        "main.lp contains the shared rules used by every network:\n\n"
                        "  - the allowed value set (e.g. 0 and 1)\n"
                        "  - the generic propagation rule that passes values between connected gates\n"
                        "  - constraints on how many inputs a gate may have\n\n"
                        "Editing main.lp can break every network if done incorrectly - a confirmation "
                        "warning will appear before you're allowed to edit it (this can be disabled "
                        "in Settings).\n\n"
                        "'Solve Network' assembles main.lp + all used gates + your network's .lp file "
                        "and runs them through Clingo, then displays the result in the Output window.",
                        wrap=500
                    )
            
            dpg.add_separator()
            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("help_popup"), width=80)
        return 0
