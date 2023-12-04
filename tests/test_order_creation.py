import requests
from urls import URL
import allure


class TestOrderCreation:

    @allure.title("Тест создания заказа с аутентификацией")
    @allure.description(
        "Проверка успешного создания заказа при наличии аутентификации пользователя. Ожидается, что заказ будет создан и в ответе будет Success.")
    def test_create_order_with_authentication_success(self, create_and_delete_user, get_ingredients):
        _, access_token = create_and_delete_user
        order_data = get_ingredients
        headers = {"Authorization": access_token}
        order_response = requests.post(URL.create_order_api, json=order_data, headers=headers)
        assert order_response.status_code == 200
        assert order_response.json()['success'] is True
        assert 'order' in order_response.json()

    @allure.title("Тест создания заказа без аутентификации")
    @allure.description(
        "Проверка создания заказа без аутентификации пользователя")
    def test_create_order_without_authentication_success(self, get_ingredients):
        order_data = get_ingredients
        order_response = requests.post(URL.create_order_api, json=order_data)
        assert 'success' in order_response.text
        assert 'order' in order_response.text

    @allure.title("Тест создания заказа без ингредиентов")
    @allure.description(
        "Проверка ошибки при попытке создания заказа без указания ингредиентов. Ожидается получение статуса ошибки и сообщения об отсутствии ингредиентов.")
    def test_create_order_without_ingredients_error(self, create_and_delete_user):
        _, access_token = create_and_delete_user
        headers = {"Authorization": access_token}
        order_data = {"ingredients": []}
        order_response = requests.post(URL.create_order_api, json=order_data, headers=headers)
        assert order_response.status_code == 400
        assert order_response.json()['message'] == "Ingredient ids must be provided"

    @allure.title("Тест создания заказа с невалидными ингредиентами")
    @allure.description(
        "Проверка ошибки при создании заказа с невалидным идентификатором ингредиентов. Ожидается получение статуса ошибки сервера.")
    def test_create_order_invalid_ingredient_hash_error(self):
        invalid_data = {"ingredients": [1, 2]}
        order_response = requests.post(URL.create_order_api, json=invalid_data)
        assert order_response.status_code == 500
