import pytest
import requests
import random

pytestmark = pytest.mark.store

# statuses to test (parametrized)
statuses = ["available", "pending", "sold", "unofficial status that should not exist"]


@pytest.mark.parametrize("status", statuses)
def test_post_order(new_pet, new_order, status):
    """
    NOTE: orders can be placed for pets with "pending", "sold" and unvalid statuses.
    """
    # create pet
    new_pet["name"] = "Staying" + str(status) + str(random.randint(000, 999))
    new_pet["status"] = str(status)

    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # create order
    new_order["petId"] = new_pet["id"]

    post_order_response = post_order(new_order)

    # orders can be placed for "available" pets
    if post_pet_response.json()["status"] == "available":
        assert post_order_response.status_code == 200
        assert post_order_response.json()["status"] == "placed"

    # orders should not be placed for "sold" or "pendng" pets
    elif (
        post_pet_response.json()["status"] == "pending"
        or post_pet_response.json()["status"] == "sold"
    ):
        assert (
            post_order_response.status_code == 400
        ), "Order placed for a pet with 'pending' or 'sold' status"

    # other status *should* not be possible
    else:
        assert (
            post_order_response.status_code == 400
        ), "Order placed for a pet with an unofficial status"


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def post_order(order):
    return requests.post("https://petstore.swagger.io/v2/store/order", json=order)
