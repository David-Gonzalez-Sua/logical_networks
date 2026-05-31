# Main application file for the Logical Networks project.

import dearpygui.dearpygui as dpg

import tools
import gui_tools as gui
import network_serializer as network


# Global variables
CONFIG = None
REGISTRY = {}

def main():
    '''Main function to run the application.'''
    global CONFIG, REGISTRY

    # MUST OCCUR IN ORDER
    # 1
    CONFIG = tools.load_config()
    
    # 2
    REGISTRY = tools.load_gates(CONFIG)

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

    dpg.set_viewport_resize_callback(app_gui.on_viewport_resize)
    
    with dpg.handler_registry():
        dpg.add_key_press_handler(key=dpg.mvKey_Delete, callback=app_gui.delete_selected)
        dpg.add_key_press_handler(key=dpg.mvKey_Back, callback=app_gui.delete_selected)

        dpg.add_key_press_handler(key=dpg.mvKey_Down,    callback=lambda: app_gui.pan(0, -20))
        dpg.add_key_press_handler(key=dpg.mvKey_Up,  callback=lambda: app_gui.pan(0, 20))
        dpg.add_key_press_handler(key=dpg.mvKey_Right,  callback=lambda: app_gui.pan(-20, 0))
        dpg.add_key_press_handler(key=dpg.mvKey_Left, callback=lambda: app_gui.pan(20, 0))

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    return 0

if __name__ == "__main__":
    main()
