import json
import random
import string

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from snippets.serializers import UserListSerializer
from .models import Snippet

User = get_user_model()


def get_dummy_user():
    dummy_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return User.objects.create_user(username=dummy_username)


class SnippetListTest(APITestCase):
    """
    Snippet List 요청에 대한 테스트
    """
    URL = '/snippets/generic-cbv/snippets/'

    @staticmethod
    def create_sample_snippets(number):
        for i in range(number):
            Snippet.objects.create(
                code="test code",
                owner=get_dummy_user(),
            )

    def test_snippet_list_status_code(self):
        """
        요청 결과의 HTTP 상태코드가 200인지 확인
        :return:
        """
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_snippet_list_count(self):
        """
        Snippet List를 요청했을 때 DB의 있는 자료수와 같은 개수를 리턴하는지 테스트
        :reurn:
        """
        self.create_sample_snippets(random.randint(5, 10))
        response = self.client.get(self.URL)
        json_data = json.loads(str(response.content, encoding='utf-8'))
        self.assertEqual(json_data['count'], Snippet.objects.count())

    def test_snippet_list_order_by_created_desc(self):
        """
        Snippet List의 결과가 생성일자 내림차순인지 확인
        Model 테스트가 아닌 API 테스트이기 때문에 response를 비교함
        :return:
        """
        self.create_sample_snippets(random.randint(5, 10))

        pk_list = list()
        page = 1

        while True:
            response = self.client.get(self.URL, {'page': page})
            data = json.loads(response.content)
            pk_list += [item['pk'] for item in data['results']]
            if data['next']:
                page += 1
            else:
                break

        self.assertEqual(
            pk_list,
            # DB에서 created 역순으로 pk만 가져오는 QuerySet으로 만든 리스트
            # values_list의 리턴 타입은 ValuesListQuerySet이기 때문에 lazy - 쿼리가 바로 실행되지 않음
            list(Snippet.objects.order_by('-created').values_list('pk', flat=True))
        )


class SnippetCreateTest(APITestCase):
    URL = '/snippets/generic-cbv/snippets/'

    def test_snippet_create_status_code(self):
        """
        201이 들어오는지
        :return:
        """
        user = get_dummy_user()
        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.URL,
            data={
                'code': "print('hello, world!')"
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_snippet_create_save_db(self):
        """
        요청 후 실제 DB에 저장되었는지(모든 필드값이 정상적으로 저장되었는지)
        :return:
        """
        snippet_data = {
            'title': 'SnippetTitle',
            'code': 'SnippetCode',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }
        user = get_dummy_user()
        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)

        check_fields = [
            'title',
            'linenos',
            'language',
            'style',
        ]

        for field in check_fields:
            self.assertEqual(data[field], snippet_data[field])

        self.assertEqual(
            data['owner'],
            UserListSerializer(user).data
        )

    def test_snippet_create_missing_code_raise_exception(self):
        """
        'code'데이터가 주어지지 않을 경우 적절한 Exception이 발생하는지
        :return:
        """
        # code만 주어지지 않은 데이터
        snippet_data = {
            'title': 'SnippetTitle',
            'linenos': True,
            'language': 'c',
            'style': 'monokai',
        }
        user = get_dummy_user()
        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.URL,
            data=snippet_data,
            format='json',
        )

        # code가 주어지지 않으면 HTTP상태코드가 400이어야 함
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
