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

    while True:
      print(allPlayers)

      for player in allPlayers:
        status = player.onTurn(canvas)
        if status == "quit":
          allPlayers.remove(player)
        
      result, winningPlayer, winningCards = Rules.getWinningPlayer(canvas['rule'], allPlayers)
      print(result, winningPlayer, winningCards)

      if result == "failed": 
        # realisticly shouldn't happen since the turn options are enforced
        print("Everyone lost due to not having any cards that matches this rule.")
        break
        
      for card in winningCards:
        winningPlayer.points += card.value
        winningPlayer.palette.popCard(card)
      
      for player in allPlayers:
        if player == winningPlayer:
          player.onTurnWin()
        else:
          player.onTurnLose()
        
        if player.isWinningGame(botsNumber + 1):
          Main.onGameWin(allPlayers)
          break
        
        playerCurrentCardAmount = len(player.hand)
        if playerCurrentCardAmount == 7: 
          continue
        player.hand.extendHand(mainDeck.deal(7 - playerCurrentCardAmount))

  @staticmethod
  def onGameWin(players: List[Player]):
    sortedPlayers = sorted(players, key=lambda p: p.points, reverse=True)
    print(f'The first place winner is: {sortedPlayers[0].name}')
    print(f'Final points: {sortedPlayers[0].points}')
    print()
    positionalWords = ['second', 'thrid', 'forth']
    for i in range(1, len(sortedPlayers)):
      print(f"The {positionalWords[i-1]} place is: {sortedPlayers[i]} with {sortedPlayers[i].points}")

  @staticmethod
  def public_static_void_main_string_args():
    # this is a java joke
    # this whole thing is a java joke
    
    # starts a while loop that will repeat until the player says no
    playAgain = True
    while playAgain:
      print("Welcome to card game, red 7")
      # calls the main game loop
      Main.game()
      # asks the user if they want to play again
      playAgain = getBool(
        "Would you like to play again? (y/n): ", 
        failedText="Input is not y or n", trueValue="y", falseValue="n"
      )


    



if __name__ == "__main__":
  Main.public_static_void_main_string_args()

