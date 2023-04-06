from Deck import Deck
from Player import Player
from Rules import Rules
from typing import List
from inputHelp import getNumber, getString, getBool

class Main:
  @staticmethod
  def game():
    mainDeck = Deck()
    
    playerName = getString("Enter your name: ")
    humanPlayer = Player(playerName, isBot=False)
    
    botsNumber = getNumber(int, "Enter the number of opponents (from 1 - 3):", range=(1, 3))
    botPlayers = [Player(f"bot {i}", isBot=True) for i in range(1, botsNumber + 1)]
    
    allPlayers = [humanPlayer, *botPlayers]
    
    # use a mutable dict so that it is passed by reference
    canvas = {'rule': Rules.RED}

    for i in range(len(allPlayers)):
      allPlayers[i] \
        .setHand(mainDeck.deal(7).sortHand()) \
        .setPalette(mainDeck.deal(1)) \
        .setCanvas(canvas) \
        .setOpponents(allPlayers[:i] + allPlayers[i+1:])

    allPlayers = sorted(allPlayers, key=lambda p: p.palette.cards[0].valueOf())

    print("====== Game Start ======\n")
    turnCount = 0
    while True:
      print(f"====== Round {turnCount} ======")
      print(f"### Current rule is: {canvas['rule']}\n")

      for player in allPlayers:
        player.onTurn()
        
      print(f"\n====== End Round {turnCount} ======\n")
      turnCount += 1

      result, winningPlayer, winningCards = Rules.getWinningPlayer(canvas['rule'], allPlayers)
      # print(result, winningPlayer, winningCards)

      if result == "failed": 
        # realisticly shouldn't happen since the turn options are enforced to 
        # only allow selection of winnable cards
        print(
          "===== Everyone lost due to not having any cards that matches this rule. ====="
        )
        Main.onGameOver(allPlayers)
        break
      
      for player in allPlayers:
        if player == winningPlayer:
          player.onTurnWin(winningCards)
        else:
          player.onTurnLose()
        print()
        
        if player.isWinningGame(botsNumber + 1):
          Main.onGameOver(allPlayers)
          return
        
        playerCurrentCardAmount = len(player.hand)
        if playerCurrentCardAmount == 7: 
          continue
        player.hand.extendHand(mainDeck.deal(7 - playerCurrentCardAmount))
      
      mainDeck.extendDeck(winningCards)
      # print(mainDeck)

  @staticmethod
  def onGameOver(players: List[Player]):
    print("===== Game Over =====\n")
    sortedPlayers = sorted(players, key=lambda p: p.points, reverse=True)
    positionalWords = ['first', 'second', 'thrid', 'forth']
    for i in range(len(sortedPlayers)):
      print(f"The {positionalWords[i]} place is: {sortedPlayers[i].name}")
      print(f'   Player hand: {sortedPlayers[i].hand}')
      print(f"   Player palette: {sortedPlayers[i].palette}")
      print(f'   Player points: {sortedPlayers[i].points}')
      print()

  @staticmethod
  def public_static_void_main_string_args():
    # this is a java joke
    # this whole thing is a java joke
    
    # starts a while loop that will repeat until the player says no
    # allows the game to be played as many times as possible
    playAgain = True
    while playAgain:
      print("---------------------------")
      print("Welcome to card game, red 7")
      print("---------------------------\n")
      # calls the main game loop
      Main.game()
      # asks the user if they want to play again
      playAgain = getBool(
        "Would you like to play again? (y/n): ", 
        failedText="Input is not y or n", trueValue="y", falseValue="n"
      )
    print("Goodbye")



if __name__ == "__main__":
  Main.public_static_void_main_string_args()

