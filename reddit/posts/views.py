from django.shortcuts import render
from .models import Post , Vote
from rest_framework import generics , permissions , mixins , status
from rest_framework.response import Response
from .serializers import PostsSeriaizer, VoteSerializer
from rest_framework.exceptions import ValidationError

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSeriaizer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(poster=self.request.user)


class PostUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostsSeriaizer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,*args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.filter(pk=pk,poster=self.request.user)
        if post.exists():
            self.destroy(request,*args,**kwargs)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("you cannot delete someone's post")
    
    def put(self,request,*args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.filter(pk=pk,poster=self.request.user)
        if post.exists():
            self.update(request,*args,**kwargs)
            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ValidationError("you cannot update someone's post")
    
class VoteCreateView(generics.CreateAPIView , mixins.DestroyModelMixin):
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
    
    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("you never voted for this post")
