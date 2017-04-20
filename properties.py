from tinydb import TinyDB, Query

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

  def __init__(self, name, price, rent, houseRents, housePrice, hotelRent):
    self.name = name
    self.price = price
    self.mortgage = price/2
    self.rent = rent
    self.houseRents = houseRents
    self.housePrice = housePrice
    self.hotelRent = hotelRent
    self.hotelPrice = housePrice

  def toString(self):
    return "Name: " + self.name + "\nPrice: " + str(self.price) + "\nMortgage: " + str(self.mortgage) + "\nRent: " + str(self.rent) + "\nHouse Rents: " + str(self.houseRents).replace('[', '').replace(']', '') + "\nHouse/Hotel Price: " + str(self.housePrice) + "\nHotel Rent: " + str(self.hotelRent) + "\nMortgaged? " + ("Yes" if self.isMortgaged else "No") + "\nOwned? " + ("Yes" if self.isOwned else "No")

# Connect to properties db
db = TinyDB('properties.db')
query = Query()
properties = []

for property in db.all():
  properties.append(Property(property['name'], property['price'], property['rent'], property['houseRents'], property['housePrice'], property['hotelRent']))

for p in properties:
  print(p.toString())
