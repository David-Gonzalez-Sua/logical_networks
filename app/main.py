# Main application file for the Logical Networks project.

import dearpygui.dearpygui as dpg
import tomllib
import os

import gui_tools as gui
import network_serializer as network


# Global variables
CONFIG = None
REGISTRY = {}
PAN_MODE = False

def load_config():
    '''Load the configuration from the config.toml file.'''
    global CONFIG
    with open("app/config.toml", "rb") as f:
        CONFIG = tomllib.load(f)
    return 0

def load_gates():
    '''Load the gates from the gates folder and store their metadata in the registry.'''
    global CONFIG, REGISTRY

    gates_folder = CONFIG["paths"]["gates_folder"]
    if not os.path.exists(gates_folder):
        os.makedirs(gates_folder)
    
    for filename in os.listdir(gates_folder):
        if filename.endswith(".lp"):
            path = os.path.join(gates_folder, filename)
            metadata = {
                "file": path,
                "name": filename[:-3],
                "inputs": 1,
                "outputs": 1
            }
    
            with open(path) as f:
                for line in f:
                    if line.startswith("%% gate:"):
                        metadata["name"] = line.split(":")[1].strip()
                    elif line.startswith("%% inputs:"):
                        metadata["inputs"] = int(line.split(":")[1].strip())
                    elif line.startswith("%% outputs:"):
                        metadata["outputs"] = int(line.split(":")[1].strip())
            
            REGISTRY[metadata["name"]] = metadata
    return 0

def main():
    '''Main function to run the application.'''
    global CONFIG, REGISTRY

    # MUST OCCUR IN ORDER
    # 1
    load_config()
    
    # 2
    load_gates()

    # 3
    dpg.create_context()
    dpg.create_viewport(
        title=CONFIG["window"]["title"],
        width=CONFIG["window"]["width"],
        height=CONFIG["window"]["height"]
    )

    app_network = network.Network()
    app_gui = gui.GUI(CONFIG, REGISTRY, app_network)
    app_gui.build_gui()

    with dpg.handler_registry():
        dpg.add_key_press_handler(key=dpg.mvKey_Delete, callback=app_gui.delete_selected)
        dpg.add_key_press_handler(key=dpg.mvKey_Back, callback=app_gui.delete_selected)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    return 0

if __name__ == "__main__":
    main()



# load_config()
# title = CONFIG["window"]["title"]
# width = CONFIG["window"]["width"]
# height = CONFIG["window"]["height"]
# gates_folder = CONFIG["paths"]["gates_folder"]
# networks_folder = CONFIG["paths"]["networks_folder"]

# load_gates()
# print("Loaded gates:")
# for gate_name, metadata in REGISTRY.items():
#     print(f"{gate_name}: {metadata}")