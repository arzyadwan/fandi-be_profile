from django.shortcuts import render

# Create your views here.

# MyITBlog/images/views.py

from rest_framework import viewsets
from .models import Image
from .serializers import ImageSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('-uploaded_at') # Ambil semua gambar, terbaru di atas
    serializer_class = ImageSerializer
    # Jika Anda ingin membatasi siapa yang bisa upload gambar via API,
    # Anda perlu menambahkan permissions (misal: IsAdminUser) di sini.
    # Untuk saat ini, kita biarkan default (siapapun bisa GET, admin bisa POST/PUT/DELETE)