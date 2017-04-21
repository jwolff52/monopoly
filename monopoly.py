# Adapted from the code in this video: https://www.youtube.com/watch?v=ubQXz5RBBtU Thanks Matt!

import random
import players as Players
import properties as Properties
from random import shuffle

# Roll values from a six by six grid
rollValues = [2,3,4,5,6,7,3,4,5,6,7,8,4,5,6,7,8,9,5,6,7,8,9,10,6,7,8,9,10,11,7,8,9,10,11,12]

squares = []

def monopoly(finish_order=2, games_order=1):

  finish = 10**finish_order
  games = 10**games_order

  # Initialize Board Indexes
  while len(squares) < 40:
    squares.append(0)

  games_finished = 0

  while games_finished < games:

    print('Game: ' + str(games_finished))

    #Initialize and shuffle Community Chest
    master_chest = [0,40,40,40,40,10,40,40,40,40,40,40,40,40,40,40]
    chest = shuffleCards(master_chest)

    #Initialize and shuffle Chance
    master_chance = [0,24,11,'U','R',40,40,'B',10,40,40,5,39,40,40,40]
    chance = shuffleCards(master_chance)

    while noWinner():
      for player in Players.players:
        print('No Winner')
        if not player.isBankrupt:
          print(player.name + "'s turn.")
          while True:
            doubles = turn(player.id, doubles)
            if doubles == 0:
              break

    games_finished += 1

def noWinner():
  remainingPlayers = Players.players
  for player in Players.players:
    if player.isBankrupt:
      remainingPlayers.remove(player)
  return len(remainingPlayers) == 0

def turn(playerID, doubles):
  diceroll = int(36*random.random())

  if diceroll in [0,7,14,21,28,35]: # Dice index's for double rolls
    doubles += 1
  else:
    doubles = 0

  if doubles >= 3:
    updatePosition(playerID, 10)
  else:
    updatePosition(playerID, rollValues[diceroll])

    if player.position in [7,22,33]: # Chance Spaces
      chance_card = chance.pop(0)
      if len(chance) == 0:
        chance = shuffleCards(master_chance)

      if chance_card != 40:
        if isinstance(chance_card, int) and chance_card != 10:
          updatePosition(playerID, chance_card)
        elif isinstance(chance_card, int) and chance_card == 10:
          updatePosition(playerID, chance_card, False)
        elif chance_card == 'U':
          amt = 0
          playerPosition = Players.players[playerID].position
          while playerPosition not in [12,28]:
            playerPosition = (playerPosition + 1)%40
            amt += 1
          updatePosition(player, amt)
        elif chance_card == 'R':
          amt = 0
          playerPosition = Players.players[playerID].position
          while player.position not in [5,15,25,35]:
            playerPosition = (playerPosition + 1)%40
            amt += 1
          updatePosition(player, amt)
        elif chance_card == 'B':
          updatePosition(player, -3)
    elif position in [2,17]: # Community Chest Spaces
      chest_card = chest.pop(0)
      if len(chest) == 0:
        chest = shuffleCards(master_chest)
      if chest_card != 40 and chect_card != 10:
        updatePosition(player, chest_card)
      elif chest_card == 10:
        updatePosition(player, chest_card, False)

    if player.position == 30: # Go to jail
      updatePosition(player, 10, False)

  squares.insert(player.position, (squares.pop(player.position) + 1))
  return doubles

def updatePosition(playerID, amt, goPassable=True):
  player = Players.players[playerID]

  origionalPosition = player.position

  if amt < 0 and abs(amt) > origionalPosition:
    amt = 39 - amt

  player.position = (player.position + amt)%40

  if goPassable and origionalPosition > player.position:
    player.money[6] += 2

  Players.players[playerID] = player

  if Properties.properties[player.position].isOwned and not Properties.properties[player.position].isMortgaged:
    Bank.payPropertyOwner(playerID)
  else:
    # Proper purchasing algorithm
    if random.random()*2 == 2:
      if Bank.purchaseProperty(playerID):
        return None
    # TODO: Auction off property

# Shuffles decks
def shuffleCards(input):
  output = [i for i in input]
  shuffle(output)
  return output

Players.init()
Properties.init()
monopoly()
print(squares)
