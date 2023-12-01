import requests
from urls import URL
import pytest
from faker import Faker
import allure

fake = Faker()


class TestUserChanges:

    @pytest.mark.parametrize('field_to_update', ['password', 'name', 'email'])
    @allure.title("Тест обновления данных пользователя с авторизацией")
    @allure.description(
        "Проверка успешного обновления данных пользователя (пароля, имени или электронной почты) при наличии авторизации.")
    def test_update_user_with_auth_success(self, field_to_update, create_with_auth_and_delete_user):
        user_data, access_token = create_with_auth_and_delete_user
        headers = {"Authorization": access_token}
        if field_to_update == "email":
            user_data['email'] = fake.email()
        elif field_to_update == "name":
            user_data['name'] = "New Name"
        elif field_to_update == "password":
            user_data['password'] = "newpassword"
        update_response = requests.patch(URL.user_change_api, json=user_data, headers=headers)
        assert update_response.status_code == 200
        assert update_response.json()['success'] is True

    @pytest.mark.parametrize('field_to_update', ['password', 'name', 'email'])
    @allure.title("Тест обновления данных пользователя без авторизации")
    @allure.description("""
    Проверка получения ошибки при попытке обновления данных пользователя (пароля, имени или электронной почты) без наличия авторизации.
    """)
    def test_update_user_without_auth_error(self, field_to_update, create_and_delete_user):
        user_data = create_and_delete_user
        if field_to_update == "email":
            user_data['email'] = fake.email()
        elif field_to_update == "name":
            user_data['name'] = "New Name"
        elif field_to_update == "password":
            user_data['password'] = "newpassword"
        update_response = requests.patch(URL.user_change_api, json=user_data)
        assert update_response.status_code == 401
        assert "You should be authorised" in update_response.text
