import pandas as pd
import random

DATA_FILE = "./data/french_words.csv"
SAVE_FILE = "./data/words_to_learn.csv"


class Deck:

    def __init__(self, from_lan, to_lan):
        self.from_lan = from_lan
        self.to_lan = to_lan
        self.deck = []
        self.load_file(self.from_lan, self.to_lan)
        self.card_count = len(self.deck)
        self.current_card_index = 0
        self.shuffle_cards()
        self.current_card = self.deck[self.current_card_index]

    def load_file(self, from_lan, to_lan):
        """Loads the data, from the save file if it exists."""
        try:
            save_data = pd.read_csv(SAVE_FILE)
        except FileNotFoundError:
            original = pd.read_csv(DATA_FILE)
            # using list comprehension, store each card as a dictionary
            self.deck = [{from_lan: row[0], to_lan: row[1]} for row in original.values]
        else:
            self.deck = [{from_lan: row[0], to_lan: row[1]} for row in save_data.values]

    def shuffle_cards(self):
        """Shuffles all cards in the deck."""
        random.shuffle(self.deck)

    def next_card(self):
        """Moves to the next card in the deck."""
        # only if there is at least one card left
        if self.card_count > 0:
            if self.current_card_index < self.card_count - 1:
                self.current_card_index += 1
            # once the final card is reached, restart with any remaining cards
            else:
                self.shuffle_cards()
                self.current_card_index = 0
            # set it as the current card
            self.current_card = self.deck[self.current_card_index]

    def remove_card(self):
        """Removes the current card from the deck."""
        # just to be safe
        if self.current_card in self.deck:
            self.deck.remove(self.current_card)
            # also update the card count
            self.card_count = len(self.deck)
        if self.card_count > 0:
            # update the save file to mark it as learned
            df = pd.DataFrame(self.deck)
        # in case all cards have been "learned"
        # unclear what was supposed to happen, this is just to avoid crashing, really
        else:
            df = pd.DataFrame({self.from_lan: ["DECK"], self.to_lan: ["COMPLETE"]})
        df.to_csv(SAVE_FILE, index=False)
