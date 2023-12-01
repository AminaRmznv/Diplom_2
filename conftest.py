from faker import Faker
import pytest
import requests
from urls import URL
import allure

fake = Faker()


@allure.step("фикстура для создания и удаления пользователя")
@pytest.fixture
def create_and_delete_user():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    response = requests.post(URL.user_creation_api, json=user_data)
    access_token = response.json().get('accessToken')
    yield user_data
    headers = {"Authorization": f"{access_token}"}
    delete_response = requests.delete(URL.user_delete_api, headers=headers, json=user_data)
    assert delete_response.status_code == 202


@allure.step("фикстура: Создание пользователя с аутентификацией и его удаление")
@pytest.fixture
def create_with_auth_and_delete_user():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    response = requests.post(URL.user_creation_api, json=user_data)
    access_token = response.json().get('accessToken')
    yield user_data, access_token
    headers = {"Authorization": f"{access_token}"}
    delete_response = requests.delete(URL.user_delete_api, headers=headers, json=user_data)
    assert delete_response.status_code == 202


@allure.step("фикстура: Регистрация и удаление пользователя")
@pytest.fixture
def register_and_delete_user():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    yield user_data
    login_response = requests.post(URL.user_login_api, json=user_data)
    headers = {"Authorization": f"{login_response.json()['accessToken']}"}
    delete_response = requests.delete(URL.user_delete_api, headers=headers, json=user_data)
    assert delete_response.status_code == 202


@allure.step("фикстура: Получение данных пользователя")
@pytest.fixture
def user_data():
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }
    return user_data
