import unittest


from Module_03.homework.hw1.hello_word_with_day import app
from freezegun import freeze_time


class TestHelloWordWithDay(unittest.TestCase):
    """
    TestHelloWordWithDay является подклассом unittest.TestCase,
    что обеспечивает его совместимость с фреймворком для автоматизированного
    тестирования unittest.
    """
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_has_username(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)


    # заморозим день 2024-04-01 - понедельник:
    @freeze_time('2024-04-01')
    def test_monday(self):
        response = self.app.get(self.base_url + 'username')
        response_text = response.data.decode()
        expected_greeting = 'Хорошего понедельника'
        self.assertIn(expected_greeting, response_text)

    @freeze_time('2024-04-05')
    def test_fryday(self):
        response = self.app.get(self.base_url + 'username')
        response_text = response.data.decode()
        expected_greeting = 'Хорошей пятницы'
        self.assertIn(expected_greeting, response_text)

    @freeze_time('2024-04-06')
    def test_saturday(self):
        response = self.app.get(self.base_url + 'username')
        response_text = response.data.decode()
        expected_greeting = 'Хорошей субботы'
        self.assertIn(expected_greeting, response_text)