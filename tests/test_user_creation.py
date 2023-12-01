import requests
from urls import URL
import allure


class TestUserCreation:

    @allure.title("Тест создания пользователя с валидными данными")
    @allure.description(
        "Проверка успешного создания пользователя с валидными данными. Ожидается получение статуса 200 и подтверждение успеха в ответе.")
    def test_create_user_with_valid_data_success(self, register_and_delete_user):
        user_data = register_and_delete_user
        response = requests.post(URL.user_creation_api, json=user_data)
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title("Тест создания существующего пользователя")
    @allure.description(
        "Проверка ошибки при попытке создания уже существующего пользователя. Ожидается получение статуса 403 и соответствующего сообщения об ошибке.")
    def test_create_existing_user_error(self, register_and_delete_user):
        user_data = register_and_delete_user
        requests.post(URL.user_creation_api, json=user_data)
        response = requests.post(URL.user_creation_api, json=user_data)
        assert response.status_code == 403
        assert 'User already exists' in response.json()['message']

    @allure.title("Тест создания пользователя с отсутствующим полем")
    @allure.description(
        "Проверка ошибки при создании пользователя без одного из обязательных полей (например, email). Ожидается получение статуса 403 и сообщения о необходимости всех полей.")
    def test_create_user_with_missing_field_error(self, user_data):
        user_data.pop('email')
        response = requests.post(URL.user_creation_api, json=user_data)
        assert response.status_code == 403
        assert 'Email, password and name are required fields' in response.json()['message']
