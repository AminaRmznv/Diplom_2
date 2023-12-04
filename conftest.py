from faker import Faker
import pytest
import requests
from urls import URL

fake = Faker()


@pytest.fixture
def create_and_delete_user():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    response = requests.post(URL.user_creation_api, json=user_data)
    access_token = response.json().get('accessToken')
    yield user_data, access_token
    headers = {"Authorization": f"{access_token}"}
    requests.delete(URL.user_delete_api, headers=headers, json=user_data)


@pytest.fixture
def create_user_data_and_delete_after_test():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    yield user_data
    login_response = requests.post(URL.user_login_api, json=user_data)
    headers = {"Authorization": f"{login_response.json()['accessToken']}"}
    requests.delete(URL.user_delete_api, headers=headers, json=user_data)


@pytest.fixture
def user_data():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    return user_data


@pytest.fixture()
def get_ingredients():
    ingredients_response = requests.get(URL.list_of_ingredients_api)
    ingredients_data = ingredients_response.json()["data"]
    selected_ingredients = [
        ingredients_data[0]["_id"],
        ingredients_data[1]["_id"]
    ]
    order_data = {"ingredients": selected_ingredients}
    return order_data
