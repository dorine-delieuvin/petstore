import pytest
import requests
import create_pet
import create_order

api = "https://petstore.swagger.io/v2"


# python -m pytest -v -s .\test_get_order.py::test_get_order
def test_get_order():
    # create pet
    # pet[0] == status code; pet[1] == pet_data
    pet = create_pet.new_pet(pet_name="Journey", status="available")
    assert pet[0] == 200
    
    pet_id = pet[1]["id"]

    # create order
    # order[0] == status code; order[1] == order_data
    order = create_order.new_order(pet_id)
    assert order[0] == 200
    
    order_id = order[1]["id"]
    
    # get order
    get_order_response = get_order(order_id)
    assert get_order_response.status_code == 200

    # check order details
    assert order[1]["petId"] == pet_id, f"{order["petId"]} instead of {pet_id}"
    assert order[1]["status"] == "placed", f"status: {order["status"]} instead of 'palced'"


## API calls
def get_order(order_id):
    return requests.get(api + f"/store/order/{order_id}")
