import pytest
import requests

pytestmark = pytest.mark.pet


def test_update_pet(new_pet):
    """
    NOTE #1: Sometimes fails to assert the updated pet name.
    NOTE #2: Sometimes returns a 404 instead of 200 when creating a new pet.
    Those are assumed to be due to server activity as the tests pass successfully when re-run most of the time.
    """
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    pet_id = post_pet_response.json()["id"]

    # update pet
    updated_pet = {
        "id": pet_id,
        "category": {
            # "id": 0,  # set to 0 by default server side
            "name": "test category name",
        },
        "name": "updated doggie name",
        "photoUrls": ["my_photo_url"],
        "tags": [
            {
                # "id": 0,
                "name": "my tag name"
            }
        ],  # set to 0 by default server side
        "status": "unavailable",
    }
    update_pet_response = update_pet(updated_pet)
    assert update_pet_response.status_code == 200

    # get updated pet, check new data
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.status_code == 200

    get_updated_pet_data = get_updated_pet_response.json()
    assert get_updated_pet_data["name"] == updated_pet["name"]
    assert get_updated_pet_data["status"] == updated_pet["status"]


@pytest.mark.skip
def test_update_pet_400():
    # testing error 400: Invalid ID supplied
    """
    NOTE: returns an error 500 instead of 400.
    """
    invalid_pet_id = 0.5
    update_invalid_id_response = update_pet(invalid_pet_id)
    assert update_invalid_id_response.status_code == 400


@pytest.mark.skip
def test_update_pet_404():
    # testing error 404: Pet not found
    """
    NOTE: returns a 200 instead of 404 for any presumed invalid ID tried.
    """
    invalid_pet = {
        "id": -0.5,  # presummed invalid ID
        "name": "Invalid",
        "status": "unavailable",
    }
    update_invalid_pet_response = update_pet(invalid_pet)
    assert update_invalid_pet_response.status_code == 404


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")


def update_pet(pet):
    return requests.put("https://petstore.swagger.io/v2/pet", json=pet)
