from tinydb import TinyDB

class Player:
  id = -1
  name = ""
  money = []
  ownedProperties = []
  amtOfRR = -1
  amtOfUtil = -1
  inJail = False
  position = -1
  mortgagedProperties = []
  isBankrupt = False

  def __init__(self, id, name):
    self.id = id
    self.name = name
    self.money = [5,1,2,1,1,4,2]
    self.ownedProperties = []
    self.mortgagedProperties = []
    self.amtOfRR = 0
    self.amtOfUtil = 0
    self.position = 0

players = []

def init():
  global players
  players = []
  # Connect to db
  db = TinyDB('players.db')

  index = 0
  for player in db.all():
    players.append(Player(index, player['name']))
    index += 1

def getPropertyOwnerID(propertyID):
  for player in players:
    if propertyID in player.ownedProperties:
      return player.id

def getPropertyOwner(propertyID):
  return players[getPropertyOwnerID(propertyID)]
