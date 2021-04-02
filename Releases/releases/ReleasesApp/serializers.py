from rest_framework import serializers
from .models import User, Release

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password = validated_data['password']
        )
        return user


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Release
        fields = ['release_date', 'title', 'artist']

    def create(self, validated_data):
        release = Release.objects.create(
            release_date=validated_data['release_date'],
            title=validated_data['title'],
            artist=validated_data['artist'],
        )
        return release
