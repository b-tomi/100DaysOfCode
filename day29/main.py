# Password Manager

import tkinter as tk
import tkinter.messagebox as mb
import random

FONT = ("Arial", 12)
BTN_FONT = ("Arial", 10)
DEFAULT_USERNAME = "myemail@mydomain.zyx"
# just to make sure the pass is always fully displayed in its field (a little more user-friendly)
DEFAULT_PASS_LENGTH = 12
# characters to use in generated passwords
LETTERS = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
NUMBERS = "1234567890"
SYMBOLS = "!@#$%^&*()-_=+[{}]<>"
DATA_FILE = "data.txt"
# special US (Unit Separator) ASCII character
SEPARATOR = "\x1f"


def generate_password():
    # using list comprehension for practice
    l_list = [let for let in LETTERS]
    n_list = [num for num in NUMBERS]
    s_list = [sym for sym in SYMBOLS]
    password = ""
    for _ in range(DEFAULT_PASS_LENGTH):
        # odds for each character: 60% for a letter, 30% number and 10% symbol
        n = random.randint(1, 10)
        if n <= 6:
            password += random.choice(l_list)
        elif n <= 9:
            password += random.choice(n_list)
        else:
            password += random.choice(s_list)

    # need to use a special tkinter identifier tk.END when clearing the field
    # .delete(0, "end") would also work, but this way it's obvious that it comes from tkinter
    password_fld.delete(0, tk.END)
    password_fld.insert(0, password)
    # clear the clipboard and copy the value
    bottom_frame.clipboard_clear()
    bottom_frame.clipboard_append(password)


def add_entry():
    """Checks the validity of the provided values and saves them into the file."""
    # using a list for easier manipulation
    new_entry = [
        website_fld.get(),
        email_fld.get(),
        password_fld.get()
    ]
    entries_valid = True
    # check for empty fields
    for field in new_entry:
        if field == "":
            entries_valid = False
            # no need to check the rest
            break
    if not entries_valid:
        mb.showwarning(title="Warning", message="Please fill out all fields.")
    else:
        # ask for confirmation
        confirm = mb.askokcancel(title=new_entry[0], message="Please confirm the following are correct:\n\n"
                                                             f"Email/Username: {new_entry[1]}\n"
                                                             f"Password: {new_entry[2]}\n\n"
                                                             f"Save entry?")
        if confirm:
            write_data(new_entry)
            # clear all fields except username
            website_fld.delete(0, tk.END)
            password_fld.delete(0, tk.END)


def write_data(entry_list):
    """Takes a LIST and writes the contents in the file, separated by the SEPARATOR character."""
    # using "append" mode so existing
    with open(DATA_FILE, "a") as f:
        # for simplicity, use the special character between each part of the entry
        f.write(f"{SEPARATOR.join(entry_list)}\n")


# main window setup
root = tk.Tk()
root.title("Password Manager")
root.iconbitmap("icon.ico")
root.geometry("500x400")
root.resizable(False, False)

# top frame
top_frame = tk.Frame(root)
top_frame.pack()
# canvas
canvas = tk.Canvas(top_frame, width=200, height=200, highlightthickness=0)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
# the top frame only has a single element, so a simple pack() works just fine
canvas.pack(padx=20, pady=20)

# bottom frame
bottom_frame = tk.Frame(root)
bottom_frame.pack()
# left column
website_lbl = tk.Label(bottom_frame, text="Website:", font=FONT, width=16)
website_lbl.grid(row=0, column=0, pady=4)
email_lbl = tk.Label(bottom_frame, text="Email/Username:", font=FONT, width=16)
email_lbl.grid(row=1, column=0, pady=4)
password_lbl = tk.Label(bottom_frame, text="Password:", font=FONT, width=16)
password_lbl.grid(row=2, column=0, pady=4)

# middle+right column, span across 2 columns
website_fld = tk.Entry(bottom_frame, font=FONT, width=32)
website_fld.grid(row=0, column=1, columnspan=2, pady=4)
# to make the cursor active in the field
website_fld.focus()
email_fld = tk.Entry(bottom_frame, font=FONT, width=32)
email_fld.grid(row=1, column=1, columnspan=2, pady=4)
email_fld.insert(0, DEFAULT_USERNAME)
add_btn = tk.Button(bottom_frame, text="Add", font=BTN_FONT, bg="#ddd", width=32, relief="raised",
                    command=add_entry)
add_btn.grid(row=3, column=1, columnspan=2, pady=8)

# middle column
password_fld = tk.Entry(bottom_frame, font=FONT, width=16)
password_fld.grid(row=2, column=1, padx=8, pady=4)

# right column
password_btn = tk.Button(bottom_frame, text="Generate Password", font=BTN_FONT, width=15, relief="raised",
                         command=generate_password)
password_btn.grid(row=2, column=2, padx=7, pady=4)

# main loop
root.mainloop()
