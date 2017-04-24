import players as Players
import properties as Properties

def purchaseProperty(playerID):
  player = Players.players[playerID]
  property = Properties.properties[player.position]
  purchased = False

  if property.price > 0:
    newMoney = subtractPrice(player.money, property.price)
    if isinstance(newMoney, list):
      player.money = newMoney
      property.isOwned = True
      player.ownedProperties.append(player.position)
      if player.position in [12,28]:
        player.amtOfUtil += 1
      if player.position in [5,15,25,35]:
        player.amtOfRR += 1
      purchased = True

  Players.players[playerID] = player
  Properties.properties[player.position] = property
  return purchased

def payPropertyOwner(playerID):
  renter = Players.players[playerID]
  property = Properties.properties[renter.position]
  owner = Players.getPropertyOwner(renter.position)

  rent = Properties.getRent(renter.position, owner.ownedProperties)

  # Handle renters money
  newMoney = subtractPrice(renter.money, rent)
  if isinstance(newMoney, list):
    renter.money = newMoney
  elif len(renter.ownedProperties) > 0:
    # TODO: Mortgage Properties
    renter.isBankrupt = True
  else:
    renter.isBankrupt = True

  owner.money = addEarnings(owner.money, rent)

  Players.players[playerID] = renter
  Properties.properties[renter.position] = property
  Players.players[owner.id] = owner

def subtractPrice(money, price):
  priceAsMoney = amountToMoneyArray(price)

  denominations = [1,5,10,20,50,100,500]

  i = 6
  while i >= 0:
    if money[i] < priceAsMoney[i] and i > 0 and i != 4:
      priceAsMoney[i] -= money[i]
      money[i] = 0
      priceAsMoney[i-1] += ((denominations[i]/denominations[i-1]) * priceAsMoney[i])
    elif money[i] < priceAsMoney[i] and i == 4:
      priceAsMoney[i] -= money[i]
      money[i] = 0
      priceAsMoney[i-1] += ((denominations[i]/denominations[i-1]) * priceAsMoney[i])
      priceAsMoney[i-3] += ((denominations[i]/denominations[i-1]) * priceAsMoney[i])
    elif money[i] < priceAsMoney[i] and i == 0:
      # TODO: Mortgage Properties
      money[i] = 0
      return None
    else:
      money[i] -= priceAsMoney[i]
    priceAsMoney[i] = 0
    i-=1

  return money

def addEarnings(money, amount):
  amountAsMoney = amountToMoneyArray(amount)

  for i in range(0,7):
    money[i] += amountAsMoney[i]

  return money

def amountToMoneyArray(amount):
  denominations = [500,100,50,20,10,5,1]
  amountAsMoney = []

  for denomination in denominations:
    if amount/denomination != 0:
      amountAsMoney.append(amount/denomination)
      amount = amount%denomination
    else:
      amountAsMoney.append(0)

  amountAsMoney.reverse()
  return amountAsMoney

