import pytest
import random


@pytest.fixture
def new_pet():
    pet_id = random.randint(1, 99999999999)

    return {
        "id": pet_id,
        "category": {
            # "id": 0, # set to 0 by default server side
            "name": "test category name"
        },
        "name": "doggie",
        "photoUrls": ["my_photo_url"],
        "tags": [
            {
                # "id": 0, # set to 0 by default server side
                "name": "my tag name"
            }
        ],
        "status": "available",
    }


@pytest.fixture
def user():
    bob = {
        "id": random.randint(1, 99999999999),
        "username": "Bob" + str(random.randint(0, 10000)),
        "firstName": "Troll",
        "lastName": "Noob",
        "email": "troll.noob@email.com",
        "password": "pw123",
        "phone": "07" + str(random.randint(000000000, 999999999)),
    }
    return bob


@pytest.fixture
def updated_user():
    new_bob = {
        "firstName": "Robert",
        "lastName": "Junior",
    }
    return new_bob


@pytest.fixture
def valid_statuses():
    return ["available", "pending", "sold"]


@pytest.fixture
def tested_statuses():
    # enter statuses to test in status1, status2 and status3 fields.
    # valid statuses are: "available", "pending" and "sold".
    # enter "None" in unused fields if testing less than 3 statuses.
    status1 = "sold"
    status2 = "pending"
    status3 = None
    return [status1, status2, status3]


"""
@pytest.fixture
def invalid_statuses():
    invalid_statuses = [None, "unavailable", "not so valid", "3210", "escaped"]
    return invalid_statuses"""
