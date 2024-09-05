import pytest
import requests
import random

pytestmark = pytest.mark.pet

# statuses to test (parametrized)
statuses = ["available", "pending", "sold"]
invalid_statuses = [None, "unavailable", "not so valid", "3210", "escaped!"]


@pytest.mark.parametrize("status", statuses)
def test_get_pet_by_status(new_pet, status):
    # test variable
    number_of_pets = 2

    # create pets with tested status
    pet_ids = []

    for i in range(number_of_pets):
        pet = new_pet

        pet["id"], pet["name"], pet["status"] = random.randint(1, 99999999999), "my pet " + str(i + 1), status
        pet_ids.append(pet["id"])

        post_pet_response = post_pet(pet)
        assert post_pet_response.status_code == 200, f"PET{i+1} failed creating."

    # check pets have been created
    for id in pet_ids:
        get_pet_response = get_pet(id)
        assert get_pet_response.status_code == 200

    # find pets by tested status
    get_pet_by_status_response = get_pet_by_status(status)
    assert get_pet_by_status_response.status_code == 200

    # check all pets has correct tested status
    get_pet_by_status_data = get_pet_by_status_response.json()

    for pet in get_pet_by_status_data:
        assert pet["status"] == status, "Incorrect statuses in response"

    # check if created IDs in response
    found = 0

    for pet in get_pet_by_status_data:
        for id in pet_ids:
            if pet["id"] == id:
                found += 1
    print(f"FOUND: {found}/{number_of_pets}")
    
    if found != number_of_pets:
        print("Created pets with tested status not found in response.")
        raise Exception


@pytest.mark.skip
def test_get_pet_by_several_statuses(new_pet, tested_statuses):
    """
    NOTE: when selecting more than one status in the search, only the first status is returned in the response.
    """
    # NOTE: test variables - update statuses to test in the conftest.py file
    # create pets with tested statuses
    for status in tested_statuses:
        pet = new_pet
        pet["id"], pet["status"], pet["name"] = random.randint(1, 99999999999), status, "my pet" + str(status)

        post_pet_response = post_pet(pet)
        assert post_pet_response.status_code == 200

    # find pets by tested statuses
    statuses_list = [tested_statuses[0], tested_statuses[1], tested_statuses[2]]
    get_pet_by_status_response = get_pet_by_status(tested_statuses[0], tested_statuses[1], tested_statuses[2])
    assert get_pet_by_status_response.status_code == 200

    # removing the "None" status from the list of tested status
    statuses_list_cleared = []
    
    for status in statuses_list:
        print(status)
        if status != None:
            statuses_list_cleared.append(status)
    print(f"CLEARED LIST: {statuses_list_cleared}")
    # check all pets in response have statuses in requested statuses
    get_pet_by_status_data = get_pet_by_status_response.json()
    returned_statuses = []

    for pet in get_pet_by_status_data:
        if pet["status"] not in returned_statuses:
            returned_statuses.append(pet["status"])
        assert pet["status"] in statuses_list_cleared, f"Incorrect status '{pet["status"]}' in response"

    # check all requested status with existing pets are returned
    for tested_status in statuses_list_cleared:
        assert (
            tested_status in returned_statuses
        ), f"Missing at least status '{tested_status}' in response:\nTested statuses: {statuses_list_cleared}\nReturned statuses: {returned_statuses}"


def test_get_pet_by_status_empty():
    """
    NOTE:
    - exploited the fact "invalid" statuses don't return an error 400.
    - used a made up status ("unused status") without creating a pet to test functionality.
    - as many pets exist for all official status "available", "pending" and "sold", deleting all of them would be time consuming and disturbing other users.
    """
    # do not create pet
    tested_status = "unused status"

    # try to find pets by tested status
    get_pet_by_status_empty_response = get_pet_by_status(tested_status)
    assert get_pet_by_status_empty_response.status_code == 200

    get_pet_by_status_empty_data = get_pet_by_status_empty_response.json()
    assert get_pet_by_status_empty_data == []


@pytest.mark.skip
@pytest.mark.parametrize("invalid_status", invalid_statuses)
def test_get_pet_by_status_400(new_pet, invalid_status):
    """
    NOTE: gives 200 even with a status other than "available", "pending" or "sold".
    """
    # create pet with invalid status
    invalid_pet = new_pet
    invalid_pet["id"], invalid_pet["status"], invalid_pet["name"] = random.randint(1, 99999999999), invalid_status, "my invalid pet" + str(invalid_status)

    post_invalid_pet_response = post_pet(invalid_pet)
    assert post_invalid_pet_response.status_code == 200

    # find pet by the invalid_status
    get_invalid_pet_by_status_response = get_pet_by_status(invalid_status)
    assert get_invalid_pet_by_status_response.status_code == 400


## API Calls
def post_pet(pet):
    return requests.post("https://petstore.swagger.io/v2/pet", json=pet)


def get_pet(pet_id):
    return requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")


def get_pet_by_status(status1=None, status2=None, status3=None):
    url = "https://petstore.swagger.io/v2/pet/findByStatus"

    if status1 != None:
        url += f"?status={status1}"

    if status2 != None and status1 != None:
        url += f"&status={status2}"
    elif status2 != None:
        url += f"?status={status2}"

    if status3 != None and (status1 != None or status2 != None):
        url += f"&status={status3}"
    elif status3 != None:
        url += f"?status={status3}"

    print(url)
    return requests.get(url)
