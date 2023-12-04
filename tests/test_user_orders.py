import requests
from urls import URL
import allure


class TestUserOrders:

    @allure.title("Тест получения заказов пользователем c авторизацией")
    @allure.description(
        "Проверка успешного получения списка заказов пользователем с авторизацией. Ожидается статус 200 и подтверждение успеха в ответе.")
    def test_get_orders_with_auth_user_success(self, create_and_delete_user):
        _, access_token = create_and_delete_user
        headers = {"Authorization": access_token}
        order_response = requests.get(URL.user_order_api, headers=headers)
        assert order_response.status_code == 200
        assert order_response.json()['success'] is True

    @allure.title("Тест получения заказов пользователем без авторизации")
    @allure.description(
        "Проверка ошибки при попытке получения списка заказов пользователем без авторизации. Ожидается статус 401 и сообщение об ошибке.")
    def test_get_orders_without_auth_user_error(self):
        order_response = requests.get(URL.user_order_api)
        assert order_response.status_code == 401
        assert order_response.json()['message'] == "You should be authorised"
