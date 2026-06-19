# gui_output.py

import dearpygui.dearpygui as dpg
import subprocess
import datetime
import tools
import sys
import os


class GUIOutput:

    # --------------------------- Run Network Logic -----------------------------------

    def run_network(self, sender, app_data):
        output_lines = []
        error_lines = []
        formatted = ""
        clingo_errors = ""

        # step 1 - extra files from config
        extra_files = []
        for f in self.CONFIG["clingo"].get("extra_files", []):
            path = tools.resource_path(f)
            if os.path.exists(path):
                extra_files.append(path)
            else:
                output_lines.append(f"[WARNING] Extra file not found: {f}")

        # step 2 - all .lp files from gates folder
        gate_files = []
        gates_folder = tools.resource_path(self.CONFIG["paths"]["gates_folder"])
        used_gates = set(node["type"] for node in self.NETWORK.nodes.values())

        if os.path.exists(gates_folder):
            for filename in sorted(os.listdir(gates_folder)):
                if filename.endswith(".lp"):
                    gate_type = filename[:-3].upper()
                    if gate_type in used_gates:
                        gate_files.append(os.path.join(gates_folder, filename))
        else:
            output_lines.append(f"[ERROR] Gates folder not found: {gates_folder}")

        # step 3 - base files (main, solve, show)
        base_files = []
        base_folder = tools.resource_path(self.CONFIG["paths"]["base_folder"])
        if os.path.exists(base_folder):
            for filename in sorted(os.listdir(base_folder)):
                if filename.endswith(".lp"):
                    base_files.append(os.path.join(base_folder, filename))
        else:
            output_lines.append(f"[ERROR] Base folder not found: {base_folder}")

        # step 4 - network snapshot
        snapshot_path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/preview.lp"
        if not os.path.exists(snapshot_path):
            output_lines.append("[ERROR] No network snapshot to run. Build a network first.")
            self._render_run_output(output_lines)
            return 1

        # assemble full file list
        all_files = extra_files + gate_files + base_files + [snapshot_path]
        file_names = " ".join(os.path.basename(f) for f in all_files)
        output_lines.append(f"[INFO] Running {len(all_files)} files: {file_names}")
        output_lines.append("")

        # step 5 - run clingo
        try:
            result = subprocess.run(
                ["clingo"] + all_files,
                capture_output=True,
                text=True,
                timeout=self.CONFIG["clingo"]["timeout"]
            )

            clingo_output = result.stdout
            clingo_errors = result.stderr

            # parse output
            interpreter_path = tools.resource_path(self.CONFIG["paths"]["output_interpreter_folder"])
            if not os.path.exists(interpreter_path):
                formatted = "[ERROR] Output interpreter not found.\n" + f"Expected at: {interpreter_path}"
            else:
                sys.path.insert(0, interpreter_path)
                from interpreter import parse
                facts, values = parse(clingo_output)
                formatter = self.load_output_script(None, None)
                formatted = formatter.format(facts, values) if formatter else "\n".join(facts)

                # update node values
                for node_id, val in values.items():
                    node_id = node_id.strip('"')  # remove quotes if present
                    if node_id in self.NETWORK.nodes:
                        self.NETWORK.nodes[node_id]["val"] = val

                self.save_snapshot(None, None)  # save updated values to snapshot
                
                # update node displays
                for node_id in self.NETWORK.nodes:
                    self.update_node_display(node_id)

            # add raw output to logs
            if clingo_output:
                output_lines.extend(clingo_output.split("\n"))
            if clingo_errors:
                error_lines = clingo_errors.split("\n")
        
        except subprocess.TimeoutExpired:
            output_lines.append(f"[ERROR] Clingo timed out after {self.CONFIG['clingo']['timeout']}s.")
        except FileNotFoundError:
            output_lines.append("[ERROR] Clingo not found. Is it installed and on your PATH?")
        except Exception as e:
            output_lines.append(f"[ERROR] Unexpected error: {e}")

        # step 6 - log output
        output_log_path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/output.log"
        error_log_path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/errors.log"
        formatted_log_path = tools.resource_path(self.CONFIG["paths"]["snapshots_folder"]) + "/formatted.log"
        try:
            # Check if over 10MB log size and warn if so
            if os.path.exists(output_log_path) and os.path.getsize(output_log_path) > 10 * 1024 * 1024:
                output_lines.append("[WARNING] Output log is over 10MB. Consider clearing it to save disk space.")
            with open(output_log_path, "a") as f:
                f.write(f"\n--- Run: {datetime.datetime.now()} ---\n")
                f.write("\n".join(output_lines))
            with open(error_log_path, "a") as f:
                f.write(f"\n--- Run: {datetime.datetime.now()} ---\n")
                f.write("\n".join(error_lines))
            with open(formatted_log_path, "a") as f:
                f.write(f"\n--- Run: {datetime.datetime.now()} ---\n")
                f.write(formatted)
        except Exception as e:
            output_lines.append(f"[WARNING] Could not write log: {e}")

        self._render_output(output_lines)
        self._render_errors(error_lines)
        self._render_formatted(formatted)

        if clingo_errors:
            self.switch_output_tab("errors")
        elif self.CONFIG["extra"]["default_to_formatted_output"]:
            self.switch_output_tab("formatted")
        else:
            self.switch_output_tab("output")

        return 0

    def _render_output(self, lines):
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
                        # wrap=self.CONFIG["window"]["width"]//5 - 10)
                        wrap=dpg.get_viewport_width() - 20)
        # dpg.set_y_scroll("run_output", dpg.get_y_scroll_max("run_output"))
        dpg.set_y_scroll("run_output", 999999)  # scroll to bottom
        return 0
            
    def _render_errors(self, lines):
        dpg.delete_item("run_errors", children_only=True)
        for line in lines:
            if line.startswith("ERROR") or "error" in line.lower():
                color = (255, 80, 80, 255)
            elif "warning" in line.lower() or "info" in line.lower():
                color = (255, 180, 80, 255)
            else:
                color = (160, 160, 160, 255)
            dpg.add_text(line if line else " ", parent="run_errors", color=color,
                        wrap=dpg.get_viewport_width() - 20)
        dpg.set_y_scroll("run_errors", 99999)
        return 0

    def _render_formatted(self, formatted):
        dpg.delete_item("run_formatted", children_only=True)
        color = (0, 255, 0, 255)  # green
        for line in formatted.split("\n"):
            dpg.add_text(line if line else " ", parent="run_formatted", color=color,
                         wrap=dpg.get_viewport_width() - 20)
        # dpg.set_y_scroll("run_formatted", 99999)
        return 0
    ## --------------------------- Output Callbacks -----------------------------------

    def toggle_output_window(self, sender, app_data):
        self.output_shown = not self.output_shown
        W = dpg.get_viewport_width()
        H = dpg.get_viewport_height()
        
        if self.output_shown:
            dpg.set_item_label("output_toggle_btn", "Output: ON")
            dpg.show_item("output_window")
            self._resize_for_output(W, H, True)
        else:
            dpg.set_item_label("output_toggle_btn", "Output: OFF")
            dpg.hide_item("output_window")
            self._resize_for_output(W, H, False)
        return 0

    def _resize_for_output(self, W, H, output_open):
        output_height = self.CONFIG["window"]["output_height"]
        main_h = H - 35 - (output_height if output_open else 0)
        
        dpg.configure_item("sidebar", height=main_h)
        dpg.configure_item("canvas", height=main_h)
        dpg.configure_item("preview", height=main_h)
        
        if output_open:
            dpg.configure_item("output_window",
                width=W, 
                height=output_height,
                pos=(0, 35 + main_h)
            )
        return 0

    def clear_output(self, sender, app_data):
        dpg.delete_item("run_output", children_only=True)
        dpg.delete_item("run_errors", children_only=True)
        dpg.delete_item("run_formatted", children_only=True)
        return 0
    
    def switch_output_tab(self, tab):
        tabs = {"output": "run_output", "errors": "run_errors", "formatted": "run_formatted"}
        btns = {"output": "tab_output_btn", "errors": "tab_errors_btn", "formatted": "tab_formatted_btn"}
        labels = {"output": "Std Out", "errors": "Std Err", "formatted": "Formatted"}
        
        for t, widget in tabs.items():
            if t == tab:
                dpg.show_item(widget)
                dpg.set_item_label(btns[t], f"> {labels[t]}")
            else:
                dpg.hide_item(widget)
                dpg.set_item_label(btns[t], labels[t])
        return 0