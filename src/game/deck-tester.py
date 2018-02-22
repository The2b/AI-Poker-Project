import deck
import copy

ourDeck = deck.Deck(None,None);

cardsDelt = copy.deepcopy(ourDeck.dealCards(10, None));

for card in cardsDelt:
    print(str(card));
