import json
import random

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Snippet


class SnippetListTest(APITestCase):
    """
    Snippet List 요청에 대한 테스트
    """
    @staticmethod
    def create_sample_snippets(number):
        for i in range(number):
            Snippet.objects.create(
                code="test code"
            )

    def test_snippet_list_status_code(self):
        """
        요청 결과의 HTTP 상태코드가 200인지 확인
        :return:
        """
        response = self.client.get('/snippets/django-view/snippets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_list_count(self):
        """
        Snippet List를 요청했을 때 DB의 있는 자료수와 같은 개수를 리턴하는지 테스트
        :reurn:
        """
        self.create_sample_snippets(random.randint(5, 10))
        response = self.client.get('/snippets/django-view/snippets/')
        json_data = json.loads(str(response.content, encoding='utf-8'))
        self.assertEqual(len(json_data), Snippet.objects.count())

    def test_snippet_list_order_by_created_desc(self):
        """
        Snippet List의 결과가 생성일자 내림차순인지 확인
        Model 테스트가 아닌 API 테스트이기 때문에 response를 비교함
        :return:
        """
        self.create_sample_snippets(random.randint(5, 10))
        response = self.client.get('/snippets/django-view/snippets/')
        json_data = json.loads(str(response.content, encoding='utf-8'))

        self.assertEqual(
            # JSON으로 전달받은 데이터에서 pk만 꺼낸 리스트
            [item['id'] for item in json_data],
            # DB에서 created 역순으로 pk만 가져오는 QuerySet으로 만든 리스트
            # values_list의 리턴 타입은 ValuesListQuerySet이기 때문에 lazy - 쿼리가 바로 실행되지 않음
            list(Snippet.objects.order_by('-created').values_list('pk', flat=True))
        )
