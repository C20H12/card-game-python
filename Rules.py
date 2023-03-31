from Card import Card
from Player import Player
from typing import List


class Rules():
  '''list of constants, color maps to rule'''
  
  RED = "Heighest card"
  ORANGE = "Most cards with the same number"
  YELLOW = "Most cards with the same color"
  GREEN = "Most number of even numbered cards"
  BLUE = "Most cards with different colors"
  INDIGO = "Longest sequence of cards"
  VIOLET = "Most number of cards with number < 4"

  @staticmethod
  def _getWinningPlayerIndexFromCardsList(filteredCards: List[List[Card]]) -> int:
    '''finds the player that is ultimately winning from their cards that fits the rule
      filteredCards Card[][] - a 2d array of players of cards they can use for this round'''
    # initialize the winning player to the first one on the list
    winningPlayerIdx = 0
    winningLen = len(filteredCards[0])
    for i in range(1, len(filteredCards)):
      length = len(filteredCards[i])
      # if the player has no cards for this rule, skip
      if length == 0:
        continue
      # if this player has more cards that fits the rule, they are winning
      if length > winningLen:
        winningPlayerIdx = i
        winningLen = length
      # if the lenth are the same, compare the highest card in the selection of cards
      elif length == winningLen:
        highestCard = max(filteredCards[i], key=Card.compareKey)
        winningPlayerHighestCard = max(filteredCards[winningPlayerIdx], key=Card.compareKey)
        if highestCard.compare(winningPlayerHighestCard) == 1:
          winningPlayerIdx = i
    return winningPlayerIdx

  @staticmethod
  def getWinningPlayer(currentRule: str, *players: Player) -> Player:
    # red is special, just get the highest card from all players in a list, then
    # get the highest in that list of highests, then get the the player with that highest card
    if currentRule == Rules.RED:
      allPlayerHighests = [max(player.palette.cards, key=Card.compareKey) for player in players]
      bestHeighest = max(allPlayerHighests, key=Card.compareKey)
      return players[allPlayerHighests.index(bestHeighest)]

    # the other rules requires iterating through the players
    cardsFitsTheRule = []
    for player in players:
      if currentRule == Rules.ORANGE:
        # track the times each *number* appears
        occurences = {}
        for card in player.palette.cards:
          if card.value in occurences:
            occurences[card.value] += 1
          else:
            occurences[card.value] = 1
        # find the most frequent appearance, then get all of the cards that appears this many
        # times. Then find the highest *numbered* card, then stores the cards with the same 
        # number for later processing. Ensures it will always get the highest.
        mostFrequentVal = max(occurences.values())
        mostFrequentKeys = [k for k, v in occurences.items() if v == mostFrequentVal]
        heighestMostFrequentCardValue = max(mostFrequentKeys)
        cardsFitsTheRule.append(
          [card for card in player.palette.cards if card.value == heighestMostFrequentCardValue]
        )
        
      if currentRule == Rules.YELLOW:
        # track the times each *color* appears
        occurences = {}
        for card in player.palette.cards:
          if card.color.value in occurences:
            occurences[card.color.value] += 1
          else:
            occurences[card.color.value] = 1
        # find the most frequent appearence, finding the highest *colored* card within
        # the most frequent ones
        mostFrequentVal = max(occurences.values())
        mostFrequentKeys = [k for k, v in occurences.items() if v == mostFrequentVal]
        # if all the colors occured exactly once, there is no repeats, just get the max
        if len(mostFrequentKeys) == len(player.palette.cards):
          cardsFitsTheRule.append([max(player.palette.cards, key=Card.compareKey)])
        else:
          heighestMostFrequentCardValue = max(mostFrequentKeys)
          cardsFitsTheRule.append(
            [card for card in player.palette.cards if card.color.value == heighestMostFrequentCardValue]
          )
        
      if currentRule == Rules.GREEN:
        # finds all the even numbered cards, store them for later processing
        cardsFitsTheRule.append([
          card for card in player.palette.cards if card.value % 2 == 0
        ])

      if currentRule == Rules.BLUE:
        # finds the cards with different colors
        uniqCards = {}
        for card in player.palette.cards:
          if card.color not in uniqCards:
            uniqCards[card.color] = card
          else:
            # if there is a color that is the same as a prev card
            # compare to see which one is larger, if larger replace the prev card
            if card.compare(uniqCards[card.color]) == 1:
              uniqCards[card.color] = card
        cardsFitsTheRule.append(list(uniqCards.values()))
        
      if currentRule == Rules.INDIGO:
        # first, find all the largest colored card for each number, then sort them
        # each number would only appear once
        uniqCards = {}
        for card in player.palette.cards:
          if card.value not in uniqCards:
            uniqCards[card.value] = card
          else:
            if card.compare(uniqCards[card.value]) == 1:
              uniqCards[card.value] = card
        uniqueNumberCardsList = sorted(list(uniqCards.values()), key=Card.compareKey)
        # initialize the run, iterate through the sorted cards
        run = [uniqueNumberCardsList[0]]
        runSegment = [uniqueNumberCardsList[0]]
        for i in range(1, len(uniqueNumberCardsList)):
          # if this card is exactly 1 larger than the prev card, we have a run
          if uniqueNumberCardsList[i].value == uniqueNumberCardsList[i - 1].value + 1:
            runSegment.append(uniqueNumberCardsList[i])
          # if the run is broken, reset the segment
          else:
            runSegment = []
          # run is set the the max of run and runSegment
          if len(runSegment) > len(run):
            run = runSegment
        # if run is 1, ie, there is not a run that exists, use the highest overall card
        if len(run) == 1:
          cardsFitsTheRule.append([max(uniqueNumberCardsList, key=Card.compareKey)])
        else:
          cardsFitsTheRule.append(run)
      
      if currentRule == Rules.VIOLET:
        # finds all cards below 4
        cardsFitsTheRule.append([
          card for card in player.palette.cards if card.value < 4
        ])

    if all(len(l) == 0 for l  in cardsFitsTheRule):
      # for GREEN and VIOLET, there is the possibility that no one has the
      # cards that fit the rule, no one wins in this case
      return None
    
    return players[Rules._getWinningPlayerIndexFromCardsList(cardsFitsTheRule)]
  
  @staticmethod
  def get(rule):
    # Return the rule corresponding to the rule color.
    return Rules.__dict__[rule]

  @staticmethod
  def help():
    # prints the help message for the rules
    print(
      '''
      The rules associated with each color:
      | Color  | Rule                                 | Example        
      | RED    | Heighest card                        | B 2 > R 1 
      | ORANGE | Most cards with the same number      | V2 B2 R2 > O6 R7
      | YELLOW | Most cards with the same color       |
      |        | compare the numbers if same          | Y2 Y6 > G1 G4
      | GREEN  | Most number of even numbered cards   | Y4 Y2 Y6 > B2
      | BLUE   | Most cards with different colors     | O7 Y5 G4 > B4 V3 I2
      | INDIGO | Largest sequence of cards            | R5 O6 G7 > O3 Y4 B5
      | VIOLET | Most number of cards with number < 4 | G1 Y2 O3 > Y1 V 1
      '''.replace('\n      ', '\n')
    )


