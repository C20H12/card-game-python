from Deck import Deck
from Hand import Hand
from Rules import Rules
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
  
  def setOpponents(self, otherPlayers: List['Player']):
    self.opponents = otherPlayers

  def _getWinnableCards(self):
    winnableCards = Hand([])
    computedColors = set()
    for card in self.hand:
      if card.color in computedColors:
        continue
      computedColors.add(card.color)
      status, winPlayer, _ = Rules.getWinningPlayer(
        Rules.get(card.color.name), [self, *self.opponents]
      )
      if status == "failed":
        continue
      print(winPlayer, _)
      if winPlayer == self:
        winnableCards.addCard(card)
    return winnableCards

  def _chooseCardIndex(self, fromCards=None):
    fromCards = fromCards or self.hand
    if self.isBot:
      return randint(0, len(fromCards) - 1)
    fromCards.printHand(pretty=True)
    print("Choose a card, enter a the card name in the format of COLOR <num>:")
    while True:
      cardName = getStringRegex(
        "Enter a card name: ", "^(RED|ORANGE|YELLOW|GREEN|BLUE|INDIGO|VIOLET) [1-7]$"
      )
      cardsStrArr = [card.toString() for card in fromCards]
      if cardName in cardsStrArr:
        index = cardsStrArr.index(cardName)
        break
      else:
        print("You don't have this card")
    return index
  
  def _humanPlayerOptions(self, canvas):
    print(f"{self.name}, here are your available actions:")
    while True:
      print(f"==== Current turn rule is: {canvas['rule']} ==== ")
      print("1 - Play a card your Palette.")
      print("2 - Play a card to the Canvas to change the game rule.")
      print("3 - Play a card to your Palette AND THEN discard a card to the Canvas.")
      print("4 - Do nothing, and lose.")
      print("5 - Check ...")
      choice = getNumber(int, "Enter an action to select: ", range=(1, 5))

      if choice in (1, 2, 3, 4):
        return choice
      else:
        while True:
          print("1 - Check your cards.")
          print("2 - Check your palette..")
          print("3 - Check opponents' palettes.")
          print("4 - Check the rules associated with each color..")
          print("5 - Back.")
          choice = getNumber(int, "Enter an action to select: ", range=(1, 5))
          if choice == 1:
            print("Your cards:")
            self.hand.printHand(pretty=True)
          elif choice == 2:
            print("Your palette:")
            self.palette.printHand(pretty=True)
          elif choice == 3:
            for player in self.opponents:
              print()
              print(f"{player.name}'s palettes:")
              player.palette.printHand(pretty=True)
          elif choice == 4:
            Rules.help()
          elif choice == 5:
            break
  
  def _playToPalette(self):
    index = self._chooseCardIndex()
    cardToPlay = self.hand.popCard(index)
    self.palette.addCard(cardToPlay)
    print(f"{self.name} played a card to palette")
  
  def _playToCanvas(self, canvas):
    winnableCards = self._getWinnableCards()
    if len(winnableCards) == 0: 
      print("You cannot choose this option as none of your cards will make you win the new rule!")
      print("You can only play to your palette.")
      self._playToPalette()
      return True
    index = self._chooseCardIndex(winnableCards) # todo: test this
    cardToPlay = self.hand.popCard(winnableCards[index])
    canvas['rule'] = Rules.get(cardToPlay.color.name)
    print(f"{self.name} played a card to the canvas")
    return False

  def onTurn(self, canvas):
    choice = 0
    if self.isBot:
      winnableCards = self._getWinnableCards()
      if len(winnableCards) == 0:
        choice = 1
      else:
        choice = randomChoices(population=[1, 2, 3, 4], weights=[0.74, 0.12, 0.12, 0.02])[0]
    else:
      choice = self._humanPlayerOptions(canvas)
     
    if choice == 1:
      self._playToPalette()
    elif choice == 2:
      self._playToCanvas(canvas)
    elif choice == 3:
      aborted = self._playToCanvas(canvas)
      if not aborted:
        self._playToPalette()
    elif choice == 4:
      print(f"{self.name} chose to lose")
      self.onTurnLose()
      return "quit"
    
    print(f"Turn over for {self.name}")
  
  def isWinningGame(self, totalPlayers: int):
    '''
    returns true if the player has enough points to win
    2 players: 40 points
    3 players: 35 points
    4 players: 30 points
    '''
    if totalPlayers == 2:
      return self.points >= 40
    if totalPlayers == 3:
      return self.points >= 35
    if totalPlayers == 4:
      return self.points >= 30

  def onTurnWin(self):
    print(f"Congrats, {self.name}, you have won!")

  def onTurnLose(self):
    print(f"Too bad, {self.name}, you lost!")

  def __repr__(self):
    outStr = '\n'
    for k, v in self.__dict__.items():
      if k == 'opponents':
        outStr += f'  {k}: {str([p.name for p in v])}'
      else:
        outStr += f'  {k}: {v}'
      outStr += '\n'
    return outStr