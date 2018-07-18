from django.urls import path

from . import views

app_name = 'snippets'
urlpatterns = [
    path(r'snippets/', views.snippet_list, name='snippet-list'),
]