from django.urls import path, include
from .views import list_view, upload

urlpatterns = [
    path('', list_view),
    path(r'list/', list_view, name='list'),
    path(r'upload/', upload, name='upload'),
]
