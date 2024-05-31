def get_list_grid(list, size):
    grid = ""
    line = ""
    for i, word in enumerate(list):
        line += str(word) + " "
        if (i + 1) % size == 0:
            grid += line + "\n"
            line = ""

    return grid.strip()


def word_has_all(word, letters):
    s = set(letters)
    for letter in word:
        s.discard(letter)

    return len(s) == 0


def word_has_only(word, letters):
    for letter in word:
        if letter not in letters:
            return False

    return True


def word_has_duplicates(word):
    seen = set()
    for letter in word:
        if letter in seen:
            return True
        seen.add(letter)

    return False


def get_menu_input(num_items):
    def is_valid_input(menu_input):
        if menu_input == "q":
            return True

        if not menu_input.isdigit():
            return False

        menu_input_num = int(menu_input)
        return menu_input_num >= 1 and menu_input_num <= num_items

    menu_input = input()
    while not is_valid_input(menu_input):
        print("Invalid. Try again.")
        menu_input = input()

    print("")

    if menu_input == "q":
        return "q"

    return int(menu_input)


def get_english_words():
    from json import load
    from pathlib import Path
    cwd = Path(__file__).resolve().parent

    return load(open(f"{cwd}\\english_words.txt", 'r'))


if __name__ == "__main__":
    # import json

    # words = []
    # with open("words_alpha.txt") as file:
    #     for word in file:
    #         words.append(word.strip())

    # json.dump(words, open(f"english-words.txt", 'w'))

    with open("english-words-lines.txt", "w") as file:
        for word in get_english_words():
            file.write(word + "\n")
