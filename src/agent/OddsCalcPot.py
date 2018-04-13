'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 28 March 2018
@project Texas Hold'em AI
@file OddsCalcPot.py
'''

'''
Gives the agent the pot odds of a certain pot based on the pot and bet amounts. Returns a decimal between 0 and 1
Calcs are as follows:
    $Current Bet
    __________________________
    $Current Bet + $Current Pot
'''

def oddsCalcPotManual(currPot, bet):
    return (bet/(currPot+bet));

def oddsCalcPot(board):
    return oddsCalcPotManual(board.getPot(), board.getBet());
