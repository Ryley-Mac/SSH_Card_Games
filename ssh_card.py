class Card:
    def __init__(self, suit: str, value: int, copies: int):
        self.suit = suit
        self.value = value
        self.faceCard = False
        self.copies = copies
    
    def __str__(self):
        return (f"{self.value} of {self.suit}")
