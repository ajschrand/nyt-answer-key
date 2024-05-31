def getCollectionAsGrid(list, gridSize):
    grid = ""
    line = ""
    for i, word in enumerate(list):
        line += str(word) + " "
        if (i + 1) % gridSize == 0:
            grid += line + "\n"
            line = ""

    return grid.strip()

def wordContainsAllLetters(word, letters):
    lettersSet = set(letters)
    for letter in word:
        lettersSet.discard(letter)

    return len(lettersSet) == 0
    
    
def wordHasOnlyLetters(word, letters):
    for letter in word:
        if letter not in letters:
            return False
        
    return True


def wordContainsDuplicateLetters(word):
    seenLetters = set()
    for letter in word:
        if letter in seenLetters:
            return True
        seenLetters.add(letter)
        
    return False


def getMenuInput(numItems):
    def isValidMenuInput(menuInput):
        if menuInput == "q":
            return True
        
        if not menuInput.isdigit():
            return False
        
        menuInputNum = int(menuInput)
        return menuInputNum >= 1 and menuInputNum <= numItems
        
    menuInput = input()
    while not isValidMenuInput(menuInput):
        print("Invalid. Try again.")
        menuInput = input()
        
    print("")
        
    if menuInput == "q":
        return "q"
    
    return int(menuInput)


def getAllEnglishWords():
    from json import load
    from pathlib import Path
    cwd = Path(__file__).resolve().parent
    
    return load(open(f"{cwd}\\english-words.txt", 'r'))


if __name__ == "__main__":
    # import json
    
    # words = []
    # with open("words_alpha.txt") as file:
    #     for word in file:
    #         words.append(word.strip())
            
    # json.dump(words, open(f"english-words.txt", 'w'))
    
    with open("english-words-lines.txt", "w") as file:
        for word in getAllEnglishWords():
            file.write(word + "\n")