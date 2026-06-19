# gui_window.py

import dearpygui.dearpygui as dpg


class GUIWindow:

    ## ------------------------ Window Utility Functions ---------------------------

    def on_viewport_resize(self):
        W = dpg.get_viewport_width()
        H = dpg.get_viewport_height()
        
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
