# NYT Answer Key

This app implements automated solvers or helpers for a variety of games in the New York Times collection: Spelling Bee, Wordle, Connections, Crossword, Sudoku, and Letter Boxed.
To use it, visit https://nyt-answer-key.onrender.com, press a game button, and press the help button in the upper right corner to learn how to use the interface. Be aware that because the app is currently hosted on a free instance of Render, the website may take up to a minute to load.


# Games

## Spelling Bee

Spelling Bee is a game where players create words using letters from the hive, which is a list of 7 letters with one designated as the center letter. The words must include the center letter and contain at least 4 letters. 4-letter words are worth 1 point each, and longer words earn 1 point per letter. Additionally, each puzzle includes at least one “pangram” which uses every letter. Pangrams are worth 1 point per letter plus 7 extra points.

The Spelling Bee solver starts with a list of all English words and filters words that are invalid for the given hive. It sorts the remaining words by point value descending and displays them to the user.

## Wordle

Wordle is a game where players try to guess a 5-letter word -- the Wordle -- in 6 or fewer attempts. Each guess must be a valid 5-letter word, and the player will be provided with information about each letter in the guess:
 - Green letters are both in the Wordle and in the correct position in the guess
 - Yellow letters are in the Wordle but are not in the correct position in the guess
 - Black letters are not in the Wordle

The Wordle solver starts with a list of all valid Wordle answers and makes or suggests guesses from it until the puzzle is solved, pruning the list of now-invalid words after each guess. It suggests guesses that maximize the fequencies of appearances of letters in their respective positions in the pruned list of Wordle answers. For example, 's' is the most common first letter in the list of Wordle answers, so the solver would initally prefer answers that start with 's'.

## Connections

Connections is a game where players are given a board of 16 words and asked to collect them into groups of 4 that share something in common. When the player makes a guess of a group, they will be told if their guess was correct or if they grouped 3 words correctly but not all 4.

The Connections solver plays in the following manner:
 1. Generate a list of all possible ways to group the 16 given words into groups of 4. 
 2. Calculate each group's median pairwise semantic similarity (MPSS). It does this by generating all possible pairs of words in the given group, calculating each pair's semantic similarity using the `SpaCy` library, and taking the median of the resulting list.
 3. Sort the possible groupings according to their MPSS.
 4. Choose the grouping with the highest MPSS as the next guess.
 5. Recieve feedback on the quality of the guess and eliminate now-invalid groupings accordingly.
 6. If the puzzle is not solved, return to step 4.

 Be aware that the Connections solver performs very poorly in human terms. Grouping words together is a very abstract task, and this particular algorithm cannot accomplish it in the allotted amount of guesses for a typical Connections game. Also note that this algorithm requires too much memory to run on a free instance of Render, so the website simply filters invalid guesses instead.

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


# Other

## Inspiration

Inspired by @aliceyliang and @sadmoody. Check out their projects! \
https://letterboxed.aliceyliang.com/ \
https://sadmoody.github.io/unwordle/