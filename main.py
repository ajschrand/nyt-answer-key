from utils import get_menu_input


def spelling_bee():
    from spelling_bee import spelling_bee

    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")

    menu_input = get_menu_input(2)
    match menu_input:
        case 1:
            spelling_bee.play_spelling_bee()
        case 2:
            center_letter, letters_list = request_NYT_data("spelling bee")
            spelling_bee.auto_spelling_bee(center_letter, letters_list)


def wordle():
    from wordle import wordle

    print("Would you like assistance with a manual Wordle game or to play automatically?")
    print("1 - Manual")
    print("2 - Automatic")

    menu_input = get_menu_input(2)
    match menu_input:
        case 1:
            wordle.play_wordle()
        case 2:
            print("Solve custom word or current NYT word?")
            print("1 - Custom")
            print("2 - NYT")

            menu_input = get_menu_input(2)
            word = ""
            match menu_input:
                case 1:
                    print("Enter the word to guess")
                    word = input()
                case 2:
                    # TODO get today's wordle word
                    pass

            print("")
            wordle.auto_wordle(word, print_guesses=True)


def connections():
    from connections import connections

    print("Would you assistance with a manual Connections game or to play automatically?")
    print("1 - Manual")
    print("2 - Automatic")

    menu_input = get_menu_input(2)
    match menu_input:
        case 1:
            connections.play_connections()
        case 2:
            print(
                "Enter 4 solution groups as lists of words separated by spaces, each on its own line")
            solution = []
            for _ in range(4):
                solution.append(input().split())

            print("")
            connections.auto_connections(solution)

    # TODO get today's connections board


def crossword():
    from crossword import crossword

    # TODO entire crossword player lol

    print("Crossword player is currently a work in progress.")


def sudoku():
    from sudoku import sudoku

    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")

    menu_input = get_menu_input(2)
    match menu_input:
        case 1:
            sudoku.play_sudoku()
        case 2:
            print("Solve easy, medium, or hard puzzle?")
            print("1 - Easy")
            print("2 - Medium")
            print("3 - Hard")

            menu_input = get_menu_input(3)
            one_D_board = []
            match menu_input:
                case 1:
                    one_D_board = request_NYT_data("sudoku easy")
                case 2:
                    one_D_board = request_NYT_data("sudoku medium")
                case 3:
                    one_D_board = request_NYT_data("sudoku hard")

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
    match menu_input:
        case 1:
            letter_boxed.play_letter_boxed()
        case 2:
            board = request_NYT_data("letter boxed")
            letter_boxed.auto_letter_boxed(board)


def request_NYT_data(game):
    from requests import get as requests_get
    from bs4 import BeautifulSoup
    import re

    def get_soup(link):
        r = requests_get(link)
        return BeautifulSoup(r.text, features="html.parser")

    def get_game_data(link):
        from json import loads

        s = get_soup(link)
        tag = s.find(string=re.compile(r"window\.gameData"))
        json = loads(tag.string.removeprefix("window.gameData = "))

        return json

    def spelling_bee_data():
        json = get_game_data("https://www.nytimes.com/puzzles/spelling-bee")

        return json["today"]["centerLetter"], json["today"]["validLetters"]

    def connections_data():
        from datetime import datetime

        today = datetime.today().strftime("%d-%m-%y")
        link = f"https://www.rockpapershotgun.com/wordle-connections-hint-and-answer-{
            today}"
        s = get_soup(link)
        answers_header = s.find(string=re.compile(
            r"What is the answer to Connections today"))
        answers_list = answers_header.find_next('ul')
        answers_tags = answers_list.find_all('li')

        solutions = []
        for element in answers_tags:
            words = re.search(r': (.*)', element.text).group(1)
            solution = words.split(', ')
            solutions.append(solution)

        return solutions

    def sudoku_data(difficulty):
        json = get_game_data("https://www.nytimes.com/puzzles/sudoku")

        match difficulty:
            case "easy":
                return json["easy"]["puzzle_data"]["puzzle"]
            case "medium":
                return json["medium"]["puzzle_data"]["puzzle"]
            case "hard":
                return json["hard"]["puzzle_data"]["puzzle"]

    def letter_boxed_data():
        json = get_game_data("https://www.nytimes.com/puzzles/letter-boxed")

        return json["sides"]

    match game:
        case "spelling bee":
            return spelling_bee_data()
        case "connections":
            return connections_data()
        case _ if game.startswith("sudoku"):
            difficulty = game.split()[1]
            return sudoku_data(difficulty)
        case "letter boxed":
            return letter_boxed_data()

    raise ValueError


# def scrapeNYTData(game):
#     from selenium import webdriver
#     from selenium.webdriver.common.keys import Keys
#     from selenium.webdriver.common.by import By

#     driver = webdriver.Chrome()
#     driver.get("http://www.python.org")

#     assert "Python" in driver.title

#     elem = driver.find_element(By.NAME, "q")
#     elem.clear()
#     elem.send_keys("pycon")
#     elem.send_keys(Keys.RETURN)

#     assert "No results found." not in driver.page_source

#     driver.close()

#     return game


if __name__ == "__main__":
    replay = ""
    while replay != "n":
        print("Enter the number of the game you would like assistance with.")
        print("1 - Spelling Bee")
        print("2 - Wordle")
        print("3 - Connections")
        print("4 - Crossword")
        print("5 - Sudoku")
        print("6 - Letter Boxed")

        menu_input = get_menu_input(6)
        match menu_input:
            case 1:
                spelling_bee()
            case 2:
                wordle()
            case 3:
                connections()
            case 4:
                crossword()
            case 5:
                sudoku()
            case 6:
                letter_boxed()
            case "q":
                break

        print("Play another game? (y/n)")
        replay = input()
        print("")
