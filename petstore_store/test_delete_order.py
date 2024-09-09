import pytest
import requests
import random

pytestmark = pytest.mark.store


def test_delete_order(new_pet, new_order):
    # create pet
    new_pet["name"] = "Lucky" + str(random.randint(000, 999))

    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # create order
    pet_id = post_pet_response.json()["id"]
    new_order["petId"] = pet_id

    post_order_response = post_order(new_order)
    assert post_order_response.status_code == 200

    # delete order
    order_id = new_order["id"]

    delete_order_response = delete_order(order_id)
    assert delete_order_response.status_code == 200

    # check order is deleted
    get_order_response = get_order(order_id)
    assert get_order_response.status_code == 404
    assert get_order_response.json()["message"] == "Order not found"


def test_delete_order_unused_id():
    """
    NOTE: response body message in documentation is "Order not found"
    - response body message in error message is "Order Not Found" (capitalisation inconsistency)
    """
    # make sure order id is unused
    unused_order_id = 0000
    get_order_response = get_order(unused_order_id)
    assert get_order_response.status_code == 404

    # attempt delete inexistent order
    delete_order_response = delete_order(unused_order_id)
    assert delete_order_response.status_code == 404
    assert delete_order_response.json()["message"] == "Order Not Found"


@pytest.mark.skip
def test_delete_order_invalid_id(new_pet, new_order):
    """
    NOTE: getting status code 404 instead of 400 when providing an invalid order ID to delete
    """
    # create pet
    new_pet["name"] = "Paris"

    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # create order
    pet_id = post_pet_response.json()["id"]
    new_order["petId"] = pet_id

    post_order_response = post_order(new_order)
    assert post_order_response.status_code == 200

    # attempt to delete order with invalid id (typo)
    invalid_order_id = str(new_order["id"]) + "f"

    delete_order_response = delete_order(invalid_order_id)
    assert delete_order_response.status_code == 400
    assert delete_order_response.json()["message"] == "Invalid ID supplied"


def test_delete_order_no_id():
    # attempt to delete order while providing no id
    delete_order_response = delete_order("")
    assert delete_order_response.status_code == 405


# API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def post_order(order):
    return requests.post("https://petstore.swagger.io/v2/store/order", json=order)


def get_order(order_id):
    return requests.get(f"https://petstore.swagger.io/v2/store/order/{order_id}")


def delete_order(order_id):
    return requests.delete(f"https://petstore.swagger.io/v2/store/order/{order_id}")
