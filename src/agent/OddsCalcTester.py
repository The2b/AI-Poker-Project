import TurnOddsCalc as TurnOddsCalc
import RiverOddsCalc as RiverOddsCalc
from board import Board, Stage
from card import Card, CardIDs
from handScanner import HandScanner

def testPairTurnToRiver(board, hand):
    board.setStage(Stage.FLOP_BETTING_ROUND);
    cards = [];
    for card in hand:
        cards.append(card);
    for card in board.getPool():
        if(card != None):
            cards.append(card);

    if(HandScanner().checkPair(cards) == 0):
        print("No pair by turn");
        board.setStage(Stage.FLOP_BETTING_ROUND);
        odds = TurnOddsCalc.pairTurnToRiver(board);
        print("Odds of pair: ", odds);
    else:
        print("Pair by turn");
        print("Cards:",[cardID.getCardID().name for cardID in cards]);
        return;

    board.setStage(Stage.RIVER_BETTING_ROUND);
    pool = board.getPool();

    cards.append(board.getTurn());
    cards.append(board.getRiver());
    print("Cards:",[card.getCardID().name for card in cards]);

def testTwoPairTurnToRiver(board, hand):
    board.setStage(Stage.FLOP_BETTING_ROUND);
    cards = [];
    for card in hand:
        cards.append(card);

    for card in board.getPool():
        if(card != None):
            cards.append(card);

    if(HandScanner().checkTwoPair(cards) == False):
        board.setStage(Stage.FLOP_BETTING_ROUND);
        if(HandScanner().checkPair(cards) != 0):
            print("Pair by turn");
            odds = TurnOddsCalc.twoPairTurnToRiverFromOne(board);
            print("Odds of two pair: ", odds);
        else:
            print("No pair by turn");
            odds = TurnOddsCalc.twoPairTurnToRiverFromZero(board);
            print("Odds of two pair: ", odds);
    else:
        print("Two pair by turn");
        print("Cards:",[cardID.getCardID().name for cardID in cards]);
        return;

    board.setStage(Stage.RIVER_BETTING_ROUND);
    pool = board.getPool();

    cards.append(board.getTurn());
    cards.append(board.getRiver());
    print("Cards:",[card.getCardID().name for card in cards]);

def testTwoPairTurnToRiverOne(board, scanner):
    pass;

if __name__ == '__main__':
    for i in range(10):
        board = Board();
        hand = [];
        hand.append(board.getDeck().dealCard());
        hand.append(board.getDeck().dealCard());

        testPairTurnToRiver(board, hand);
        print("");
        testTwoPairTurnToRiver(board, hand);
        print("");
