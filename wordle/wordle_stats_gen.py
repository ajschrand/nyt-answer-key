from pathlib import Path
cwd = Path(__file__).resolve().parent

# ------------------------------------------
parentDir = cwd.parent

import sys
sys.path.append(str(parentDir))
# ------------------------------------------

import concurrent.futures
import pandas as pd

from wordle import autoWordle

DEFAULT_STARTING_GUESS = "crate"

VALID_WORDLE_ANSWERS = []
with open(f"{cwd}\\wordle-answers-alphabetical.txt", 'r') as f:
    for line in f:
        VALID_WORDLE_ANSWERS.append(line.strip())

# Find the best starting word for autoWordle
# Run autoWordle on all valid Wordle answers with each valid Wordle answer as the starting guess
# Save the results to a CSV file
def findBestStartingWord():
    scores = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(
            massAutoWordle, startingGuess=word, printProgress=False) for word in VALID_WORDLE_ANSWERS]
        for future in concurrent.futures.as_completed(futures):
            word, meanScore = future.result()
            scores[word] = meanScore
            print(f"{word}: {meanScore}")

    df = pd.DataFrame.from_dict(scores, orient='index', columns=['mean'])
    df = df.sort_values(by='mean', ascending=True)
    df.to_csv(f"{cwd}\\wordle-starting-answers.csv")


# Run autoWordle on all valid Wordle answers and record the number of guesses required to solve each word
# Save the results to a CSV file
# Print a summary of the results
def massAutoWordle(startingGuess=DEFAULT_STARTING_GUESS, saveResults=False, printProgress=False):
    scores = []
    numCompleted = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(autoWordle, word, startingGuess)
                   for word in VALID_WORDLE_ANSWERS]
        for future in concurrent.futures.as_completed(futures):
            scores.append(future.result())
            numCompleted += 1
            if numCompleted % 100 == 0 and printProgress:
                print(f"{numCompleted} words completed.", end="\r")
    
    record = pd.DataFrame({'word': VALID_WORDLE_ANSWERS, 'score': scores})

    if saveResults:
        record.to_csv(f"{cwd}\\wordle-answers-scores.csv", index=False)
        print(record.describe())

    return startingGuess, record['score'].mean()


if __name__ == "__main__":
    print(massAutoWordle(printProgress=True))