from django.shortcuts import render
from rest_framework import generics,permissions
from . import serializers
from .permissions import *
from django.contrib.auth.models import User
from .models import Post

#USERS=======================
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializers

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializers

#POST=======================
class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerReadOnly]


