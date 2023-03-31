from Deck import Deck
from Rules import Rules
from Player import Player
from typing import List
from random import randint, choices as randomChoices
from inputHelp import getNumber, getStringRegex


class Player:
  '''represents a player, tracks its hand, palette and points
     contains functions to act in a turn'''
  def __init__(self, name: str, isBot: bool, deck: Deck) -> None:
    self.name = name
    self.isBot = isBot
    self.hand = deck.deal(7).sortHand()
    self.palette = deck.deal(1)
    self.points = 0

  def chooseCardIndex(self):
    if self.isBot:
      return randint(0, len(self.hand.cards))
    self.hand.printHand(pretty=True)
    print("Choose a card, enter a the card name in the format of COLOR <num>:")
    while True:
      cardName = getStringRegex(
        "Enter a card name: ", "^(RED|ORANGE|YELLOW|GREEN|BLUE|INDIGO|VIOLET) [1-7]$"
      )
      cardsStrArr = [card.toString() for card in self.hand.cards]
      if cardName in cardsStrArr:
        index = cardsStrArr.index(cardName)
        break
      else:
        print("You don't have this card")
    return index    

  def _processChoices(self, choice, canvas):
    match choice:
      case 1:
        print(f"{self.name} played a card to palette")
        cardToPlay = self.hand.popCard(self.chooseCardIndex())
        self.palette.addCard(cardToPlay)
      case 2:
        print(f"{self.name} played a card to the canvas")
        cardToPlay = self.hand.popCard(self.chooseCardIndex())
        canvas['rule'] = Rules.get(cardToPlay.color.name)
      case 3:
        print(f"{self.name} played a card played a card to palette and canvas")
        cardToPlay = self.hand.popCard(self.chooseCardIndex())
        self.palette.addCard(cardToPlay)
        canvas['rule'] = Rules.get(cardToPlay.color.name)
      case 4:
        print(f"{self.name} chose to lose")
        self.onLose()
  
  def _humanPlayerOptions(self, otherPlayers: List[Player], canvas):
    print(f"{self.name}, here are your available actions:")
    while True:
      print(f"Current turn rule is: {canvas['rule']}")
      print("1 - Play a card your Palette.")
      print("2 - Play a card to the Canvas to change the game rule.")
      print("3 - Play a card to your Palette AND THEN discard a card to the Canvas.")
      print("4 - Do nothing, and lose.")
      print("5 - Check ...")
      choice = getNumber(int, "Enter an action to select: ", range=(1, 5))
      
      if choice in (1, 2, 3, 4):
        self._processChoices(choice, canvas)
        break
      elif choice == 5:
        while True:
          print("1 - Check your cards.")
          print("2 - Check your palette..")
          print("3 - Check opponents' palettes.")
          print("4 - Check the rules associated with each color..")
          print("5 - Back.")
          choice = getNumber(int, "Enter an action to select: ", range=(1, 5))
          match choice:
            case 1:
              print("Your cards:")
              self.hand.printHand(pretty=True)
            case 2:
              print("Your palette:")
              self.palette.printHand(pretty=True)
            case 3:
              for player in otherPlayers:
                print()
                print(f"{player.name}'s palettes:")
                player.palette.printHand(pretty=True)
            case 4:
              Rules.help()
            case 5:
              break

  def onTurn(self, canvas, otherPlayers: List[Player]):
    choice = 0
    if self.isBot:
      choice = randomChoices(population=[1, 2, 3, 4], weights=[0.74, 0.12, 0.12, 0.02])[0]
      self._processChoices(choice, canvas)
    else:
      self._humanPlayerOptions(otherPlayers, canvas)
    print(f"Turn over for {self.name}")

  def onWin(self):
    print(f"Congrats, {self.name}, you have won!")

  def onLose(self):
    print(f"Too bad, {self.name}, you lost!")

  def __repr__(self):
    return '\n'.join(str(self.__dict__).split(',')) + '\n'
