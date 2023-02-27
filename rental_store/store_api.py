import rental_store.repositories
from fastapi import FastAPI, HTTPException
from rental_store.data_models import FilmRentResponseModel, FilmRentRequestModel, FilmReturnRequestModel,\
    FilmReturnResponseModel, Inventory
from rental_store.store_checkout import StoreCheckout, RentError, ReturnError


store = FastAPI()

rental_store.repositories.data_storage


@store.post("/films/rent", response_model=FilmRentResponseModel)
def api_rent_films(rent_request: FilmRentRequestModel):

    try:
        response = StoreCheckout.rent_films(rent_request)

    except RentError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Rent error."}
        )

    except Exception as e:
        raise HTTPException(
            status_code=504,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.post("/films/return", response_model=FilmReturnResponseModel)
def api_return_films(return_request: FilmReturnRequestModel):

    try:
        response = StoreCheckout.return_films(return_request)

    except ReturnError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"X-Error": "Return error."}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/films", response_model=Inventory)
def api_get_film_inventory():

    try:
        response = StoreCheckout.get_film_inventory()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/store/ledger")
def api_get_ledger():

    return get_ledger()


@store.post("/customers/add")
def api_add_customer():

    return add_customer()


@store.get("/customers/{customer_id}")
def api_get_customer(customer_id: int):

    try:
        response = StoreCheckout.get_customer(customer_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
            headers={"X-Error": "Unexpected error."}
        )

    return response


@store.get("/customers")
def api_get_customers():

    return StoreCheckout.get_customers()


@store.post("/demo")
def api_start_demo():

    StoreCheckout.load_demo_data()

    return "Demo data loaded"
