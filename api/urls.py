from django.urls import path, include
from .views import ListPhotosView, ListUsersView

urlpatterns = [
    path('photos/',ListPhotosView.as_view(), name="photo-view"),
]
