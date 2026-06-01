# C-MCPN
### Clingo McCulloch-Pitts Network Editor

**David J. Gonzalez Sua** · University of Northern Colorado

**Joshua T. Guerin Ph.D.** · University of Northern Colorado

---

*A visual node-based editor for building and executing neural networks defined in Answer Set Programming (ASP) using Clingo. Full abstract coming soon.*

---

## Install & Run

To install and use the app, the two necessary files are located in: logical_networks_editor/

```bash
bash install.sh
bash run.sh
```

To run a network directly on the terminal, the files needed are located in: logical_networks_editor/C-MCPN/

```bash
clingo base/main.lp networks/[network].lp gates/[gate_1].lp ... gates/[gate_n].lp
```

Pipe the clingo output into the interpreter provided for somewhat more readable output:

```bash
clingo base/main.lp ... | python3 tools/interpreter.py
```

To run the 1BitAdder sample network on the terminal, use the following command: 
*NOTE: an input and an expansion for this are in development*

```bash
clingo base/main.lp networks/1BitAdder.lp gates/input.lp gates/output.lp gates/and.lp gates/or.lp gates/xor.lp | python3 tools/interpreter.py
```

![Python](https://img.shields.io/badge/python-3.11-blue)
<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->
> Requires Python 3.14.5+
> Requires Clingo 5.8.0+

<!-- Open preview: Cmd+Shift+V opens it in a new tab, or Cmd+K V opens it side-by-side with your editor. -->