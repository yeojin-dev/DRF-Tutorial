from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from ..models import Snippet
from ..serializers import (
    UserListSerializer,
    SnippetDetailSerializer,
    SnippetListSerializer,
)

User = get_user_model()

__all__ = (
    'SnippetList',
    'SnippetDetail',
    'UserList',
    'UserDetail',
)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SnippetListSerializer
        elif self.request.method == 'POST':
            return SnippetDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetDetailSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
