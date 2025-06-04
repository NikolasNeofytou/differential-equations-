# differential-equations-
This repository contains a simple command line tool to visualise differential
equations.  The program is written in Python and relies on ``sympy`` and
``matplotlib`` for solving and plotting.

### Installation

Install the dependencies with ``pip``:

```bash
pip install -r requirements.txt
```

### Usage

Run ``visualizer.py`` and enter a differential equation in LaTeX form or select
one of the provided examples:

```bash
python3 visualizer.py
```

After solving, a graph is saved to ``solution.png`` in the current directory.
