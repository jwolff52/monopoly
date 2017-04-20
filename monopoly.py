# Adapted from the code in this video: https://www.youtube.com/watch?v=ubQXz5RBBtU Thanks Matt!

import random
from random import shuffle

def monopoly(finish_order=2, games_order=1):

  finish = 10**finish_order
  games = 10**games_order

  # Initialize Board Indexes
  squares = []

  while len(squares) < 40:
    squares.append(0)

  # Roll values from a six by six grid
  rollValues = [2,3,4,5,6,7,3,4,5,6,7,8,4,5,6,7,8,9,5,6,7,8,9,10,6,7,8,9,10,11,7,8,9,10,11,12]

  games_finished = 0

  while games_finished < games:

    #Initialize and shuffle Community Chest
    master_chest = [0,40,40,40,40,10,40,40,40,40,40,40,40,40,40,40]
    chest = shuffleCards(master_chest)

    #Initialize and shuffle Chance
    master_chance = [0,24,11,'U','R',40,40,'B',10,40,40,5,39,40,40,40]
    chance = shuffleCards(master_chance)

    doubles = 0

    position = 0

    rolls = 0

    while rolls < finish:

      diceroll = int(36*random.random())

      if diceroll in [0,7,14,21,28,35]: # Dice index's for double rolls
        doubles += 1
      else:
        doubles = 0

      if doubles >= 3:
        position = 10
      else:
        position = (position + rollValues[diceroll])%40

        if position in [7,22,33]: # Chance Spaces
          chance_card = chance.pop(0)
          if len(chance) == 0:
            chance = shuffleCards(master_chance)

          if chance_card != 40:
            if isinstance(chance_card, int):
              position = chance_card
            elif chance_card == 'U':
              while position not in [12,28]:
                position = (position + 1)%40
            elif chance_card == 'B':
              position = position - 3
        elif position in [2,17]: # Community Chest Spaces
          chest_card = chest.pop(0)
          if len(chest) == 0:
            chest = shuffleCards(master_chest)
          if chest_card != 40:
            position = chest_card

        if position == 30: # Go to jail
          position = 10

      squares.insert(position, (squares.pop(position) + 1))

      rolls += 1

    games_finished += 1

  return squares

# Shuffles decks
def shuffleCards(input):
  output = [i for i in input]
  shuffle(output)
  return output

print(monopoly())
