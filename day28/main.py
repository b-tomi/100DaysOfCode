# Pomodoro

import tkinter as tk

# number of work repetitions before a long break
INITIAL_REPS = 4
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
# colors for easier access
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


def count_down(count):
    """Takes the number of seconds as INT and counts down until reaches zero."""
    # update the canvas text with the formatted time
    canvas.itemconfig(timer_text, text=split_time(count))
    if count > 0:
        params["timer"] = root.after(1000, count_down, count - 1)
    else:
        start_timer()


def split_time(time):
    """Takes the number of seconds as INT and returns it as STR in "MM:SS" format."""
    # split the time to minutes and seconds
    minutes = time // 60
    seconds = time % 60
    return f"{format_time(minutes)}:{format_time(seconds)}"


def format_time(num):
    """Takes an INT and returns the value as STR that includes the initial zero."""
    if num == 0:
        return "00"
    else:
        # using the ternary operator for practice: [on_true] if [expression] else [on_false]
        return str(num) if num >= 10 else f"0{num}"


def start():
    """Initializes a timer, unless there is one already running."""
    # to avoid starting multiple timers
    # if not params["timer"]: would also work, but this seems more readable
    if params["timer"] is None:
        start_timer()


def start_timer():
    """Starts the timer with the defined parameters."""
    # update the number of checkmark
    checkmarks = "✔" * params["checks"]
    check_label.config(text=checkmarks)

    # all reps and breaks complete
    if params["reps_left"] == 0 and params["breaks_left"] == 0:
        # unclear what to do once the whole session is complete, so just reset
        reset()
    # long break after 4 work reps and 3 short breaks
    elif params["reps_left"] == 0 and params["breaks_left"] == 1:
        timer_label.config(text="Break", fg=RED)
        params["breaks_left"] -= 1
        count_down(LONG_BREAK_MIN * 60)
    # short break after a work rep
    elif params["reps_left"] < params["breaks_left"]:
        timer_label.config(text="Break", fg=PINK)
        params["breaks_left"] -= 1
        count_down(SHORT_BREAK_MIN * 60)
    # do another work rep
    else:
        timer_label.config(text="Work", fg=GREEN)
        params["reps_left"] -= 1
        params["checks"] += 1
        count_down(WORK_MIN * 60)


def reset():
    """Resets the timer."""
    # unless there is an active timer, this should evaluate as "falsy"
    if params["timer"]:
        root.after_cancel(params["timer"])
    reset_params()
    # reset the modified labels
    timer_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    check_label.config(text="")


def reset_params():
    """Resets the timer parameters to their initial value."""
    # number of remaining work reps and breaks
    params["reps_left"] = INITIAL_REPS
    params["breaks_left"] = INITIAL_REPS
    # count the number of displayed checkmarks 
    params["checks"] = 0
    # store the timer
    params["timer"] = None


# for sake of simplicity, store variables in a dictionary
params = {}
# moved these to a function to avoid repetition
reset_params()

# main window setup
root = tk.Tk()
root.title("Pomodoro")
root.iconbitmap("icon.ico")
root.geometry("400x360")
root.resizable(False, False)
root.config(bg=YELLOW)

# left column
start_btn = tk.Button(text="Start", fg="grey", bg=GREEN, font=(FONT_NAME, 11), width=6, relief="ridge", command=start)
start_btn.grid(row=2, column=0, padx=20)

# middle column
timer_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 36))
timer_label.grid(row=0, column=1, pady=4)
# canvas
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
bg_image = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=bg_image)
canvas.grid(row=1, column=1)
timer_text = canvas.create_text(100, 132, text="00:00", fill="white", font=(FONT_NAME, 34, "bold"))
# checkmarks
check_label = tk.Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 18), width=10)
check_label.grid(row=3, column=1)

# right column
reset_btn = tk.Button(text="Reset", fg="grey", bg=PINK, font=(FONT_NAME, 11), width=6, relief="ridge", command=reset)
reset_btn.grid(row=2, column=2, padx=12)

# main loop
root.mainloop()
