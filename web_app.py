from flask import Flask, render_template, request, jsonify
from random import shuffle

from spelling_bee.spelling_bee import auto_spelling_bee
from wordle.wordle import generate_guesses

from sudoku.sudoku import auto_sudoku
from letter_boxed.letter_boxed import auto_letter_boxed

from utils.scraping_utils import spelling_bee_data
from utils.scraping_utils import sudoku_data
from utils.scraping_utils import connections_data
from utils.scraping_utils import letter_boxed_data

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

# API endpoint for getting wordle answers for the passed guess info
@app.route('/api/wordle', methods=['POST'])
def api_wordle():
    data = request.get_json()
    guess_info = data.get('guessInfo')
    result = generate_guesses(guess_info)
    return jsonify(result=result)

# API endpoint for getting spelling bee answers for the passed puzzle
@app.route('/api/spelling_bee', methods=['POST'])
def api_spelling_bee():
    data = request.get_json()
    center_letter = data.get('centerLetter')
    letters_list = data.get('lettersList')
    result = auto_spelling_bee(center_letter, letters_list)
    return jsonify(result=result)

# API endpoint for getting today's spelling bee puzzle
@app.route('/api/spelling_bee/todays_puzzle', methods=['GET'])
def api_sb_todays_puzzle():
    _, lettters_list = spelling_bee_data()
    result = lettters_list
    return jsonify(result=result)

# API endpoint for solving a sudoku puzzle
@app.route('/api/sudoku', methods=['POST'])
def api_sudoku():
    data = request.get_json()
    board = data.get('board')
    result = auto_sudoku(board)
    return jsonify(result=result)

# API endpoint for getting today's easy sudoku puzzle
@app.route('/api/sudoku/easy', methods=['GET'])
def api_sudoku_easy():
    sudoku = sudoku_data("easy")
    result = sudoku
    return jsonify(result=result)

# API endpoint for getting today's medium sudoku puzzle
@app.route('/api/sudoku/medium', methods=['GET'])
def api_sudoku_medium():
    sudoku = sudoku_data("medium")
    result = sudoku
    return jsonify(result=result)

# API endpoint for getting today's hard sudoku puzzle
@app.route('/api/sudoku/hard', methods=['GET'])
def api_sudoku_hard():
    sudoku = sudoku_data("hard")
    result = sudoku
    return jsonify(result=result)



# API endpoint for getting today's connections puzzle
@app.route('/api/connections/todays_puzzle', methods=['GET'])
def api_c_todays_puzzle():
    solutions = connections_data()
    board = [word for group in solutions for word in group]
    shuffle(board)
    result = board
    return jsonify(result=result)

# API endpoint for solving a letter boxed puzzle
@app.route('/api/letter_boxed', methods=['POST'])
def api_letter_boxed():
    data = request.get_json()
    board = data.get('board')
    result = auto_letter_boxed(board)
    return jsonify(result=result)

# API endpoint for getting today's letter boxed puzzle
@app.route('/api/letter_boxed/todays_puzzle', methods=['GET'])
def api_lb_todays_puzzle():
    sides = letter_boxed_data()
    result = sides
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)