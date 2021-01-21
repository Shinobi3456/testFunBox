from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
import time
import redis


class VisitedLinksTests(APITestCase):

    def test_method_get(self):
        """Проверяем доступность метода GET"""
        response = self.client.get('/api/visited_links', format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {'status': 'Method "GET" not allowed.'})

    def test_empty_data(self):
        """Проверка если не передали данные"""
        response = self.client.post('/api/visited_links', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'Expecting value: line 1 column 1 (char 0)'})

    def test_incorrect_link(self):
        """Не валидный запрос ссылки"""
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        data = {"links": [
            "https://ya.ru",
            "https:\/ya.ru?q=123",
            "https://funbox.ru",
            "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"
        ]}

        from_time = time.time()
        response = self.client.post('/api/visited_links', data, format='json')
        to_time = time.time()

        visited = redis_instance.zrangebylex('visited', f'[{from_time}', f'[{to_time}')
        links = []
        for row in visited:
            links.append(str(row).split('--')[1][:-1])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'Incorrect links: https:\\/ya.ru?q=123'})
        self.assertEqual(len(visited), 3)
        self.assertEqual(links, ["https://ya.ru", "https://funbox.ru",
                                 "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"])

    def test_less_links(self):
        """Тест на для проверки если отсутвует links в запросе"""
        data = {"links_test": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "https://funbox.ru",
            "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"
        ]}

        response = self.client.post('/api/visited_links', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': "Not find 'links'."})

    def test_links_type_list(self):
        """Тест что links это list"""
        data = {"links": 'test'}
        response = self.client.post('/api/visited_links', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': "Links must be of type list."})

    def test_correct_request(self):
        """Тест кооректный запрос"""
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        data = {"links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "https://funbox.ru",
            "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"
        ]}

        from_time = time.time()
        response = self.client.post('/api/visited_links', data, format='json')
        to_time = time.time()

        visited = redis_instance.zrangebylex('visited', f'[{from_time}', f'[{to_time}')
        links = []
        for row in visited:
            links.append(str(row).split('--')[1][:-1])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'ok'})
        self.assertEqual(len(visited), 4)
        self.assertEqual(links, ["https://ya.ru", "https://ya.ru?q=123", "https://funbox.ru",
                                 "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"])


class VisitedDomainsTests(APITestCase):

    def test_method_post(self):
        """Проверяем доступность метода POST"""
        response = self.client.post('/api/visited_domains', format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {'status': 'Method "POST" not allowed.'})

    def test_less_params(self):
        """Проверка если не передали параметры или некорректные"""
        response = self.client.get('/api/visited_domains', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'No "from" or "to" parameters specified'})

    def test_param_from_is_not_digit(self):
        """Поведение если в качестве параметра from передано не число"""
        from_time = 'num32'
        to_time = 1610604705

        response = self.client.get(f'/api/visited_domains?from={from_time}&to={to_time}', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'From must be a number'})

    def test_param_to_is_not_digit(self):
        """Поведение если в качестве параметра to передано не число"""
        from_time = 1610603441
        to_time = 'num32'

        response = self.client.get(f'/api/visited_domains?from={from_time}&to={to_time}', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'From must be a number'})

    def test_correct_request(self):
        """Проверяем выполнение корректного запроса"""
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        links = [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "https://funbox.ru",
            "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"
        ]

        from_time = str(time.time())
        for link in links:
            redis_instance.zadd('visited', {f'{str(time.time())}--{link}': 0})
        to_time = str(time.time()+1)

        response = self.client.get(f'/api/visited_domains?from={from_time.split(".")[0]}&to={to_time.split(".")[0]}',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {"domains": set(["ya.ru", "funbox.ru", "stackoverflowdsfsdfds.com"]), "status": "ok"})
