from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post

class UserSerializers(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    class Meta:
        model = User
        fields = ['id','username','posts']


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = ['id','title','body','owner']

