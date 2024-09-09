import pytest
import requests

pytestmark = pytest.mark.pet


def test_post_pet(new_pet):
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet
    pet_id = post_pet_response.json()["id"]

    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    # check data are same as the ones pushed
    assert get_pet_response.json()["status"] == new_pet["status"]
    assert get_pet_response.json()["name"] == new_pet["name"]


@pytest.mark.skip
def test_post_pet_invalid_id(new_pet):
    """
    NOTE: getting 500 when trying to POST a new pet with invalid id (e.g. "1234f")
    """
    # create pet
    new_pet["id"] = str(new_pet["id"]) + "f"

    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet
    pet_id = post_pet_response.json()["id"]

    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200
    assert get_pet_response.json()["id"] == new_pet["id"]


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")
