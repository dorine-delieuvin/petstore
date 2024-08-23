import requests
import random
import datetime


def new_order(pet_id=9223372036854775807):
    order_id = random.randint(1, 99999999999)

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
    assert post_order_response.status_code == 200
    post_order_data = post_order_response.json()
    return post_order_data


if __name__ == "__main__":
    new_order()
