from rest_framework import serializers
from .models import Post , Vote

class PostsSeriaizer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source="poster.username")
    poster_id = serializers.ReadOnlyField(source="poster.id")
    votes = serializers.SerializerMethodField('get_votes')

    def get_votes(self,obj):
        return Vote.objects.filter(post=obj).count()
    class Meta:
        model = Post
        fields = ['id','title','url','poster','votes','poster_id','created_at']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']