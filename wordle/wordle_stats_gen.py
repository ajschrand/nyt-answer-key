from pathlib import Path
cwd = Path(__file__).resolve().parent

# ------------------------------------------
parent_dir = cwd.parent

import sys
sys.path.append(str(parent_dir))
# ------------------------------------------

import concurrent.futures
import pandas as pd

from wordle import auto_wordle

DEFAULT_STARTING_GUESS = "crate"

VALID_WORDLE_ANSWERS = []
with open(f"{cwd}\\wordle_answers_alphabetical.txt", 'r') as f:
    for line in f:
        VALID_WORDLE_ANSWERS.append(line.strip())

# Find the best starting word for auto_wordle
# Run auto_wordle on all valid Wordle answers with each valid Wordle answer as the starting guess
# Save the results to a CSV file
def score_starting_words():
    scores = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(
            mass_auto_wordle, start_guess=word, print_progress=False) for word in VALID_WORDLE_ANSWERS]
        for future in concurrent.futures.as_completed(futures):
            word, score = future.result()
            scores[word] = score
            print(f"{word}: {score}")

    df = pd.DataFrame.from_dict(scores, orient='index', columns=['mean'])
    df = df.sort_values(by='mean', ascending=True)
    df.to_csv(f"{cwd}\\wordle_starting_answers.csv")


# Run auto_wordle on all valid Wordle answers and record the number of guesses required to solve each word
# Save the results to a CSV file
# Print a summary of the results
def mass_auto_wordle(start_guess=DEFAULT_STARTING_GUESS, save_results=False, print_progress=False):
    scores = []
    num_completed = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(auto_wordle, word, start_guess)
                   for word in VALID_WORDLE_ANSWERS]
        for future in concurrent.futures.as_completed(futures):
            scores.append(future.result())
            num_completed += 1
            if num_completed % 100 == 0 and print_progress:
                print(f"{num_completed} words completed.", end="\r")
    
    record = pd.DataFrame({'word': VALID_WORDLE_ANSWERS, 'score': scores})

    if save_results:
        record.to_csv(f"{cwd}\\wordle_answers_scores.csv", index=False)
        print(record.describe())

    return start_guess, record['score'].mean()


if __name__ == "__main__":
    score_starting_words()