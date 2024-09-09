import pytest
import requests
import random

pytestmark = pytest.mark.store


def test_get_inventory(new_pet, valid_statuses):
    # create pet for each official status
    for status in valid_statuses:
        new_pet["id"], new_pet["name"], new_pet["status"] = (
            random.randint(1, 99999999999),
            "Fetch" + str(random.randint(000, 999)),
            status,
        )

        post_pet_response = post_pet(new_pet)
        assert post_pet_response.status_code == 200

    # display the inventory
    get_inventory_response = get_inventory()
    assert get_inventory_response.status_code == 200

    # check statuses are in response and number of pet for the statuses are at least one
    for status in valid_statuses:
        assert (
            status in get_inventory_response.json()
            and get_inventory_response.json()[status] > 0
        )


@pytest.mark.skip
def test_get_inventory_empty(valid_statuses):
    """
    NOTE: can't test scenario, would disturbe other users and time consuming to delete all existing pets
    """
    # don't create pet // make sure the inventory is empty
    # display the inventory
    get_inventory_response = get_inventory()
    assert get_inventory_response.status_code == 200

    # check statuses are in response and number of pet for the statuses are at least one
    for status in valid_statuses:
        assert (
            status in get_inventory_response.json()
            and get_inventory_response.json()[status] == 0
        )


def test_post_inventory(new_pet, valid_statuses):
    # create pet for each official status
    for status in valid_statuses:
        new_pet["id"], new_pet["name"], new_pet["status"] = (
            random.randint(1, 99999999999),
            "Spot" + str(random.randint(000, 999)),
            status,
        )

        post_pet_response = post_pet(new_pet)
        assert post_pet_response.status_code == 200

    # attempt to display the inventory using invalid request method POST
    post_inventory_response = post_inventory()
    assert post_inventory_response.status_code == 405


## API calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_inventory():
    return requests.get(f"https://petstore.swagger.io/v2/store/inventory")


def post_inventory():
    return requests.post(f"https://petstore.swagger.io/v2/store/inventory")
