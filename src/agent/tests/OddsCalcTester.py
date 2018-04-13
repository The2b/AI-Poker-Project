import OddsCalcHole
from Board import Board, Stage
from Card import Card, CardIDs
from HandScanner import HandScanner, HandIDs
import random
import OddsCalc
#import timeit
#import pdb # @DEBUG
import statistics as stat

def fullSim2():
    board = Board();
    cards = [];
    cards.append(board.getDeck().dealCard());
    cards.append(board.getDeck().dealCard());
    isIn = True;

    oppoCards = [];
    oppoCards.append(board.getDeck().dealCard());
    oppoCards.append(board.getDeck().dealCard());

    board.setStage(Stage.FLOP_BETTING_ROUND);
    board.setPot(random.randint(20,250));
    board.setBet(random.randint(5,100));

    for card in board.getPool():
        if(card != None):
            cards.append(card);
            oppoCards.append(card);
    
    if(OddsCalc.oddsCalc(cards, board)):
        board.addToPot(board.getBet());
    else:
        isIn = False;

    board.setStage(Stage.TURN_BETTING_ROUND);
    cards.append(board.getTurn());
    oppoCards.append(board.getTurn());
    board.setBet(random.randint(5,100));

    if(isIn and OddsCalc.oddsCalc(cards, board)):
        board.addToPot(board.getBet());

    board.setStage(Stage.RIVER_BETTING_ROUND);
    cards.append(board.getRiver());
    oppoCards.append(board.getRiver());

    print();
    print("Agent cards:", [card.getCardID().name for card in cards]);
    print("Opponent cards:", [card.getCardID().name for card in oppoCards]);
    print();

    scanner = HandScanner();
    
    winner = scanner.declareWinner([cards, oppoCards], board);

    if(type(winner) == list):
        print();
        print("Winners:",winner);
        print();
    elif(type(winner) == int):
        print();
        print("Winner:",["Agent","Opponent"][winner]);
        print();
    else:
        print();
        print("ERROR 901: declareWinner returned an unexpected value");
        print();

    #print("GC Objects:",len(gc.get_objects()));
    #gc.collect();
    #print("GC Objects PM:",len(gc.get_objects()));

if __name__ == '__main__':
    #'''
    time = timeit.timeit(fullSim2,number=100);
    print();
    print("Total time over 100 iterations:",time);
    print("Average time per run:",time/100);
    #'''

    #getHolePointsFull();
