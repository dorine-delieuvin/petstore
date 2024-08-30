import pytest
import requests
import petstore_store.create as create

pytestmark = pytest.mark.store

api = "https://petstore.swagger.io/v2"


# python -m pytest -v -s .\test_post_order.py::test_post_order
def test_post_order():
    # create pet
    # pet[0] == status code; pet[1] == pet_data
    pet = create.new_pet(pet_name="Pennies", status="available")
    assert pet[0] == 200
    
    pet_id = pet[1]["id"]

    # create order
    # order[0] == status code; order[1] == order_data
    order = create.new_order(pet_id)
    assert order[0] == 200, f"Getting {order[0]} instead of 200."

    # check order details
    assert order[1]["petId"] == pet_id, f"{order["perID"]} instead of {pet_id}"
    assert order[1]["status"] == "placed", f"status: {order["status"]} instead of 'placed'"

# python -m pytest -v -s .\test_post_order.py::test_post_order_unavailable_pet
@pytest.mark.skip
def test_post_order_unavailable_pet():
    '''
    NOTE: orders can be placed for "pending" pets.
    '''
    # create pet
    # pet[0] == status code; pet[1] == pet_data
    unavailable_pet = create.new_pet(pet_name="Staying", status="pending")
    assert unavailable_pet[0] == 200
    
    pet_id = unavailable_pet[1]["id"]
    
    # create order
    # order[0] == status code; order[1] == order_data
    order = create.new_order(pet_id)
    assert order[0] == 400, f"Getting {order[0]} instead of 400."


## API Calls
def post_order(order):
    return requests.post(api + "/store/order", json=order)
