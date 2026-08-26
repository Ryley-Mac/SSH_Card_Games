import ssh_blackjack.py
class BlakJackLobby:
    def __init__(self, players):
        self.players = players # {username: address}
        self.started = False
        self.blackjack = None
    
    def _start(self):
        self.started = True

    def _stop(self):
        self.started = False

    def _play(self):
        if self.blackjack is None:
            self.blackjack = BlackJack(self.players)
