# Debugging

# ====ORIGINAL====================================================

# # Describe Problem
# def my_function():
#   for i in range(1, 20):
#     if i == 20:
#       print("You got it")
# my_function()

# ====DEBUGGED============================

def my_function():
    # range(a, b) stops at "b - 1"
    for i in range(1, 21):
        if i == 20:
            print("You got it")


# PEP8 requires 2 spaces after a function definition
my_function()

# for sake of readability, print a blank line between the exercises
print()
# ====ORIGINAL====================================================

# # Reproduce the Bug
# from random import randint
# dice_imgs = ["❶", "❷", "❸", "❹", "❺", "❻"]
# dice_num = randint(1, 6)
# print(dice_imgs[dice_num])

# ====DEBUGGED============================

# PEP8 says imports should go to the top, but keeping them here to make things more obvious
# from random import randint
# simpler to use "choice" instead
from random import choice


# added proper spacing after the import statement, according to PEP8
dice_imgs = ["❶", "❷", "❸", "❹", "❺", "❻"]
# indices (a.k.a "indexes") in Python start from 0, so we need to either use (0, length):
# dice_num = randint(0, 6)
# or just use this instead, after updating the import statement
# dice_num = choice(dice_imgs)
print(choice(dice_imgs))

print()
# ====ORIGINAL====================================================

# # Play Computer
# year = int(input("What's your year of birth?"))
# if year > 1980 and year < 1994:
#   print("You are a millenial.")
# elif year > 1994:
#   print("You are a Gen Z.")

# ====DEBUGGED============================

# added a space at the end of the string to make it more readable
year_str = input("What's your year of birth? ")
# make sure the input is actually an integer
try:
    year = int(year_str)
    # writing it as a single statement is much more readable
    if 1980 < year < 1994:
        # fixed the spelling
        print("You are a millennial.")
    # need to include "="
    elif year >= 1994:
        print("You are a Gen Z.")
    # an "else" clause might be missing, unclear whether it's omission was intentional or an error
# generally it would be a good idea to keep asking the user for a valid input
# for sake of simplicity, just displaying an error message this time
except ValueError:
    print("You did not enter a valid value.")

print()
# ====ORIGINAL====================================================

# # Fix the Errors
# age = input("How old are you?")
# if age > 18:
# print("You can drive at age {age}.")

# ====DEBUGGED============================

# added a space at the end of the string to make it more readable
age_str = input("How old are you? ")
# as above, make sure the input is valid
try:
    age = int(age_str)
    # also need to include "=", unless the law only allows from the age of 19
    # obviously, this depends on the particular country, and sometimes even state
    # and the type/class of vehicle, etc.
    if age >= 18:
        # need to turn this to an f-string so {age} is not treated as a simple string
        print(f"You can drive at age {age}.")
    # an "elif" or "else" clause might be missing, unclear whether their omission was intentional or an error
# as above, just a simple error message
except ValueError:
    print("You did not enter a valid value.")

print()
# ====ORIGINAL====================================================

# #Print is Your Friend
# pages = 0
# word_per_page = 0
# pages = int(input("Number of pages: "))
# word_per_page == int(input("Number of words per page: "))
# total_words = pages * word_per_page
# print(total_words)

# ====DEBUGGED============================

# declaring the two variables is not necessary in this case
# like above, it would be probably a good idea to check whether the inputs are valid INTs
# skipping it to avoid repetition
pages = int(input("Number of pages: "))
# "==" is a comparison operator, a simple assignment "=" is needed
word_per_page = int(input("Number of words per page: "))
total_words = pages * word_per_page
print(total_words)

print()


# ====ORIGINAL====================================================

# #Use a Debugger
# def mutate(a_list):
#   b_list = []
#   for item in a_list:
#     new_item = item * 2
#   b_list.append(new_item)
#   print(b_list)

# ====DEBUGGED============================

def mutate(a_list):
    b_list = []
    for item in a_list:
        new_item = item * 2
        # fixed the indentation so this gets executed when it was intended
        b_list.append(new_item)
    print(b_list)


# added proper spacing after the function definition
# fixed the list formatting to match PEP8
mutate([1, 2, 3, 5, 8, 13])
