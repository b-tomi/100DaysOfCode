# Rock Paper Scissors

import random


rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# put them into a list for easier access
choices_list = [rock, paper, scissors]

print("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.")
# make sure the input is valid
options_list = ["0", "1", "2"]
while True:
    player_choice_str = input("> ")
    if player_choice_str not in options_list:
        print("Invalid choice. Type 0 for Rock, 1 for Paper or 2 for Scissors.")
    else:
        break

# change the data type now, should be safe now since we are sure it's one of the valid options
player_choice = int(player_choice_str)
print(choices_list[player_choice])

# computer's choice
cpu_choice = random.randint(0, 2)
print("Computer chose:")
print(choices_list[cpu_choice])

# evaluate the result
# if the same, it's a tie
if player_choice == cpu_choice:
    print("It's a tie.")
# cases when the player wins: (rock and scissors) or (paper and rock) or (scissors and paper)
elif (player_choice == 0 and cpu_choice == 2) or\
        (player_choice == 1 and cpu_choice == 0) or\
        (player_choice == 2 and cpu_choice == 1):
    print("You win.")
# anything else means the cpu wins
else:
    print("You lose.")
