# OOP Coffee Machine

from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
import art


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


machine_on = True
machine = CoffeeMaker()
money_machine = MoneyMachine()
menu = Menu()
while machine_on:
    # show the logo between each transaction
    print(art.logo)
    print(f"Please choose a beverage: {menu.get_items()}")
    # re-using the function from the previous day
    # since there doesn't seem to be a way to retrieve a proper list of beverages using the provided classes,
    # unfortunately, the beverage options need to be hard-coded here
    choice = get_input(["latte", "espresso", "cappuccino", "report", "off"])
    if choice == "report":
        machine.report()
        money_machine.report()
    elif choice == "off":
        machine_on = False
    else:
        # retrieve the requested drink
        bev = menu.find_drink(choice)
        # process the transaction
        if machine.is_resource_sufficient(bev):
            print(f"Please insert ${bev.cost}.")
            # this will crash on an invalid input
            # it will also display the incorrect "change" when insufficient amount of money is inserted
            # during the 2nd and subsequent orders
            # but since the assignment specifically said not to touch the classes...
            if money_machine.make_payment(bev.cost):
                machine.make_coffee(bev)

print("Goodbye.")
