# gui_canvas.py

import dearpygui.dearpygui as dpg
import tools


class GUICanvas:

    ## ------------------------------ Canvas Callbacks ------------------------------

    def add_gate_node(self, sender, app_data, user_data):
        '''Adds a new node to the canvas based on the gate type.'''
        gate = user_data
        gate_type = gate["type"]
        
        self.NETWORK.counts[gate_type] = self.NETWORK.counts.get(gate_type, 0) + 1
        node_id = f"{gate_type}_{self.NETWORK.counts[gate_type]}"
        uid = dpg.generate_uuid()
        
        with dpg.node(label=node_id, parent="node_editor", tag=uid):
            for i in range(gate["inputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                    dpg.add_text("in")
            for i in range(gate["outputs"]):
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                    dpg.add_text("out")
        
        result = self.NETWORK.add_node(node_id, gate_type, gate["inputs"], uid)
        if result == 1:
            dpg.delete_item(uid)
            self.NETWORK.counts[gate_type] -= 1
            return 1
        pos = self.get_free_position()
        dpg.set_item_pos(uid, pos)

        self.update_preview()
        self.update_input_template()

        if dpg.is_item_shown("gate_editor_box_wrapper"):
            self.select_gate_for_editor(sender, app_data, gate_type)
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
    
    def clear_canvas(self, sender, app_data):
        if not self.NETWORK.nodes:
            return 0
        
        if not self.CONFIG["window"].get("warn_on_clear_canvas", True):
            self._confirm_clear_canvas(sender, app_data)
            return 0
        
        pos = dpg.get_mouse_pos(local=False)
        if dpg.does_item_exist("clear_confirm_popup"):
            dpg.delete_item("clear_confirm_popup")
        
        with dpg.window(label="Confirm Clear", modal=True, tag="clear_confirm_popup", no_resize=True, pos=pos):
            dpg.add_text("This will delete all nodes and links. Are you sure?", color=(255, 180, 80, 255))
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label="Clear", width=80, callback=lambda: self._dismiss_clear_warning(False))
                dpg.add_button(label="Clear, don't ask again", width=200, callback=lambda: self._dismiss_clear_warning(True))
                dpg.add_button(label="Cancel", width=80, callback=lambda: dpg.delete_item("clear_confirm_popup"))
        return 0
    
    def _dismiss_clear_warning(self, dont_show_again):
        if dont_show_again:
            self.CONFIG["window"]["warn_on_clear_canvas"] = False
            config_path = tools.resource_path("app/config.toml")
            with open(config_path, "r") as f:
                content = f.read()
            content = content.replace("warn_on_clear_canvas = true", "warn_on_clear_canvas = false")
            with open(config_path, "w") as f:
                f.write(content)
        
        dpg.delete_item("clear_confirm_popup")
        self._confirm_clear_canvas(None, None)

    def _confirm_clear_canvas(self, sender, app_data):
        # delete all links FIRST
        for link_id in list(self.NETWORK.links.keys()):
            dpg.delete_item(link_id)
        
        # then delete all nodes
        for node_id, node in list(self.NETWORK.nodes.items()):
            dpg.delete_item(node["dpg_id"])
        
        self.NETWORK.nodes = {}
        self.NETWORK.links = {}
        self.NETWORK.counts = {}
        self.NETWORK.input_nodes = []
        
        self.update_preview()
        self.update_input_template()
        dpg.delete_item("clear_confirm_popup")
        return 0

    def delete_selected(self, sender, app_data):
        selected_nodes = dpg.get_selected_nodes("node_editor")
        selected_links = dpg.get_selected_links("node_editor")
        
        # delete explicitly selected links first
        for link in selected_links:
            self.NETWORK.delete_link(link)
            dpg.delete_item(link)
        
        # before deleting nodes, find and delete ALL links attached to them
        # (not just selected ones) to avoid dangling/double-delete
        for node in selected_nodes:
            node_id = next(k for k, v in self.NETWORK.nodes.items() if v["dpg_id"] == node)
            
            # delete any links still attached to this node
            for link_id, (src, tgt, _) in list(self.NETWORK.links.items()):
                if src == node_id or tgt == node_id:
                    self.NETWORK.delete_link(link_id)
                    dpg.delete_item(link_id)
            
            self.NETWORK.delete_node(node_id)
            dpg.delete_item(node)
        
        self.update_preview()
        self.update_input_template()
        return 0
    
    def delete_selected_keypress(self, sender, app_data):
        # block if any modal popup is open
        for tag in ["rename_popup", "save_popup", "load_popup", "error_popup", "clear_confirm_popup"]:
            if dpg.does_item_exist(tag) and dpg.is_item_shown(tag):
                return 1
        
        if not dpg.is_item_hovered("node_editor"):
            return 1
        
        self.delete_selected(sender, app_data)
        return 0
    
    def on_node_double_click(self, sender, app_data):
        pos = dpg.get_mouse_pos()
        if dpg.does_item_exist("rename_popup"):
            dpg.delete_item("rename_popup")

        for node_id, node in self.NETWORK.nodes.items():
            if dpg.is_item_hovered(node["dpg_id"]):
                with dpg.window(label="Rename Node", modal=True, tag="rename_popup", no_resize=True, pos=pos):
                    dpg.add_text(f"Rename {node_id}:")
                    dpg.add_input_text(tag="rename_input", default_value=node_id)
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Rename", callback=self._confirm_rename, user_data=node_id)
                        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("rename_popup"))
                dpg.focus_item("rename_input")  # Focuses input box for convenience
                break

    def _confirm_rename(self, sender, app_data, user_data):
        '''Confirms the renaming of a node, updating all relevant data structures and the display.'''
        old_id = user_data
        new_id = dpg.get_value("rename_input")
        if not new_id or new_id == old_id or new_id in self.NETWORK.nodes:
            dpg.delete_item("rename_popup")
            return 1
        
        # update network
        self.NETWORK.nodes[new_id] = self.NETWORK.nodes.pop(old_id)
        if old_id in self.NETWORK.input_nodes:
            idx = self.NETWORK.input_nodes.index(old_id)
            self.NETWORK.input_nodes[idx] = new_id

        # update links
        for link_id, (src, tgt, idx) in self.NETWORK.links.items():
            if src == old_id:
                self.NETWORK.links[link_id] = (new_id, tgt, idx)
            if tgt == old_id:
                self.NETWORK.links[link_id] = (src, new_id, idx)
        
        # update inputs/outputs lists on all nodes
        for node in self.NETWORK.nodes.values():
            node["inputs"] = [new_id if x == old_id else x for x in node["inputs"]]
            node["outputs"] = [new_id if x == old_id else x for x in node["outputs"]]

        # update dpg label
        dpg.set_item_label(self.NETWORK.nodes[new_id]["dpg_id"], new_id)
        dpg.delete_item("rename_popup")
        self.update_preview()
        return 0

    ## -------------------------- Canvas Utility Functions ----------------------------
    
    def pan(self, dx, dy):
        if not dpg.is_item_hovered("node_editor"):
            return 1

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
                gate = self.REGISTRY[node["type"]]
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
