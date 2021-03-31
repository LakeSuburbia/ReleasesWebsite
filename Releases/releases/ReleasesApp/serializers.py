from rest_framework import serializers
from .models import User, Release

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Release
        fields = ['release_date', 'title', 'artist']
