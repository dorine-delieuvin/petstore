import pytest
import random


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
