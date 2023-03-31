from Card import Card
from typing import List


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

  def popCard(self, index=-1):
    '''remove the card at the index and returns it'''
    return self.cards.pop(index)

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