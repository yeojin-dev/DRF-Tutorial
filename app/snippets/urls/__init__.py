from django.urls import path, include

from . import django_view, api_view, mixins, generic_cbv, viewsets_router

app_name = 'snippets'

urlpatterns = [
    path('django-view/', include(django_view)),
    path('mixins/', include(mixins)),
    path('api-view/', include(api_view)),
    path('generic-cbv/', include(generic_cbv)),
    path('viewsets-router/', include(viewsets_router)),
]
