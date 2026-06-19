# gui_tools.py
# GUI components for the Logical Networks project

import dearpygui.dearpygui as dpg

import gui.gui_canvas as canvas
import gui.gui_files as files
import gui.gui_update as update
import gui.gui_output as output
import gui.gui_window as window
import gui.gui_preview as preview
import gui.gui_gates as gates
import gui.gui_scripts as scripts


class GUI(
    canvas.GUICanvas,
    files.GUIFiles,
    update.GUIUpdate,
    output.GUIOutput,
    window.GUIWindow,
    preview.GUIPreview,
    gates.GUIGates,
    scripts.GUIScripts
):
    def __init__(self, CONFIG, REGISTRY, NETWORK):
        self.CONFIG = CONFIG
        self.REGISTRY = REGISTRY
        self.NETWORK = NETWORK
        
        self.last_save_name = None
        self.current_gate_in_editor = None
        self.current_input_script = None
        self.output_shown = False
    
    def build_gui(self):
        CONFIG = self.CONFIG
        REGISTRY = self.REGISTRY
        # T = CONFIG["window"]["title"]
        W = CONFIG["window"]["width"]
        H = CONFIG["window"]["height"]
        output_h = CONFIG["window"]["output_height"]
        output_script_h = CONFIG["window"]["output_script_height"]
        preview_w = CONFIG["window"]["preview_width"]
        sidebar_w = CONFIG["window"]["sidebar_width"]

        with dpg.window(label="toolbar", width=W, height=35, min_size=[100, 30], pos=(0,0), tag="toolbar", no_title_bar=True, no_scrollbar=True, no_resize=True, no_move=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Logical Network Editor", color=(255, 255, 0))
                # dpg.add_button(label="Recenter", callback=self.recenter)
                dpg.add_button(label="Quick Save", callback=self.quick_save)
                dpg.add_button(label="Save", callback=self.save_network_as)
                dpg.add_button(label="Load", callback=self.load_network)
                dpg.add_button(label="Reorganize", callback=self.reorganize)
                dpg.add_button(label="Clear", callback=self.clear_canvas)
                dpg.add_button(label="Delete Selected", callback=self.delete_selected)
                dpg.add_button(label="Output: OFF", tag="output_toggle_btn", callback=self.toggle_output_window)

        with dpg.window(label="Sidebar", width=sidebar_w, height=H-35, pos=(0,35), tag="sidebar", no_title_bar=True, no_resize=True, no_close=True, no_move=True, no_collapse=True):
            dpg.add_text("Controls:\n- Click and drag to create links\n\n"
                         + "- Select and press Delete/\n  Backspace to delete\n"
                         + "- Use arrow keys to pan\n- Click 'Recenter' to reset\n view\n"
                         + "- Edit gate definitions in the \n  Gate Editor and click 'Draw' to\n  add to canvas\n"
                         + "- Close the gate editor to draw\n  neurons with one click\n"
                         + "- Double click a gate to edit its name\n")
            
            dpg.add_separator()
            dpg.add_text("Gates:")
            dpg.add_separator()
            with dpg.child_window(tag="gate_list", parent="sidebar", width=sidebar_w-40, auto_resize_y=True, border=False):
                pass

            dpg.add_separator()
            dpg.add_text("Input Script:")
            dpg.add_input_text(
                tag="input_script",
                multiline=True,
                width=sidebar_w-40,
                height=150,
                default_value="inputs = [\n    # Inputs\n]",
                callback=self.apply_inputs
            )
            dpg.add_button(label="Refresh", callback=self.update_input_template, width=sidebar_w-40)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Revert", callback=self.revert_input_script, width=(sidebar_w-48)//2)
                dpg.add_button(label="Update", tag="input_script_rerun_btn", callback=self.apply_inputs, width=(sidebar_w-48)//2)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save As", callback=self.save_input_script_as, width=(sidebar_w-48)//2)
                dpg.add_button(label="Load", callback=self.load_input_script_popup, width=(sidebar_w-48)//2)
        
        with dpg.window(label="Canvas", width=W-sidebar_w-preview_w, height=H-35, pos=(sidebar_w,35), tag="canvas", no_resize=True, no_close=True, no_move=True, no_collapse=True, no_scroll_with_mouse=False):
            with dpg.node_editor(
                tag="node_editor",
                callback=self.on_link_created,
                delink_callback=self.on_link_deleted):
                pass

        with dpg.window(label="Preview", width=preview_w, height=H-35, pos=(W-preview_w,35), no_title_bar=True, tag="preview", no_resize=True, no_close=True, no_move=True, no_collapse=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Preview:")
                dpg.add_combo(
                    items=["LP", "JSON", "main.lp"],
                    tag="preview_selector",
                    default_value="LP",
                    width=120,
                    callback=self.on_preview_selector_changed
                )
                dpg.add_button(label="Edit", tag="preview_edit_btn", callback=self.toggle_preview_edit, width=50)
                dpg.add_button(label="Save", tag="preview_save_btn", callback=self.save_preview_file, width=50, show=False)
                dpg.add_button(label="Revert", tag="preview_revert_btn", callback=self.revert_preview_file, width=60, show=False)
            dpg.add_separator()
            with dpg.child_window(tag="preview_text", width=-1, height=-(output_script_h + 55), border=False):
                dpg.add_child_window(tag="preview_colored", width=-1, height=-1, border=False)
                dpg.add_input_text(
                    tag="preview_editor",
                    multiline=True,
                    width=-1,
                    height=-1,
                    default_value="",
                    enabled=False,
                    show=False
                )

            dpg.add_separator()
            dpg.add_text("Output Script:")
            with dpg.child_window(tag="output_script_editor_wrapper", width=-1, height=output_script_h, border=False):
                dpg.add_input_text(tag="output_script_editor", multiline=True, width=-1, height=-1, default_value="")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save As", callback=self.save_output_script_as, width=(preview_w-40)//3)
                dpg.add_button(label="Load", callback=self.load_output_script_popup, width=(preview_w-40)//3)
                dpg.add_button(label="Revert", callback=self.revert_output_script, width=(preview_w-40)//3)

        with dpg.window(label="Output", tag="output_window", 
                        pos=(0, H-35), width=W, height=output_h,
                        no_resize=True, no_close=True, no_move=True, 
                        no_collapse=True, no_title_bar=True, show=False):
            with dpg.group(horizontal=True):
                buttons_width = 160 + 100 + 60 + 70 + 70 + 90 # rough estimate of all items
                dpg.add_text("Clingo Output", color=(255, 255, 0))
                dpg.add_spacer(tag="output_spacer", width=W - buttons_width)  # push buttons to the right
                # dpg.add_text("Clingo Output", color=(255, 255, 0))
                dpg.add_button(label="Solve Network", callback=self.run_network, width=100)
                dpg.add_button(label="Clear", callback=self.clear_output, width=60)
                dpg.add_button(label="Std Out", tag="tab_output_btn", callback=lambda: self.switch_output_tab("output"), width=70)
                dpg.add_button(label="Std Err", tag="tab_errors_btn", callback=lambda: self.switch_output_tab("errors"), width=70)
                dpg.add_button(label="Formatted", tag="tab_formatted_btn", callback=lambda: self.switch_output_tab("formatted"), width=90)
            dpg.add_separator()
            with dpg.child_window(tag="run_output", width=-1, height=-1, border=False):
                pass
            with dpg.child_window(tag="run_errors", width=-1, height=-1, border=False, show=False):
                pass
            with dpg.child_window(tag="run_formatted", width=-1, height=-1, border=False, show=False):
                pass

        # bind terminal theme
        with dpg.theme() as terminal_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 255))
        dpg.bind_item_theme("output_window", terminal_theme)

        self.build_gate_list()
        self.update_preview()
        self.update_input_template()
        self.load_default_output_script(None, None)

        if self.CONFIG["window"]["output_open"]:
            self.toggle_output_window(None, None)
        return 0
    
    def build_gate_list(self):
        REGISTRY = self.REGISTRY
        editor_open = self.CONFIG["window"]["gate_editor_open"]
        sidebar_w = self.CONFIG["window"]["sidebar_width"]
        editor_h = self.CONFIG["window"]["gate_editor_height"]
        
        with dpg.group(parent="gate_list"):
            dpg.add_button(
                label="Gate Editor: ON" if editor_open else "Gate Editor: OFF",
                tag="gate_editor_toggle_btn",
                width=sidebar_w-40,
                callback=self.toggle_gate_editor
            )
            with dpg.child_window(tag="gate_editor_box_wrapper", width=sidebar_w-40, height=editor_h, show=editor_open, border=True):
                dpg.add_child_window(tag="gate_editor_colored", width=-1, height=-1, border=False)
                dpg.add_input_text(
                    tag="gate_editor_box",
                    multiline=True,
                    width=-1,
                    height=-1,
                    enabled=False,
                    show=False,
                    default_value=""
                )
            with dpg.group(horizontal=True, tag="gate_editor_controls", show=editor_open):
                dpg.add_button(
                    label="Add",
                    tag="gate_add_btn",
                    callback=self.add_gate_node,
                    user_data=self.REGISTRY.get(self.current_gate_in_editor),
                    width=50
                )
                dpg.add_button(
                    label="Edit",
                    tag="gate_edit_btn",
                    callback=self.toggle_gate_editor_mode,
                    width=50
                )
                dpg.add_button(
                    label="Save",
                    tag="gate_save_btn",
                    callback=self.save_gate,
                    width=50,
                    show=False
                )
                dpg.add_button(
                    label="Delete",
                    tag="gate_delete_btn",
                    callback=self.delete_gate,
                    user_data=self.current_gate_in_editor,
                    width=50
                )
        
        dpg.add_separator(parent="gate_list")

        # virtual "custom gate" entry
        with dpg.group(tag="gate_group_NEW", parent="gate_list"):
            dpg.add_button(
                label="New Custom Gate",
                tag="gate_btn_NEW",
                callback=self.select_custom_template,
                width=sidebar_w-40
            )

        dpg.add_separator(parent="gate_list")

        for gate_type, gate in REGISTRY.items():
            with dpg.group(tag=f"gate_group_{gate_type}", parent="gate_list"):
                dpg.add_button(
                    label=gate_type,
                    tag=f"gate_btn_{gate_type}",
                    callback=self.gate_btn_callback,
                    user_data={"type": gate_type, "gate": gate},
                    # indent=10,
                    width=sidebar_w-40
                    )
        return 0
