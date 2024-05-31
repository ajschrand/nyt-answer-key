from utils import getMenuInput

def handleSpellingBeeRequest():
    from spelling_bee import spelling_bee
    
    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")
    
    menuInput = getMenuInput(2)
    match menuInput:
        case 1:
            spelling_bee.playSpellingBee()
        case 2:
            yellowLetter, lettersList = requestNYTData("spelling bee")
            spelling_bee.autoSpellingBee(yellowLetter, lettersList)
    

def handleWordleRequest():
    from wordle import wordle
    
    print("Would you like assistance with a manual Wordle game or to play automatically?")
    print("1 - Manual")
    print("2 - Automatic")
    
    menuInput = getMenuInput(2)
    match menuInput:
        case 1:
            wordle.playWordle()
        case 2:
            print("Solve custom word or current NYT word?")
            print("1 - Custom")
            print("2 - NYT")
            
            menuInput = getMenuInput(2)
            word = ""
            match menuInput:
                case 1:
                    print("Enter the word to guess")
                    word = input()
                case 2:
                    # TODO get today's wordle word
                    pass
            
            print("")
            wordle.autoWordle(word, printGuesses=True)
            

def handleConnectionsRequest():
    from connections import connections
    
    print("Would you assistance with a manual Connections game or to play automatically?")
    print("1 - Manual")
    print("2 - Automatic")
    
    menuInput = getMenuInput(2)
    match menuInput:
        case 1:
            connections.playConnections()
        case 2:
            print("Enter 4 solution groups as lists of words separated by spaces, each on its own line")
            solution = []
            for _ in range(4):
                solution.append(input().split())
            
            print("")
            connections.autoConnections(solution)
            
    # TODO get today's connections board


def handleCrosswordRequest():
    from crossword import crossword
    
    # TODO entire crossword player lol
    
    print("Crossword player is currently a work in progress.")


def handleSudokuRequest():
    from sudoku import sudoku
    
    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")
    
    menuInput = getMenuInput(2)
    match menuInput:
        case 1:
            sudoku.playSudoku()
        case 2:
            print("Solve easy, medium, or hard puzzle?")
            print("1 - Easy")
            print("2 - Medium")
            print("3 - Hard")

            menuInput = getMenuInput(3)
            oneDimensionalBoard = []
            match menuInput:
                case 1:
                    oneDimensionalBoard = requestNYTData("sudoku easy")
                case 2:
                    oneDimensionalBoard = requestNYTData("sudoku medium")
                case 3:
                    oneDimensionalBoard = requestNYTData("sudoku hard")
                    
            twoDimensionalBoard = []
            row = []
            for i, num in enumerate(oneDimensionalBoard):
                row.append(num)
                
                if (i + 1) % 9 == 0:
                    twoDimensionalBoard.append(row)
                    row = []
            
            sudoku.autoSudoku(twoDimensionalBoard)
                    

def handleLetterBoxedRequest():
    from letter_boxed import letter_boxed
    
    print("Solve custom puzzle or current NYT puzzle?")
    print("1 - Custom")
    print("2 - NYT")
    
    menuInput = getMenuInput(2)
    match menuInput:
        case 1:
            letter_boxed.playLetterBoxed()
        case 2:
            board = requestNYTData("letter boxed")
            letter_boxed.autoLetterBoxed(board)

    
def requestNYTData(game):
    from requests import get as requestsGet
    from bs4 import BeautifulSoup
    import re
    
    def getSoupFromLink(link):
        r = requestsGet(link)
        return BeautifulSoup(r.text, features="html.parser")
    
    def getGameDataJSONFromLink(link):
        from json import loads
        
        s = getSoupFromLink(link)
        gameDataTag = s.find(string=re.compile(r"window\.gameData"))
        gameDataJSON = loads(gameDataTag.string.removeprefix("window.gameData = "))
        
        return gameDataJSON
    
    def requestSpellingBeeData():
        json = getGameDataJSONFromLink("https://www.nytimes.com/puzzles/spelling-bee")
        
        return json["today"]["centerLetter"], json["today"]["validLetters"]
    
    def requestConnectionsData():
        from datetime import datetime
        
        today = datetime.today().strftime("%d-%m-%y")
        link = f"https://www.rockpapershotgun.com/wordle-connections-hint-and-answer-{today}"
        s = getSoupFromLink(link)
        answersHeader = s.find(string=re.compile(r"What is the answer to Connections today"))
        answersList = answersHeader.find_next('ul')
        answersTags = answersList.find_all('li')
        
        solutions = []
        for listElement in answersTags:
            listText = re.search(r': (.*)', listElement.text).group(1)
            solution = listText.split(', ')
            solutions.append(solution)
    
        return solutions
    
    def requestSudokuData(difficulty):
        json = getGameDataJSONFromLink("https://www.nytimes.com/puzzles/sudoku")
        
        match difficulty:
            case "easy":
                return json["easy"]["puzzle_data"]["puzzle"]
            case "medium":
                return json["medium"]["puzzle_data"]["puzzle"]
            case "hard":
                return json["hard"]["puzzle_data"]["puzzle"]
            
    def requestLetterBoxedData():
        json = getGameDataJSONFromLink("https://www.nytimes.com/puzzles/letter-boxed")
        
        return json["sides"]
    
    match game:
        case "spelling bee":
            return requestSpellingBeeData()
        case "connections":
            return requestConnectionsData()
        case _ if game.startswith("sudoku"):
            difficulty = game.split()[1]
            return requestSudokuData(difficulty)
        case "letter boxed":
            return requestLetterBoxedData()
        
    raise ValueError


def scrapeNYTData(game):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    
    assert "Python" in driver.title
    
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    
    assert "No results found." not in driver.page_source
    
    driver.close()
    
    return game


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
        
        gameInput = getMenuInput(6)
        match gameInput:
            case 1:
                handleSpellingBeeRequest()
            case 2:
                handleWordleRequest()
            case 3:
                handleConnectionsRequest()
            case 4:
                handleCrosswordRequest()
            case 5:
                handleSudokuRequest()
            case 6:
                handleLetterBoxedRequest()
            case "q":
                break
                
        print("Play another game? (y/n)")
        replay = input()
        print("")