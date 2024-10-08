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


def wordle_data():
    s = get_soup("https://www.techradar.com/news/wordle-today")
    answer_header = s.find(string=re.compile(r"…"))
    answer_tag = answer_header.find_next('strong')
    return answer_tag.text.lower().strip()
    

def spelling_bee_data():
    json = get_game_data("https://www.nytimes.com/puzzles/spelling-bee")

    return json["today"]["centerLetter"], json["today"]["validLetters"]


def connections_data():
    from datetime import datetime

    today = datetime.today().strftime("%d-%m-%y")
    # Having this string on multiple lines breaks Render's deployment for some reason
    # So keep it on one line, despite the PEP8 violation
    link = f"https://www.rockpapershotgun.com/connections-hint-and-answers-{today}"
    s = get_soup(link)
    answers_header = s.find(string=re.compile(
        r"What are today's Connections answers?"))
    answers_list = answers_header.find_next('ul')
    answers_tags = answers_list.find_all('li')

    solutions = []
    for element in answers_tags:
        words = re.search(r': (.*)', element.text).group(1)
        solution = words.split(', ')
        solutions.append([word.lower() for word in solution])

    return solutions


def sudoku_data(difficulty):
    json = get_game_data("https://www.nytimes.com/puzzles/sudoku")

    if difficulty == "easy":
        return json["easy"]["puzzle_data"]["puzzle"]
    elif difficulty == "medium":
        return json["medium"]["puzzle_data"]["puzzle"]
    elif difficulty == "hard":
        return json["hard"]["puzzle_data"]["puzzle"]


def letter_boxed_data():
    json = get_game_data("https://www.nytimes.com/puzzles/letter-boxed")
    board = [side.lower() for side in json["sides"]]
    return board

