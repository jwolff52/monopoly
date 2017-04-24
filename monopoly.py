# Adapted from the code in this video: https://www.youtube.com/watch?v=ubQXz5RBBtU Thanks Matt!

import random
import players as Players
import properties as Properties
import bank as Bank
from random import shuffle

# Roll values from a six by six grid
rollValues = [2,3,4,5,6,7,3,4,5,6,7,8,4,5,6,7,8,9,5,6,7,8,9,10,6,7,8,9,10,11,7,8,9,10,11,12]

#Initialize Community Chest
master_chest = [0,40,40,40,40,10,40,40,40,40,40,40,40,40,40,40]
chest = []

#Initialize Chance
master_chance = [0,24,11,'U','R',40,40,'B',10,40,40,5,39,40,40,40]
chance = []

def init():
  global chest
  global chance
  chest = shuffleCards(master_chest)
  chance = shuffleCards(master_chance)

def monopoly(finish_order=2, games_order=1):

  finish = 10**finish_order
  games = 10**games_order

  squares = []

  # Initialize Board Indexes
  while len(squares) < 40:
    squares.append(0)

  games_finished = 0

  while games_finished < games:

    print('Game: ' + str(games_finished))

    turns = 0

    while noWinner():
      if turns%100 == 0:
        print('Turn: ' + str(turns))
        for player in Players.players:
          print(player.name)
          print('Money: ' + str(player.money))
          print('Properties: ' + str(player.ownedProperties))
          print('Position: ' + str(player.position))
          print('')
      # print('No winner')
      for player in Players.players:
        playerList = ""
        for player in Players.players:
          playerList += player.name + ", "
        print(playerList + str(len(Players.players)))
        # print('Player: ' + player.name)
        if not player.isBankrupt:
          # print(player.name + "'s turn.")
          while True:
            doubles = 0
            doubles, squares = turn(player.id, doubles, squares)
            if doubles == 0:
              break
      turns+=1

    games_finished += 1

  return squares

def noWinner():
  remainingPlayers = Players.players
  for player in Players.players:
    if player.isBankrupt:
      remainingPlayers.remove(player)
  return len(remainingPlayers) > 0

def turn(playerID, doubles, squares):
  diceroll = int(36*random.random())

  if diceroll in [0,7,14,21,28,35]: # Dice index's for double rolls
    doubles += 1
  else:
    doubles = 0

  if doubles >= 3:
    goToJail(playerID)
  else:
    updatePosition(playerID, rollValues[diceroll])

    position = Players.players[playerID].position

    if position in [7,22,33]: # Chance Spaces
      global chance
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
          updatePosition(playerID, amt)
        elif chance_card == 'R':
          amt = 0
          playerPosition = Players.players[playerID].position
          while playerPosition not in [5,15,25,35]:
            playerPosition = (playerPosition + 1)%40
            amt += 1
          updatePosition(playerID, amt)
        elif chance_card == 'B':
          updatePosition(playerID, -3)
    elif position in [2,17]: # Community Chest Spaces
      global chest
      chest_card = chest.pop(0)
      if len(chest) == 0:
        chest = shuffleCards(master_chest)
      if chest_card != 40 and chest_card != 10:
        updatePosition(playerID, chest_card)
      elif chest_card == 10:
        goToJail(playerID)

    if position == 30: # Go to jail
      goToJail(playerID)

  squares.insert(position, (squares.pop(position) + 1))
  return doubles, squares

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
  elif not Properties.properties[player.position].isOwned and player.position not in Properties.unpurchasableProperties:
    # Proper purchasing algorithm
    if Bank.purchaseProperty(playerID):
      return None
    else:
      0
      # TODO: Auction off property

def goToJail(playerID):
  player = Players.players[playerID]

  distance = 0

  if player.position <= 10:
    distance = 10 - player.position
  else:
    distance = 10 + (39 - player.position)

  updatePosition(playerID, distance, False)
  player.inJail = True

  Players.players[playerID] = player

# Shuffles decks
def shuffleCards(input):
  output = [i for i in input]
  shuffle(output)
  return output

init()
Players.init()
Properties.init()
print(monopoly())
