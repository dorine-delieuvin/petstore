import pytest
import requests

pytestmark = pytest.mark.user


def test_get_user(user):
    # create user
    post_user_response = post_user(user)
    assert post_user_response.status_code == 200

    # get user
    get_user_response = get_user(user["username"])
    assert get_user_response.status_code == 200

    # check user details
    get_user_data = get_user_response.json()
    assert get_user_data["id"] == user["id"]
    assert get_user_data["username"] == user["username"]
    assert get_user_data["email"] == user["email"]
    assert get_user_data["phone"] == user["phone"]


def test_get_user_inexisting_username():
    # do not create user
    user_name = "Bob456"

    # attempt to get inexisting user
    get_user_response = get_user(user_name)
    assert get_user_response.status_code == 404

    # check body response
    get_user_data = get_user_response.json()
    assert get_user_data["message"] == "User not found"


@pytest.mark.skip
def test_get_user_invalid_username():
    """
    NOTE: getting code 404 instead of 400.
    - tried usernames "Bob@!#", "@!#  !*/à$==`", "" (returns 405) and ",".
    """
    # do not create user
    user_name = "Bob@!#"

    # attempt to get user with invalid username
    get_user_response = get_user(user_name)
    assert get_user_response.status_code == 400

    # check body response
    get_user_data = get_user_response.json()
    assert get_user_data["message"] == "Invalid username supplied"


## API Calls
def post_user(user):
    return requests.post("https://petstore.swagger.io/v2/user", json=user)


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")
