# Secret Auction

import art


print(art.logo)
print("Welcome to the secret auction program.")

# dictionary to store the name-bid pairs
bids = {}
# set condition to break out of the loop
bidding_over = False

while not bidding_over:
    # unclear whether multiple bids by the same person should be allowed
    # and whether it's possible for a subsequent bid by the same person to be LOWER than their previous one
    print("What's your name?")
    # so, just check if there's already a bid with that name (keep it case sensitive)
    while True:
        name = input("> ")
        # reject an empty input
        if name == "":
            print("Please enter a name.")
        # this should get evaluated as "truthy" (i.e. True) if there is a value assigned to it in the dictionary
        elif bids.get(name):
            print(f"There is already a bid by {name}. Please enter a different name.")
        else:
            break

    print("What is your bid?")
    # make sure it's a valid amount (no cents, to keep it simple)
    while True:
        bid_str = input("> $")
        if bid_str == "0":
            print("$0 is not a proper bid. Please try again.")
        elif not bid_str.isdigit():
            print("Please enter a valid amount.")
        else:
            bid = int(bid_str)
            break

    # add to the dictionary, already made sure it's a new key
    bids[name] = bid

    print("Are there any other bidders? Type \"yes\" or \"no\".")
    choice = input("> ").lower()

    # skip checking the input, just keep going until "no" is entered
    if choice == "no":
        bidding_over = True

    # since the "replit" module is not available and there doesn't seem to be a simple way to clear the screen that
    # would RELIABLY work on different platforms, i.e. "import os" AND "os.system("clear")" OR "os.system("cls")" ...
    # ... just print a bunch of blank lines instead, both between each bid and at the end
    print("\n" * 100)

# find the highest bid
winner_name = ""
top_bid = 0
for key in bids:
    # unclear what to do if there are multiple winners (with identical bids), just pick whoever gets processed first
    if bids[key] > top_bid:
        top_bid = bids[key]
        winner_name = key

print(f"The winner is {winner_name} with a bid of ${top_bid}.")
