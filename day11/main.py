# Blackjack

import random

import art


def draw_card(count):
    """Returns a LIST with "count" amount of random cards."""
    # list of card values, infinite amount of each of them
    card_deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    drawn_cards = []
    for _ in range(count):
        drawn_cards.append(random.choice(card_deck))
    return drawn_cards


def calculate_score(card_list):
    """Returns the sum of card values as INT, 0 meaning a Blackjack."""
    # make a temporary copy of the list, so that the original one doesn't get modified
    temp_card_list = card_list.copy()
    # sort the new list of cards in descending order
    temp_card_list.sort(reverse=True)
    score = 0
    # if blackjack, return the score 0
    if temp_card_list == [11, 10]:
        return score
    else:
        score = sum(temp_card_list)
        # deal with aces having a value of 11 or 1, if present it should be the first value in the list
        while score > 21 and temp_card_list[0] == 11:
            # delete the first element (i.e. 11) and add a new one with value 1 to the end of the list
            temp_card_list.pop(0)
            temp_card_list.append(1)
            score = sum(temp_card_list)
            # if there was more than one ace, and the score is still too high, process the next one
        return score


def display_score(plyr_list, game_over):
    """Display the score for all players in the list."""
    # the formatted original list of cards, and "BLACKJACK!" instead of the score "0"
    # dealer's score
    if plyr_list[0]["has_blackjack"]:
        print(f"Dealer's cards: {fix_aces(plyr_list[0]['cards'])} BLACKJACK!")
    elif game_over:
        print(f"Dealer's cards: {fix_aces(plyr_list[0]['cards'])} Score: {plyr_list[0]['score']}")
    else:
        # just show the revealed card
        # question marks for the score make more sense than showing the value of the first card
        print(f"Dealer's first card: {fix_aces(plyr_list[0]['revealed_cards'])} Score: ??")

    # user's score
    if plyr_list[1]["has_blackjack"]:
        print(f"Your cards: {fix_aces(plyr_list[1]['cards'])} BLACKJACK!")
    else:
        print(f"Your cards: {fix_aces(plyr_list[1]['cards'])} Score: {plyr_list[1]['score']}")


def fix_aces(card_list):
    """Takes a list of cards, changes aces from "11" to "A" and returns a formatted STRING."""
    # to avoid confusing the user, always display aces a "A", regardless how they are counted
    formatted_list = []
    # add some basic formatting, looks (a little) better than just simply printing the list
    for val in card_list:
        if val == 11:
            formatted_list.append("[A]")
        else:
            formatted_list.append(f"[{val}]")
    # return it as a string
    return "".join(formatted_list)


def play():
    """Play one round of the game."""
    # it would be much easier to use objects, but sticking with just what the course has covered so far
    # initialize players as dictionaries, then store them in a list for easier manipulation
    cpu = {
        "cards": [],
        "revealed_cards": [],
        "score": 0,
        "has_blackjack": False,
    }
    user = {
        "cards": [],
        "score": 0,
        "has_blackjack": False,
    }
    list_of_players = [cpu, user]

    is_game_over = False

    # draw 2 initial cards, loop through each player in the list
    for player in list_of_players:
        player["cards"] = draw_card(2)
        player["score"] = calculate_score(player["cards"])
        if player["score"] == 0:
            player["has_blackjack"] = True
    # update revealed cards and revealed score for the dealer, i.e. the player with index 0 in list_of_players
    # it should be the first card in their list of cards, also save it as a list (with a single value)
    list_of_players[0]["revealed_cards"] = [list_of_players[0]["cards"][0]]

    # check for instant win (i.e. any blackjack) condition
    if cpu["has_blackjack"] or user["has_blackjack"]:
        is_game_over = True

    # user's turn
    if not is_game_over:
        user_done = False
        while not user_done:
            display_score(list_of_players, is_game_over)
            print("\nType \"y\" to get another card, type \"n\" to pass.")
            card_choice = input("> ")
            if card_choice == "y":
                print("You draw a card.\n")
                # draw one card and add it to the list (remember it's also list), and update the score
                user["cards"].extend(draw_card(1))
                user["score"] = calculate_score(user["cards"])
                if user["score"] > 21:
                    user_done = True
                    is_game_over = True
            else:
                user_done = True

    # the dealer's turn, always draw when score is less than 17
    if not is_game_over:
        while cpu["score"] < 17:
            print("The dealer draws a card.\n")
            cpu["cards"].extend(draw_card(1))
            cpu["score"] = calculate_score(cpu["cards"])

    is_game_over = True
    # display final score, this will display all the dealer's cards now that is_game_over = True
    display_score(list_of_players, is_game_over)

    # evaluate the result
    if cpu["has_blackjack"] and not user["has_blackjack"]:
        print("\nDealer has a blackjack, DEALER wins.\n")
    # not quite sure how this situation should be evaluated, so might as well be a tie
    elif cpu["has_blackjack"] and user["has_blackjack"]:
        print("\nYou both have a blackjack, it's a tie!\n")
    elif user["has_blackjack"]:
        print("\nYou have a blackjack, YOU win.\n")
    elif cpu["score"] > 21:
        print("\nDealer went over. YOU win.\n")
    elif user["score"] > 21:
        print("\nYou went over. DEALER wins.\n")
    elif user["score"] == cpu["score"]:
        print("\nIt's a tie!\n")
    elif user["score"] > cpu["score"]:
        print("\nYOU win.\n")
    else:
        print("\nDEALER wins.\n")


# main loop
while True:
    print(art.logo)
    play()
    print("Do you want to to play another round?")
    quit_choice = input("> ")
    if quit_choice != "y":
        break
    # again, since the "replit" module is not available, just print a couple blank lines to "clear" the screen
    print("\n" * 100)

print("Thanks for playing!")
