from django.contrib import admin

# Register your models here.

# myitblog_backend/categories/admin.py

from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent') # Tambahkan 'parent' di sini
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('parent',) # Tambahkan filter berdasarkan parent