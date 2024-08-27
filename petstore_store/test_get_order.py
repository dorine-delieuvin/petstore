import pytest
import requests
import create

api = "https://petstore.swagger.io/v2"


# python -m pytest -v -s .\test_get_order.py::test_get_order
def test_get_order():
    # create pet
    # pet[0] == status code; pet[1] == pet_data
    pet = create.new_pet(pet_name="Journey", status="available")
    assert pet[0] == 200
    
    pet_id = pet[1]["id"]

    # create order
    # order[0] == status code; order[1] == order_data
    order = create.new_order(pet_id)
    assert order[0] == 200
    
    order_id = order[1]["id"]
    
    # get order
    get_order_response = get_order(order_id)
    assert get_order_response.status_code == 200

    # check order details
    assert order[1]["petId"] == pet_id, f"{order["petId"]} instead of {pet_id}"
    assert order[1]["status"] == "placed", f"status: {order["status"]} instead of 'palced'"

# python -m pytest -v -s .\test_get_order.py::test_get_order_unused_id
def test_get_order_unused_id():
    # do not create pet
    # do not create order
    # attempt getting order
    unused_order_id = 0000
    get_unused_order_id_response = get_order(unused_order_id)
    assert get_unused_order_id_response.status_code == 404, f"Code {get_unused_order_id_response.status_code} instead of 404."
    
    get_invalid_order_data = get_unused_order_id_response.json()
    assert get_invalid_order_data["message"] == "Order not found"
    

## API calls
def get_order(order_id):
    return requests.get(api + f"/store/order/{order_id}")
