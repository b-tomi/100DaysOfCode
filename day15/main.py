# Coffee Machine

import art


MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

COIN_VALUES = {
    "quarter": 0.25,
    "dime": 0.1,
    "nickel": 0.05,
    "penny": 0.01,
}


def process_transaction():
    """Processes the whole transaction and returns a BOOL."""
    # ask to choose a beverage
    print("What would you like? (espresso/latte/cappuccino)")
    bev_choice = get_input(["espresso", "latte", "cappuccino", "off"])
    # terminate the transaction and break out of the main loop
    if bev_choice == "off":
        return False
    # check if there are enough resources, if not, terminate the transaction
    elif not enough_resources(bev_choice):
        return True

    # ask to insert coins (might not be always grammatically correct)
    print(f"You have selected a {bev_choice}. PLease insert ${MENU[bev_choice]['cost']}.")
    inserted_sum = get_coins()
    # if not enough money was inserted, terminate the transaction
    if inserted_sum < MENU[bev_choice]['cost']:
        print(f"Sorry, that's not enough money. ${round(inserted_sum, 2)} refunded.")
        return True

    # process the order, store the income and subtract used resources
    process_money(MENU[bev_choice]['cost'])
    # return any excess money
    if inserted_sum > MENU[bev_choice]['cost']:
        print(f"Here is ${round(inserted_sum - MENU[bev_choice]['cost'], 2)} change.")
    process_resources(bev_choice)
    print(f"Here is your {bev_choice}. Enjoy!")

    # terminate the transaction (but continue the main loop)
    return True


def print_report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']}")


def enough_resources(bev):
    """Checks whether there are enough resources for the selected beverage, and returns a BOOL."""
    for res in MENU[bev]["ingredients"]:
        # loop through each required resource, and compare to the available amount
        if MENU[bev]["ingredients"][res] > resources[res]:
            # skip checking the other resources once one fails the check
            print(f"Sorry, there is not enough {res}.")
            return False
    return True


def get_coins():
    """Asks the user to insert coins, counts their total value and returns a FLOAT."""
    total_coin_value = 0
    for val in COIN_VALUES:
        # not always grammatically correct, e.g. "penny"+"s"
        print(f"How many {val}s (${COIN_VALUES[val]}) would you like to insert?")
        total_coin_value += COIN_VALUES[val] * get_int()
        print(f"Total inserted: ${total_coin_value}")
    return total_coin_value


def process_resources(bev):
    """Takes a STR and subtracts the corresponding resources."""
    for res in MENU[bev]["ingredients"]:
        resources[res] -= MENU[bev]["ingredients"][res]


def process_money(val):
    """Takes a FLOAT and adds it to the money variable."""
    # could have just included this in "process_resources()", but doing it this way means less work in the future,
    # in case something like a "withdraw money" functionality gets added... or something
    resources["money"] += val


def get_input(choices_list):
    """Gets input from the user and returns it as STR. Only accepts choices from the provided list."""
    while True:
        user_choice = input("> ").lower()
        if user_choice not in choices_list:
            # format the options to include in the error message looks a little better
            # this will also include the "hidden" choices
            formatted_choices = ""
            for i in range(len(choices_list)):
                # for the first option, or if there is only a single option
                if i == 0:
                    formatted_choices += f'"{choices_list[i]}"'
                # for each next, up until the penultimate option
                elif i < len(choices_list) - 1:
                    formatted_choices += f', "{choices_list[i]}"'
                # for the final option
                else:
                    formatted_choices += f' or "{choices_list[i]}"'
            print(f"Invalid choice. Please type {formatted_choices}.")
        else:
            return user_choice


def get_int():
    """Gets input from the user and returns it as INT. Only accepts "0" or a natural number."""
    while True:
        input_string = input("> ")
        # accept 0 and positive INTs
        if not input_string.isdigit():
            print("Please enter a valid number of coins.")
        else:
            return int(input_string)


# starting resources in the machine, also included money
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0,
}

# main loop
machine_on = True
while machine_on:
    # show the logo between each transaction
    print(art.logo)
    print("Would you like a beverage? Type \"y\" or \"n\":")
    # only accept the valid choices
    quit_choice = get_input(["y", "n", "report", "off"])
    if quit_choice == "report":
        print_report()
    elif quit_choice == "off":
        machine_on = False
    elif quit_choice == "n":
        # break out of the loop without "turning off"
        break
    else:
        # process the transaction, it will return False if the user chooses "off"
        machine_on = process_transaction()

if not machine_on:
    print("The coffee machine is now off.")
else:
    print("Goodbye.")
