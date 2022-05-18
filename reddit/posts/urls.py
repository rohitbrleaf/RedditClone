from django.urls import path
from .views import *

urlpatterns = [
    path('/',PostListCreateView.as_view(),name="posts"),
    path('/<int:pk>/vote',VoteCreateView.as_view(),name="vote"),
    path('/<int:pk>/posts',PostUpdateDeleteView.as_view(),name="RUD")
]