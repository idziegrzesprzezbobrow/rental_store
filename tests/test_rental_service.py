import unittest
import uuid
from datetime import date

from rental_store.api.api_models import FilmRentRequestModel, FilmRentRequestItemModel
from rental_store.models import Film, FilmType
from rental_store.repository.przemo_repositories import InMemoryRentalsRepository, \
    FilmRentalDetails, FilmRepository
from rental_store.service.price_calculator import PriceCalculator
from rental_store.service.rental_service import RentalService

"""
- Trying to follow the testing conventions from: https://realpython.com/python-testing/ How to make object hashable -

- to be able to add it to the set() or dict(): 
 https://stackoverflow.com/questions/7152497/making-a-python-user-defined-class-sortable-hashable 

- Had to fight with Pydantic BaseClass thingy - don't have time to do that so remove some - I belive it should be only 
used for models returned from the API

- How to enable type checking in Pytonn: https://realpython.com/python-type-checking/

- Still don't understand the differences between @staticmethod @classmethod and instance methods :-/ in python

- Will need to add https://peps.python.org/pep-0008/#function-and-method-arguments

- Used the DI as in https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html and 
https://realpython.com/python-class-constructor/

- How to restric access - modules and accessibility:
https://stackoverflow.com/questions/59315472/is-there-anyway-to-restrict-a-method-in-module-from-import-in-python
https://docs.python.org/3/tutorial/modules.html


- Implementing an interface in python: 
https://realpython.com/python-interface/

"""


# This is example of how we can mock without using any framework, simple isn't it
class MockedPriceCalculator(PriceCalculator):

    def calculate_rent_charge(self, film: Film, up_front_days: int):
        return 11, "SEK"

    def calculate_rent_surcharge(self, film: Film, up_front_days: int, date_of_rent: date):
        return 9999, "DONNER"


class MockedFilmRepository(FilmRepository):
    def save_film(self, new_film: Film):
        pass

    def mark_as_rented(self, film_id: uuid.UUID):
        pass

    def mark_as_returned(self, film_id: uuid.UUID):
        pass

    def find_film(self, film_id: uuid.UUID) -> Film:
        return Film(id=film_id, title="", type=FilmType.REGULAR, items_total=5, available_items=3)


class RentalServiceTest(unittest.TestCase):
    def setUp(self):
        # TODO: we are testing both RentalService and Calculator in here we should use some mocks
        self.film_repository = MockedFilmRepository()
        self.rental_repository = InMemoryRentalsRepository()
        self.rental_service = RentalService(film_repository=self.film_repository,
                                            rental_repository=self.rental_repository,
                                            calculator=MockedPriceCalculator())

    # TODO: what are the test case naming conventions?
    def test_when_no_films_available_empty_then_should_return_empty_list(self):
        # when
        request = FilmRentRequestModel(customer_id=uuid.uuid4(), rented_films=[])
        result = self.rental_service.rent_films(request)

        # then
        self.assertEqual(result, set())

    def test_when_all_films_available_empty_then_should_return_empty_list(self):
        # given
        film1_id = uuid.uuid4()
        film1 = Film(
            id=film1_id,
            title="Spider Man",
            type=FilmType.REGULAR,
            items_total=50,
            available_items=50
        )
        self.film_repository.save_film(film1)

        # when
        requested_films = FilmRentRequestItemModel(film_id=film1_id, up_front_days=3)
        request = FilmRentRequestModel(customer_id=uuid.uuid4(),
                                       rented_films=[requested_films])
        result = self.rental_service.rent_films(request)

        # then
        expected = {(FilmRentalDetails(film_id=film1_id, rental_date=date.today(), charged=11, up_front_days=3))}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
