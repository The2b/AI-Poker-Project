import Deck
import copy

ourDeck = Deck.Deck(None,None);

CardsDelt = copy.deepcopy(ourDeck.dealCards(10, None));

for Card in CardsDelt:
    print(str(Card));
