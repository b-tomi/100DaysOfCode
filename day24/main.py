# Mail Merge

LETTER_TEMPLATE = "./Input/Letters/starting_letter.txt"
INVITED_NAMES = "./Input/Names/invited_names.txt"
OUTPUT_FOLDER = "./Output/ReadyToSend/"


def load_template(text_file):
    """Takes a text file and returns its content as a STR."""
    with open(text_file, mode="r") as file:
        letter_template = file.read()
        return letter_template


def load_names(text_file):
    """Takes a text file and returns its lines in a LIST of STRs."""
    with open(text_file, mode="r") as file:
        names = []
        for line in file:
            # remove the new line character
            names.append(line.strip("\n"))
        return names


def save_letter(content, file_name):
    """Takes STRs and saves the content in a text file with the provided name."""
    # set the relative path and file name with appropriate extension
    output = OUTPUT_FOLDER + file_name + ".txt"
    with open(output, mode="w") as file:
        file.write(content)


# load the template and the list of names
template = load_template(LETTER_TEMPLATE)
name_list = load_names(INVITED_NAMES)
for name in name_list:
    # replace the placeholder with a name
    letter = template.replace("[name]", name)
    # save as a new text file called name.txt
    save_letter(letter, name)
