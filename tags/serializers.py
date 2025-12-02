# myitblog_backend/tags/serializers.py

from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count'] # Tambahkan 'post_count'
        read_only_fields = ['post_count']