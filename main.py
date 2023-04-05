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
    humanPlayer = Player(playerName, False, mainDeck)
    
    botsNumber = getNumber(int, "Enter the number of opponents (from 1 - 3):", range=(1, 3))
    botPlayers = [Player(f"bot {i}", True, mainDeck) for i in range(1, botsNumber + 1)]
    
    allPlayers = sorted([humanPlayer, *botPlayers], 
                        key=lambda plr: plr.palette.cards[-1].value)
    
    for i in range(len(allPlayers)):
      allPlayers[i].setOpponents(allPlayers[:i] + allPlayers[i+1:])

    # use a mutable dict so that it is passed by reference
    canvas = {'rule': Rules.RED}

    print("====== Game Start ======\n")
    turnCount = 0
    while True:
      # print(allPlayers)
      print(f"====== Turn {turnCount} ======")
      print(f"### Current turn rule is: {canvas['rule']}\n")
      turnCount += 1

      for player in allPlayers:
        status = player.onTurn(canvas)
        if status == "quit":
          allPlayers.remove(player)
        print()
      print(f"====== End Turn {turnCount} ======\n")

      result, winningPlayer, winningCards = Rules.getWinningPlayer(canvas['rule'], allPlayers)
      # print(result, winningPlayer, winningCards)

      if result == "failed": 
        # realisticly shouldn't happen since the turn options are enforced to 
        # only allow selection of winnable cards
        print(
          "===== Everyone lost due to not having any cards that matches this rule. ====="
        )
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
      
      mainDeck.extendDeck(Deck(winningCards))
      # print(mainDeck)

  @staticmethod
  def onGameOver(players: List[Player]):
    print("====== Game Over ======\n")
    sortedPlayers = sorted(players, key=lambda p: p.points, reverse=True)
    positionalWords = ['first', 'second', 'thrid', 'forth']
    for i in range(len(sortedPlayers)):
      print(f"The {positionalWords[i-1]} place is: {sortedPlayers[i].name}")
      print(f'   Player hand: {sortedPlayers[i].hand}')
      print(f"   Player palette: {sortedPlayers[i].palette}")
      print(f'   Player points: {sortedPlayers[i].points}')
      print()

  @staticmethod
  def public_static_void_main_string_args():
    # this is a java joke
    # this whole thing is a java joke
    
    # starts a while loop that will repeat until the player says no
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




if __name__ == "__main__":
  Main.public_static_void_main_string_args()

