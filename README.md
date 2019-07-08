# Ostmodern Python Code Test

The goal of this exercise is to test that you know your way around Django and
REST APIs. Approach it the way you would an actual long-term project.

The idea is to build a platform on which your users can buy and sell Starships.
To make this process more transparent, it has been decided to source some
technical information about the Starships on sale from the [Starship
API](https://swapi.co/documentation#starships).

A Django project some initial data models have been created already. You may need
to do some additional data modelling to satify the requirements.

## Getting started

* This test works with either
  [Docker](https://docs.docker.com/compose/install/#install-compose) or
  [Vagrant](https://www.vagrantup.com/downloads.html)
* Get the code from `https://github.com/ostmodern/python-code-test`
* Do all your work in your own `develop` branch
* Once you have downloaded the code the following commands will get the site up
  and running

```shell
# For Docker
docker-compose up
# You can run `manage.py` commands using the `./manapy` wrapper

# For Vagrant
vagrant up
vagrant ssh
# Inside the box
./manage.py runserver 0.0.0.0:8008
```
* The default Django "It worked!" page should now be available at
  http://localhost:8008/

## Tasks

Your task is to build a JSON-based REST API for your frontend developers to
consume. You have built a list of user stories with your colleagues, but you get
to decide how to design the API. Remember that the frontend developers will need
some documentation of your API to understand how to use it.

We do not need you to implement users or authentication, to reduce the amount of
time this exercise will take to complete. You may use any external libraries you
require.

* We need to be able to import all existing
  [Starships](https://swapi.co/documentation#starships) to the provided Starship
  Model
* A potential buyer can browse all Starships
* A potential buyer can browse all the listings for a given `starship_class`
* A potential buyer can sort listings by price or time of listing
* To list a Starship as for sale, the user should supply the Starship name and
  list price
* A seller can deactivate and reactivate their listing

After you are done, create a release branch in your repo and send us the link.

## Endpoints

Interacting with the API is simple, there are 3 main methods of interaction.
* Get all the starships: GET /starships/ships/
* returns a list of ships:
```shell
[
    {
        "passengers": "38000",
        "cargo_capacity": "250000000",
        "crew": "279144",
        "length": "19000",
        "hyperdrive_capacity": "2.0",
        "class": "Star dreadnought",
        "manufacturer": "Kuat Drive Yards, Fondor Shipyards"
    },
    ...
]
```

* Get all the listings: GET /starships/listings/
* Query string parameters: starship_class, sort_by (date or price)
* if no starship_class or invalid sort_by returns 400
* returns a list of listings for a given starship class
```shell
{
    "listings": [
        {
            "active": true,
            "ship": {
                "passengers": "0",
                "cargo_capacity": "110",
                "crew": "1",
                "length": "12.5",
                "hyperdrive_capacity": "1.0",
                "class": "Starfighter",
                "manufacturer": "Incom Corporation"
            },
            "date_listed": "2019-07-06T10:38:34.618586+00:00",
            "price": 100,
            "name": "Bloody Bastard III"
        },
        ...
        ]
}
```

* Submit a listing for a starship: POST /starships/listing/
* Request data of the form:
```shell
{
	"starship_class": "[STARSHIP_CLASS]",
	"price": "[PRICE]",
	"name": "[NAME]",
	"manufacturer": "[MANUFACTURER]"
}
```
* If any of them are missing returns a 400
* Successful submission returns 201 with:
```shell
{
    "listing": {
        "active": true,
        "ship": {
            "passengers": "0",
            "cargo_capacity": "110",
            "crew": "1",
            "length": "12.5",
            "hyperdrive_capacity": "1.0",
            "class": "[CLASS]",
            "manufacturer": "[MANUFACTURER]"
        },
        "date_listed": "2019-07-08T07:52:43.898062+00:00",
        "price": [PRICE],
        "name": "[NAME]"
    }
}
```

* Deactivate / Activate a listing: PUT /starships/listing/
* Request data of the form:
```shell
{
	"name": "[NAME]",
}
```
* If no name supplied returns 404
* successful submission returns 200 with:
```shell
{
    "listing": {
        "active": true / false,
        "ship": {
            "passengers": "0",
            "cargo_capacity": "110",
            "crew": "1",
            "length": "12.5",
            "hyperdrive_capacity": "1.0",
            "class": "[CLASS]",
            "manufacturer": "[MANUFACTURER]"
        },
        "date_listed": "2019-07-08T07:52:43.898062+00:00",
        "price": [PRICE],
        "name": "[NAME]"
    }
}
```
