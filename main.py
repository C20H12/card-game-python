from Player import Player
from Deck import Deck
from Rules import Rules
from inputHelp import getNumber, getString

class Main:
  @staticmethod
  def game():
    print("Welcome to card game, red 7")
  
    mainDeck = Deck()
    
    playerName = getString("Enter your name: ")
    humanPlayer = Player(playerName, False, mainDeck)
    
    botsNumber = getNumber(int, "Enter the number of opponents (from 1 - 3):", range=(1, 3))
    botPlayers = [Player(f"bot {i}", True, mainDeck) for i in range(1, botsNumber + 1)]
    
    allPlayers = sorted([humanPlayer, *botPlayers], 
                        key=lambda plr: plr.palette.cards[-1].value)
    canvas = {'rule': Rules.RED}
    print(allPlayers)
    for i in range(len(allPlayers)):
      allPlayers[i].onTurn(canvas, allPlayers[:i] + allPlayers[i+1:])
      
  @staticmethod
  def public_static_void_main_string_args():
    # this is a java joke
    Main.game()
    



if __name__ == "__main__":
  Main.public_static_void_main_string_args()

