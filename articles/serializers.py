# myitblog_backend/articles/serializers.py

from rest_framework import serializers
from django.db.models import F, Q
from .models import Article
from categories.serializers import CategoryHierarchicalSerializer # Pastikan ini diimpor dengan benar
from tags.serializers import TagSerializer
from images.serializers import ImageSerializer


class ArticleSerializer(serializers.ModelSerializer):
    categories = CategoryHierarchicalSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    # Field BARU untuk Navigasi Kontekstual
    previous_article = serializers.SerializerMethodField()
    next_article = serializers.SerializerMethodField()


    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'summary', 'markdown_content',
            'published_date', 'updated_date', 'is_published',
            'author_username', 'categories', 'tags', 'featured_image_url',
            'previous_article', 'next_article' # Tambahkan field baru di sini
        ]
        read_only_fields = ['id', 'published_date', 'updated_date', 'author_username']

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.featured_image.image_file.url)
            return obj.featured_image.image_file.url
        return None

    # Method untuk mendapatkan artikel SEBELUM artikel saat ini (Perbaikan Final)
    def get_previous_article(self, obj):
        try:
            # Logic: Cari artikel yang (Tanggal < Tanggal Sekarang) ATAU (Tanggal SAMA dan ID < ID Sekarang)
            prev_article = Article.objects.filter(
                Q(published_date__lt=obj.published_date) | 
                Q(published_date=obj.published_date, id__lt=obj.id)
            ).order_by('-published_date', '-id').first()
            
            if prev_article:
                return {
                    'title': prev_article.title,
                    'slug': prev_article.slug,
                }
            return None
        except:
            return None

    # Method untuk mendapatkan artikel SESUDAH artikel saat ini (Simple logic yang sudah diverifikasi)
    def get_next_article(self, obj):
        try:
            # Menggunakan published_date__gt yang Anda verifikasi bekerja
            next_article = Article.objects.filter(
                published_date__gt=obj.published_date
            ).order_by('published_date').first()
            
            if next_article:
                return {
                    'title': next_article.title,
                    'slug': next_article.slug,
                }
            return None
        except:
            return None