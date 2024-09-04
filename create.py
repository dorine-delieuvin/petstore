import requests
import random


def new_pet(
    pet_name="doggie",
    status="available",
    category_name="test category name",
    photo_url="my_photo_url",
    tag_name="my tag name",
    pet_id=random.randint(1, 99999999999),
):

    pet = {
        "id": pet_id,
        "category": {
            # "id": 0, # set to 0 by default server side
            "name": category_name
        },
        "name": pet_name,
        "photoUrls": [photo_url],
        "tags": [
            {
                # "id": 0, # set to 0 by default server side
                "name": tag_name
            }
        ],
        "status": status,
    }

    post_pet_response = requests.post("https://petstore.swagger.io/v2/pet", json=pet)
    post_pet_data = post_pet_response.json()

    # pet[0] == status code; pet[1] == pet_data
    return post_pet_response.status_code, post_pet_data


def new_order(pet_id=9223372036854775807, order_id=random.randint(1, 99999999999)):

    order = {
        "id": order_id,
        "petId": pet_id,
        "quantity": 1,
        # "shipDate": "2024-08-23T13:54:01.624Z",
        "status": "placed",
        "complete": True,
    }
    post_order_response = requests.post(
        "https://petstore.swagger.io/v2/store/order", json=order
    )
    post_order_data = post_order_response.json()

    # order[0] == status code; order[1] == order_data
    return post_order_response.status_code, post_order_data


def new_user(
    user_id=random.randint(1, 99999999999),
    user_name="Bob" + str(random.randint(0, 10000)),
    first_name="Troll",
    last_name="Noob",
    email="troll.noob@email.com",
    password="p",
    phone="07" + str(random.randint(000000000, 999999999)),
    user_status=1,
):
    user = {
        "id": user_id,
        "username": user_name,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
        "phone": phone,
        "userStatus": user_status,
    }

    post_user_response = requests.post("https://petstore.swagger.io/v2/user", json=user)

    # user[0] == status code; user[1] == user
    return post_user_response.status_code, user


if __name__ == "__main__":
    print(new_pet(), new_order(), new_user())
