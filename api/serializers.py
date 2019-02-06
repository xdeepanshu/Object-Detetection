from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import User

Photo = apps.get_model('detect','Photo')


class PhotosSerializer(serializers.ModelSerializer):
	class Meta:
		model = Photo
		fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'