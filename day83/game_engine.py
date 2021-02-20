import art

# default values for player names
PLAYERS = ("P1", "P2")
# for consistency, with indexes, 0 and 1 will refer to players
# and 2 will indicate an empty field, i.e. MARKS[2] = " "
MARKS = ("x", "o", " ")
# not very PEP8 compliant, but more readable
COORDINATES = {
    "A1": 0, "B1": 1, "C1": 2,
    "A2": 3, "B2": 4, "C2": 5,
    "A3": 6, "B3": 7, "C3": 8
}


class GameEngine:
    def __init__(self, p1_name=PLAYERS[0], p2_name=PLAYERS[1]):
        self._players = (p1_name, p2_name)
        self._score = [0, 0]
        self._board = []
        self._round = 0
        self._turn = 0
        self._in_progress = False

    def start(self):
        """Starts a new game."""
        self.new_round()
        print(art.logo)

    def new_round(self):
        """Starts a new round."""
        self._round += 1
        # again, 0 and 1 are the players, 2 represents an empty field
        self._board = [2, 2, 2, 2, 2, 2, 2, 2, 2]
        self._turn = 0
        self._in_progress = True

    def round_in_progress(self):
        """Checks if there is a round in progress and returns a BOOL."""
        return self._in_progress

    def print_score(self, final=False):
        """Prints the current round and the score."""
        # this is a little basic, but I decided not to clutter the output too much
        if final:
            print(f"# FINAL SCORE after {self._round} round(s)")
        else:
            print(f"# SCORE: Round #{self._round}")
        print(f"# {self._players[0]}: {self._score[0]}")
        print(f"# {self._players[1]}: {self._score[1]}")

    def print_board(self):
        """Prints the current board."""
        self.print_score()
        # populate the fields on the board
        # using list comprehension to provide args for the str.format() method
        print(art.board.format(*[MARKS[field] for field in self._board]))

    def next_move(self):
        """Evaluates the board and if there is no winner, asks for the next move."""
        # evaluate the board
        winner = self._check_winner()
        if winner is not None:
            if winner == -1:
                print("It's a tie!")
            else:
                print(f"{self._players[winner]} wins!")
        else:
            # ask for the next move, include their defined mark in the prompt for reference
            print(f"{self._players[self._turn]} ({MARKS[self._turn]}) what's your move?")
            new_index = self._get_input()
            # add the new mark to the board
            self._board[new_index] = self._turn
            # switch to the other player
            if self._turn == 0:
                self._turn = 1
            else:
                self._turn = 0

    def _get_input(self):
        while True:
            raw_input = input("> ").upper()
            # check if it's a valid coordinate
            if raw_input not in COORDINATES:
                print("Please choose a valid field (e.g. A1, B2, C3, etc.)")
            else:
                chosen_index = COORDINATES[raw_input]
                # make sure the field is still empty
                if self._board[chosen_index] != 2:
                    print("Please choose a blank field.")
                else:
                    return chosen_index

    def _check_winner(self):
        winner = None
        # evaluate each player
        for player in [0, 1]:
            # evaluate rows, using the field indexes (indices?)
            # look at the COORDINATES dictionary for reference
            for i in [0, 3, 6]:
                if player == self._board[i] == self._board[i + 1] == self._board[i + 2]:
                    winner = player
            # evaluate columns
            for i in [0, 1, 2]:
                if player == self._board[i] == self._board[i + 3] == self._board[i + 6]:
                    winner = player
            # evaluate diagonals
            if player == self._board[0] == self._board[4] == self._board[8] or \
                    player == self._board[2] == self._board[4] == self._board[6]:
                winner = player
        # end round if a winner was found
        if winner is not None:
            # increase their score
            self._score[winner] += 1
            self._in_progress = False
        # if no winner, but no empty fields left, it's a tie
        elif 2 not in self._board:
            # using -1 to indicate a tie
            winner = -1
            self._in_progress = False
        # return the winner's index, -1, or None
        return winner
