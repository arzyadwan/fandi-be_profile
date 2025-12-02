from django.shortcuts import render

# Create your views here.

# MyITBlog/tags/views.py

from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name') # Ambil semua tag, urutkan berdasarkan nama
    serializer_class = TagSerializer
    lookup_field = 'slug' # Menggunakan slug sebagai lookup field untuk URL