from Deck import Deck
from Board import Board, Stage
from Card import Suits
import Card
from HandScanner import HandScanner
import RiverOddsCalc as RiverOddsCalc

def calcOdds(board, hand):
    board.setStage(Stage.TURN_BETTING_ROUND);
    cards = [];
    for card in hand:
        cards.append(card);

    for card in board.getFlop():
        cards.append(card);

    cards.append(board.getTurn());

    scanner = HandScanner();

    hasPair = False;
    hasTwoPair = False;
    hasThree = False;
    hasStraight = False;
    hasFlush = False;
    hasFullHouse = False;
    hasFour = False;
    hasStraightFlush = False;
    hasFive = False;

    print([card.getCardID().name for card in cards]);

    if(scanner.checkPair(cards)):
        print("Has a pair");
        hasPair = True;
    if(scanner.checkTwoPair(cards)):
        print("Has two pairs");
        hasTwoPair = True;
    if(scanner.checkThreeOfAKind(cards)):
        print("Has a three of a kind");
        hasThree = True;
    if(scanner.checkStraight(cards)): # Don't have a function for this
        print("Has a straight");
        hasStraight = True;
    if(scanner.checkFlush(cards)):
        print("Has a flush");
        hasFlush = True;
    if(scanner.checkFullHouse(cards)):
        print("Has a full house");
        hasFullHouse = True;
    if(scanner.checkFourOfAKind(cards)):
        print("Has a four of a kind");
        hasFour = True;
    if(scanner.checkStraightFlush(cards)): # Don't have a function for this
        print("Has a straight flush");
        hasStraightFlush = True;
    if(scanner.checkFiveOfAKind(cards)):
        print("Has a five of a kind");
        hasFive = True;

    # Not efficient, but it's just testing
    if(not hasPair): # Can be gotten at any point
        print("Odds of a pair:",(RiverOddsCalc.pairRiverOdds(cards, board) * 100));

    if(not hasTwoPair):
        if(not hasPair):
            print("Odds of two pairs:",0);
        else:
            print("Odds of two pairs:",(RiverOddsCalc.twoPairRiverOdds(cards, board) * 100));

    if(not hasThree):
        if(not hasPair):
            print("Odds of a three of a kind:",0);
        else:
            print("Odds of a three of a kind:",(RiverOddsCalc.threeRiverOdds(cards, board) * 100));

    if(not hasStraight): # Conditionals are built-in
        print("Odds of a straight:",RiverOddsCalc.straightRiverOdds(cards, board) * 100);

    if(not hasFlush):
        suits = [card.getCardSuit() for card in cards];
        suitsCount = [suits.count(suit) for suit in Suits];

        if(max(suitsCount) < 4):
            print("Odds of a flush:",0);
        elif(max(suitsCount) >= 5):
            print("Odds of a flush:",100);
        elif(max(suitsCount) == 4):
            print("Odds of a flush:",(RiverOddsCalc.flushRiverOdds(cards, board) * 100));
        else:
            print("Flush checker is brkoen");

    if(not hasFullHouse): # This one has built in checks. There's no way around it
        print("Odds of a full house:",(RiverOddsCalc.fullHouseRiverOdds(cards, board) * 100));

    if(not hasFour):
        if(not hasThree):
            print("Odds of a four of a kind:",0);
        else:
            print("Odds of a four of a kind:",(RiverOddsCalc.fourRiverOdds(cards, board) * 100));

    if(not hasStraightFlush):
        print("Odds of a straight flush:",(RiverOddsCalc.straightFlushRiverOdds(cards, board) * 100));

    if(not hasFive):
        if(not hasFour):
            print("Odds of a five of a kind:",0);
        else:
            print("Odds of a five of a kind:",(RiverOddsCalc.fiveRiverOdds(cards, board) * 100));

if __name__ == '__main__':
    print("Starting...");
    board = Board();
    hand = board.getDeck().dealCards(2);

    calcOdds(board, hand);

    board.setStage(Stage.RIVER_BETTING_ROUND);
    cards = [];
    for card in hand:
        cards.append(card);

    for card in board.getPool():
        cards.append(card);

    print([card.getCardID().name for card in cards]);
    print("Actual result:",HandScanner().checkBestHand(cards));
