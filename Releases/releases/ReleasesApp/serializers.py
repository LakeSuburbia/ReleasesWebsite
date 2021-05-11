from rest_framework import serializers
from .models import Release, ReleaseScore, User


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = ["release_date", "title", "artist"]

    def create(self, validated_data):
        release = Release.objects.create(
            release_date=validated_data["release_date"],
            title=validated_data["title"],
            artist=validated_data["artist"],
        )
        return release


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseScore
        fields = ["user", "release", "score"]

    def create(self, validated_data):
        score = ReleaseScore.objects.create(
            user=User.objects.filter(username__iexact=validated_data["user"]),
            release=Release.objects.filter(title_iexact=validated_data["release"]),
            score=validated_data["score"],
        )
        return score
