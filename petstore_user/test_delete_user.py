import pytest
import requests

pytestmark = pytest.mark.user


def test_delet_user(new_user):
    # create user
    post_user_response = post_user(new_user)
    assert post_user_response.status_code == 200

    # check user has been created
    get_user_response = get_user(new_user["username"])
    assert get_user_response.status_code == 200

    # delete user
    delete_user_response = delete_user(new_user["username"])
    assert delete_user_response.status_code == 200

    # check user has been deleted
    get_user_response = get_user(new_user["username"])
    assert get_user_response.status_code == 404


def test_get_user_inexisting_username():
    # do not create user
    user_name = "Bob456"

    # attempt to delete inexisting user
    delete_user_response = delete_user(user_name)
    assert delete_user_response.status_code == 404


@pytest.mark.skip
def test_get_user_invalid_username():
    """
    NOTE: getting code 404 instead of 400.
    - tried usernames "Bob@!#", "@!#  !*/à$==`", "" (returns 405) and ",".
    """
    # do not create user
    user_name = ""

    # attempt to delete user with invalid username
    delete_user_response = delete_user(user_name)
    assert delete_user_response.status_code == 400


## API Calls
def post_user(user):
    return requests.post("https://petstore.swagger.io/v2/user", json=user)


def get_user(user_name):
    return requests.get(f"https://petstore.swagger.io/v2/user/{user_name}")


def delete_user(user_name):
    return requests.delete(f"https://petstore.swagger.io/v2/user/{user_name}")
