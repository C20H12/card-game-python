from Card import Card
from Hand import Hand
from inputHelp import getNumber
from random import randint, choices as randomChoices
from re import match as regexMatch
from Rules import Rules
from typing import List


class Player:
  '''
  represents a player, tracks its hand, palette and points
    contains functions to act in a turn
  '''
  def __init__(self, name: str, isBot: bool):
    self.name = name
    self.isBot = isBot
    self.points = 0
  
  '''
  these chaining methods set up the player
  design pattern: creational - builder
    allows for a more readable and flexible way to create a player
  relationship: Hand - composition
    player owns a hand, the hand cannot exist without the player
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

  '''
  private helper functions
  '''
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
    print(
      "Choose a card, enter a the card name in the format of <color's first letter><number>:"
    )
    while True:
      while not regexMatch(
        "^[roygbiv][1-7]$",
        cardName := input("Enter a card to select: "),
      ):
        print("Input does not match pattern!")
      
      cardsStrArr = [card.toAbbreviatedString() for card in fromCards]
      if cardName in cardsStrArr:
        index = cardsStrArr.index(cardName)
        break
      else:
        print("You don't have this card")
    return index
  
  def _humanPlayerOptions(self):
    '''
    prints the human's options, then allow the player to choose a turn option
    or an option to check the game state (cards, palettes, rules)
    returns the choice (the human player) makes
    '''
    print(f"{self.name}, here are your available actions:")
    print("------")
    while True:
      print("1 - Play a card your Palette.")
      print("2 - Play a card to the Canvas to change the game rule.")
      print("3 - Play a card to your Canvas AND THEN discard a card to the Palette.")
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
            for opponent in self._opponents:
              print()
              print(f"{opponent.name}'s palettes:")
              opponent.palette.printHand(pretty=True)
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
      and falls back to playing to the palette
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
    print(f"### Rules Changed to: {self.canvas['rule']}")
    return False

  '''
  public event handlers
  design pattern: behavioral - observer
    a one-to-many dependency relationship (game to players), 
    the player will change state when game notifies it to  
  '''
  def onTurn(self):
    '''
    on the player's turn the player can choose a action to perform
    '''
    choice = 0
    if self.isBot:
      # if it a bot, check if it has winnable cards
      # ie. can choose option 2 or 3
      winnableCards = self._getWinnableCards()
      if len(winnableCards) == 0: # can't
        choice = 1
      else: # can, choose a random one
        # the weights affect the probability of choosing each option
        # so it doesn't always choose to lose
        choice = randomChoices(population=[1, 2, 3, 4], weights=[0.74, 0.12, 0.12, 0.02])[0]
    else:
      # display menu text and get a choice from input
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
      print(f"{self.name} chose to do nothing.")
    
    print(f"Turn over for {self.name}")
    print()

  def onTurnWin(self, winningCards: List['Card']):
    '''
    display a message for winning a round
    on a win, the player's points increase by the value 
      of the numbers on the cards they win with
    prints out the winning cards and points
    '''
    for card in winningCards:
      self.points += card.value
      self.palette.popCard(card)
    print(f"*** Congrats, {self.name} has won this round!")
    print(f'The winning cards are {winningCards}')
    print(f'Current points: {self.points}')

  def onTurnLose(self):
    '''
    display a message for losing a round
    prints out the points
    '''
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
    '''
    string represtation of the player
    the opponents list is shrinked to a non verbose list
    '''
    outStr = '\n'
    for k, v in self.__dict__.items():
      if k == '_opponents':
        outStr += f'  {k}: {str([p.name for p in v])}'
      else:
        outStr += f'  {k}: {v}'
      outStr += '\n'
    return outStr