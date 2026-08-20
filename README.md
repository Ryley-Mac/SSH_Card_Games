# SSH_Card_Games
An SSH server which enables multiplayer card games from a terminal.


## Flow
1) User's shall SSH into the main lobby, which enables them to select a card game lobby to join.

2) User's may join a game lobby only if they disconnected from an active game, or if no game is active. *Only a single instance of each game lobby may run at a time.

3) The game may only be started if all players ready up. *Players may vote kick players successfully with majority vote. This prevents a connection from freezing the lobby.

4) Upon starting a game, user's will be shown text art of the current state of hands and cards which are allowed to be visible.

5) On a player's turn, they will be prompted with their legal options, and the server will wait for their move before continuing.

6) Upon game completion, the user's will be given the option to play again or exit to the main lobby.
