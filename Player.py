from Card import Card
from Hand import Hand
from inputHelp import getNumber
from random import randint, choices as randomChoices
from re import match as regexMatch
from Rules import Rules
from typing import List


class Player:
  '''represents a player, tracks its hand, palette and points
     contains functions to act in a turn'''
  def __init__(self, name: str, isBot: bool):
    self.name = name
    self.isBot = isBot
    self.points = 0
  
  '''
  these methods set up the player
  design pattern: creational - builder
    allows for a more readable flexible way to create a player
  they also allow chaining
  '''
  def setHand(self, hand: Hand):
    self.hand = hand
    return self
  
  def setPalette(self, hand: Hand):
    self.palette = hand
    return self
  
  def setOpponents(self, otherPlayers: List['Player']):
    self._opponents = otherPlayers
    return self
  
  def setCanvas(self, canvas):
    self.canvas = canvas
    return self

  def _getWinnableCards(self):
    '''
    looks for cards which when changed to the card's rule, 
    will make the player win
    caches the colors in a set to avoid duplicate computation
    returns a Hand object
    '''
    winnableCards = Hand([])
    computedColors = set()
    for card in self.hand:
      if card.color in computedColors:
        continue
      computedColors.add(card.color)
      status, winPlayer, _ = Rules.getWinningPlayer(
        Rules.get(card.color.name), [self, *self._opponents]
      )
      if status == "failed":
        continue
      if winPlayer == self:
        winnableCards.addCard(card)
    return winnableCards

  def _chooseCardIndexFromHand(self, fromCards=None):
    '''
    helper function to get a card index from the player's hand
    -allows the player to choose a card from their own hand or 
      from a given hand
    -prints the hand to the console, then
      the player can choose a card by entering the card's name
    -rejects inputs that is not in the format specified, and
      rejects inputs that is a card that is not in the given hand
    returns the index of the card chosen in the hand
    '''
    fromCards = fromCards or self.hand
    if self.isBot:
      return randint(0, len(fromCards) - 1)
    fromCards.printHand(pretty=True)
    print("Choose a card, enter a the card name in the format of COLOR <num>:")
    while True:
      while not regexMatch(
        "^(RED|ORANGE|YELLOW|GREEN|BLUE|INDIGO|VIOLET) [1-7]$",
        cardName := input("Enter a card to select: ").upper(),
      ):
        print("Input does not match pattern!")
      
      cardsStrArr = [card.toString() for card in fromCards]
      if cardName in cardsStrArr:
        index = cardsStrArr.index(cardName)
        break
      else:
        print("You don't have this card")
    return index
  
  def _humanPlayerOptions(self):
    '''
    prints the human's options, then allows the player to choose a turn option
    or an option to check the game state (cards, palettes, rules)
    returns the turn choice made
    '''
    print(f"{self.name}, here are your available actions:")
    print("------")
    while True:
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
            for player in self._opponents:
              print()
              print(f"{player.name}'s palettes:")
              player.palette.printHand(pretty=True)
          elif choice == 4:
            Rules.help()
          elif choice == 5:
            break
  
  def _playToPalette(self):
    '''
    helper function to play a card to the player's palette
    -allows the player to choose a card from their own hand
      then removes the card from the hand and adds it to the palette
    '''
    index = self._chooseCardIndexFromHand()
    cardToPlay = self.hand.popCard(index)
    self.palette.addCard(cardToPlay)
    print(f"{self.name} played a card to palette")
  
  def _playToCanvas(self):
    '''
    helper function to play a card to the canvas
    -allows the player to choose a card from their own hand
      then removes the card from the hand and adds it to the canvas
    aborts if the player has no winnable cards
    returns if the process was aborted
    '''
    winnableCards = self._getWinnableCards()
    if len(winnableCards) == 0: 
      print("You cannot choose this option as none of your cards will make you win the new rule!")
      print("You can only play to your palette.")
      self._playToPalette()
      return True
    index = self._chooseCardIndexFromHand(winnableCards)
    cardToPlay = self.hand.popCard(winnableCards.cards[index])
    self.canvas['rule'] = Rules.get(cardToPlay.color.name)
    print(f"{self.name} played a card to the canvas")
    print(f"### Rules Changed to: f{self.canvas['rule']}")
    return False

  def onTurn(self):
    choice = 0
    if self.isBot:
      winnableCards = self._getWinnableCards()
      if len(winnableCards) == 0:
        choice = 1
      else:
        choice = randomChoices(population=[1, 2, 3, 4], weights=[0.74, 0.12, 0.12, 0.02])[0]
    else:
      choice = self._humanPlayerOptions()
     
    if choice == 1:
      self._playToPalette()
    elif choice == 2:
      self._playToCanvas()
    elif choice == 3:
      aborted = self._playToCanvas()
      if not aborted:
        self._playToPalette()
    elif choice == 4:
      print(f"{self.name} chose to lose")
      self.onTurnLose()
      return "quit"
    
    print(f"Turn over for {self.name}")

  def onTurnWin(self, winningCards: List['Card']):
    for card in winningCards:
      self.points += card.value
      self.palette.popCard(card)
    print(f"*** Congrats, {self.name} has won this round!")
    print(f'The winning cards are {winningCards}')
    print(f'Current points: {self.points}')

  def onTurnLose(self):
    print(f"*** Too bad, {self.name} has lost this round!")
    print(f"Current points: {self.points}")

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

  def __repr__(self):
    outStr = '\n'
    for k, v in self.__dict__.items():
      if k == '_opponents':
        outStr += f'  {k}: {str([p.name for p in v])}'
      else:
        outStr += f'  {k}: {v}'
      outStr += '\n'
    return outStr