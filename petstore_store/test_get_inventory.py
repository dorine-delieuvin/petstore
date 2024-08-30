import pytest
import requests
import create

pytestmark = pytest.mark.store

api = "https://petstore.swagger.io/v2"
statuses = ["available", "sold", "pending"]


def test_get_inventory():
    # create pet for each official status
    # pet[0] == status code; pet[1] == pet_data
    for i in statuses:
        pet = create.new_pet(status=i)
        assert pet[0] == 200

    # display the inventory
    get_inventory_response = get_inventory()
    assert get_inventory_response.status_code == 200

    # check statuses are in response and number of pet for the statuses are at least one
    get_inventory_data = get_inventory_response.json()
    for i in statuses:
        assert i in get_inventory_data and get_inventory_data[i] > 0


@pytest.mark.skip
def test_get_inventory_empty():
    """
    NOTE: can't test scenario, would disturbe other users and time consuming to delete all existing pets
    """
    # don't create pet // make sure the inventory is empty
    # display the inventory
    get_inventory_response = get_inventory()
    assert get_inventory_response.status_code == 200

    # check statuses are in response and number of pet for the statuses are at least one
    get_inventory_data = get_inventory_response.json()
    for i in statuses:
        assert i in get_inventory_data and get_inventory_data[i] == 0


def test_post_inventory():
    # create pet for each official status
    # pet[0] == status code; pet[1] == pet_data
    for i in statuses:
        pet = create.new_pet(status=i)
        assert pet[0] == 200

    # display the inventory
    post_inventory_response = post_inventory()
    assert post_inventory_response.status_code == 405


## API calls
def get_inventory():
    return requests.get(api + f"/store/inventory")


def post_inventory():
    return requests.post(api + f"/store/inventory")
