from django.contrib import admin

# Register your models here.

# myitblog_backend/articles/admin.py

from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published', 'updated_date')
    list_filter = ('is_published', 'categories', 'tags', 'author')
    search_fields = ('title', 'markdown_content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    raw_id_fields = ('author', 'featured_image') # Mempermudah pemilihan objek terkait
    filter_horizontal = ('categories', 'tags') # Tampilan lebih baik untuk ManyToMany