from Player import Player
from Deck import Deck
from Rules import Rules
from inputHelp import getNumber, getString

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
    print(allPlayers)

    while True:
      print(allPlayers)

      for player in allPlayers:
        player.onTurn(canvas)

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
        if player.isWinning(botsNumber + 1):
          return player
        
        playerCurrentCardAmount = len(player.hand)
        if playerCurrentCardAmount == 7: 
          continue
        player.hand.extendHand(mainDeck.deal(7 - playerCurrentCardAmount))


  @staticmethod
  def public_static_void_main_string_args():
    # this is a java joke
    # this whole thing is a java joke
    print("Welcome to card game, red 7")

    ultimateWinner = Main.game()
    print(ultimateWinner)
    



if __name__ == "__main__":
  Main.public_static_void_main_string_args()

