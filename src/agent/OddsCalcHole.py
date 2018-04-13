'''
@author Thomas Lenz <thomas.lenz96@gmail.com> AS The2b
@date 12 April 2018
@project Texas Hold'em AI
@file OddsCalcHole.py
'''

from HandScanner import HandScanner, HandIDs
import statistics as stat

'''
To save on CPU time, we're going to use a point-based formula instead of exact calculations
Due to the number of cards, we find the error to be an acceptable cost to save the time
The following formula is an implementation of Chen's Formula
'''

def oddsCalcHolePoints(cards, board, numAgents=2):
    scanner = HandScanner();
    ACE_POINTS = 10;
    KING_POINTS = 8;
    QUEEN_POINTS = 7;
    JACK_POINTS = 6;

    points = 0;
    nums = [card.getCardNum() for card in cards];
    # Remove low aces, make them high
    while(nums.count(1) > 0):
        nums.remove(1);
        nums.append(14);
    isPair = False;
    starightPoint = False;
    
    for num in nums:
        if(num > 10):
            if(num == 11):
                points += JACK_POINTS;
            elif(num == 12):
                points += QUEEN_POINTS;
            elif(num == 13):
                points += KING_POINTS;
            elif(num == 14):
                points += ACE_POINTS;

        elif(num <= 10): # If it's not a special card, take half the face value
            points += num/2;

    if(scanner.checkPair(cards) != -1): # If it's a pair, double the points, min 5
        points *= 2;
        if(points == 5): # 5-5 gets a bonus point
            points += 1;

        points = max([points, 5]); # min 5
        isPair = True;

    suits = [card.getCardSuit() for card in cards];
    if(suits.count(suits[0]) > 1): # Add two points if they're suited
        points += 2;
    
    diff = abs(nums[0] - nums[1]);
    diffPoints = [0, 0, 1, 2, 4, 5]; # Pair, connected, 1 missing between the cards, 2 missing, 3 missing, 4+ missing

    if((diff == 1 or diff == 2) and max(nums) < 12): # Connected, max less than queen. Can make all higher straights
        points += 1;

    points -= diffPoints[min(diff, 5)];

    return points;

def oddsCalcHole(cards, board, numAgents=2):
    fullPoints = [];
    for card1 in [card for card in board.getDeck().getCards() if card not in cards]:
        for card2 in [card for card in board.getDeck().getCards() if card not in cards and card.getCardID().value >= card1.getCardID().value and card != card1]:
            fullPoints.append(oddsCalcHolePoints([card1, card2], board, numAgents));

    ourPoints = oddsCalcHolePoints(cards, board, numAgents);
    fullPoints.append(ourPoints);

    handsWeBeat = len([points for points in fullPoints if points < ourPoints]);
    handsWeTie = len([points for points in fullPoints if points == ourPoints]);
    handsWeLoseTo = len([points for points in fullPoints if points > ourPoints]);

    totalHands = len(fullPoints);
    return [handsWeBeat/totalHands, handsWeLoseTo/totalHands, handsWeTie/totalHands];
