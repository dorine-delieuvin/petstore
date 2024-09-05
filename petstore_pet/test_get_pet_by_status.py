import pytest
import requests
import random

pytestmark = pytest.mark.pet

statuses = ["available", "pending", "sold"]


@pytest.mark.parametrize("status", statuses)
def test_get_pet_by_status(new_pet, status):
    # test variable
    number_of_pets = 2

    # create pets with tested status
    pet_ids = []

    for i in range(number_of_pets):
        pet = new_pet

        pet["name"] = "my pet " + str(i + 1)
        pet["status"] = status
        pet["id"] = random.randint(1, 99999999999)
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
        print("Created pets with tested status not found.")
        raise Exception


'''@pytest.mark.skip
def test_get_pet_by_several_statuses():
    """
    NOTE: when selecting more than one status in the search, only the first status is returned in the response.
    """
    # test variables - update status1, 2, 3 to the status to test in list valid_status
    valid_status = ["available", "pending", "sold"]
    status1 = valid_status[2]
    status2 = valid_status[1]
    status3 = None

    # create pets with tested statuses
    for status in valid_status:
        # create pet with status
        pet = new_pet()
        pet["status"], pet["name"] = status, "my pet"

        post_pet_response = post_pet(pet)
        assert post_pet_response.status_code == 200

    # find pets by tested statuses
    statuses = [status1, status2, status3]
    get_pet_by_status_response = get_pet_by_status(status1, status2, status3)
    assert get_pet_by_status_response.status_code == 200

    # removing the "None" status from the list of tested status
    tested_statuses = []
    
    for i in statuses:
        if i != None:
            tested_statuses.append(i)
    
    # check all pets in response have correct tested statuses
    get_pet_by_status_data = get_pet_by_status_response.json()
    returned_statuses = []

    for pet in get_pet_by_status_data:
        if pet["status"] not in returned_statuses:
            returned_statuses.append(pet["status"])
        assert pet["status"] in tested_statuses, f"Incorrect status {pet["status"]} in response"

    # check all requested status with existing pets are returned
    for i in tested_statuses:
        assert (
            i in returned_statuses
        ), f"Missing at least status '{i}' in response:\nTested statuses: {tested_statuses}\nReturned statuses: {returned_statuses}"


def test_get_pet_by_status_empty():
    """
    NOTE:
    - exploited the fact "invalid" statuses don't return an error 400.
    - used a made up status ("unused status") without creating a pet to test functionality.
    - as many pets exist for all official status "available", "pending" and "sold", deleting all of them would be time consuming and disturbing other users.
    """
    # test variables
    status = [None, "available", "pending", "sold", "unused status"]
    tested_status = status[4]

    # do not create pet
    # try to find pets by tested status
    get_pet_by_status_empty_response = get_pet_by_status(tested_status)
    assert get_pet_by_status_empty_response.status_code == 200

    get_pet_by_status_empty_data = get_pet_by_status_empty_response.json()
    assert get_pet_by_status_empty_data == []


invalid_statuses = [None, "unavailable", "not so valid", "3210", "escaped"]

#@pytest.mark.skip
@pytest.mark.parametrize("invalid_status", invalid_statuses)
def test_get_pet_by_status_400(new_pet, invalid_statuses):
    """
    NOTE: gives 200 even with a status other than "available", "pending" or "sold".
    """
    # create pets with invalid_status
    response_status_codes = []

    for status in invalid_statuses:
        # create pet with invalid status
        new_pet["id"] = random.randint(1, 99999999999)
        invalid_pet = new_pet
        invalid_pet["status"], invalid_pet["name"] = status, "my invalid pet"

        post_invalid_pet_response = post_pet(invalid_pet)
        assert post_invalid_pet_response.status_code == 200

        # find pet by the invalid_status and store response status code
        get_invalid_pet_by_status_response = get_pet_by_status(status)
        response_status_codes.append(get_invalid_pet_by_status_response.status_code)

    print(response_status_codes)
    assert (
        response_status_codes[0]
        and response_status_codes[1]
        and response_status_codes[2]
        and response_status_codes[3]
        and response_status_codes[4]
    ) == 400, (
        f"Fails, at least one status code different from 400: {response_status_codes}"
    )'''


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
