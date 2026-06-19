# tools.py
# Utility functions for the Logical Networks project

import sys
import os
import tomllib


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    
    # walk up from __file__ until we find the relative path
    base = os.path.dirname(os.path.abspath(__file__))
    while base != os.path.dirname(base):  # stop at filesystem root
        candidate = os.path.join(base, relative)
        if os.path.exists(candidate):
            return candidate
        base = os.path.dirname(base)
    
    raise FileNotFoundError(f"Could not find {relative} from any parent directory.")

def load_config():
    '''Load the configuration from the config.toml file.'''
    with open(resource_path("app/config.toml"), "rb") as f:
        CONFIG = tomllib.load(f)
    return CONFIG

def load_gates(CONFIG):
    '''Load the gates from the gates folder and store their metadata in the registry.'''
    REGISTRY = {}
    gates_folder = resource_path(CONFIG["paths"]["gates_folder"])
    if not os.path.exists(gates_folder):
        os.makedirs(gates_folder)
    
    for filename in os.listdir(gates_folder):
        if filename.endswith(".lp"):
            path = os.path.join(gates_folder, filename)
            metadata = {
                "file": path,
                "type": filename[:-3],
                "inputs": 1,
                "outputs": 1
            }
    
            with open(path) as f:
                for line in f:
                    if line.startswith("%% gate:"):
                        metadata["type"] = line.split(":")[1].strip()
                    elif line.startswith("%% inputs:"):
                        metadata["inputs"] = int(line.split(":")[1].strip())
                    elif line.startswith("%% outputs:"):
                        metadata["outputs"] = int(line.split(":")[1].strip())
            
            REGISTRY[metadata["type"]] = metadata
    return REGISTRY