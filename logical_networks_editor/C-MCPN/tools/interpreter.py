# interpreter.py
# This script interprets Clingo Answer Set output
#
# inputs: clingo output from stdin, a file, or a string variable
# outputs: (list of facts "val(neuron_id, value)."), dictionary of values{neuron_id, value})
#
# Usage:
# as pipe -- NOTE: only prints formatted facts when piped, not the values dictionary
#    clingo files.lp | python interpreter.py
# with file
#    python interpreter.py output.txt
# with raw string from another script
#    from interpreter import parse
#    result = parse(clingo_output_string)

import sys


def get_input(source=None):
    '''
    Accept Clingo output from:
    - None / '-'     : stdin (pipe or CLI)
    - str path       : file path
    - other str      : raw string content
    '''
    if source is None or source == '-':
        if not sys.stdin.isatty():
            return sys.stdin.read()
        return ""
    
    try:
        with open(source) as f:
            return f.read()
    except (FileNotFoundError, OSError):
        # not a valid path, treat as raw string
        return source
    
def parse(source=None):
    content = get_input(source).split("\n")
    
    toks_last = None
    toks = None
    
    for line in content:
        toks_next = line.split()
        if not toks_next:
            continue
        if toks_next[0].startswith(("OPT", "SAT", "UNSAT")):
            status = toks_next[0]
            break
        toks_last = toks
        toks = toks_next
    else:
        return [], {}
    
    if status.startswith("UNSAT"):
        print("No solution found.")
        return [], {}
    
    if status.startswith("OPT"):
        toks = toks_last
    
    facts = []
    values = {}
    for t in toks:
        if t.startswith("val"):
            line = t[4:-1]
            param = line.split(',')
            neuron_id_raw = param[0]
            neuron_id_clean = neuron_id_raw.strip('"')
            value = param[1]
            facts.append(f"val({neuron_id_raw}, {value}).")
            values[neuron_id_clean] = value
        else:
            facts.append(t.replace(",", ", ") + ".")
    
    return facts, values

if __name__ == "__main__":
    # called directly from CLI or as a pipe
    source = sys.argv[1] if len(sys.argv) > 1 else None
    facts, values = parse(source)
    print(facts)
