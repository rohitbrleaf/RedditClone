from rest_framework import serializers
from .models import Post , Vote

class PostsSeriaizer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")
    class Meta:
        model = Post
        fields = ['id','title','url','poster','poster_id','created_at']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']