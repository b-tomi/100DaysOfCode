# Hangman

import hangman_art as art
import hangman_words as words
import random


def get_guess():
    while True:
        g = input("Guess a letter: ").lower()
        # repeated guesses of the same letter should not count as a "bad" guess
        if g in guessed_letter_list:
            print(f"You have already guessed the letter \"{g}\".")
        # make sure the guess is a single character
        elif g not in letter_list:
            print("The guess has to be a single letter. Please try again.")
        else:
            # "return" will also break out the infinite loop, just like "break"
            return g


# typing a whole list of all letters manually is tedious, so just making one from a simple string
letter_list = list("abcdefghijklmnopqrstuvwxyz")
# to store letters that have already been guessed
guessed_letter_list = []

# randomly pick a word, then save it as a list of characters
chosen_word = list(random.choice(words.word_list))
# the display list, fill it with "_" for each character
display = []
for i in range(len(chosen_word)):
    display.append("_")

# set conditions to break out of main loop
game_over = False
is_winner = False
# the number of lives at the beginning actually depends on the number of elements in the "stages" list
# better to avoid hard-coding it to "6" though
lives = len(art.stages) - 1

print(art.logo)
print(f"Pssst, the solution is \"{''.join(chosen_word)}\".")

while not game_over:
    # get the input, using a function to make the code more readable
    guess = get_guess()

    # add the letter to the "guessed" list
    guessed_letter_list.append(guess)

    # evaluate the guess, and update the display list if needed
    good_guess = False
    for i in range(len(chosen_word)):
        if chosen_word[i] == guess:
            display[i] = guess
            # set to True if there was at least one match
            good_guess = True

    if good_guess:
        # check for win condition
        # count the "_" in the display list, none means all characters have been guessed already
        if display.count("_") == 0:
            is_winner = True
            game_over = True
    else:
        print(f"The letter \"{guess}\" is not in the word. You lose a life.")
        lives -= 1
        # check for game over condition
        if lives == 0:
            game_over = True

    # print the display list as a string and the corresponding "art"
    print(" ".join(display))
    print(art.stages[lives])

# after game over, print the final result
if is_winner:
    print("You win!")
else:
    print("Game over.")
