import pytest
import requests
import create

pytestmark = pytest.mark.store


api = "https://petstore.swagger.io/v2"


def test_delete_order():
    # create pet
    # pet[0] == status code; pet[1] == pet_data
    pet = create.new_pet(pet_name="Lucky")
    assert pet[0] == 200
    pet_id = pet[1]["id"]

    # create order
    # pet[0] == status code; pet[1] == pet_data
    order = create.new_order(pet_id)
    assert order[0] == 200
    order_id = order[1]["id"]

    # delete order
    delete_order_response = delete_order(order_id)
    assert delete_order_response.status_code == 200

    # check order is deleted
    get_order_response = get_order(order_id)
    get_order_data = get_order_response.json()
    assert get_order_response.status_code == 404
    assert get_order_data["message"] == "Order not found"


def test_delete_order_unused_id():
    """
    NOTE: response body message in documentation is "Order not found"
    response body message in error message is "Order Not Found" (capitalisation inconsistency)
    """
    # do not create pet
    # do not create order
    # make sure order id is unused
    unused_order_id = 0000
    get_order_response = get_order(unused_order_id)
    assert get_order_response.status_code == 404

    # attempt delete inexistent order
    delete_order_response = delete_order(unused_order_id)
    delete_order_data = delete_order_response.json()
    assert delete_order_response.status_code == 404
    assert delete_order_data["message"] == "Order Not Found"


@pytest.mark.skip
def test_delete_order_invalid_id():
    """
    NOTE: getting status code 404 instead of 400 when providing an invalid order ID to delete
    """
    # create pet
    # pet[0] == status code; pet[1] == pet_data
    pet = create.new_pet(pet_name="Paris")
    assert pet[0] == 200

    pet_id = pet[1]["id"]

    # create order
    # pet[0] == status code; pet[1] == pet_data
    order = create.new_order(pet_id)
    assert order[0] == 200

    order_id = order[1]["id"]
    invalid_order_id = str(order_id) + "f"

    # attempt to delete order with invalid id (typo)
    delete_order_response = delete_order(invalid_order_id)
    delete_order_data = delete_order_response.json()
    assert delete_order_response.status_code == 400
    assert delete_order_data["message"] == "Invalid ID supplied"


def test_delete_order_no_id():
    # do not create pet
    # do not create order
    # attempt to delete order while providing no id
    delete_order_response = delete_order("")
    assert delete_order_response.status_code == 405


# API Calls
def delete_order(order_id):
    return requests.delete(api + f"/store/order/{order_id}")


def get_order(order_id):
    return requests.get(api + f"/store/order/{order_id}")
