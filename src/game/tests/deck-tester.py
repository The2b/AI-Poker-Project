from Deck import Deck
import copy

ourDeck = Deck(None,None);

CardsDelt = copy.deepcopy(ourDeck.dealCards(10));

for Card in CardsDelt:
    print(type(ourDeck));
