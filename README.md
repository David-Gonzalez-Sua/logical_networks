# C-MCPN: The Clingo McCulloch-Pitts Network Editor

The Clingo McCullough-Pitts Network Editor (C-MCPN) is an internally designed system for research into more efficient [artificial neural network](https://en.wikipedia.org/wiki/Neural_network_(machine_learning) (ANN) representations, inference, and learning.

C-MCPN is designed to represent, and provide inference over, [McCullough-Pitts Networks](https://en.wikipedia.org/wiki/Artificial_neuron#McCulloch%E2%80%93Pitts_(MCP)_neuron) (MCPNs). MCPNs are an early form of ANNs, preceding advancements in ANN neurons and structures that paved the way for machine learning over ANNs.

At its core, C-MCPN uses advanced satisfiability technology to represent and provide inference over ANNs. In particular, our representations and associated "algorithms" for inference are written in the language of Clingo, an [Answer Set Programming language](https://en.wikipedia.org/wiki/Answer_set_programming) (ASP) from [Potassco Technologies](https://potassco.org/). These systems are designed for solving computationally difficult problems, in particular those in [NP-Complete](https://en.wikipedia.org/wiki/NP-completeness) and [NP-Hard](https://en.wikipedia.org/wiki/NP-hardness). By merging ANN and ASP technologies we hope to discover mechanisms with which we can accelerate the learning and inference processes to create more computationally efficient systems.

## Background
The rise of large language model (LLM) and other machine learning (ML) technologies has created an exciting and simultaneously disquieting atmosphere. Massive footprints in terms of physical real estate, water and power usage, heat generation, and other issues related to contemporary machine learning training and inference are simultaneously altering the public perception of computing, both in both positive and negative ways.

C-MCPN is a part of a larger research network that seeks to create more efficient processes, in particular with respect to problems that require significant computational power. We hope to use existing technology from artificial intelligence, in particular satisfiability systems, to create a more sustainable computational landscape.

## Application Overview
C-MCPN is designed as a terminal-based utility, and is (optionally) enhanced with a graphical user interface (GUI) for user efficiency and convenience. The GUI allows for a drag-and-drop interface for rapid prototyping of ANN nodes and structures. As a domain to ground the software, we have included the ANN representations of a number of basic digital logic "gates", allowing for convenient experimentation in digital hardware as a starting point for the user.

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

# Attributions
**David J. Gonzalez Sua** · University of Northern Colorado

**Joshua T. Guerin Ph.D.** · University of Northern Colorado
