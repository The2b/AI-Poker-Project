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

    '''
    print();
    print("[WIN, LOSE, TIE]:",victorOdds); # @DEBUG
    print();
    '''

    return victorOdds;

def oddsCalcPot(board):
    return OddsCalcPot.oddsCalcPot(board);
