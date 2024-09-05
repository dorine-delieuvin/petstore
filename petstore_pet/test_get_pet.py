import pytest
import requests

pytestmark = pytest.mark.pet


def test_get_pet(new_pet):
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    pet_id = post_pet_response.json()["id"]

    # get pet
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    # check pet info
    get_pet_data = get_pet_response.json()
    assert get_pet_data["id"] == pet_id
    assert get_pet_data["name"] == new_pet["name"]
    assert get_pet_data["status"] == new_pet["status"]


def test_get_pet_404():
    # don't create pet
    inexistant_pet_id = 0

    # get pet
    get_pet_response = get_pet(inexistant_pet_id)
    assert get_pet_response.status_code == 404
    assert get_pet_response.json()["message"] == "Pet not found"


@pytest.mark.skip
def test_get_pet_400(new_pet):
    """
    NOTE: when providing an invalid pet ID, the API assigns a default ID "9223372036854775807" to the pet instead of returning an error
    """
    # create pet with an invalid ID
    new_pet["id"] = -0.5
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    invalid_pet_id = post_pet_response.json()["id"]

    # get pet
    get_invalid_pet_response = get_pet(invalid_pet_id)
    assert get_invalid_pet_response.status_code == 400, print(
        get_invalid_pet_response.json()["id"]
    )


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")
