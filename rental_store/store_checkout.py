from datetime import date
from rental_store.calculator import calculate_rent_charge, calculate_rent_surcharge
from rental_store.repositories import Repository
from rental_store.data_models import \
    FilmRentResponseModel,\
    FilmRentRequestModel,\
    FilmReturnRequestModel,\
    FilmRentResponseItemModel, \
    FilmReturnResponseModel,\
    FilmReturnResponseItemModel,\
    FilmInventoryItemModel,\
    FilmInventoryModel,\
    Film,\
    Customer
import uuid


class AvailabilityError(Exception):

    def __init__(self, message: str):
        self.message = message


class DuplicateRentError(Exception):

    def __init__(self, message: str):
        self.message = message


class RentError(Exception):

    def __init__(self, message):
        self.message = message


def rent_films(rent_request: FilmRentRequestModel):

    request_id = uuid.uuid4()

    for item in rent_request.rented_films:

        try:
            reserve_film(request_id, item.film_id)

        except AvailabilityError as e:
            raise RentError(str(e))

        except DuplicateRentError as e:
            raise RentError(str(e))

    customer = Repository.get_customer(rent_request.customer_id)
    response_items = []

    for item in rent_request.rented_films:

        film = Repository.get_film_by_id(item.film_id)
        print(item.film_id)
        print(film.id)

        charge, currency = calculate_rent_charge(film, item.up_front_days)

        Repository.add_record_to_rental_ledger(request_id, customer.id, film.id, item.up_front_days, charge, date.today())

        response_items.append(FilmRentResponseItemModel(film_id=film.id, charge=charge, currency=currency))

    return FilmRentResponseModel(rented_films=response_items)


def return_films(self, return_request: FilmReturnRequestModel):

    response_items = []

    for item in return_request.returned_films:

        film = self.repository.get_film_by_id(item.film_id)
        customer = self.repository.get_customer(return_request.customer_id)
        surcharge, currency = self.price_calculator.calculate_rent_surcharge(film, customer)

        self.return_film(customer, film, surcharge, date.today())

        response_items.append(FilmReturnResponseItemModel(film_id=film.film_id, surcharge=surcharge, currency=currency))

    return FilmReturnResponseModel(returned_films=response_items)


def get_film_inventory():

    films = self.film_inventory.get_all()
    films_formatted = []
    for item in films:
        films_formatted = FilmInventoryItemModel(**item)

    return FilmInventoryModel(film_inventory=films_formatted)


def get_customers_rentals(customer_id: int):
    pass


def reserve_film(request_id, film):
    pass


def add_record_to_rental_ledger(self, request_id):
    self.repository.add_film_to_rentals_ledger(customer.id, film.id, up_front_days, charge, date_of_rent)


def return_film(self, customer: Customer, film: Film, surcharge: int, date_of_return):
    self.repository.mark_film_as_returned_in_rentals_ledger(customer.id, film.id, surcharge, date_of_return)

