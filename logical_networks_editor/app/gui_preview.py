# gui_preview.py

import dearpygui.dearpygui as dpg

import tools
import os


class GUIPreview:

    ## ---------------------------- Preview Callbacks --------------------------------

    def toggle_preview_edit(self, sender, app_data):
        if self.CONFIG["window"].get("warn_on_base_edit", True):
            self._show_base_edit_warning()
            return
        # hide colored, show editor with current content
        if dpg.does_item_exist("preview_colored"):
            dpg.hide_item("preview_colored")
        content = self._get_current_file_content()
        dpg.set_value("preview_editor", content)
        dpg.show_item("preview_editor")
        dpg.configure_item("preview_editor", enabled=True)
        dpg.show_item("preview_save_btn")
        dpg.show_item("preview_revert_btn")
        dpg.hide_item("preview_edit_btn")

    def _show_base_edit_warning(self):
        if dpg.does_item_exist("base_edit_warning"):
            dpg.delete_item("base_edit_warning")
        
        pos = dpg.get_mouse_pos(local=False)
        with dpg.window(label="Warning", modal=True, tag="base_edit_warning", no_resize=True, pos=pos):
            dpg.add_text("Editing this file directly can break your network.\nProceed with caution.", color=(255, 180, 80, 255))
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Okay", width=80, callback=lambda: self._dismiss_base_warning(False))
                dpg.add_button(label="Okay, don't show again", width=180, callback=lambda: self._dismiss_base_warning(True))

    def _dismiss_base_warning(self, dont_show_again):
        if dont_show_again:
            self.CONFIG["window"]["warn_on_base_edit"] = False
            config_path = tools.resource_path("app/config.toml")
            with open(config_path, "r") as f:
                content = f.read()
            content = content.replace("warn_on_base_edit = true", "warn_on_base_edit = false")
            with open(config_path, "w") as f:
                f.write(content)
        dpg.delete_item("base_edit_warning")
        
        # enable edit mode
        if dpg.does_item_exist("preview_colored"):
            dpg.hide_item("preview_colored")
        content = self._get_current_file_content()
        dpg.set_value("preview_editor", content)
        dpg.show_item("preview_editor")
        dpg.configure_item("preview_editor", enabled=True)
        dpg.show_item("preview_save_btn")
        dpg.show_item("preview_revert_btn")
        dpg.hide_item("preview_edit_btn")

    def _get_current_file_content(self):
        selected = dpg.get_value("preview_selector")
        if selected == "LP":
            path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        elif selected == "JSON":
            path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.json"
        elif selected == "main.lp":
            path = tools.resource_path(self.CONFIG["paths"]["base_folder"]) + "/main.lp"
        if not os.path.exists(path):
            return "File not found."
        with open(path) as f:
            return f.read()

    def on_preview_selector_changed(self, sender, app_data):
        selected = app_data
        
        # reset to readonly on switch
        dpg.configure_item("preview_editor", enabled=False)
        dpg.hide_item("preview_save_btn")
        dpg.show_item("preview_edit_btn")
        
        if selected == "LP":
            path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        elif selected == "JSON":
            path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.json"
        elif selected == "main.lp":
            path = tools.resource_path(self.CONFIG["paths"]["base_folder"]) + "/main.lp"
        
        if not os.path.exists(path):
            self._show_preview_readonly("File not found.")
            return
        with open(path) as f:
            content = f.read()
        
        self._show_preview_readonly(content)

    def revert_preview_file(self, sender, app_data):
        content = self._get_current_file_content()
        dpg.configure_item("preview_editor", enabled=False)
        dpg.hide_item("preview_save_btn")
        dpg.hide_item("preview_revert_btn")
        dpg.show_item("preview_edit_btn")
        self._show_preview_readonly(content)