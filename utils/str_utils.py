from json import load


class MenuOption:
    def __init__(self, title, function):
        self.title = title
        self.function = function

    def run(self):
        return self.function()

    def __str__(self):
        return self.title


class Menu:
    def __init__(self, title, options=[]):
        self.title = title
        self.options = [MenuOption(title, function)
                        for title, function in options]

    def add_option(self, title, function):
        self.options.append(MenuOption(title, function))

    def is_valid_input(self, menu_input):
        if menu_input == "q":
            return True

        if not menu_input.isdigit():
            return False

        return 1 <= int(menu_input) <= len(self.options)

    def get_input(self):
        menu_input = input()
        while not self.is_valid_input(menu_input):
            print("Invalid. Try again.")
            menu_input = input()

        print("")

        return menu_input

    def run(self):
        print(self)
        menu_input = self.get_input()
        if menu_input == "q":
            return

        return self.options[int(menu_input) - 1].run()

    def __str__(self):
        s = f"{self.title}\n"
        for i, option in enumerate(self.options):
            s += f"{i + 1} - {option}\n"
        s += "q - Quit"

        return s


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
    return len(set(letters) - set(word)) == 0


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


def get_english_words():
    return load(open(f"utils/english_words.txt", 'r'))


def get_wordle_answers():
    return load(open(f"utils/wordle_answers.txt", 'r'))
