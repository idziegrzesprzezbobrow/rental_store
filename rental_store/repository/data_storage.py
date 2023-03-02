import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel

from rental_store.models import Inventory, Customer, Film, Ledger, PriceList, RentalRecord


class InMemoryFilmRepository:
    def __init__(self):
        self.films: dict[Film] = dict()

    # I Suppose it will add or update
    def save_film(self, new_film):
        self.films[new_film.id] = new_film

    def mark_as_rented(self, film_id):
        film = self.films[film_id]
        film.available_items -= 1

    def mark_as_returned(self, film_id):
        film = self.films[film_id]
        film.available_items += 1

    def find_film(self, film_id) -> Film:
        return self.films[film_id]


class InMemoryCustomerRepository:
    customers: dict[Customer] = dict()

    # I Suppose it will add or update
    def save(self, customer):
        self.customers[customer.id] = customer


class FilmRentalDetails(BaseModel):
    film_id: UUID  # TODO: should we always set it to None
    rental_date: datetime.date
    charged: int = None  # TODO: change to floating point
    up_front_days: int = None

    def __hash__(self):
        return hash(self.film_id)


class Rental(BaseModel):
    customer_id: UUID
    details: set[FilmRentalDetails] = set()


class InMemoryRentalsRepository:
    def __init__(self):
        self.rentals: dict[Rental] = dict()

    def save(self, rental):
        self.rentals[rental.customer_id] = rental

    def find_by_customer_id(self, customer_id):
        return self.rentals[customer_id]


class ListMemoryDataStorage(BaseModel):
    customers: list[Customer] = []
    inventory: Inventory = Inventory()
    ledger: Ledger = Ledger()
    price_list: PriceList = PriceList()
    film_types: list[str] = ["New release", "Regular", "Old"]

    def load_demo_data(self):
        self.inventory.films = [
            Film(
                id=0,
                title="Matrix 11",
                type="New release",
                items_total=50
            ),
            Film(
                id=1,
                title="Spider Man",
                type="Regular",
                items_total=50
            ),
            Film(
                id=2,
                title="Spider Man 2",
                type="Regular",
                items_total=50
            ),
            Film(
                id=3,
                title="Out of Africa",
                type="Old",
                items_total=50
            )
        ]

        self.customers = [
            Customer(
                id=0,
                rentals=[]
            ),
            Customer(
                id=1,
                rentals=[]
            ),
            Customer(
                id=2,
                rentals=[]
            )
        ]

        self.ledger = Ledger(
            rentals=[
                RentalRecord(
                    request_id=uuid4(),
                    film_id=0,
                    customer_id=1,
                    date_of_rent=datetime.date.today() - datetime.timedelta(days=3),
                    up_front_days=1,
                    charge=40
                ),
                RentalRecord(
                    request_id=uuid4(),
                    film_id=2,
                    customer_id=0,
                    date_of_rent=datetime.date.today() - datetime.timedelta(days=6),
                    up_front_days=1,
                    charge=90
                ),
                RentalRecord(
                    request_id=uuid4(),
                    film_id=3,
                    customer_id=2,
                    date_of_rent=datetime.date.today() - datetime.timedelta(days=5),
                    up_front_days=3,
                    charge=150
                )
            ]
        )
