from django.contrib import admin

# Register your models here.

# myitblog_backend/images/admin.py

from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image_file', 'uploaded_at')
    search_fields = ('caption', 'alt_text')
    list_filter = ('uploaded_at',)