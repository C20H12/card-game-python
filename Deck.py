from random import randint
from Card import Card
from Colors import Colors
from Hand import Hand

class Deck:
  '''represents a deck, contains all the cards the game is going to use'''
  def __init__(self):
    '''builds the deck of 49 cards, using a nested list comp'''
    cardList = [Card(color, num) \
                for num in range(1, 8) \
                for color in iter(Colors)]
    shuffled = self.shuffleDeck(cardList)
    self._cards = shuffled

  def deal(self, size: int):
    '''give out a size number of cards then remove that section from this Deck
       returns a Hand'''
    hand = self._cards[:size]
    del self._cards[:size]
    return Hand(hand)

  def shuffleDeck(self, deck=None):
    '''
    Shuffles the deck of cards to a random order
    - uses the Fisher-Yates shuffle algorithm
    - loops through the list, swaps a random index from i to the end
      with the current index
    - returns the shuffled list
    '''
    deck = deck or self._cards
    if len(deck) == 0:
      return deck
    length = len(deck)
    for i in range(length - 2):
      randomIdx = randint(i, length - 1)
      deck[i], deck[randomIdx] = deck[randomIdx], deck[i]
    return deck

