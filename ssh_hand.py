from card import Card

class Hand:
    def __init__(self):
        self.name = "Guest"
        self.cards = []
        self.sum = 0
        self.suitCount = {}
        self.player = False
    
    def add(self, card):
        self.cards.append(card)

    def play(self, card):
        if self.cards is not None or self.cards is not []:
            self.cards.remove(card)
            return(f"{self.name}: Playing {card}")

    def show(self, count):
        cardCount = len(self.cards)
        allCards = ""
        if count >= cardCount:
            for card in self.cards:
                allCards += (f"{self.name}: Has {card}\n")
        else:
            counter = 0
            while counter < count:
                allCards += (f"{self.name}: Has {self.cards[counter]}\n")
                counter += 1
        return allCards
