from django.urls import path, include

app_name = 'snippets'

urlpatterns = [
    path('django-view/', include('snippets.urls.django_view'))
]
