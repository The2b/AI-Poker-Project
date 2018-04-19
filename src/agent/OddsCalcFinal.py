'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 12 April 2018
@project Texas Hold'em AI
@file OddsCalcFinal
@errorcodes 10XX
'''

import sys
from HandScanner import HandScanner, HandIDs

def oddsCalcFinal(cards, board):
    agentBestHand = HandScanner().checkBestHand(cards);
    oppoHandList = oddsCalcFinalOppo(cards, board);

    wins = sum([i for i in oppoHandList if oppoHandList.index(i) < agentBestHand.value]); # Add all the hands we have a better hand than
    ties = sum([i for i in oppoHandList if oppoHandList.index(i) == agentBestHand.value]);
    losses = sum([i for i in oppoHandList if oppoHandList.index(i) > agentBestHand.value]);
    total = sum(oppoHandList);

    return [wins/total, losses/total, ties/total];

def oddsCalcFinalOppo(cards, board):
    scanner = HandScanner();
    oppoHand = [];
    for card in board.getPool():
        if(card != None):
            oppoHand.append(card);
        else:
            print("ERROR: Cards in pool are null during the final round. Exiting...");
            sys.exit(1001);

    idList = [0 for i in HandIDs];
    for card1 in [card for card in board.getDeck().getCards() if card not in cards]:
        oppoHand.append(card1);
        for card2 in [card for card in board.getDeck().getCards() if card not in cards and card.getCardID().value > card1.getCardID().value]:
            oppoHand.append(card2);
            idList[scanner.checkBestHand(oppoHand).value] += 1;
            oppoHand.pop(len(oppoHand)-1);
        oppoHand.pop(len(oppoHand)-1);

    return idList;
