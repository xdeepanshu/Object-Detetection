from django.apps import apps
from .serializers import PhotosSerializer, UsersSerializer
from rest_framework import generics
from django.contrib.auth.models import User


Photo = apps.get_model('detect','Photo')

class ListPhotosView(generics.ListAPIView):
	"""
	To access all the photos.
	"""
	queryset = Photo.objects.all()
	serializer_class = PhotosSerializer

class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer