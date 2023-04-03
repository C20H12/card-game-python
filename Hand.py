from Card import Card
from typing import List, Union


class Hand:
  '''represents a hand, a collection of cards'''
  def __init__(self, cards: List[Card]):
    self.cards = cards
    
  def printHand(self, pretty=False):
    '''Prints the deck of cards, each card on a new line
       uses the colored representation if pretty is true'''
    if not self.cards:
      print("Deck is empty.")
      return
    for card in self.cards:
      if pretty:
        card.printCardPretty()
      else:
        card.printCardStr()
    print()

  def addCard(self, *cards):
    '''append cards to deck'''
    self.cards += cards
  
  def extendHand(self, hand: 'Hand'):
    self.cards += hand.cards

  def popCard(self, index: Union[int, Card] = -1):
    '''remove the card at the index and returns it
       or alternatively, find the exact card and pop it
       raises ValueError if card is not found
    '''
    if type(index) is int:
      return self.cards.pop(index)
    else:
      return self.cards.pop(self.cards.index(index))

  def sortHand(self):
    '''sort the deck in ascending order'''
    self.cards.sort(key=Card.compareKey)
    return self

  def clearHand(self):
    '''clear the cards'''
    self.cards = []

  def __repr__(self):
    '''string representation of this hand,
       displays the cards in an array like structure separateed by 2 spaces
       [card1  card2  ]'''
    return str(self.cards).replace(",", "  ")

  def __len__(self):
    '''returns the number of cards in this hand'''
    return len(self.cards)
  
  def __iter__(self):
    '''iterate over the cards in this hand'''
    for card in self.cards:
      yield card
  
  def __contains__(self, card):
    '''check if the card is in this hand'''
    return card in self.cards