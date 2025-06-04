from flask import Flask, render_template, request
import sympy as sp
from visualizer import parse_equation, solve_and_plot, EXAMPLES, CHEATSHEET

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    latex_input = ''
    solution_latex = None
    image_url = None
    error = None
    if request.method == 'POST':
        latex_input = request.form.get('latex', '')
        try:
            eq = parse_equation(latex_input)
            sol, steps = solve_and_plot(eq, out_file='static/solution.png')
            solution_latex = sp.latex(sol)
            image_url = 'static/solution.png'
            solution_steps = steps
        except Exception as exc:
            error = str(exc)
    return render_template('index.html',
                           latex_input=latex_input,
                           solution_latex=solution_latex,
                           image_url=image_url,
                           solution_steps=solution_steps if 'solution_steps' in locals() else None,
                           examples=EXAMPLES,
                           cheatsheet=CHEATSHEET,
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)
