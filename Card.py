from Colors import Colors
from functools import cmp_to_key


class Card:
  '''represents a card, each has a color and a number'''
  def __init__(self, color: Colors, value: int):
    self.color = color
    self.value = value
  
  def compare(self, other: 'Card') -> int:
    '''compare 2 cards, if their values are the same them compare colors
       returns 1 if this is larger than other, -1 if this is smaller
    '''
    if self.value == other.value:
      return 1 if self.color.value > other.color.value else -1
    else:
      return 1 if self.value > other.value else -1

  # converting the compare function to a key function (returns a bool)
  # so that it can be used in built in interable functions
  compareKey = cmp_to_key(compare)
  
  def printCardPretty(self):
    '''pretty print the card with the color and formatting
       pads the color name with spaces so that it is in the center
    '''
    colorName = self.color.name
    nameLen = len(colorName)
    WIDTH = 10
    spacesPadBefore = (WIDTH - nameLen) // 2
    spacesPadAfter = WIDTH - nameLen - spacesPadBefore
    Colors.printColored(self.color, "┏━━━━━━━━━━┓")
    Colors.printColored(self.color, f"┃{' ' * spacesPadBefore}{self.color.name}{' ' * spacesPadAfter}┃")
    Colors.printColored(self.color, f"┃    {self.value}     ┃")
    Colors.printColored(self.color, "┃          ┃")
    Colors.printColored(self.color, "┗━━━━━━━━━━┛")

  def printCardStr(self):
    '''print card as a string'''
    print(f"{self.color.name} {self.value}")

  def toString(self):
    '''return a string representation of the card'''
    return f"{self.color.name} {self.value}"
  
  def valueOf(self):
    return self.value * 10 + self.color.value

  def __repr__(self):
    '''string representation of the class
       useful for debug printing'''
    return self.toString()
