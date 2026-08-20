from ssh_signals import Signal, SignalType
from ssh_deck import Deck
from ssh_hand import Hand
import time

class BlackJack:
    def __init__(self):
        self.deck = Deck(1)
        self.deck.initialize()
        self.deck.shuffle()

        self.dealerHand = Hand()
        self.dealerHand.name = "Dealer"
        print(Signal(type=SignalType.DEAL, message=self.deck.deal(self.dealerHand, 2)))
        self.hands = []
        
        time.sleep(0.5)

        self.gameStarted = False

    def _playerTurn(self, hand):
        """Asks user if they want to hit or stay.
        Ends turn if they stay.
        Recursively runs again if they hit."""

        belowTwentyOne = self._validateHand(hand)
        totalCards = len(hand.cards)
        if not belowTwentyOne:
            return

        userInput = ""
        while not (userInput.lower() == "hit" or userInput.lower() == "stay"): 
            userInput = input("Hit or Stay? ")

        if userInput.lower() == "hit":
            print(Signal(type=SignalType.DEAL, message=self.deck.deal(hand, 1)))
            self._playerTurn(hand)
        return

    def _validateHand(self, hand):
        """Detects if a hand has blackjack or has busted."""
        self._calculateSum(hand)
        if hand.sum == 21:
            print(Signal(type=SignalType.BLACKJACK, message=hand.show(len(hand.cards)), data={hand.name:hand.cards}, value=hand.sum))
            return False
        elif hand.sum > 21:
            print(Signal(type=SignalType.BUST, message=hand.show(len(hand.cards)), data={hand.name:hand.cards}, value=hand.sum))
            return False
        else:
            print(Signal(type=SignalType.INFO, message=hand.show(len(hand.cards)), data={hand.name:hand.cards}, value=hand.sum))
            return True

    def _calculateSum(self, hand, count=None):
        """Helper to calculate the sum of all cards in a hand."""
        hand.sum = 0
        aceCount = 0
        handLen = len(hand.cards)
        
        if count == None:
            count = handLen

        if handLen <= count:
            for card in hand.cards:
               if card.value in self.deck.FACECARDS:
                   hand.sum += 10
               elif card.value == "Ace":
                   aceCount += 1
               else:
                   hand.sum += self.deck.VALUES[card.value][0]
        else:
            for i in range(count):
                card = hand.cards[i]
                if card.value in self.deck.FACECARDS:
                    hand.sum += 10
                elif card.value == "Ace":
                    aceCount += 1
                else:
                    hand.sum += self.deck.VALUES[card.value][0]

        while aceCount > 0:
            if (11 + hand.sum) <= 21:
                hand.sum += 11
            else:
                hand.sum += 1
            aceCount -= 1

    def start(self, playerCount):
        while playerCount > 0:
            hand = Hand()
            hand.name = f"Guest{playerCount}"
            print(Signal(type=SignalType.DEAL, message=self.deck.deal(hand, 2)))
            self.hands.append(hand)        
            playerCount -= 1

            self._calculateSum(self.dealerHand, 1)
            print(Signal(type=SignalType.INFO, message=self.dealerHand.show(1), data={self.dealerHand.name:self.dealerHand.cards}, value=self.dealerHand.sum))

            for hand in self.hands:
                self._playerTurn(hand)
           
           # Must extract dealer hand logic from here and place after this logic.
           # Use self.hands to compare dealer's hand with each player's hand.
           # If dealer hand is >= 17, the dealer shall stay.
           # If the highest player hand <= 21 is > dealer hand, the dealer shall hit,
           # otherwise the dealer shall stay.
            if hand.sum < 22:
                while self._validateHand(self.dealerHand): # Dealer hits while under 17
                    if self.dealerHand.sum > 16:
                       # print(Signal(SignalType.INFO, message=self.dealerHand.show(len(self.dealerHand.cards)), data={self.dealerHand.name:self.dealerHand.cards}, value=self.dealerHand.sum))
                        break
                    print(Signal(type=SignalType.DEAL, message=self.deck.deal(self.dealerHand, 1)))
                   
                    time.sleep(0.5)

            if hand.sum > 21 or self.dealerHand.sum >= 21:
                self._calculateSum(self.dealerHand)
                #print(Signal(SignalType.INFO, message=self.dealerHand.show(len(self.dealerHand.cards)), data={self.dealerHand.name:self.dealerHand.cards}, value=self.dealerHand.sum))
           
            if (self.dealerHand.sum > 21 or self.dealerHand.sum < hand.sum ) and hand.sum < 22:
                print(Signal(type=SignalType.WIN, message=hand.show(len(hand.cards)), data={hand.name:hand.cards}, value=hand.sum))
            elif (hand.sum > 21 or hand.sum < self.dealerHand.sum) and self.dealerHand.sum < 22:
                print(Signal(type=SignalType.LOSE, message=self.dealerHand.show(len(self.dealerHand.cards)), data={self.dealerHand.name:self.dealerHand.cards}, value=self.dealerHand.sum))
            else:
                print(Signal(type=SignalType.DRAW, message=f"{hand.show(len(hand.cards))}: {self.dealerHand.show(len(self.dealerHand.cards))}", data={self.dealerHand.name:self.dealerHand.cards, hand.name:hand.cards}, value=hand.sum))

if __name__ == '__main__':
    bj = BlackJack()
    bj.start(1)
