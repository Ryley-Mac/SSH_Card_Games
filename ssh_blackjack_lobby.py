import ssh_blackjack.py
class BlakJackLobby:
    def __init__(self, players):
        self.players = players # {username: address}
        self.started = False
        self.blackjack = None
        self.currentSignal = None
    
    def _start(self):
        self.started = True

    def _stop(self):
        self.started = False

    def _play(self):
        if started is False and self.blackjack is None and self.players > 0:
            self._start()
            self.blackjack = BlackJack(self.players)
            self.blackjack.start(self.players)
            while self.started:
                self.currentSignal = self.blackjack.signalBuffer.pop()
                print(self.currentSignal.keys)

