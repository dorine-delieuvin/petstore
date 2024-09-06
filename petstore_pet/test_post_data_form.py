import pytest
import requests
import random

pytestmark = pytest.mark.pet

# data to test (parametrize)
valid_forms = [
    {"name": "Max"},
    {"status": "sold"},
    {"name": "Bella", "status": "pending"},
]

invalid_forms = [
    {"name": ""},
    {"status": "flying"},
    {},
]


@pytest.mark.parametrize("valid_form", valid_forms)
def test_post_data_form_valid(new_pet, valid_form):
    # create pet
    new_pet["name"] = "Mickey" + str(random.randint(000, 999))
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet data
    pet_id = post_pet_response.json()["id"]

    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200
    assert get_pet_response.json()["name"] == new_pet["name"]
    assert get_pet_response.json()["status"] == new_pet["status"]
    
    print(f"\nPET DATA BEFORE UPDATE: {get_pet_response.json()["name"]}, {get_pet_response.json()["status"]}.")

    # update pet data via form
    post_data_form_response = post_data_form(pet_id, valid_form)
    assert post_data_form_response.status_code == 200

    # check data has been updated according to form
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.status_code == 200

    if "name" in valid_form:
        assert get_updated_pet_response.json()["name"] == valid_form["name"]

    if "status" in valid_form:
        assert get_updated_pet_response.json()["status"] == valid_form["status"]
    
    print(f"PET DATA AFTER UPDATE: {get_updated_pet_response.json()["name"]}, {get_updated_pet_response.json()["status"]}.")



@pytest.mark.skip
@pytest.mark.parametrize("invalid_form", invalid_forms)
def test_post_data_form_incorrect_data(new_pet, invalid_form):
    """
    NOTE 1: when empty name given via form, the name remain unchanged. No error is raised.
    
    NOTE 2: when invalid status given via form, the status is created and pet data updated. No error is raised and code 200 is returned.
    
    NOTE 3: when empty form is submitted, the name and status remain unchanged. No error is raised, 200 is returned.
    """
    # create pet
    new_pet["name"] = "Meannie" + str(random.randint(000, 999))
    post_pet_response = post_pet(new_pet)
    assert post_pet_response.status_code == 200

    # check the created pet data
    pet_id = post_pet_response.json()["id"]

    get_pet_response = get_pet(pet_id)
    assert get_pet_response.status_code == 200
    assert get_pet_response.json()["name"] == new_pet["name"]
    assert get_pet_response.json()["status"] == new_pet["status"]
    
    print(f"\nPET DATA BEFORE UPDATE ATTEMPT: {get_pet_response.json()["name"]}, {get_pet_response.json()["status"]}.")

    # update pet data via invalid form
    post_data_form_response = post_data_form(pet_id, invalid_form)  # response asserted on last line

    # check the pet info after update attempt
    get_updated_pet_response = get_pet(pet_id)
    assert get_updated_pet_response.status_code == 200

    print(f"PET DATA AFTER UPDATE ATTEMPT: {get_updated_pet_response.json()["name"]}, {get_updated_pet_response.json()["status"]}.")

    assert post_data_form_response.status_code == 400

def test_post_data_form_unused_id():
    # ensure tested id is unused
    unused_pet_id = 00000
    get_unused_id_response = get_pet(unused_pet_id)
    assert get_unused_id_response.status_code == 404

    # attempt to update data for this unused id
    form = {"name": "Ghost"}

    post_data_form_response = post_data_form(unused_pet_id, form)
    assert post_data_form_response.status_code == 404


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")


def post_data_form(pet_id, form):
    return requests.post(f"https://petstore.swagger.io/v2/pet/{pet_id}", data=form)
