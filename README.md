# NYT Games Solver

This app implements automated solvers for a variety of games in the New York Times collection. These games currently include Spelling Bee, Wordle, Connections, Crossword, Sudoku, and Letter Boxed.

The app is currently interactable via Command Line Interface (CLI). To start the app, download the code and run `python main.py` in the parent directory.


# Games

## Spelling Bee

Spelling Bee is a game where players create words using letters from the hive, which is a list of 7 letters with one designated as the center letter. The words must include the center letter and contain at least 4 letters. 4-letter words are worth 1 point each, and longer words earn 1 point per letter. Additionally, each puzzle includes at least one “pangram” which uses every letter. Pangrams are worth 1 point per letter plus 7 extra points.

The Spelling Bee solver starts with a list of all English words and filters words that are invalid for the given hive. It sorts the remaining words by point value descending.

## Wordle

Wordle is a game where players try to guess a 5-letter word -- the Wordle -- in 6 or fewer attempts. Each guess must be a valid 5-letter word, and the player will be provided with information about each letter in the guess:
 - Green letters are both in the Wordle and in the correct position in the guess
 - Yellow letters are in the Wordle but are not in the correct position in the guess
 - Black letters are not in the Wordle

The Wordle solver starts with a list of all valid Wordle answers and makes or suggests guesses from it until the puzzle is solved, pruning the list of now-invalid words after each guess. The way it determines its next guess depends on the amount of information (total number of yellow and green letters) it currently has:
 - If the solver knows 2 or fewer letters, it makes the guess that maximizes the fequencies of appearances of letters in their respective positions in the list of Wordle answers. For example, 's' is the most common first letter in the list of Wordle answers, so the solver would prefer answers that start with 's', given that they are valid with respect to any previously made guesses.
 - If the solver knows 3 or more letters, it makes the guess that is the most frequently used word from among the remaining choices. It does this by referencing the `wordfreq` library.

## Connections

Connections is a game where players are given a board of 16 words and asked to collect them into groups of 4 that share something in common. When the player makes a guess of a group, they will be told if their guess was correct or if they grouped 3 words correctly but not all 4.

The Connections solver plays in the following manner:
 1. Generate a list of all possible ways to group the 16 given words into groups of 4. 
 2. Calculate each group's median pairwise semantic similarity (MPSS). It does this by generating all possible pairs of words in the given group, calculating each pair's semantic similarity using the `SpaCy` library, and taking the median of the resulting list.
 3. Sort the possible groupings according to their MPSS.
 4. Choose the grouping with the highest MPSS as the next guess.
 5. Recieve feedback on the quality of the guess and eliminate now-invalid groupings accordingly.
 6. If the puzzle is not solved, return to step 4.

## Crossword

Crossword puzzles are word puzzles that are usually in the shape of a square or rectangle.  The puzzle consists of black and white squares.  The goal of a crossword is to fill the white boxes with the answers to a series of questions.  The shaded squares separate the answers.

The crossword solver is not currently implemented.

## Sudoku

Sudoku is a number game played on a grid of 9 x 9 spaces. Within the rows and columns are 9 squares made up of 3 x 3 spaces. Each row, column and square must be filled with the numbers 1-9, without repeating any numbers within the row, column or square.

The sudoku solver implements a brute-force recursive backtracking algorithm. It plays in the following manner:
 1. Find the first blank grid space.
 2. Try placing a valid number in that space.
 3. Find the next blank grid space and place a valid number in the space.
 4. If there are no valid numbers for that space, return to the previous blank grid space until there is a valid number for that space and place the next valid number for that space. 
 5. If the puzzle is not solved, return to step 3.

## Letter Boxed

Letter Boxed is a game where players must create a sequence of words that uses all the letters in the given square. The square consists of 4 sides that each have 3 distinct letters for a total of 12 letters. Words in the sequence must be at least 3 letters long, and consecutive letters cannot be from the same side. The last letter of a word in the sequence must be the first letter of the next word. Words cannot be proper nouns or hyphenated

The Letter Boxed solver starts with a list of all English words and eliminates the words that cannot be formed using the given square. Then, it finds all one and two word solutions for the given square from the list of valid words as follows:
 - It finds one word solutions by getting all the words from the valid words list that contain all 12 letters from the square. There are usually no such words.
 - It finds two word solutions by starting with each valid word, finding the valid words that begin with its last letter, and determining whether the two words together use all 12 letters from the square. The NYT guarantees that at least one such solution will exist.
