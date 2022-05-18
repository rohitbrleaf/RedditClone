from django.shortcuts import render
from .models import Post , Vote
from rest_framework import generics , permissions
from .serializers import PostsSeriaizer, VoteSerializer
from rest_framework.exceptions import ValidationError

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSeriaizer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(poster=self.request.user)


class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        user = self.request.user

        return Vote.objects.filter(post=post,voter=user)
    
    def perform_create(self,serializer):
        if self.get_queryset().exists():
            raise ValidationError("you cannot vote this post more than once")
        serializer.save(voter=self.request.user , post=Post.objects.get(pk=self.kwargs['pk']))