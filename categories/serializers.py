# myitblog_backend/categories/serializers.py

from rest_framework import serializers
from django.db.models import Count
from .models import Category

# Serializer dasar untuk kategori
class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'children']
        read_only_fields = ['children', 'post_count']

    # Metode untuk mendapatkan serializer untuk anak-anak
    def get_children(self, obj):
        # TAMBAHKAN .order_by('name') DI SINI
        children_queryset = obj.children.all().annotate(post_count=Count('articles')).order_by('name') 
        return CategorySerializer(children_queryset, many=True).data

# Serializer hierarkis yang hanya mengembalikan kategori tingkat atas
class CategoryHierarchicalSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'children']
        read_only_fields = ['children', 'post_count']

    def get_children(self, obj):
        # TAMBAHKAN .order_by('name') DI SINI
        children_queryset = obj.children.all().annotate(post_count=Count('articles')).order_by('name')
        return CategoryHierarchicalSerializer(children_queryset, many=True).data