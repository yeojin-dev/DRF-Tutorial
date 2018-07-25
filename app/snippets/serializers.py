from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Snippet

User = get_user_model()

__all__ = (
    'UserSerializer',
    'SnippetSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'snippets',
        ]


class SnippetSerializer(serializers.ModelSerializer):
    # ReadOnlyField - 입력은 JSON 외부에서 받지만(유효성 검사 제외) 읽어들일 때는 필요함
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = [
            'id',
            'title',
            'code',
            'linenos',
            'language',
            'style',
            'owner',
        ]

        # 아래와 같이 설정하면 JSON에는 id가 나옴 - owner가 외래키이기 때문
        # read_only_fields = [
        #     'owner',
        # ]