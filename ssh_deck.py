import random
from ssh_card import Card
from ssh_hand import Hand

class Deck:
    def  __init__(self, copies):
        self.SUITS = ["Diamonds", "Hearts", "Clubs", "Spades"]
        self.VALUES = {"Ace": [1, 11],
            "Two": [2],
            "Three": [3],
            "Four": [4],
            "Five": [5],
            "Six": [6],
            "Seven": [7],
            "Eight": [8],
            "Nine": [9],
            "Ten": [10],
            "Jack": [11],
            "Queen": [12],
            "King": [13]
           }
        self.FACECARDS = ["Jack", "Queen", "King"]
        self.COPIES = copies
        self.cards = []

    def initialize(self):
        self.cards = []
        for suit in self.SUITS:
           for value in self.VALUES:
               self.cards.append(Card(suit, value, self.COPIES))
    
    def shuffle(self):
        if self.cards == []:
            return ("Error: you must initialize the deck before shuffling...")

        random.shuffle(self.cards)

    def deal(self, hand, count):
        """Removes a number of 'card's from the deck equal to 'count',
        and adds the removed 'card's to the given 'hand'."""
        fullOutput = ""
        while count > 0:
            card = self.cards.pop()
            hand.add(card)
            count -= 1
            fullOutput += (f"Deck: dealt a card to {hand.name}\n")
        return fullOutput
