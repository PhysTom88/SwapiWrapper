
def ship_to_dict(ship):
    return {
        "class": ship.starship_class,
        "manufacturer": ship.manufacturer,
        "length": ship.length,
        "hyperdrive_capacity": ship.hyperdrive_rating,
        "cargo_capacity": ship.cargo_capacity,
        "crew": ship.crew,
        "passengers": ship.passengers
    }


def listing_to_dict(listing):
    return {
        "ship": ship_to_dict(listing.ship_type),
        "price": listing.price,
        "name": listing.name,
        "date_listed": listing.listed_date.isoformat(),
        "active": listing.active
    }