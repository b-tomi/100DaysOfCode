# Higher Lower Game

from random import randint

import art
import game_data as gd


def play():
    """Play a round."""
    # initial setup
    score = 0
    # get an initial dict and its index
    dict_a, index_a = get_entry()
    is_game_over = False
    while not is_game_over:
        # get another dict and its index, make sure it's not the same one
        dict_b, index_b = get_entry(exclude_one=True, excluded_index=index_a)

        print(art.logo)
        # odd place to put this, but since since this is where the exercise wants this...
        # only display if the player passes the first round
        if score > 0:
            print(f"You're right! Current score: {score}.")
        # print values from dict_a
        # these might not be always grammatically correct, e.g. "a Actor"
        print(f"Compare A: {dict_a['name']}, a {dict_a['description']} from {dict_a['country']}.")
        print(art.vs)
        # print values from dict_b
        print(f"Against B: {dict_b['name']}, a {dict_b['description']} from {dict_b['country']}.")

        print("\nWho has more followers? Type \"A\" or \"B\":")

        # get user input, valid choices are in provided list (they need to be uppercase)
        choice = get_input(["A", "B"])

        # evaluate the choice
        # this doesn't seem to be the case now, but just in case changes are made to the data in the future
        if dict_a["follower_count"] == dict_b["follower_count"]:
            # unclear what to do when their numbers are identical, so just accept anything as correct
            score += 1
        elif dict_a["follower_count"] > dict_b["follower_count"]:
            if choice == "A":
                score += 1
            else:
                is_game_over = True
        elif dict_a["follower_count"] < dict_b["follower_count"]:
            if choice == "B":
                score += 1
            else:
                is_game_over = True

        # the B entry becomes the A entry for the next round
        if not is_game_over:
            dict_a = dict_b
            index_a = index_b
        # "clear" the screen
        print("\n" * 100)

    # once the player loses
    print(art.logo)
    print(f"Sorry that's wrong. Final score: {score}.\n")


def get_entry(exclude_one=False, excluded_index=0):
    """Returns a randomly picked entry and its index as a tuple of DICT and INT, other than the one matching
    the provided index."""
    entries = len(gd.data)
    chosen_index = randint(0, entries - 1)
    chosen_dict = gd.data[chosen_index]
    # make sure the chosen index and dict are not the same
    while exclude_one and chosen_index == excluded_index:
        chosen_index = randint(0, entries - 1)
        chosen_dict = gd.data[chosen_index]
    return chosen_dict, chosen_index


def get_input(choices_list):
    """Gets input from the user, returns it as STR. Only accepts choices from the provided list."""
    while True:
        user_choice = input("> ").upper()
        if user_choice not in choices_list:
            # add quotation marks around the choices, so the error message looks a little better
            formatted_list = []
            for char in choices_list:
                formatted_list.append(f"\"{char}\"")
            print(f"Invalid choice. Please type {' or '.join(formatted_list)}.")
        else:
            return user_choice


# main loop
while True:
    # play a round
    play()
    print("Do you want to play another round? Type \"Y\" or \"N\":")
    # only accept the valid choices
    quit_choice = get_input(["Y", "N"])
    if quit_choice == "N":
        break
    else:
        # "clear" the screen before playing again
        print("\n" * 100)

print("Thanks for playing.")
