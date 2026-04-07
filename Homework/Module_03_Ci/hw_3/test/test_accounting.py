import unittest

# from accounting import app
# from accounting import storage
from Module_03.homework.hw3.accounting import app
from Module_03.homework.hw3.accounting import storage
from Module_03.homework.hw3.accounting import add
from Module_03.homework.hw3.accounting import calculate_month


class TestAccounting(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = app.test_client()

        # Инициализация данных
        storage.update({
            2023: {1: {1: 100, 'month_total': 100}, 'year_total': 100},
            2024: {4: {4: 200, 5: 300, 'month_total': 500}, 'year_total': 500}
        })

    def test_add_correct(self):
        responce = self.app.get('/add/20240506/200')
        self.assertEqual(responce.status_code, 200)

    def test_add_type_error(self):
        with self.assertRaises(TypeError):
            add('yymmdd')

    # для этого теста в основном пролижении функции add()
    # закомментируем блок try-ecxept
    def test_add_value_error(self):
        with self.assertRaises(ValueError):
            # передадим не существующую дату
            add('20240232', 200)


    # ===========================================================================
    def test_calculate_year(self):
        responce = self.app.get('/calculate/2023')  # 100
        self.assertEqual(responce.status_code, 200)

    # если в `storage` ничего нет:
    def test_calculate_year_empty_storage(self):
        storage.clear()
        response = self.app.get('/calculate/2023')
        response_text = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn('В эту дату нет трат!', response_text)


    # ===========================================================================
    def test_calculate_month(self):
        responce = self.app.get('/calculate/2024/04')   #500
        self.assertEqual(responce.status_code, 200)

    # введем дату, которой нет в `storage`
    def test_calculate_month_key_error(self):
        with self.assertRaises(KeyError):
            calculate_month(1900, 300)

    # если в `storage` ничего нет:
    def test_calculate_month_empty(self):
        storage.clear()
        responce = self.app.get('/calculate/2024/04')
        self.assertEqual(responce.status_code, 500)