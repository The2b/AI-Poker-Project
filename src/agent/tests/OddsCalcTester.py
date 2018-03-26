import TurnOddsCalc as TurnOddsCalc
import RiverOddsCalc as RiverOddsCalc
from Board import Board, Stage
from Card import Card, CardIDs
from HandScanner import HandScanner

def testPairTurnToRiver(cards, board):
    if(HandScanner().checkPair(cards) == 0):
        odds = TurnOddsCalc.pairTurnToRiver(board);
        print("Odds of pair:", odds);
        return;
    else:
        print("Odds of pair:",1);
        return;

def testTwoPairTurnToRiver(cards, board):
    if(not HandScanner().checkTwoPair(cards)):
        if(HandScanner().checkPair(cards) != 0):
            odds = TurnOddsCalc.twoPairTurnToRiverFromOne(board);
            print("Odds of two pair:", odds);
            return;

        else:
            odds = TurnOddsCalc.twoPairTurnToRiverFromZero(board);
            print("Odds of two pair:", odds);
            return;
    else:
        print("Odds of two pair:",1);
        return;

def testThreeTurnToRiver(cards, board):
    if(HandScanner().checkThreeOfAKind(cards) == 0):
        # Get matched cards
        assert(type(cards) == list);
        cardSet = set([card.getCardNum() for card in cards]);

        numMatched = len(cards) - len(cardSet); # This assignment will break if there's already a three of a kind. Luckily, thats not an issue here
        numUnmatched = len(cards) - (2 * numMatched);

        odds = TurnOddsCalc.threeTurnToRiver(board, numUnmatched, numMatched);

        print("Odds of a three of a kind:",odds);
        return;
    else:
        print("Odds of a three of a kind:",1);

def testStraightTurnToRiver(cards, board):  # @TODO Fix these worker functions
    if(not HandScanner().checkStraight(cards)):
        odds = TurnOddsCalc.straightTurnToRiver(cards, board);
        print("Odds of straight:",odds);
        return;
    else:
        print("Odds of straight:",1);
        return;

def testFlushTurnToRiver(cards, board):
    if(not HandScanner().checkFlush(cards)):
        odds = TurnOddsCalc.flushTurnToRiver(cards, board);
        print("Odds of flush:",odds);
        return;
    else:
        print("Odds of flush:",1);
        return;

def testFullHouseTurnToRiver(cards, board):
    if(not HandScanner().checkFullHouse(cards)):
        odds = TurnOddsCalc.fullHouseTurnToRiver(cards, board);
        print("Odds of full house:",odds);
        return;
    else:
        print("Odds of full house:",1);
        return;

def testFourTurnToRiver(cards, board):
    if(not HandScanner().checkFourOfAKind(cards)):
        odds = TurnOddsCalc.fourTurnToRiver(cards, board);
        print("Odds of four of a kind:",odds);
        return;
    else:
        print("Odds of four of a kind:",1);
        return;

def testFiveTurnToRiver(cards, board):
    if(not HandScanner().checkFiveOfAKind(cards)):
        odds = TurnOddsCalc.fiveTurnToRiver(cards, board);
        print("Odds of five of a kind:",odds);
        return;
    else:
        print("Odds of five of a kind:",1);
        return;


if __name__ == '__main__':
    #for i in range(10):
        board = Board();
        board.setStage(Stage.FLOP_BETTING_ROUND);

        cards = [];
        cards.append(board.getDeck().dealCard());
        cards.append(board.getDeck().dealCard());

        for card in board.getPool():
            if(card != None):
                cards.append(card);

        print("Cards:",[cardID.getCardID().name for cardID in cards]);

        print();
        testPairTurnToRiver(cards, board);
        testTwoPairTurnToRiver(cards, board);
        testThreeTurnToRiver(cards, board);
        #testStraightTurnToRiver(cards, board); # @TODO Fix this
        testFlushTurnToRiver(cards, board);
        testFullHouseTurnToRiver(cards, board);
        testFourTurnToRiver(cards, board);
        testFiveTurnToRiver(cards, board);
        print();

        board.setStage(Stage.TURN_BETTING_ROUND);
        cards.append(board.getTurn());
        print("Turn:",[cardID.getCardID().name for cardID in cards]);

        board.setStage(Stage.RIVER_BETTING_ROUND);
        cards.append(board.getRiver());
        print("River:",[cardID.getCardID().name for cardID in cards]);

        print();
        print("Best hand:",HandScanner().checkBestHand(cards).name);
