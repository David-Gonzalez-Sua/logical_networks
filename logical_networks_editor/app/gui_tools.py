# Tools for building the GUI using DearPyGui.
#

import subprocess
import datetime
import os

import dearpygui.dearpygui as dpg
import tools


class GUI:
    def __init__(self, CONFIG, REGISTRY, NETWORK):
        self.CONFIG = CONFIG
        self.REGISTRY = REGISTRY
        self.NETWORK = NETWORK

        self.last_save_name = None
        self.current_gate_in_editor = None

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

        with dpg.window(label="Sidebar", width=200, height=H-35, pos=(0,35), tag="sidebar", no_resize=True, no_close=True, no_move=True, no_collapse=True):
        # with dpg.window(label="Sidebar", width=W//8, height=H-40, pos=(0,40), tag="sidebar"):
            dpg.add_text("Controls:\n- Click and drag to create links\n- Select and press Delete/\nBackspace to delete\n- Use arrow keys to pan\n- Click 'Recenter' to reset\n view")

            dpg.add_text("Gates:")
            dpg.add_separator()
            # for name, gate in REGISTRY.items():
            #     dpg.add_button(label=name, callback=self.add_gate_node, user_data=gate)
            # with dpg.child_window(tag="gate_list", parent="sidebar", width=190, height=-1, border=False):
            #     pass
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
        
        with dpg.window(label="Canvas", width=W-200-W//5, height=H-35, pos=(200,35), tag="canvas", no_resize=True, no_close=True, no_move=True, no_collapse=True):
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
            with dpg.child_window(tag="preview_text", width=-1, height=-200, border=False):
                pass
            self.update_preview()

            dpg.add_separator()
            dpg.add_button(label="Run Network", callback=self.run_network, width=-1)
            with dpg.child_window(tag="run_output", width=-1, height=180, border=True):
                dpg.add_text("Output will appear here.", tag="run_output_text", wrap=W//5 - 10)

        return 0

    ## ------------------------------ Canvas Callbacks ------------------------------

    def add_gate_node(self, sender, app_data, user_data):
        gate = user_data
        name = gate["name"]
        
        self.NETWORK.counts[name] = self.NETWORK.counts.get(name, 0) + 1
        node_id = f"{name}_{self.NETWORK.counts[name]}"
        uid = dpg.generate_uuid()
        
        with dpg.node(label=node_id, parent="node_editor", tag=uid):
            for i in range(gate["inputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                    dpg.add_text("in")
            for i in range(gate["outputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text("out")
        
        self.NETWORK.add_node(node_id, name, gate["inputs"], uid)
        pos = self.get_free_position()
        dpg.set_item_pos(uid, pos)

        self.update_preview()
        self.update_input_template()
        return 0

    def on_link_created(self, sender, app_data):
        source_pin = app_data[0]
        target_pin = app_data[1]
        
        source_id = None
        target_id = None
        target_input_index = None

        for node_id, node in self.NETWORK.nodes.items():
            children = dpg.get_item_children(node["dpg_id"], slot=1)
            if source_pin in children:
                source_id = node_id
            if target_pin in children:
                target_id = node_id
                target_input_index = children.index(target_pin)

        link_uid = dpg.generate_uuid()
        dpg.add_node_link(source_pin, target_pin, parent="node_editor", tag=link_uid)
        self.NETWORK.add_link(link_uid, source_id, target_id, target_input_index)
        self.update_preview()
        return 0

    def on_link_deleted(self, sender, app_data):
        self.NETWORK.delete_link(app_data)
        dpg.delete_item(app_data)
        self.update_preview()
        return 0
    
    def delete_selected(self, sender, app_data):
        selected_nodes = dpg.get_selected_nodes("node_editor")
        selected_links = dpg.get_selected_links("node_editor")
        
        for node in selected_nodes:
            node_id = next(k for k, v in self.NETWORK.nodes.items() if v["dpg_id"] == node)
            self.NETWORK.delete_node(node_id)
            dpg.delete_item(node)
        
        for link in selected_links:
            self.NETWORK.delete_link(link)
            dpg.delete_item(link)
        
        self.update_preview()
        self.update_input_template()
        return 0

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
    
    ## ------------------------------ Preview Callbacks --------------------------------

    # def update_preview(self):
    #     self.save_snapshot(None, None)
    #     # path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.json"
    #     path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        
    #     if not os.path.exists(path):
    #         dpg.set_value("preview_text", "Preview not available.")
    #         return 1
        
    #     with open(path) as f:
    #         preview = f.read()
        
    #     dpg.set_value("preview_text", preview)
    #     return 0
    
    def update_preview(self):
        self.save_snapshot(None, None)
        path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        # path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.json"
        
        if not os.path.exists(path):
            dpg.delete_item("preview_text", children_only=True)
            dpg.add_text("Preview not available.", parent="preview_text")
            return 1
        
        with open(path) as f:
            preview = f.read()
        
        self._render_lp_preview(preview)
        return 0

    def _render_lp_preview(self, lp_text):
        dpg.delete_item("preview_text", children_only=True)
        
        for line in lp_text.split("\n"):
            stripped = line.strip()
            
            if stripped.startswith("%"):
                color = (120, 120, 120, 255)      # comments - gray
            elif ":-" in stripped:
                color = (100, 180, 255, 255)      # rules - blue
            elif stripped.startswith(":~"):
                color = (255, 180, 80, 255)       # weak constraints - orange
            elif stripped.startswith("#"):
                color = (255, 220, 50, 255)       # directives - yellow
            elif stripped.endswith("."):
                color = (220, 220, 220, 255)      # facts - white
            else:
                color = (160, 160, 160, 255)      # everything else - dim

            dpg.add_text(line if line else " ", parent="preview_text", color=color)
    
    def update_input_template(self):
        input_nodes = [nid for nid, n in self.NETWORK.nodes.items() if n["name"] == "INPUT"]
        lines = ["inputs = ["]
        
        for nid in input_nodes:
            val = self.NETWORK.nodes[nid]["val"]
            lines.append(f"    {val},  # {nid}")
        lines.append("]")
        
        dpg.set_value("input_script", "\n".join(lines))
        return 0
    
    def apply_inputs(self, sender, app_data):
        script = dpg.get_value("input_script")
        local = {}
        try:
            exec(script, {}, local)
            values = local.get("inputs", [])
        except Exception as e:
            print(f"Input script error: {e}")
            return 1
        
        input_nodes = [nid for nid, n in self.NETWORK.nodes.items() if n["name"] == "INPUT"]
        
        if len(values) != len(input_nodes):
            print(f"Expected {len(input_nodes)} inputs, got {len(values)}")
            return 1
        if any(v is None for v in values):
            print("All inputs must be set.")
            return 1
        
        for node_id, val in zip(input_nodes, values):
            self.NETWORK.nodes[node_id]["val"] = val
        
        self.update_preview()
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
        dpg.configure_item("gate_editor_box", enabled=False)
        dpg.set_item_label("gate_edit_toggle", "Edit")
        return 0

    def toggle_gate_readonly(self, sender, app_data):
        currently_enabled = dpg.is_item_enabled("gate_editor_box")
        dpg.configure_item("gate_editor_box", enabled=not currently_enabled)
        dpg.set_item_label("gate_edit_toggle", "Lock" if not currently_enabled else "Edit")
        return 0
    
    def gate_btn_callback(self, sender, app_data, user_data):
        name = user_data["name"]
        gate = user_data["gate"]
        if dpg.is_item_shown("gate_editor_box"):
            self.select_gate_for_editor(sender, app_data, name)
        else:
            self.add_gate_node(sender, app_data, gate)

    
    ## -------------------------- Canvas Utility Functions ----------------------------
    
    def pan(self, dx, dy):
        for node_id, node in self.NETWORK.nodes.items():
            pos = dpg.get_item_pos(node["dpg_id"])
            dpg.set_item_pos(node["dpg_id"], [pos[0]+dx, pos[1]+dy])
        return 0

    def recenter(self):
        for node_id, node in self.NETWORK.nodes.items():
            dpg.set_item_pos(node["dpg_id"], [0, 0])
        return 0

    def reorganize(self):
        '''Longest path layering — Sugiyama et al. (1981)
           assigns each node to the layer of its furthest predecessor + 1'''
        if not self.NETWORK.nodes:
            return

        # step 1 - longest path layering
        layers = {}

        def get_layer(node_id):
            if node_id in layers:
                return layers[node_id]
            
            node = self.NETWORK.nodes[node_id]
            predecessors = [src for src in node["inputs"] if src is not None]
            
            if not predecessors:
                layers[node_id] = 0
            else:
                layers[node_id] = max(get_layer(p) for p in predecessors) + 1
            
            return layers[node_id]

        for node_id in self.NETWORK.nodes:
            get_layer(node_id)

        # step 2 - group by layer
        layer_groups = {}
        for node_id, layer in layers.items():
            layer_groups.setdefault(layer, []).append(node_id)

        # step 3 - position
        x_start = 50
        x_spacing = 200
        y_spacing = 150
        y_start = 50

        for layer, node_ids in sorted(layer_groups.items()):
            x = x_start + layer * x_spacing
            for i, node_id in enumerate(node_ids):
                y = y_start + i * y_spacing
                dpg.set_item_pos(self.NETWORK.nodes[node_id]["dpg_id"], [x, y])
        return 0

    def get_free_position(self):
        x_spacing = 150
        y_spacing = 100
        x_start = 20
        y_start = 20
        max_cols = 8

        occupied = set()
        for node in self.NETWORK.nodes.values():
            pos = dpg.get_item_pos(node["dpg_id"])
            if pos == [0, 0]:
                continue
            col = max(0, round((pos[0] - x_start) / x_spacing))
            row = max(0, round((pos[1] - y_start) / y_spacing))
            if 0 <= col < max_cols:
                occupied.add((col, row))

        row = 0
        while True:
            for col in range(max_cols):
                if (col, row) not in occupied:
                    return [x_start + col * x_spacing, y_start + row * y_spacing]
            row += 1

    def rebuild_from_network(self):
        try:
            dpg.delete_item("node_editor", children_only=True)
            
            # pass 1 - rebuild nodes
            for node_id, node in self.NETWORK.nodes.items():
                gate = self.REGISTRY[node["name"]]
                uid = dpg.generate_uuid()
                
                with dpg.node(label=node_id, parent="node_editor", tag=uid):
                    for i in range(gate["inputs"]):
                        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                            dpg.add_text("in")
                    for i in range(gate["outputs"]):
                        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                            dpg.add_text("out")
                
                self.NETWORK.nodes[node_id]["dpg_id"] = uid
            
            # pass 2 - rebuild links
            new_links = {}
            for _, (source_id, target_id, target_input_index) in self.NETWORK.links.items():
                source_uid = self.NETWORK.nodes[source_id]["dpg_id"]
                target_uid = self.NETWORK.nodes[target_id]["dpg_id"]
                
                source_children = dpg.get_item_children(source_uid, slot=1)
                target_children = dpg.get_item_children(target_uid, slot=1)
                
                source_out_pin = source_children[-1]
                target_in_pin = target_children[target_input_index]
                
                link_uid = dpg.generate_uuid()
                dpg.add_node_link(source_out_pin, target_in_pin, parent="node_editor", tag=link_uid)
                new_links[link_uid] = (source_id, target_id, target_input_index)
            
            self.NETWORK.links = new_links
            self.reorganize()
            self.update_preview()
            return 0
        
        except Exception as e:
            print(f"Error rebuilding from network: {e}")

    ## ------------------------ Other Utility Functions ---------------------------

    def on_viewport_resize(self):
        W = dpg.get_viewport_width()
        H = dpg.get_viewport_height()

        dpg.configure_item("toolbar", width=W)
        dpg.configure_item("sidebar", height=H-35)
        dpg.configure_item("canvas", width=W-200-W//5, height=H-35)
        dpg.configure_item("preview", width=W//5, height=H-35, pos=(W-W//5, 35))

    def build_gate_list(self):
        REGISTRY = self.REGISTRY
        DEFAULT_GATES = {"INPUT", "OUTPUT"}
        
        with dpg.group(parent="gate_list"):
            dpg.add_button(
                label="Gate Editor: OFF",
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
                show=False,
                default_value=""
            )
            with dpg.group(horizontal=True, tag="gate_editor_controls", show=False):
                dpg.add_button(
                    label="Draw",
                    tag="gate_add_btn",
                    callback=self.add_gate_node,
                    user_data=self.REGISTRY.get(self.current_gate_in_editor),
                    width=60
                )
                dpg.add_button(
                    label="Edit",
                    tag="gate_edit_toggle",
                    callback=self.toggle_gate_readonly,
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
    
    def run_network(self, sender, app_data):
        output_lines = []

        # step 1 - base files from config
        base_files = []
        for f in self.CONFIG["clingo"].get("base_files", []):
            path = tools.resource_path(f)
            if os.path.exists(path):
                base_files.append(path)
            else:
                output_lines.append(f"[WARNING] Base file not found: {f}")

        # step 2 - all .lp files from gates folder
        gate_files = []
        gates_folder = tools.resource_path(self.CONFIG["paths"]["gates_folder"])
        if os.path.exists(gates_folder):
            for filename in sorted(os.listdir(gates_folder)):
                if filename.endswith(".lp"):
                    gate_files.append(os.path.join(gates_folder, filename))
        else:
            output_lines.append(f"[ERROR] Gates folder not found: {gates_folder}")

        # step 3 - special files (main, solve, show)
        special_files = []
        networks_folder = tools.resource_path(self.CONFIG["paths"]["networks_folder"])
        for special in ["main.lp", "solve.lp", "show.lp"]:
            path = os.path.join(networks_folder, special)
            if os.path.exists(path):
                special_files.append(path)
            else:
                output_lines.append(f"[INFO] Optional file not found, skipping: {special}")

        # step 4 - network snapshot
        snapshot_path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        if not os.path.exists(snapshot_path):
            output_lines.append("[ERROR] No network snapshot to run. Build a network first.")
            self._render_run_output(output_lines)
            return 1

        # assemble full file list
        all_files = base_files + gate_files + special_files + [snapshot_path]
        output_lines.append(f"[INFO] Running {len(all_files)} files:")
        for f in all_files:
            output_lines.append(f"  {os.path.basename(f)}")
        output_lines.append("")

        # step 5 - run clingo
        try:
            result = subprocess.run(
                ["clingo"] + all_files,
                capture_output=True,
                text=True,
                timeout=self.CONFIG["clingo"]["timeout"]
            )
            clingo_output = result.stdout if result.stdout else result.stderr
            output_lines.extend(clingo_output.split("\n"))
        except subprocess.TimeoutExpired:
            output_lines.append(f"[ERROR] Clingo timed out after {self.CONFIG['clingo']['timeout']}s.")
        except FileNotFoundError:
            output_lines.append("[ERROR] Clingo not found. Is it installed and on your PATH?")
        except Exception as e:
            output_lines.append(f"[ERROR] Unexpected error: {e}")

        # step 6 - log output
        log_path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/output.log"
        try:
            with open(log_path, "a") as f:
                f.write(f"\n--- Run: {datetime.datetime.now()} ---\n")
                f.write("\n".join(output_lines))
        except Exception as e:
            output_lines.append(f"[WARNING] Could not write log: {e}")

        self._render_run_output(output_lines)
        return 0

    def _render_run_output(self, lines):
        dpg.delete_item("run_output", children_only=True)
        for line in lines:
            if line.startswith("[ERROR]"):
                color = (255, 80, 80, 255)      # red
            elif line.startswith("[WARNING]"):
                color = (255, 180, 80, 255)     # orange
            elif line.startswith("[INFO]"):
                color = (100, 180, 255, 255)    # blue
            else:
                color = (0, 255, 0, 255)        # green - normal clingo output
            dpg.add_text(line if line else " ", parent="run_output", color=color, 
                        wrap=self.CONFIG["window"]["width"]//5 - 10)