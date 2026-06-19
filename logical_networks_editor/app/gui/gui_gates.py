# gui_gates.py

import dearpygui.dearpygui as dpg


class GUIGates:

    ## ------------------------------- Gate Editor UI --------------------------------

    def toggle_gate_editor(self, sender, app_data):
        currently_shown = dpg.is_item_shown("gate_editor_box_wrapper")
        if not currently_shown:
            dpg.show_item("gate_editor_box_wrapper")
            dpg.show_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: ON")
            
            # if nothing selected, show the custom template readonly
            if self.current_gate_in_editor is None:
                self._show_gate_readonly(self._get_custom_template())
        else:
            dpg.hide_item("gate_editor_box_wrapper")
            dpg.hide_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: OFF")
            dpg.configure_item("gate_editor_box", enabled=False)
            dpg.set_item_label("gate_edit_btn", "Edit")
        return 0
    
    def select_gate_for_editor(self, sender, app_data, user_data):
        gate_type = user_data
        gate = self.REGISTRY[gate_type]
        
        with open(gate["file"]) as f:
            content = f.read()
        
        self.current_gate_in_editor = gate_type
        dpg.configure_item("gate_add_btn", user_data=gate)
        
        if not dpg.is_item_shown("gate_editor_box_wrapper"):
            dpg.show_item("gate_editor_box_wrapper")
            dpg.show_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: ON")
        
        # Default to readonly view
        self._show_gate_readonly(content)
        return 0
    
    def select_custom_template(self, sender, app_data):
        self.current_gate_in_editor = None
        content = self._get_custom_template()
        
        if not dpg.is_item_shown("gate_editor_box_wrapper"):
            dpg.show_item("gate_editor_box_wrapper")
            dpg.show_item("gate_editor_controls")
            dpg.set_item_label("gate_editor_toggle_btn", "Gate Editor: ON")
        
        # Default to readonly view
        self._show_gate_readonly(content)

        # Default to edit mode with template loaded
        # dpg.hide_item("gate_editor_colored")
        # dpg.set_value("gate_editor_box", content)
        # dpg.show_item("gate_editor_box")
        # dpg.configure_item("gate_editor_box", enabled=True)
        # dpg.hide_item("gate_edit_btn")
        # dpg.show_item("gate_save_btn")
        return 0
    
    def toggle_gate_editor_mode(self, sender, app_data):
        dpg.hide_item("gate_editor_colored")
        content = dpg.get_value("gate_editor_box") if dpg.is_item_shown("gate_editor_box") else self._get_gate_content_for_edit()
        dpg.set_value("gate_editor_box", content)
        dpg.show_item("gate_editor_box")
        dpg.configure_item("gate_editor_box", enabled=True)
        dpg.hide_item("gate_edit_btn")
        dpg.show_item("gate_save_btn")
        return 0
    
    def gate_btn_callback(self, sender, app_data, user_data):
        gate_type = user_data["type"]
        gate = user_data["gate"]
        if dpg.is_item_shown("gate_editor_box_wrapper"):
            self.select_gate_for_editor(sender, app_data, gate_type)
        else:
            self.add_gate_node(sender, app_data, gate)
        return 0
    
    ## ----------------------------- Gate Display Helpers ------------------------------

    def _show_gate_readonly(self, content):
        dpg.hide_item("gate_editor_box")
        dpg.delete_item("gate_editor_colored", children_only=True)
        dpg.show_item("gate_editor_colored")
        self._render_gate_colored(content)
        dpg.set_item_label("gate_edit_btn", "Edit")
        dpg.hide_item("gate_save_btn")
        dpg.show_item("gate_edit_btn")
        return 0
    
    def _render_gate_colored(self, lp_text):
        for line in lp_text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("%"):
                color = (120, 120, 120, 255)
            elif ":-" in stripped:
                color = (100, 180, 255, 255)
            elif stripped.startswith(":~"):
                color = (255, 180, 80, 255)
            elif stripped.startswith("#"):
                color = (255, 220, 50, 255)
            elif stripped.endswith(".") or stripped.endswith(","):
                color = (220, 220, 220, 255)
            else:
                color = (160, 160, 160, 255)
            dpg.add_text(line if line else " ", parent="gate_editor_colored", color=color)
        return 0
    
    def _get_gate_content_for_edit(self):
        if self.current_gate_in_editor and self.current_gate_in_editor in self.REGISTRY:
            with open(self.REGISTRY[self.current_gate_in_editor]["file"]) as f:
                return f.read()
        return self._get_custom_template()
    
    def _get_custom_template(self):
        return (
            '%% gate: CUSTOM_NAME\n'
            '%% inputs: 2\n'
            '%% outputs: 1\n'
            '\n'
            '% Change CUSTOM_NAME both here and above\n'
            '% type("TYPE")\n'
            'type("CUSTOM_NAME").\n'
            '\n'
            '% Replace the following with your gate  logic\n'
            '% gate(TYPE, OUTPUT, INPUTS)\n'
            'gate("CUSTOM_NAME", Out, In1, In2) :-\n'
            '    values(In1), values(In2),\n'
            '    Out = 1 - (In1 * In2).\n'
            '\n'
            '% NOTE: If using more than two inputs, main.lp must be updated accordingly.\n'
        )
