# Mile to Kilometers Converter

import tkinter as tk

FONT = ("Arial", 12)
CONV_FACTOR = 1.60934


def calculate():
    mil_str = entry_box.get()
    try:
        mil = float(mil_str)
        kms_str = str(round(mil * CONV_FACTOR, 2))
        # change the color in case the previous entry was invalid
        converted.config(text=kms_str, fg="black")
    except ValueError:
        converted.config(text="Invalid input", fg="red")


# main window setup
root = tk.Tk()
root.title("Mile to Kilometers Converter")
root.iconbitmap("icon.ico")
root.geometry("300x150")
root.resizable(False, False)

# left column
equal = tk.Label(root, text="is equal to", fg="grey", font=FONT, width=12)
equal.grid(row=1, column=0)

# middle column
entry_box = tk.Entry(root, font=FONT, width=10)
entry_box.grid(row=0, column=1, padx=10, pady=16)
# using a simple label for the result
converted = tk.Label(root, text="", font=FONT, width=10)
converted.grid(row=1, column=1)
calculate_btn = tk.Button(root, text="Calculate", font=FONT, width=8, height=1, command=calculate)
calculate_btn.grid(row=2, column=1, pady=20)

# right column
miles = tk.Label(root, text="Miles", font=FONT, width=6)
miles.grid(row=0, column=2)
kms = tk.Label(root, text="Km", font=FONT, width=6)
kms.grid(row=1, column=2)

# main loop
root.mainloop()
