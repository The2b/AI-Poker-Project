This directory contains DeepStack match logs in a format based on the one used in the Annual Computer Poker Competition.  The files are formatted as plain text with each line corresponding to a game/hand of poker.  You should be able to open the file with your choice of text editor.  Some options that should come included on your computer are Notepad for Windows or TextEdit for OSX.  

The high-level format of each hand is:

STATE:<Hand#>:<Stacks>:<Blinds>:<Betting>:<Cards>:<Payoff>:<Player Positions> # <Timestamp>

We use the following example hand to illustrate.

STATE:1001400037:20150|19850:300|150:r750c/cc/r1500f:8sQd|Ks7h/2d3d4d/6d:750|-750:DeepStack|Nate_@NateMeyvis


"STATE:1001400037" – Hand index

For the freezeout matches, we constructed hand indexes that should make it easier to import the accompanying PokerStars logs.  The last 5 digits of the index specifies the hand number for this match.  In this example, "00037" indicates that this is the thirty-seventh hand of the match.  The preceding digits are based on the player and match number.


"DeepStack|player.account" – Player positions

In this example DeepStack is player 1, the big blind, and player 2 (the human player) would be in the small blind.


20150|19850 – Chip stacks for player1|player2

The chips available to each player at the start of the hand.  Players start each match with stacks of 20000 (200 big blinds).


300|150 – Blinds for player1|player2

Blinds in our freezeout matches start at 100|50 and increase every 10 hands.


"r750c/cc/r1500f" – The betting history

 'f' : folds
 'c' : check/call
 'rX' : raise to X  (note, "raise to" rather than "raise by": the player's total chips in the pot)
 '/' : round separator
 Note that the initial blinds are not listed in the betting history.


"8sQd|Ks7h/2d3d4d/6d" – Cards dealt

The private cards for each player, starting with the big blind (player 1, 8sQd), the small blind (player 2, Ks7h), and the public cards for each round (separated with '/').


750|-750 – Chips won/lost by player1|player2
