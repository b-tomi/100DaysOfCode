# Caesar Cipher

import art


def caesar(cipher_text, shift_amount, cipher_direction):
    # deal with the case when the shift number is higher than the number of letters
    # e.g. with 26 letters, the result of a shift by 27 is the same as a shift by 1
    if shift_amount > len(alphabet):
        shift_amount = shift_amount % len(alphabet)
    # in case of decoding
    if cipher_direction == "decode":
        shift_amount = len(alphabet) - shift_amount
    text_out = ""
    for char in cipher_text:
        if char in alphabet:
            index_in = alphabet.index(char)
            index_out = index_in + shift_amount
            # if the new index would end up beyond the list, roll over to the beginning
            if index_out > len(alphabet) - 1:
                index_out -= len(alphabet)
            text_out += alphabet[index_out]
        # if not a letter, just copy the original character
        # maybe it would be a good idea to make a special case for the situation when NEITHER of the characters is
        # a letter of the alphabet, resulting in the original and encoded/decoded string to be identical
        else:
            text_out += char
    return text_out


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

print(art.logo)

# repeat unless the user enters "no"
while True:
    # get the inputs, check for validity when needed
    print("Type \"encode\" to encrypt, type \"decode\" to decrypt:")
    # using a boolean (e.g. reverse = True) instead would be better, but since the assignment wants a string...
    direction = ""
    while True:
        direction = input("> ").lower()
        if direction == "encode" or direction == "decode":
            break
        else:
            print("Invalid choice. Please enter \"encode\" or \"decode\".")
    print("Type your message:")
    text = input("> ").lower()

    print("Type the shift number:")
    shift = 0
    while True:
        shift_str = input("> ")
        if shift_str.isdigit():
            shift = int(shift_str)
            # reject 0,  while it is technically a valid choice, not a very good one
            # also reject any other number that would result in a shift by 0 characters (i.e. multiplies of 26)
            if shift % len(alphabet) == 0:
                print(f"Invalid choice. Shifting by {shift} would result in an identical message.")
            else:
                # keep the shift value as it was entered, will deal with it later
                break
        else:
            print("Invalid choice. Please enter a positive integer.")

    # already made sure that direction can either be "encode" or "decode", nothing else
    result = caesar(cipher_text=text, shift_amount=shift, cipher_direction=direction)

    # print the result, including the original shift value that the user entered
    print(f"The message \"{text}\" {direction}d using a shift of {shift} is \"{result}\".")

    # condition to break out of the infinite loop
    print("Type \"yes\" if you want to go again. Otherwise type \"no\".")
    choice = input("> ").lower()
    # skip checking the input, just keep going until "no" is entered
    if choice == "no":
        break

print("Goodbye.")
