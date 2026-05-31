# gui_output.py

import dearpygui.dearpygui as dpg
import subprocess
import datetime
import tools
import os


class GUIOutput:

    # --------------------------- Run Network Logic -----------------------------------

    def run_network(self, sender, app_data):
        output_lines = []

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
        used_gates = set(node["name"] for node in self.NETWORK.nodes.values())

        if os.path.exists(gates_folder):
            for filename in sorted(os.listdir(gates_folder)):
                if filename.endswith(".lp"):
                    gate_name = filename[:-3].upper()
                    if gate_name in used_gates:
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
            if result.stderror:
                clingo_output += "\n" + result.stderr
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
                        # wrap=self.CONFIG["window"]["width"]//5 - 10)
                        wrap=self.CONFIG["window"]["width"] - 50)
        # dpg.set_y_scroll("run_output", dpg.get_y_scroll_max("run_output"))
        dpg.set_y_scroll("run_output", 999999)  # scroll to bottom
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
