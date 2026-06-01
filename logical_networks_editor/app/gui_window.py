# gui_window.py

import dearpygui.dearpygui as dpg


class GUIWindow:

    ## ------------------------ Window Utility Functions ---------------------------

    def on_viewport_resize(self):
        W = dpg.get_viewport_width()
        H = dpg.get_viewport_height()
        
        output_buttons_width = 160 + 100 + 60 + 70 + 70 + 90 # rough estimate of all items in output header
        if dpg.does_item_exist("output_spacer"):
            dpg.configure_item("output_spacer", width=W - output_buttons_width)
        
        preview_w = self.CONFIG["window"]["preview_width"]
        dpg.configure_item("toolbar", width=W)
        self._resize_for_output(W, H, self.output_shown)
        dpg.configure_item("preview", width=preview_w, pos=(W-preview_w, 35))
        dpg.configure_item("canvas", width=W-200-preview_w)
        return 0
    
    def toggle_gate_editor(self, sender, app_data):
        currently_shown = dpg.is_item_shown("gate_editor_box")
        if not currently_shown:
            dpg.show_item("gate_editor_box")
            dpg.show_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: ON")
        else:
            dpg.hide_item("gate_editor_box")
            dpg.hide_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: OFF")
            dpg.configure_item("gate_editor_box", enabled=False)
            dpg.set_item_label("gate_edit_toggle", "Edit")
        return 0

    def select_gate_for_editor(self, sender, app_data, user_data):
        name = user_data
        gate = self.REGISTRY[name]
        
        with open(gate["file"]) as f:
            content = f.read()
        dpg.set_value("gate_editor_box", content)
        self.current_gate_in_editor = name
        dpg.configure_item("gate_add_btn", user_data=gate)

        # show editor if not already open
        if not dpg.is_item_shown("gate_editor_box"):
            dpg.show_item("gate_editor_box")
            dpg.show_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: ON")
        # reset to readonly
        dpg.configure_item("gate_editor_box", enabled=True)
        # dpg.set_item_label("gate_edit_toggle", "Edit")  # deprecated
        return 0
