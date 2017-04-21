import players as Players
import properties as Properties

class Bank:
  def purchaseProperty(playerID):
    player = Players.players[playerID]
    property = Properties.property[player.position]
    purchased = False

    if property.price > 0:
      newMoney = subtractPrice(player.money, property.price)
      if not isinstance(newMoney, None):
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
    property = Properties.property[renter.position]
    owner = Players.getPropertyOwner(renter.position)

    rent = Properties.getRent(property.id, owner.id)

    # Handle renters money
    newMoney = subtractPrice(renter.money, rent)
    if not isinstance(newMoney, None):
      renter.money = newMoney
    elif len(renter.ownedProperties) > 0:
      # TODO: Mortgage Properties
      0
    else:
      renter.isBankrupt = True

    owner.money = addEarnings(owner.money, rent)

    Players.players[playerID] = renter
    Properties.properties[renter.position] = property
    Players.players[owner.id] = owner
