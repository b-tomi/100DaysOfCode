import tkinter as tk

from quiz_brain import QuizBrain


THEME_COLOR = "#375362"
FONT = ("Arial", 18, "italic")
SCORE_FONT = ("Arial", 12, "bold")
TRUE_IMAGE = "./images/true.png"
FALSE_IMAGE = "./images/false.png"


class QuizInterface:

    # this will make sure that quiz_brain is a QuizBrain object
    def __init__(self, quiz_brain: QuizBrain):
        self.qb = quiz_brain
        self.root = tk.Tk()
        self.root.title("Quizzler")
        self.root.iconbitmap("icon.ico")
        self.root.geometry("340x500")
        self.root.resizable(False, False)
        self.root.configure(bg=THEME_COLOR)

        # top row
        self.score_lbl = tk.Label(self.root, text="", fg="white", bg=THEME_COLOR, font=SCORE_FONT)
        self.score_lbl.grid(row=0, column=1, pady=20)

        # middle row
        self.canvas = tk.Canvas(self.root, width=300, height=250, highlightthickness=0, bg="white")
        # set width=280 so the text wraps
        self.question_text = self.canvas.create_text(150, 125, text="", font=FONT, width=280)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # bottom row
        true_img = tk.PhotoImage(file=TRUE_IMAGE)
        self.true_btn = tk.Button(self.root, image=true_img, highlightthickness=0, bg=THEME_COLOR, relief="flat",
                                  command=self.choose_true)
        self.true_btn.grid(row=2, column=0, pady=20)

        false_img = tk.PhotoImage(file=FALSE_IMAGE)
        self.false_btn = tk.Button(self.root, image=false_img, highlightthickness=0, bg=THEME_COLOR, relief="flat",
                                   command=self.choose_false)
        self.false_btn.grid(row=2, column=1, pady=20)

        # load the initial question
        self.get_next_question()

        # main loop
        self.root.mainloop()

    def get_next_question(self):
        """Displays the next question on the canvas."""
        # reset the canvas color
        self.canvas.config(bg="white")
        # set the score label
        self.score_lbl.config(text=f"Score: {self.qb.score}")

        if self.qb.still_has_questions():
            self.canvas.itemconfig(self.question_text, text=self.qb.next_question())
        else:
            self.canvas.itemconfig(self.question_text, text="No questions left.")
            # disable the buttons
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def choose_true(self):
        """Evaluates a click on the "True" button."""
        # using a lambda function for these would might been a little simpler, but this seems more readable
        self.give_feedback(self.qb.check_answer("True"))

    def choose_false(self):
        """Evaluates a click on the "False" button."""
        self.give_feedback(self.qb.check_answer("False"))

    def give_feedback(self, is_right):
        """Evaluates the answer."""
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        # wait for 1 second
        self.root.after(1000, self.get_next_question)
