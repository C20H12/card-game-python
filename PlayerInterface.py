from typing import List
from Hand import Hand


class PlayerInterface:
  '''a simple representation of player, kind of like an interface in java
     also needed to get around the cyclic import error when annotating the Rules functions
     (Rules imports Player & Player imports Rules)
     also, maximum java immersive-ness ykyk'''
  name: str # public 
  isBot: bool # public
  hand: Hand # public
  palette: Hand # public
  points: int # public
  _opponents: List['PlayerInterface'] # private
  def onTurn(self, canvas: dict, otherPlayers: List['PlayerInterface']):
    pass