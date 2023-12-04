import requests
from urls import URL
from faker import Faker
import allure

fake = Faker()


class TestUserChanges:

    @allure.title("Тест обновления электронной почты пользователя с авторизацией")
    @allure.description(
        "Проверка успешного обновления электронной почты пользователя при наличии авторизации.")
    def test_update_user_email_with_auth_success(self, create_and_delete_user):
        user_data, access_token = create_and_delete_user
        headers = {"Authorization": access_token}
        user_data['email'] = fake.email()
        update_response = requests.patch(URL.user_change_api, json=user_data, headers=headers)
        assert update_response.status_code == 200
        assert update_response.json()['success'] is True

    @allure.title("Тест обновления имени пользователя с авторизацией")
    @allure.description(
        "Проверка успешного обновления имени пользователя при наличии авторизации.")
    def test_update_user_name_with_auth_success(self, create_and_delete_user):
        user_data, access_token = create_and_delete_user
        headers = {"Authorization": access_token}
        user_data['name'] = "New Name"
        update_response = requests.patch(URL.user_change_api, json=user_data, headers=headers)
        assert update_response.status_code == 200
        assert update_response.json()['success'] is True

    @allure.title("Тест обновления пароля пользователя с авторизацией")
    @allure.description(
        "Проверка успешного обновления пароля пользователя при наличии авторизации.")
    def test_update_user_password_with_auth_success(self, create_and_delete_user):
        user_data, access_token = create_and_delete_user
        headers = {"Authorization": access_token}
        user_data['password'] = "newpassword"
        update_response = requests.patch(URL.user_change_api, json=user_data, headers=headers)
        assert update_response.status_code == 200
        assert update_response.json()['success'] is True

    @allure.title("Тест обновления электронной почты пользователя без авторизации")
    @allure.description(
        "Проверка получения ошибки при попытке обновления электронной почты пользователя без наличия авторизации.")
    def test_update_user_email_without_auth_error(self, create_and_delete_user):
        user_data, _ = create_and_delete_user
        user_data['email'] = fake.email()
        update_response = requests.patch(URL.user_change_api, json=user_data)
        assert update_response.status_code == 401
        assert "You should be authorised" in update_response.text

    @allure.title("Тест обновления имени пользователя без авторизации")
    @allure.description("Проверка получения ошибки при попытке обновления имени пользователя без наличия авторизации.")
    def test_update_user_name_without_auth_error(self, create_and_delete_user):
        user_data, _ = create_and_delete_user
        user_data['name'] = fake.name()
        update_response = requests.patch(URL.user_change_api, json=user_data)
        assert update_response.status_code == 401
        assert "You should be authorised" in update_response.text

    @allure.title("Тест обновления пароля пользователя без авторизации")
    @allure.description("Проверка получения ошибки при попытке обновления пароля пользователя без наличия авторизации.")
    def test_update_user_password_without_auth_error(self, create_and_delete_user):
        user_data, _ = create_and_delete_user
        user_data['password'] = fake.password()
        update_response = requests.patch(URL.user_change_api, json=user_data)
        assert update_response.status_code == 401
        assert "You should be authorised" in update_response.text
