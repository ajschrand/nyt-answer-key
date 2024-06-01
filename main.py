from utils.str_utils import get_menu_input
from utils import scraping_utils


def spelling_bee():
    from spelling_bee import spelling_bee

    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")

    menu_input = get_menu_input(2)
    if menu_input == 1:
        spelling_bee.play_spelling_bee()
    elif menu_input == 2:
        center_letter, letters_list = scraping_utils.spelling_bee_data()
        spelling_bee.auto_spelling_bee(center_letter, letters_list)


def wordle():
    from wordle import wordle

    print("Would you like assistance with a manual Wordle game or to play automatically?")
    print("1 - Manual")
    print("2 - Automatic")

    menu_input = get_menu_input(2)
    if menu_input == 1:
        wordle.play_wordle()
    elif menu_input == 2:
        print("Solve custom word or current NYT word?")
        print("1 - Custom")
        print("2 - NYT")

        menu_input = get_menu_input(2)
        if menu_input == 1:
            print("Enter the word to guess")
            word = input()
            print("")

            wordle.auto_wordle(word, print_guesses=True)
        elif menu_input == 2:
            wordle.auto_wordle(scraping_utils.wordle_data(),
                               print_guesses=True)


def connections():
    from connections import connections

    print("Would you assistance with a manual Connections game or to play automatically?")
    print("1 - Manual")
    print("2 - Automatic")

    game_type = get_menu_input(2)

    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")

    puzzle_source = get_menu_input(2)

    if puzzle_source == 1:
        if game_type == 1:
            connections.play_connections()
        elif game_type == 2:
            print(
                "Enter 4 solution groups as lists of words separated by spaces, each on its own line")
            solutions = []
            for _ in range(4):
                solutions.append(input().split())

            print("")
            connections.auto_connections(solutions)
    elif puzzle_source == 2:
        solutions = scraping_utils.connections_data()

        if game_type == 1:
            from random import shuffle

            word_list = [word for solution in solutions for word in solution]
            shuffle(word_list)

            print(f"Board: {" ".join(word_list)}")
            connections.play_connections()
        elif game_type == 2:
            connections.auto_connections(solutions)


def sudoku():
    from sudoku import sudoku

    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")

    menu_input = get_menu_input(2)
    if menu_input == 1:
        sudoku.play_sudoku()
    elif menu_input == 2:
        print("Solve easy, medium, or hard puzzle?")
        print("1 - Easy")
        print("2 - Medium")
        print("3 - Hard")

        menu_input = get_menu_input(3)
        one_D_board = []
        if menu_input == 1:
            one_D_board = scraping_utils.sudoku_data("easy")
        elif menu_input == 2:
            one_D_board = scraping_utils.sudoku_data("medium")
        elif menu_input == 3:
            one_D_board = scraping_utils.sudoku_data("hard")

        two_D_board = []
        row = []
        for i, num in enumerate(one_D_board):
            row.append(num)

            if (i + 1) % 9 == 0:
                two_D_board.append(row)
                row = []

        sudoku.auto_sudoku(two_D_board)


def letter_boxed():
    from letter_boxed import letter_boxed

    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")

    menu_input = get_menu_input(2)
    if menu_input == 1:
        letter_boxed.play_letter_boxed()
    elif menu_input == 2:
        board = scraping_utils.letter_boxed_data()
        letter_boxed.auto_letter_boxed(board)


if __name__ == "__main__":
    replay = ""
    while replay != "n":
        print("Enter the number of the game you would like assistance with.")
        print("1 - Spelling Bee")
        print("2 - Wordle")
        print("3 - Connections")
        print("4 - Sudoku")
        print("5 - Letter Boxed")

        menu_input = get_menu_input(5)
        if menu_input == 1:
            spelling_bee()
        elif menu_input == 2:
            wordle()
        elif menu_input == 3:
            connections()
        elif menu_input == 4:
            sudoku()
        elif menu_input == 5:
            letter_boxed()
        elif menu_input == "q":
            break

        print("Play another game? (y/n)")
        replay = input()
        print("")
