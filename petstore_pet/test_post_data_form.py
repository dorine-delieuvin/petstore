import pytest
import requests
import random

pytestmark = pytest.mark.pet


def test_post_data_form_status(new_pet):
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet data
    pet_id = post_pet_response.json()["id"]
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    get_pet_data = get_pet_response.json()
    assert get_pet_data["status"] == new_pet["status"]

    # update status only via form
    form = {
        # "name": "Max",
        "status": "sold"
    }

    post_data_form_response = post_data_form(pet_id, form)
    assert post_data_form_response.status_code == 200

    # check data has been updated
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.json()["status"] == form["status"]


def test_post_data_form_both(new_pet):
    # create pet
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet data
    pet_id = post_pet_response.json()["id"]
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    get_pet_data = get_pet_response.json()
    print(get_pet_data["name"], get_pet_data["status"])  # doggie, available
    assert get_pet_data["name"] == new_pet["name"]
    assert get_pet_data["status"] == new_pet["status"]

    # update name and status via form
    form = {"name": "Bella", "status": "pending"}

    post_data_form_response = post_data_form(pet_id, form)
    assert post_data_form_response.status_code == 200

    # check data has been updated
    get_updated_pet_response = get_pet(pet_id)
    get_updated_pet_data = get_updated_pet_response.json()
    print(
        get_updated_pet_data["name"], get_updated_pet_data["status"]
    )  # Bella, pending
    assert get_updated_pet_data["name"] == form["name"]
    assert get_updated_pet_data["status"] == form["status"]


def test_post_data_form_unused_id():
    # ensure tested id is unused
    unused_pet_id = 00000
    get_unused_id_response = get_pet(unused_pet_id)
    assert get_unused_id_response.status_code == 404

    # attempt to update data for this unused id
    form = {
        "name": "Ghost",
        # "status": "sold"
    }

    post_data_form_response = post_data_form(unused_pet_id, form)
    assert post_data_form_response.status_code == 404


@pytest.mark.skip
def test_post_data_form_empty_name(new_pet):
    """
    NOTE: when empty name given via form, the name remain unchanged. No error is raised.
    """
    # create pet
    new_pet["name"] = "Max"
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet data
    pet_id = post_pet_response.json()["id"]
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    get_pet_data = get_pet_response.json()
    print(get_pet_data["name"], get_pet_data["status"])  # Max, available
    assert get_pet_data["name"] == new_pet["name"]
    assert get_pet_data["status"] == new_pet["status"]

    # attempt to update with empty name
    form = {
        "name": "",
        # "status": "sold"
    }

    post_data_form_response = post_data_form(pet_id, form)  # response asserted later

    # check the pet info after update
    get_updated_pet_reponse = get_pet(pet_id)
    assert get_updated_pet_reponse.status_code == 200

    print(
        get_updated_pet_reponse.json()["name"], get_updated_pet_reponse.json()["status"]
    )  # still Max, available (does not update)

    assert post_data_form_response.status_code == 400


# python -m pytest -v -s .\test_pet.py::test_post_data_form_invalid_status
@pytest.mark.pet
@pytest.mark.pet_data_form
@pytest.mark.skip
def test_post_data_form_invalid_status():
    """
    NOTE: when invalid status given via form, the status is created. No error is raised and code 200 is returned.
    """
    # create pet
    pet = new_pet()
    pet["name"] = "Invalid"
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    post_pet_data = post_pet_response.json()

    # check the created pet data
    pet_id = post_pet_data["id"]
    print(pet_id)
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    get_pet_data = get_pet_response.json()
    print(get_pet_data["name"], get_pet_data["status"])  # Invalid, available
    assert get_pet_data["name"] == pet["name"]
    assert get_pet_data["status"] == pet["status"]

    # attempt to update with invalid status
    form = {
        # "name": "Valid",
        "status": "flying"
    }

    post_data_form_response = post_data_form(pet_id, form)

    # check the pet info after update
    get_updated_pet_reponse = get_pet(pet_id)
    assert get_updated_pet_reponse.status_code == 200
    get_updated_pet_data = get_updated_pet_reponse.json()
    print(get_updated_pet_data["name"], get_updated_pet_data["status"])

    assert (
        post_data_form_response.status_code == 400
    ), f"Failed, gives {post_data_form_response.status_code} instead of 400"


# python -m pytest -v -s .\test_pet.py::test_post_data_form_no_data
@pytest.mark.pet
@pytest.mark.pet_data_form
@pytest.mark.skip
def test_post_data_form_no_data():
    """
    NOTE: when empty form is submitted, the name and status remain unchanged. No error is raised, 200 is returned.
    """
    # create pet
    pet = new_pet()
    pet["name"] = "Perfect"
    post_pet_response = post_pet(pet)
    assert post_pet_response.status_code == 200

    post_pet_data = post_pet_response.json()

    # check the created pet data
    pet_id = post_pet_data["id"]
    print(pet_id)
    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200

    get_pet_data = get_pet_response.json()
    print(get_pet_data["name"], get_pet_data["status"])  # Perfect, available
    assert get_pet_data["name"] == pet["name"]
    assert get_pet_data["status"] == pet["status"]

    # attempt to update with empty form
    form = {
        # "name": "Valid",
        # "status": "sold"
    }

    post_data_form_response = post_data_form(pet_id, form)

    # check the pet info after update
    get_updated_pet_reponse = get_pet(pet_id)
    assert get_updated_pet_reponse.status_code == 200
    get_updated_pet_data = get_updated_pet_reponse.json()
    print(get_updated_pet_data["name"], get_updated_pet_data["status"])

    assert (
        post_data_form_response.status_code == 400
    ), f"Failed, gives {post_data_form_response.status_code} instead of 400"


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")


def post_data_form(pet_id, form):
    return requests.post(f"https://petstore.swagger.io/v2/pet/{pet_id}", data=form)
