from Deck import Deck
from Player import Player
from Rules import Rules
from Colors import Colors
from Card import Card

def rulesTest(rule, expectedWinPlayerName):
  '''tests all the rules against the test cases'''
  def decorate(func):
    def wrap(players):
      print(f"testing rule: {rule}\n")
      usedCards = func(players)
      for i in range(len(players)):
        player = players[i]
        player.palette.clearHand()
        player.palette.addCard(*usedCards[i])
        player.palette.printHand()
      win = Rules.getWinningPlayer(rule, players)
      try:
        if expectedWinPlayerName is None:
          assert win[0] == "failed"
        else:
          assert win[1].name == expectedWinPlayerName
      except AssertionError:
        print("result: " + win.name, "expected: " + expectedWinPlayerName)
        raise AssertionError()
      print("=====passed=======\n\n")
    return wrap
  return decorate

deck = Deck()
players = [Player("p" + str(i + 1), False, deck) for i in range(3)]



@rulesTest(Rules.RED, "p1")
def test_playerWithLargestCard(players):
  return [[
    Card(Colors.RED, 7),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.VIOLET, 5),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.INDIGO, 7),
  ]]

test_playerWithLargestCard(players)

@rulesTest(Rules.ORANGE, "p3")
def test_sameNumberOfSameNumberedCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.GREEN, 4),
    Card(Colors.ORANGE, 3),
    Card(Colors.INDIGO, 2),
    Card(Colors.YELLOW, 2),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.VIOLET, 5),
    Card(Colors.YELLOW, 5),
    Card(Colors.INDIGO, 4),
    Card(Colors.VIOLET, 3),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.INDIGO, 7),
    Card(Colors.VIOLET, 4),
    Card(Colors.ORANGE, 4),
    Card(Colors.RED, 5),
  ]]

@rulesTest(Rules.ORANGE, "p1")
def test_onePlayerHasMoreSameNumberedCards(players):
  return [[
    Card(Colors.GREEN, 3),
    Card(Colors.ORANGE, 3),
    Card(Colors.RED, 3),
    Card(Colors.INDIGO, 3),
  ],
  [
    Card(Colors.GREEN, 6),
    Card(Colors.VIOLET, 5),
    Card(Colors.INDIGO, 4),
    Card(Colors.VIOLET, 3),
  ],
  [
    Card(Colors.BLUE, 7),
    Card(Colors.INDIGO, 7),
    Card(Colors.RED, 5),
    Card(Colors.BLUE, 5),
  ]]

@rulesTest(Rules.ORANGE, "p3")
def test_noOneHasRepeatedNumberedCards(players):
  return [[
    Card(Colors.GREEN, 6),
    Card(Colors.ORANGE, 5),
    Card(Colors.RED, 4),
  ],
  [
    Card(Colors.VIOLET, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 4),

  ],
  [
    Card(Colors.BLUE, 7),
    Card(Colors.INDIGO, 6),
    Card(Colors.RED, 5),
  ]]

test_sameNumberOfSameNumberedCards(players)
test_onePlayerHasMoreSameNumberedCards(players)
test_noOneHasRepeatedNumberedCards(players)

@rulesTest(Rules.YELLOW, "p1")
def test_sameNumberOfSameColorCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.RED, 4),
    Card(Colors.RED, 3),
    Card(Colors.INDIGO, 2),
    Card(Colors.INDIGO, 3),
    Card(Colors.INDIGO, 4),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 4),
  ], [
    Card(Colors.BLUE, 6),
    Card(Colors.BLUE, 5),
    Card(Colors.BLUE, 4),
    Card(Colors.ORANGE, 4),
  ]]

@rulesTest(Rules.YELLOW, "p3")
def test_oneHasMoreSameColoredCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.RED, 4),
    Card(Colors.INDIGO, 3),
    Card(Colors.INDIGO, 2),
    Card(Colors.INDIGO, 1),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 4),
    Card(Colors.INDIGO, 5),
    Card(Colors.INDIGO, 6),
  ], [
    Card(Colors.BLUE, 6),
    Card(Colors.BLUE, 5),
    Card(Colors.BLUE, 4),
    Card(Colors.BLUE, 3),
    Card(Colors.ORANGE, 4),
  ]]

@rulesTest(Rules.YELLOW, "p3")
def test_noOneHasRepeatedColoredCards(players):
  return [[
    Card(Colors.GREEN, 6),
    Card(Colors.ORANGE, 5),
    Card(Colors.RED, 4),
  ],
  [
    Card(Colors.VIOLET, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 4),

  ],
  [
    Card(Colors.BLUE, 7),
    Card(Colors.INDIGO, 6),
    Card(Colors.RED, 3),
  ]]
  
test_sameNumberOfSameColorCards(players)
test_oneHasMoreSameColoredCards(players)
test_noOneHasRepeatedColoredCards(players)

@rulesTest(Rules.GREEN, "p1")
def test_sameNumberOfEvenCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.RED, 4),
    Card(Colors.INDIGO, 2),
    Card(Colors.INDIGO, 1),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 4),
    Card(Colors.INDIGO, 5),
  ], [
    Card(Colors.BLUE, 6),
    Card(Colors.BLUE, 4),
    Card(Colors.ORANGE, 4),
  ]]
  
