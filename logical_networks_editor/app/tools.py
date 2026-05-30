# tools.py
# Utility functions for the Logical Networks project

import sys
import os
import tomllib


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
    return REGISTRY