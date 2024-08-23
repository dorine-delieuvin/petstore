import pytest
import requests
import random
import create_pet
import create_order

api = "https://petstore.swagger.io/v2"


# python -m pytest -v -s .\test_post_order.py::test_post_order
def test_post_order():
    # create pet
    pet = create_pet.new_pet(pet_name="Pennies", status="available")
    pet_id = pet["id"]
    print(pet_id)

    # create order
    order = create_order.new_order(pet_id)
    print(order)
    post_order_response = post_order(order)
    assert (
        post_order_response.status_code == 200
    ), f"Getting {post_order_response.status_code} instead of 200."

    # check order details
    assert order["petId"] == pet_id, f"{order["perID"]}//{pet_id}"
    assert order["status"] == "placed", f"status: {order["status"]}"

# python -m pytest -v -s .\test_post_order.py::test_post_order_unavailable_pet
def test_post_order_unavailable_pet():
    '''
    NOTE: orders can be placed for "sold" pets.
    '''
    # create pet
    unavailable_pet = create_pet.new_pet(pet_name="Staying", status="sold")
    pet_id = unavailable_pet["id"]
    print(pet_id)
    
    # create order
    order = create_order.new_order(pet_id)
    print(order)

    post_order_response = post_order(order)
    assert (
        post_order_response.status_code == 400
    ), f"Getting {post_order_response.status_code} instead of 400."


## API Calls
def post_order(order):
    return requests.post(api + "/store/order", json=order)
