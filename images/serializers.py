# myitblog_backend/images/serializers.py

from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    # field 'image_file' akan otomatis dihandle oleh ModelSerializer
    # karena itu adalah ImageField/FileField
    class Meta:
        model = Image
        fields = '__all__' # Mengikutkan semua field dari model Image
        # Atau Anda bisa spesifik: fields = ['id', 'image_file', 'caption', 'alt_text', 'uploaded_at']