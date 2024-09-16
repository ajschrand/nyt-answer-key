from utils.str_utils import Menu
from utils import scraping_utils


def spelling_bee():
    from spelling_bee import spelling_bee

    def spelling_bee_custom():
        spelling_bee.play_spelling_bee()

    def spelling_bee_nyt():
        center_letter, letters_list = scraping_utils.spelling_bee_data()
        answers = spelling_bee.auto_spelling_bee(center_letter, letters_list)
        print(answers)

    menu = Menu(
        "Would you like to solve a custom Spelling Bee puzzle or the current NYT Spelling Bee puzzle?")
    menu.add_option("Custom", spelling_bee_custom)
    menu.add_option("NYT", spelling_bee_nyt)
    menu.run()


def wordle():
    from wordle import wordle

    def wordle_manual():
        wordle.play_wordle()

    def wordle_auto_specific():
        word = input("Enter the word to guess: ")
        print("")
        wordle.auto_wordle(word, print_guesses=True)

    def wordle_auto_current():
        word = scraping_utils.wordle_data()
        wordle.auto_wordle(word, print_guesses=True)

    menu = Menu("What type of Wordle game would you like to play?")
    menu.add_option("Manual", wordle_manual)
    menu.add_option("Automatic (specific NYT word)", wordle_auto_specific)
    menu.add_option("Automatic (current NYT word)", wordle_auto_current)
    menu.run()


def connections():
    from connections import connections

    def connections_manual_custom():
        connections.play_connections()

    def connections_manual_nyt():
        from random import shuffle

        solutions = scraping_utils.connections_data()
        word_list = [word for solution in solutions for word in solution]
        shuffle(word_list)

        print(f"Board: {" ".join(word_list)}")
        connections.play_connections()

    def connections_auto_custom():
        print("Enter 4 solution groups as lists of words separated by spaces, each on its own line")
        solutions = []
        for _ in range(4):
            solutions.append(input().split())

        print("")
        connections.auto_connections(solutions)

    def connections_auto_nyt():
        solutions = scraping_utils.connections_data()
        connections.auto_connections(solutions)

    menu = Menu("What type of Connections game would you like to play?")
    menu.add_option("Manual (custom board)", connections_manual_custom)
    menu.add_option("Manual (NYT board)", connections_manual_nyt)
    menu.add_option("Automatic (custom board)", connections_auto_custom)
    menu.add_option("Automatic (NYT board)", connections_auto_nyt)
    menu.run()


def sudoku():
    from sudoku import sudoku

    def sudoku_custom():
        sudoku.play_sudoku()

    def sudoku_nyt(difficulty):
        one_D_board = scraping_utils.sudoku_data(difficulty)
        two_D_board = [one_D_board[i:i + 9]
                       for i in range(0, len(one_D_board), 9)]
        sudoku.solve_sudoku(two_D_board)

    menu = Menu(
        "What type of Sudoku game would you like to automatically solve?")
    menu.add_option("Manual", sudoku_custom)
    menu.add_option("NYT (easy)", lambda: sudoku_nyt("easy"))
    menu.add_option("NYT (medium)", lambda: sudoku_nyt("medium"))
    menu.add_option("NYT (hard)", lambda: sudoku_nyt("hard"))
    menu.run()


def letter_boxed():
    from letter_boxed import letter_boxed

    def letter_boxed_custom():
        letter_boxed.play_letter_boxed()

    def letter_boxed_nyt():
        board = scraping_utils.letter_boxed_data()
        solutions = letter_boxed.auto_letter_boxed(board)
        print(solutions[:11], 1)

    menu = Menu(
        "Would you like to solve a custom Letter Boxed puzzle or the current NYT Letter Boxed puzzle?")
    menu.add_option("Custom", letter_boxed_custom)
    menu.add_option("NYT", letter_boxed_nyt)
    menu.run()


if __name__ == "__main__":
    print("Welcome to NYT Answer Key!")
    
    menu = Menu("Which game would you like to play?")
    menu.add_option("Spelling Bee", spelling_bee)
    menu.add_option("Wordle", wordle)
    menu.add_option("Connections", connections)
    menu.add_option("Sudoku", sudoku)
    menu.add_option("Letter Boxed", letter_boxed)

    while True:
        menu.run()

        if input("Play another game? (y/n): ") != "y":
            break

        print("")
