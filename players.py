from tinydb import TinyDB

class Player:


class Players:

  players = []

  def __init__(self):
    # Connect to db
    db = TinyDB('players.db')

    for player in db.all():
      players.append()
