from flask import Flask, render_template, request, jsonify
from wordle.wordle import generate_guesses

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spelling_bee')
def spelling_bee():
    return render_template('spelling_bee.html')

@app.route('/wordle')
def wordle():
    return render_template('wordle.html')

@app.route('/connections')
def connections():
    return render_template('connections.html')

@app.route('/sudoku')
def sudoku():
    return render_template('sudoku.html')

@app.route('/letter_boxed')
def letter_boxed():
    return render_template('letter_boxed.html')

# API endpoint for Wordle logic
@app.route('/api/wordle', methods=['POST'])
def api_wordle():
    data = request.get_json()
    guess_info = data.get('guess_info')
    result = generate_guesses(guess_info)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)