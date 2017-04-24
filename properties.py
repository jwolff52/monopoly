from tinydb import TinyDB

class Property:

  name = ""
  price = -1
  mortgage = -1
  rent = -1
  houseRents = [-1, -1, -1, -1]
  housePrice = -1
  hotelRent = -1
  hotelPrice = -1
  isMortgaged = False
  isOwned = False
  houses = -1
  hasHotel = False

  def __init__(self, name, price, rent, houseRents, housePrice, hotelRent):
    self.name = name
    self.price = price
    self.mortgage = price/2
    self.rent = rent
    self.houseRents = houseRents
    self.housePrice = housePrice
    self.hotelRent = hotelRent
    self.hotelPrice = housePrice
    self.houses = 0

  def toString(self):
    return "Name: " + self.name + "\nPrice: " + str(self.price) + "\nMortgage: " + str(self.mortgage) + "\nRent: " + str(self.rent) + "\nHouse Rents: " + str(self.houseRents).replace('[', '').replace(']', '') + "\nHouse/Hotel Price: " + str(self.housePrice) + "\nHotel Rent: " + str(self.hotelRent) + "\nMortgaged? " + ("Yes" if self.isMortgaged else "No") + "\nOwned? " + ("Yes" if self.isOwned else "No")

properties = []

unpurchasableProperties = [0,2,4,7,10,17,20,22,30,33,36,38]

sets = [(1,3), (5,10,15,20), (6,8,9), (11,13,14), (12,28), (16,18,19), (21,23,24), (26,27,29), (31,32,34), (37,39)]

def init():
  # Connect to properties db
  db = TinyDB('properties.db')

  for property in db.all():
    properties.append(Property(property['name'], property['price'], property['rent'], property['houseRents'], property['housePrice'], property['hotelRent']))


def getRent(propertyID, ownersProperties):
  pSet = []
  for set in sets:
    if propertyID in set:
      pSet = set
      break

  ownedInSet = 0
  for property in ownersProperties:
    if property in set:
      ownedInSet += 1

  property = properties[propertyID]

  if property.houses == 0:
    if len(pSet) == ownedInSet:
      return property.rent*2
    else:
      return property.rent
  elif property.hasHotel:
    return property.hotelRent
  else:
    return property.houseRents[property.houses-1]
