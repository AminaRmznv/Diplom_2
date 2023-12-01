import requests
from urls import URL
import allure


class TestUserLogin:

    @allure.title("Тест входа в систему зарегистрированным пользователем")
    @allure.description(
        "Проверка успешного входа в систему зарегистрированным пользователем. Ожидается получение статуса 200 и подтверждение успеха в ответе.")
    def test_login_with_registered_user_success(self, create_and_delete_user):
        user_data = create_and_delete_user
        login_response = requests.post(URL.user_login_api, json=user_data)
        assert login_response.status_code == 200
        assert login_response.json()['success'] is True

    @allure.title("Тест входа в систему с невалидными данными")
    @allure.description(
        "Проверка ошибки входа в систему с использованием невалидных данных. Ожидается получение статуса 401 и сообщения об ошибке.")
    def test_login_with_invalid_data_error(self, create_and_delete_user):
        user_data = create_and_delete_user.copy()
        user_data['email'] = 'fakelogin@gmail.com'
        login_response = requests.post(URL.user_login_api, json=user_data)
        assert login_response.status_code == 401
        assert 'email or password are incorrect' in login_response.text