@rulesTest(Rules.GREEN, "p2")
def test_oneHasMoreEvenCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.RED, 4),
    Card(Colors.INDIGO, 2),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.INDIGO, 4),
    Card(Colors.INDIGO, 6),
    Card(Colors.INDIGO, 2),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.BLUE, 5),
    Card(Colors.ORANGE, 1),
  ]]

@rulesTest(Rules.GREEN, None)
def test_noOneHasEvenCards(players):
  return [[
    Card(Colors.RED, 1),
    Card(Colors.RED, 3),
    Card(Colors.INDIGO, 5),
  ], [
    Card(Colors.INDIGO, 7),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 1),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.BLUE, 5),
    Card(Colors.ORANGE, 1),
  ]]

test_sameNumberOfEvenCards(players)
test_oneHasMoreEvenCards(players)
test_noOneHasEvenCards(players)

  
@rulesTest(Rules.BLUE, "p1")
def test_oneHasMoreDiffColoredCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 2),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.INDIGO, 4),
    Card(Colors.INDIGO, 6),
    Card(Colors.INDIGO, 2),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.BLUE, 5),
    Card(Colors.ORANGE, 1),
  ]]
  
@rulesTest(Rules.BLUE, "p3")
def test_sameNumberOfDiffColoredCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 2),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.INDIGO, 4),
    Card(Colors.ORANGE, 2),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.GREEN, 5),
    Card(Colors.ORANGE, 1),
  ]]
  
@rulesTest(Rules.BLUE, "p3")
def test_noOneHasDiffColoredCards(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.RED, 4),
    Card(Colors.RED, 2),
  ], [
    Card(Colors.INDIGO, 4),
    Card(Colors.INDIGO, 6),
    Card(Colors.INDIGO, 2),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.BLUE, 5),
    Card(Colors.BLUE, 1),
  ]]

test_oneHasMoreDiffColoredCards(players)
test_sameNumberOfDiffColoredCards(players)
test_noOneHasDiffColoredCards(players)


@rulesTest(Rules.INDIGO, "p2")
def test_oneHasMoreCardsInARun(players):
  return [[
    Card(Colors.RED, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 4),
    Card(Colors.RED, 4),
  ], [
    Card(Colors.GREEN, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 5),
    Card(Colors.INDIGO, 4),
    Card(Colors.INDIGO, 3),
  ], [
    Card(Colors.BLUE, 7),
    Card(Colors.BLUE, 5),
    Card(Colors.ORANGE, 4),
  ]]

@rulesTest(Rules.INDIGO, "p2")
def test_sameNuberOfRunCards(players):
  return [[
    Card(Colors.VIOLET, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 4),
  ], [
    Card(Colors.RED, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.YELLOW, 4),
  ], [
    Card(Colors.BLUE, 6),
    Card(Colors.ORANGE, 5),
    Card(Colors.ORANGE, 4),
  ]]

@rulesTest(Rules.INDIGO, "p2")
def test_noOneHasRunCards(players):
  return [[
    Card(Colors.VIOLET, 6),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 4),
  ], [
    Card(Colors.RED, 7),
    Card(Colors.GREEN, 5),
    Card(Colors.YELLOW, 5),
  ], [
    Card(Colors.BLUE, 3),
    Card(Colors.ORANGE, 3),
    Card(Colors.RED, 6),
  ]]

test_oneHasMoreCardsInARun(players)
test_sameNuberOfRunCards(players)
test_noOneHasRunCards(players)


@rulesTest(Rules.VIOLET, "p3")
def test_oneHasMoreCardsBelow4(players):
  return [[
    Card(Colors.VIOLET, 6),
    Card(Colors.GREEN, 4),
    Card(Colors.INDIGO, 4),
  ], [
    Card(Colors.RED, 7),
    Card(Colors.GREEN, 5),
    Card(Colors.YELLOW, 5),
  ], [
    Card(Colors.BLUE, 3),
    Card(Colors.ORANGE, 3),
    Card(Colors.RED, 6),
  ]]

@rulesTest(Rules.VIOLET, "p1")
def test_sameNumberOfCardsBelow4(players):
  return [[
    Card(Colors.VIOLET, 3),
    Card(Colors.GREEN, 3),
    Card(Colors.INDIGO, 3),
  ], [
    Card(Colors.RED, 1),
    Card(Colors.GREEN, 1),
    Card(Colors.YELLOW, 1),
  ], [
    Card(Colors.BLUE, 2),
    Card(Colors.ORANGE, 2),
    Card(Colors.RED, 2),
  ]]

@rulesTest(Rules.VIOLET, None)
def test_noOneHasCardsBelow4(players):
  return [[
    Card(Colors.VIOLET, 6),
    Card(Colors.GREEN, 5),
    Card(Colors.INDIGO, 4),
  ], [
    Card(Colors.RED, 7),
    Card(Colors.GREEN, 7),
    Card(Colors.YELLOW, 7),
  ], [
    Card(Colors.BLUE, 4),
    Card(Colors.ORANGE, 4),
    Card(Colors.RED, 4),
  ]]

test_oneHasMoreCardsBelow4(players)
test_sameNumberOfCardsBelow4(players)
test_noOneHasCardsBelow4(players)