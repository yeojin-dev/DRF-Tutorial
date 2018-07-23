from django.urls import path, include

from . import django_view, api_view

app_name = 'snippets'

urlpatterns = [
    path('django-view/', include(django_view)),
    path('api-view/', include(api_view))
]
