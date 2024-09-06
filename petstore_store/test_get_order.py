import pytest
import requests
import random

pytestmark = pytest.mark.store


def test_get_order(new_pet, new_order):
    # create pet
    new_pet["name"], new_pet["status"] = (
        "Journey" + str(random.randint(000, 999)),
        "available",
    )

    post_pet_reponse = post_pet(new_pet)
    assert post_pet_reponse.status_code == 200

    # create order
    pet_id = new_pet["id"]
    new_order["petId"] = pet_id

    post_order_response = post_order(new_order)
    assert post_order_response.status_code == 200

    # get order
    order_id = new_order["id"]

    get_order_response = get_order(order_id)
    assert get_order_response.status_code == 200

    # check order details
    assert get_order_response.json()["petId"] == pet_id
    assert get_order_response.json()["status"] == "placed"


def test_get_order_unused_id():
    # ensure tested order id is unused
    unused_order_id = 0000
    get_unused_order_id_response = get_order(unused_order_id)
    assert get_unused_order_id_response.status_code == 404

    # attempt to get order using unused order id
    get_invalid_order_data = get_unused_order_id_response.json()
    assert get_invalid_order_data["message"] == "Order not found"


# @pytest.mark.skip
def test_get_order_invalid_id_existing(new_pet, new_order):
    """
    NOTE: getting error 404 when attempting to create (POST) an order with invalid id (e.i "000f)
    """
    # create pet
    new_pet["name"], new_pet["status"] = (
        "Oupsy" + str(random.randint(000, 999)),
        "available",
    )

    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # create order
    invalid_order_id = "000f"
    new_order["id"], new_order["petId"] = invalid_order_id, new_pet["id"]

    post_order_response = post_order(new_order)
    # assert post_order_response.status_code == 200

    # attempt to get order
    get_invalid_order_response = get_order(invalid_order_id)
    assert get_invalid_order_response.status_code == 400
    assert get_invalid_order_response.json()["message"] == "Invalid ID supplied"


@pytest.mark.skip
def test_get_order_invalid_id_not_existing():
    """
    NOTE: getting error 404 instead of 400 when attempting to retreive (GET) an order with an invalid id (e.i "000f) while no order exist with this id, simulating a typing error from the user.
    """
    # attempt to get order
    invalid_order_id = "000f"
    get_invalid_order_response = get_order(invalid_order_id)
    assert get_invalid_order_response.status_code == 400
    assert get_invalid_order_response.json()["message"] == "Invalid ID supplied"


## API calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def post_order(order):
    return requests.post("https://petstore.swagger.io/v2/order", json=order)


def get_order(order_id):
    return requests.get(f"https://petstore.swagger.io/v2/store/order/{order_id}")
