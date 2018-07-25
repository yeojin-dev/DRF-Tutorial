from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SnippetListSerializer
from ..models import Snippet

__all__ = (
    'SnippetList',
    'SnippetDetail',
)


class SnippetList(APIView):
    def get(self, request, format=None):
        snippets = Snippet.objects.order_by('-created')
        serializer = SnippetListSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            snippet = Snippet.objects.get(pk=pk)
            return snippet
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = SnippetListSerializer(
            self.get_object(pk)
        )
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        snippet = self.get_object(pk)
        data = JSONParser().parse(request)
        serializer = SnippetListSerializer(snippet, data=data)

        # code 필드는 반드시 필요하기 때문에 code 값이 비어있으면 is_valid() 통과 불가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk, format=None):
        snippet = self.get_object(pk)
        data = JSONParser().parse(request)

        # PATCH 메소드와 partial=True 인자 설정으로 부분 변경 가능함
        serializer = SnippetListSerializer(snippet, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
