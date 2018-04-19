'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 09 April 2018
@project Texas Hold'em AI
@file OddsCalcRiver.py
@errorcodes 7XX

This set of functions replaces the old RiverOddsCalc module
'''

import multiprocessing as mp
#import pdb # @DEBUG
import sys # exit
from copy import deepcopy
from HandScanner import HandScanner, HandIDs
from Card import Card, CardIDs

'''
Calculates the odds of victory, ties, and losses between exactly two agents

@param Card[] cards
@param Board board
@return float victorOdds [win, lose, tie]
'''
def oddsCalcRiver(cards, board):
    agentOdds = oddsCalcRiverAgent(cards, board);
    oppoOdds = oddsCalcRiverOppoMP(cards, board);

    oddsMatrix = [[0 for i in HandIDs] for j in HandIDs];

    win = 0;
    lose = 0;
    tie = 0;

    for aIndex in range(len(agentOdds)):
        for oIndex in range(len(oppoOdds)):
            #oddsMatrix[aIndex][oIndex] = agentOdds[aIndex] * oppoOdds[oIndex]; # @DEBUG Mostly only here for a visual representation of the matrix. Not functional in any way.
            if(aIndex > oIndex):
                win += (agentOdds[aIndex] * oppoOdds[oIndex]);
            elif(aIndex == oIndex):
                tie += (agentOdds[aIndex] * oppoOdds[oIndex]);
            elif(aIndex < oIndex):
                lose += (agentOdds[aIndex] * oppoOdds[oIndex]);
            else:
                print("ERROR: Shouldn't have gotten here. Agent odds is not greater than, equal to, or less than oppo odds. Error: 701");
                sys.exit(701);

    return [win, lose, tie];

'''
Handles the odds calcs for the using agent

@param Card[] cards
@param Board board
@return float oddsList[HandIDs]
'''
def oddsCalcRiverAgent(cards, board):
    scanner = HandScanner();

    validCards = [Card(card) for card in CardIDs if card not in [card.getCardID() for card in cards]];
    for i in range(board.getDeck().getNumDecks() - 1):
        for card in CardIDs:
            validCards.append(Card(card));

    idList = [0 for hand in HandIDs];
    oddsList = [];

    cardsCopy = deepcopy(cards);
    for card1 in validCards:
        cardsCopy.append(card1);
        idList[scanner.checkBestHand(cardsCopy).value] += 1;
        cardsCopy.pop(len(cardsCopy) - 1);

    agentSum = sum(idList);

    oddsList = [(count / agentSum) for count in idList];

    return oddsList;

'''
Handles the odds calcs for the agent opposing the using agent

@param Card[] cards
@param Board board
@return float oddsList[HandIDs] 
'''
def oddsCalcRiverOppo(cards, board):
    # Build what we know the opponent can use
    oppoCards = [];

    for card in board.getPool():
        if(card != None):
            oppoCards.append(card);
        
    # Enumerate all the possible combos, check if they work
    scanner = HandScanner();

    validCards = [Card(card) for card in CardIDs if card not in [card.getCardID() for card in cards]];
    for i in range(board.getDeck().getNumDecks() - 1):
        for card in CardIDs:
            validCards.append(Card(card));

    idList = [0 for hand in HandIDs];

    oppoCardsCopy = deepcopy(oppoCards);
    for card1 in validCards:
        oppoCardsCopy.append(card1);
        for card2 in [card for card in validCards if card != card1]:
            oppoCardsCopy.append(card2);
            for card3 in [card for card in validCards if(card.getCardID().value > card1.getCardID().value and card.getCardID().value > card2.getCardID().value)]:
                oppoCardsCopy.append(card3);
                idList[scanner.checkBestHand(oppoCardsCopy).value] += 1;
                oppoCardsCopy.pop(len(oppoCardsCopy) - 1);
            oppoCardsCopy.pop(len(oppoCardsCopy) - 1);
        oppoCardsCopy.pop(len(oppoCardsCopy) - 1);
    
    oppoSum = sum(idList);
    oddsList = [(count / oppoSum) for count in idList];

    return oddsList;


NUM_PROCESSES = 12;

'''
Handles the same as above, but in a multi-process fashion

@param Card[] cards
@param Board board
@return float oddsList[HandIDs]
'''
def oddsCalcRiverOppoMP(cards, board):
    # Create multiprocessing resources
    pool = mp.Pool(processes=NUM_PROCESSES);
    resList = [];
    idList = [0 for i in HandIDs];

    # Build what we know the opponent can use
    oppoCards = [];

    for card in board.getPool():
        if(card != None):
            oppoCards.append(card);
        
    # Enumerate all the possible combos, check if they work
    scanner = HandScanner();


    validCards = [Card(card) for card in CardIDs if card not in [card.getCardID() for card in cards]];
    for i in range(board.getDeck().getNumDecks() - 1):
        for card in CardIDs:
            validCards.append(Card(card));

    idList = [0 for hand in HandIDs];

    #pdb.set_trace(); # @DEBUG

    oppoCardsCopy = deepcopy(oppoCards);
    for card1 in validCards:
        oppoCardsCopy.append(card1);
        resList.append(pool.apply_async(__oddsCalcRiverOppoMPWorker,[oppoCardsCopy, card1, validCards, scanner]));
        oppoCardsCopy.pop(len(oppoCardsCopy) - 1);

    pool.close();
    pool.join();

    for res in [result.get() for result in resList]:
        for i in range(len(res)):
            idList[i] += res[i];


    oppoSum = sum(idList);
    return[(count / oppoSum) for count in idList];

'''
This is a specialized method meant to be called only in the oddsCalcRiverOppoMP function
'''
def __oddsCalcRiverOppoMPWorker(oppoCards, card1, validCards, scanner, index=0):
        idList = [0 for i in HandIDs];
        oppoCardsCopy = deepcopy(oppoCards);
        for card2 in [card for card in validCards if card.getCardID().value > card1.getCardID().value]:
            oppoCardsCopy.append(card2);
            for card3 in [card for card in validCards if(card.getCardID().value > card1.getCardID().value and card.getCardID().value > card2.getCardID().value)]:
                oppoCardsCopy.append(card3);
                idList[scanner.checkBestHand(oppoCardsCopy).value] += 1;
                oppoCardsCopy.pop(len(oppoCardsCopy) - 1);
            oppoCardsCopy.pop(len(oppoCardsCopy) - 1);
        return idList;
