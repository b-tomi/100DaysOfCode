# Calculator

import art


def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    # already made sure to avoid division by zero
    return n1 / n2


# prints available operations, in a single line, to make it look nicer
def list_operations():
    text = "Available operations: "
    for key in operations:
        # this will also add an extra space at the end of the string, but it doesn't really matter
        text += key + " "
    print(text)


# get the inputs and make sure they are valid
# using a single function for both numbers (returns a FLOAT) and the symbols (returns a STR)
def get_input(is_symbol=False):
    # get the symbol
    if is_symbol:
        while True:
            sym = input("> ")
            if sym in operations:
                return sym
            else:
                print(f"{sym} is not a valid option.")
                # remind the user what's available
                list_operations()
                print("Please select one of the above.")
    # else get a number
    while True:
        num_string = input("> ")
        if num_string == "":
            print("Please enter a value.")
        # check if the string is a number, accepts negative ones as well
        elif is_float(num_string):
            return float(num_string)
        else:
            print("Please enter a number.")


# checks if a string is a float or not
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


# dictionary with references to the functions as values
operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

# recursion really isn't a good fit for this
new_calculation = True
result = 0

while True:
    # only executed at the first run, or when the user chooses "new calculation"
    if new_calculation:
        print(art.logo)
        print("What's the first number?")
        num1 = get_input()
    else:
        num1 = result

    # print all keys from the operations dictionary
    # made it a function so it can be called from elsewhere too
    list_operations()

    print("Pick an operation from the above line:")
    symbol = get_input(is_symbol=True)

    # get the second number, but make sure it's not 0 if division was selected
    print("What's the next number?")
    while True:
        num2 = get_input()
        if symbol == "/" and num2 == 0:
            print("You have chosen to divide by zero. Please input a non-zero number.")
        else:
            break

    # calculate the result by using the function assigned to that particular key
    result = operations[symbol](num1, num2)
    print(f"{num1} {symbol} {num2} = {result}")

    print(f"Type \"y\" to continue calculating with {result}, or type \"n\" to start a new calculation. "
          f"Anything else will exit the program.")
    choice = input("> ")
    if choice == "y":
        # continue to next iteration using "result" as num1
        new_calculation = False
    elif choice == "n":
        new_calculation = True
    else:
        break

print("Goodbye.")
