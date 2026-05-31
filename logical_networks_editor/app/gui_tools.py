# gui_tools.py
# GUI components for the Logical Networks project

import dearpygui.dearpygui as dpg

import gui_canvas as canvas
import gui_files as files
import gui_update as update
import gui_output as output
import gui_window as window


class GUI(
    canvas.GUICanvas,
    files.GUIFiles,
    update.GUIUpdate,
    output.GUIOutput,
    window.GUIWindow
):
    def __init__(self, CONFIG, REGISTRY, NETWORK):
        self.CONFIG = CONFIG
        self.REGISTRY = REGISTRY
        self.NETWORK = NETWORK
        
        self.last_save_name = None
        self.current_gate_in_editor = None
        self.output_shown = False
    
    def build_gui(self):
        CONFIG = self.CONFIG
        REGISTRY = self.REGISTRY
        # T = CONFIG["window"]["title"]
        W = CONFIG["window"]["width"]
        H = CONFIG["window"]["height"]

        # with dpg.window(label="toolbar", width=W, height=40, pos=(0,0), tag="toolbar", no_title_bar=True, no_scrollbar=True, no_resize=True, no_move=True):
        with dpg.window(label="toolbar", width=W, height=35, min_size=[100, 30], pos=(0,0), tag="toolbar", no_title_bar=True, no_scrollbar=True, no_resize=True, no_move=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Logical Network Editor", color=(255, 255, 0))
                # dpg.add_button(label="Recenter", callback=self.recenter)
                dpg.add_button(label="Quick Save", callback=self.quick_save)
                dpg.add_button(label="Save", callback=self.save_network_as)
                dpg.add_button(label="Load", callback=self.load_network)
                dpg.add_button(label="Reorganize", callback=self.reorganize)
                dpg.add_button(label="Delete Selected", callback=self.delete_selected)
                dpg.add_button(label="Output: OFF", tag="output_toggle_btn", callback=self.toggle_output_window)

        with dpg.window(label="Sidebar", width=200, height=H-35, pos=(0,35), tag="sidebar", no_resize=True, no_close=True, no_move=True, no_collapse=True):
        # with dpg.window(label="Sidebar", width=W//8, height=H-40, pos=(0,40), tag="sidebar"):
            dpg.add_text("Controls:\n- Click and drag to create links\n"
                         + "- Select and press Delete/\nBackspace to delete\n"
                         + "- Use arrow keys to pan\n- Click 'Recenter' to reset\n view\n"
                         + "- Edit gate definitions in the Gate Editor\n  and click 'Draw' to add to canvas\n"
                         + "- Close the gate editor to draw neurons with one click\n"
                         + "- Double click a gate to edit its name\n")

            dpg.add_text("Gates:")
            dpg.add_separator()
            with dpg.child_window(tag="gate_list", parent="sidebar", width=200, auto_resize_y=True, border=False):
                pass
            self.build_gate_list()

            dpg.add_separator()
            dpg.add_text("Input Script:")
            dpg.add_input_text(
                tag="input_script",
                multiline=True,
                width=180,
                height=150,
                default_value="inputs = [\n    # Inputs\n]"
            )
            dpg.add_button(label="Update Inputs", callback=self.apply_inputs)
        
        with dpg.window(label="Canvas", width=W-200-W//5, height=H-35, pos=(200,35), tag="canvas", no_resize=True, no_close=True, no_move=True, no_collapse=True, no_scroll_with_mouse=False):
        # with dpg.window(label="Canvas", width=W-W//8-W//5, height=H-30, pos=(W//8,30), tag="canvas"):
            with dpg.node_editor(
                tag="node_editor",
                callback=self.on_link_created,
                delink_callback=self.on_link_deleted):
                pass

        with dpg.window(label="Preview", width=W//5, height=H-35, pos=(W-W//5,35), tag="preview", no_resize=True, no_close=True, no_move=True, no_collapse=True):
            dpg.add_text("Logical Network Preview:")
            dpg.add_separator()
            # dpg.add_text("", tag="preview_text")
            with dpg.child_window(tag="preview_text", width=-1, height=-1, border=False):
                pass
            self.update_preview()
        
        with dpg.window(label="Output", tag="output_window", 
                        pos=(0, H-35), width=W, height=CONFIG["window"]["output_height"],
                        no_resize=True, no_close=True, no_move=True, 
                        no_collapse=True, no_title_bar=True, show=False):
            with dpg.group(horizontal=True):
                dpg.add_text("Clingo Output", color=(255, 255, 0))
                dpg.add_button(label="Run Network", callback=self.run_network, width=100)
                dpg.add_button(label="Clear", callback=lambda: dpg.delete_item("run_output", children_only=True), width=60)
            dpg.add_separator()
            with dpg.child_window(tag="run_output", width=-1, height=-1, border=False):
                pass

        # bind terminal theme
        with dpg.theme() as terminal_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 255))
        dpg.bind_item_theme("output_window", terminal_theme)

        return 0
    
    def build_gate_list(self):
        REGISTRY = self.REGISTRY
        editor_open = self.CONFIG["window"]["gate_editor_open"]
        
        with dpg.group(parent="gate_list"):
            dpg.add_button(
                label="Gate Editor: ON" if editor_open else "Gate Editor: OFF",
                tag="gate_editor_toggle_btn",
                width=180,
                callback=self.toggle_gate_editor
            )
            dpg.add_input_text(
                tag="gate_editor_box",
                multiline=True,
                width=180,
                height=150,
                enabled=False,
                show=editor_open,
                default_value=""
            )
            with dpg.group(horizontal=True, tag="gate_editor_controls", show=editor_open):
                dpg.add_button(
                    label="Draw",
                    tag="gate_add_btn",
                    callback=self.add_gate_node,
                    user_data=self.REGISTRY.get(self.current_gate_in_editor),
                    width=60
                )
                dpg.add_button(
                    label="Save",
                    tag="gate_save_btn",
                    callback=self.save_gate,
                    width=60
                )
        
        dpg.add_separator(parent="gate_list")

        for name, gate in REGISTRY.items():
            with dpg.group(tag=f"gate_group_{name}", parent="gate_list"):
                dpg.add_button(
                    label=name,
                    tag=f"gate_btn_{name}",
                    callback=self.gate_btn_callback,
                    user_data={"name": name, "gate": gate},
                    # indent=10,
                    width=180
                    )
        return 0