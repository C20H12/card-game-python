from Card import Card
from Colors import Colors
from Hand import Hand
from random import randint

class Deck:
  '''represents a deck, contains all the cards the game is going to use'''
  def __init__(self, initCards=None):
    '''builds the deck of 49 cards, using a nested list comp'''
    if initCards == None:
      cardList = [Card(color, num) \
                  for num in range(1, 8) \
                  for color in iter(Colors)]
      shuffled = self.shuffleCards(cardList)
      self._cards = shuffled
    else:
      self._cards = self.shuffleCards(initCards[:])

  def deal(self, size: int):
    '''give out a size number of cards then remove that section from this Deck
       returns a Hand'''
    hand = self._cards[:size]
    del self._cards[:size]
    return Hand(hand)

  def shuffleCards(self, cards):
    '''
    Shuffles the deck of cards to a random order
    - uses the Fisher-Yates shuffle algorithm
    - loops through the list, swaps a random index from i to the end
      with the current index
    - returns the shuffled list
    '''
    if len(cards) == 0:
      return cards
    length = len(cards)
    for i in range(length - 2):
      randomIdx = randint(i, length - 1)
      cards[i], cards[randomIdx] = cards[randomIdx], cards[i]
    return cards

  def extendDeck(self, otherDeck: 'Deck'):
    self._cards += otherDeck._cards
  
  def __repr__(self):
    return str(self._cards)