'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 09 April 2018
@project Texas Hold'em AI
@file OddsCalc.py
@errorcodes 8XX

This set of functions replaces the old OddsCalc module
'''

import sys # exit
#import pdb # @DEBUG

from HandScanner import HandScanner, HandIDs
from Board import Stage, Board
import OddsCalcHole
import OddsCalcTurn
import OddsCalcRiver
import OddsCalcFinal
import OddsCalcPot

WIN = 0;
TIE = 2;
LOSE = 1;

MARGIN = .1;

'''
Calculates the odds of victory, ties, and losses between exactly two agents

@param Card[] cards
@param Board board
@return float victorOdds [win, lose, tie]
'''
def oddsCalc(cards, board):
    # Get the odds of winning, losing, and tying from the correct module
    if(board.getStage() == Stage.FIRST_BETTING_ROUND):
        victorOdds = OddsCalcHole.oddsCalcHole(cards, board);
    elif(board.getStage() == Stage.FLOP_BETTING_ROUND):
        victorOdds = OddsCalcTurn.oddsCalcTurn(cards, board);
    elif(board.getStage() == Stage.TURN_BETTING_ROUND):
        victorOdds = OddsCalcRiver.oddsCalcRiver(cards, board);
    elif(board.getStage() == Stage.RIVER_BETTING_ROUND):
        victorOdds = OddsCalcFinal.oddsCalcFinal(cards, board);

    # Nothing below this point should be in this function @TODO
    potOdds = OddsCalcPot.oddsCalcPot(board);

    # If we want strict wins v losses and to ignore ties and have a flat margin, use this.
    print("[WIN, LOSE, TIE]:",victorOdds); # @DEBUG
    print("Pot odds:",potOdds);
    '''
    winsReal = victorOdds[WIN];
    lossesReal = victorOdds[LOSE];
    wins = (winsReal / (winsReal + lossesReal));
    losses = (lossesReal / (winsReal + lossesReal));
    
    margin = MARGIN;
    '''

    # If we want the tie to be the margin, we can use this
    '''
    wins = victorOdds[WIN];
    losses = victorOdds[LOSE];
    margin = victorOdds[TIE];
    '''

    wins = victorOdds[WIN] + ((victorOdds[TIE] / 2) * (board.getStage().value >= Stage.TURN_BETTING_ROUND.value)); # The boolean logic at the end is meant to say that if we're after the turn, count a tie as half a win. If we're before the turn, don't count it at all
    losses = victorOdds[LOSE] + ((victorOdds[TIE] / 2) * (board.getStage().value < Stage.TURN_BETTING_ROUND.value)) ; # Opposite of the previous

    # Here, we just decide raw. Once we add in money, we'll add in the margin
    if(wins > potOdds):
        print("Stay in");
    elif(wins < potOdds):
        print("Fold");
    elif(wins == potOdds):
        print("Stay in. Even");
    else:
        print("ERROR: wins and loses not different or equal. Error 801");
        sys.exit(801);
    return victorOdds;

def oddsCalcPot(board):
    return OddsCalcPot.oddsCalcPot(board);
