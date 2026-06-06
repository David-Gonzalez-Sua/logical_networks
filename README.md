# C-MCPN
### Clingo McCulloch-Pitts Network Editor

**David J. Gonzalez Sua** · University of Northern Colorado

**Joshua T. Guerin Ph.D.** · University of Northern Colorado

---

*A visual node-based editor for building and executing neural networks defined in Answer Set Programming (ASP) using Clingo. Full abstract coming soon.*

---

## Install & Run

The install and run scripts are located in `logical_networks_editor/`.

### macOS / Linux

**Dependencies:** [Clingo](https://potassco.org/clingo/) (`brew install clingo` on Mac), Python 3.12+

```bash
bash install.sh
bash run.sh
```

### Windows

**Dependencies:** [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

```bat
install.bat
run.bat
```

---

## Terminal Usage

To run a network directly on the terminal, the files needed are located in `logical_networks_editor/C-MCPN/`:

```bash
clingo base/main.lp networks/[network].lp gates/[gate_1].lp ... gates/[gate_n].lp
```

Pipe the Clingo output into the interpreter provided for more readable output:

```bash
clingo base/main.lp ... | python3 tools/interpreter.py
```

To run the 1BitAdder sample network:
*NOTE: an input and an expansion for this are in development*

```bash
clingo base/main.lp networks/1BitAdder.lp gates/input.lp gates/output.lp gates/and.lp gates/or.lp gates/xor.lp | python3 tools/interpreter.py
```

---

![Python](https://img.shields.io/badge/python-3.12-blue)
![Clingo](https://img.shields.io/badge/clingo-5.8.0-orange)
<!-- ![License](https://img.shields.io/badge/license-MIT-green) -->