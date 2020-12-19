# Guess the Number

import random

import art


def play(a, b, diff, cheat_mode):
    """Play a round using the provided parameters."""
    # choose the random number
    secret_num = random.randint(a, b + 1)
    # for the "testing" mode
    if cheat_mode:
        print(f"*******************\n"
              f"CHEAT MODE ENABLED:\n"
              f"The number is {secret_num}\n"
              f"*******************")
    lives = diff
    is_game_over = False
    victory = False
    while not is_game_over:
        # just so it doesn't say "1 attempts" (i.e. plural)
        if lives == 1:
            print(f"You have {lives} attempt remaining to guess the number.")
        else:
            print(f"You have {lives} attempts remaining to guess the number.")
        guess = get_integer(a, b)
        # evaluate the guess
        if guess == secret_num:
            victory = True
            is_game_over = True
            print(f"Correct! The number was {secret_num}.")
        elif guess > secret_num:
            lives -= 1
            print("Too high!")
        elif guess < secret_num:
            lives -= 1
            print("Too low!")
        # check game_over condition
        if lives == 0:
            is_game_over = True
            print("No more attempts left.")
    # print the result
    if victory:
        print("\nYou win.\n")
    else:
        print("\nYou lose.\n")


def choose_difficulty(att_dict):
    """Takes a dictionary and returns the key chosen by the user."""
    # just some simple formatting, won't be grammatically correct if there are more than 2 keys
    choices_list = []
    for key in att_dict:
        choices_list.append(f"\"{key}\"")
    print(f"Choose a difficulty. Type {' or '.join(choices_list)}:")
    # make sure the user chooses a valid option
    while True:
        diff_choice = input("> ").lower()
        if diff_choice in att_dict:
            break
        print(f"Invalid option. Please choose {' or '.join(choices_list)}.")
    return att_dict[diff_choice]


def get_integer(a, b):
    """Asks the user to input a number from the provided range, and returns an INT."""
    print("Make a guess:")
    while True:
        guess_str = input("> ")
        # make sure it's a valid choice
        try:
            guess_int = int(guess_str)
            if not (a <= guess_int <= b):
                print(f"Please enter an integer between {a} and {b}.")
            else:
                return guess_int
        except ValueError:
            print("Please enter an integer.")


# main loop
while True:
    # to avoid hard-coding them, set the options for the game here
    # REQUIREMENT: INT, and "num_to" >= "num_from" (negative numbers are acceptable!)
    num_from = -50
    num_to = 50
    # there need to be at least 2 keys, or having to "choose" doesn't make sense, possible to add more
    # REQUIREMENT: the values have to be an INT > 0
    attempts_dict = {
        "easy": 10,
        "hard": 5,
        "extreme": 3,
    }
    # enable "testing" mode
    # REQUIREMENT: BOOL
    testing_mode = False

    print(art.logo)
    print("Welcome to the Number Guessing Game!\n")
    print(f"I'm thinking of a number between {num_from} and {num_to}.")
    attempts = choose_difficulty(attempts_dict)

    # play a round with the specific parameters
    play(num_from, num_to, attempts, testing_mode)

    print("Enter \"y\" to play again, or anything else to quit.")
    quit_choice = input("> ")
    if quit_choice != "y":
        break
    # "clear" the screen before the next round
    print("\n" * 100)

print("Thanks for playing.")
