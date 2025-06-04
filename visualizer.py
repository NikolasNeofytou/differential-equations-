import sys
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy import Eq
from sympy.plotting import plot, plot3d

EXAMPLES = [
    r"\frac{d}{dx} y(x) = y(x)",
    r"\frac{d}{dx} y(x) + y(x) = 0",
    r"\frac{\partial u(x,t)}{\partial t} - \frac{\partial^2 u(x,t)}{\partial x^2} = 0"
]

CHEATSHEET = r"""
Common LaTeX commands:
  \frac{d y}{d x}          first derivative
  \frac{\partial u}{\partial x} partial derivative
  \frac{\partial^2 u}{\partial x^2} second partial derivative
  y(x), u(x, t)             functions of variables
"""

def display_examples():
    print(CHEATSHEET)
    print("Examples of differential equations:")
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"  {i}: {ex}")


def parse_equation(latex_eq: str) -> Eq:
    if '=' not in latex_eq:
        raise ValueError("Equation must contain '=' sign")
    lhs_latex, rhs_latex = [s.strip() for s in latex_eq.split('=', 1)]
    lhs = parse_latex(lhs_latex)
    rhs = parse_latex(rhs_latex)
    return Eq(lhs, rhs)


def substitute_constants(expr):
    constants = [c for c in expr.atoms(sp.Symbol) if c.name.startswith('C')]
    for C in constants:
        expr = expr.subs(C, 1)
    return expr

def substitute_undef_funcs(expr):
    try:
        from sympy.core.function import AppliedUndef
    except Exception:
        return expr
    funcs = list(expr.atoms(AppliedUndef))
    for f in funcs:
        expr = expr.subs(f, 0)
    return expr


def solve_and_plot(eq: Eq, out_file: str = 'solution.png'):
    """Solve the equation and save a plot along with textual steps.

    Parameters
    ----------
    eq : sympy.Eq
        Equation to solve.
    out_file : str
        Output path for the generated plot.

    Returns
    -------
    (sympy.Eq, list[str])
        Solved equation and list of steps performed.
    """
    steps = []
    funcs = list(eq.atoms(sp.Function))
    if not funcs:
        raise ValueError("Could not determine dependent variable in equation")
    func = funcs[0]
    vars_ = func.args
    try:
        if len(vars_) == 1:
            var = vars_[0]
            steps.append(f"Identified an ordinary differential equation in {var}.")
            steps.append("Solving using SymPy dsolve().")
            sol = sp.dsolve(eq)
            sol_expr = sol.rhs
            steps.append("Simplifying solution and substituting constants.")
            sol_expr = substitute_constants(sol_expr)
            sol_expr = substitute_undef_funcs(sol_expr)
            steps.append("Generating 2D plot of the solution.")
            p = plot(sol_expr, (var, -5, 5), show=False)
            p.save(out_file)
            sol = sp.Eq(func, sol_expr)
        else:
            steps.append("Identified a partial differential equation.")
            steps.append("Solving using SymPy pdsolve().")
            sol = sp.pdsolve(eq)
            sol_expr = sol.rhs
            if len(vars_) == 2:
                var1, var2 = vars_
                steps.append("Simplifying solution and substituting constants.")
                sol_expr = substitute_constants(sol_expr)
                sol_expr = substitute_undef_funcs(sol_expr)
                steps.append("Generating 3D plot of the solution.")
                p = plot3d(sol_expr, (var1, -5, 5), (var2, -5, 5), show=False)
                p.save(out_file)
                sol = sp.Eq(func, sol_expr)
            else:
                raise NotImplementedError("More than two independent variables")
    except NotImplementedError as e:
        raise NotImplementedError("SymPy could not solve this equation") from e
    return sol, steps


def main():
    display_examples()
    inp = input("Enter LaTeX equation or number: ").strip()
    if inp.isdigit() and 1 <= int(inp) <= len(EXAMPLES):
        latex_eq = EXAMPLES[int(inp)-1]
    else:
        latex_eq = inp
    try:
        eq = parse_equation(latex_eq)
    except Exception as e:
        print("Error parsing equation:", e)
        sys.exit(1)
    sol = solve_and_plot(eq)
    print("Solution:")
    sp.pprint(sol)
    print("Graph saved to solution.png")

if __name__ == "__main__":
    main()
