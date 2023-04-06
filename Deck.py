from Card import Card
from Colors import Colors
from Hand import Hand
from random import randint

class Deck:
  '''represents a deck, contains all the cards the game is going to use
     - design pattern: creational - singleton
       only a single instance would be created for each game
       and all players access one main deck
       this is done because in an actual card game, you would only have one 
       deck from which player draws from
  '''
  def __init__(self):
    '''builds the deck of 49 cards, using a nested list comprehension'''
    cardList = [Card(color, num) \
                for num in range(1, 8) \
                for color in iter(Colors)]
    shuffled = self.shuffleCards(cardList)
    self._cards = shuffled

  def deal(self, size: int):
    '''give out a size number of cards then remove that section from this Deck
       - returns a Hand
       - design pattern: creational - factory method'''
    hand = self._cards[:size]
    del self._cards[:size]
    return Hand(hand)

  def shuffleCards(self, cards):
    '''
    Shuffles the deck of cards to a random order
    uses the Fisher-Yates shuffle algorithm
    loops through the list, swaps a random index from i to the end
      with the current index
    cards is a list of Card
    returns the shuffled list
    '''
    if len(cards) == 0:
      return cards
    length = len(cards)
    for i in range(length - 2):
      randomIdx = randint(i, length - 1)
      cards[i], cards[randomIdx] = cards[randomIdx], cards[i]
    return cards

  def extendDeck(self, cards):
    '''
    add cards to this deck
    cards is a list of Card
    '''
    self._cards += cards
  
  def __repr__(self):
    '''string representation, hooks the repr of cards'''
    return str(self._cards)