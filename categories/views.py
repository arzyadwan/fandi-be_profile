from django.shortcuts import render

# Create your views here.

# MyITBlog/categories/views.py

from rest_framework import viewsets
from django.db.models import Count
from .models import Category
from .serializers import CategoryHierarchicalSerializer # Perbarui import

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # Hanya ambil kategori tingkat atas (yang tidak punya parent)
    queryset = Category.objects.filter(parent__isnull=True).annotate(post_count=Count('articles')).order_by('name')
    serializer_class = CategoryHierarchicalSerializer
    lookup_field = 'slug'
