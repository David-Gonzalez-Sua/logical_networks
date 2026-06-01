## script: default
## description: Default output formatter

def format(facts, values):
    output = ""

    # Format values first
    if values:
        output += "Neuron Values:\n"
        for neuron_id, value in values.items():
            output += f"  {neuron_id}: {value}\n"
        output += "\n"

    # Then format facts
    if facts:
        output += "Facts:\n"
        for fact in facts:
            output += f"  {fact}\n"
            
    return output