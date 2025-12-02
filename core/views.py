# myitblog_backend/core/views.py (Kode Final dan Lengkap)

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination # Import Paginasi
from rest_framework.exceptions import NotFound # Import NotFound untuk Detail View
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear, ExtractMonth
import calendar
from articles.models import Article
from categories.models import Category
from images.models import Image
from tags.models import Tag
from articles.serializers import ArticleSerializer
from categories.serializers import CategoryHierarchicalSerializer
from images.serializers import ImageSerializer
from tags.serializers import TagSerializer


# --- VIEWSETS STANDAR ---

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True).annotate(post_count=Count('articles')).order_by('name')
    serializer_class = CategoryHierarchicalSerializer
    lookup_field = 'slug'

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().annotate(post_count=Count('articles')).order_by('name')
    serializer_class = TagSerializer
    lookup_field = 'slug'

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all().order_by('-uploaded_at')
    serializer_class = ImageSerializer

# --- ARCHIVES VIEWSET ---

class ArchiveViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Article.objects.annotate(
            year=ExtractYear('published_date'),
            month=ExtractMonth('published_date')
        ).values('year', 'month').annotate(post_count=Count('id')).order_by('-year', '-month')

        archives = []
        for item in queryset:
            year = item['year']
            month_number = item['month']
            month_name = calendar.month_name[month_number]
            post_count = item['post_count']

            year_obj = next((a for a in archives if a['year'] == year), None)
            if not year_obj:
                year_obj = {'year': year, 'total_posts': 0, 'months': []}
                archives.append(year_obj)
            
            year_obj['months'].append({
                'month': month_name,
                'month_number': month_number,
                'post_count': post_count
            })
            year_obj['total_posts'] += post_count

        return Response(archives)

# --- ARTICLE LIST APIVIEW (Custom List dengan Pagination Manual) ---

class ArticleListAPIView(APIView):
    def get(self, request, format=None):
        queryset = Article.objects.filter(is_published=True).order_by('-published_date')
        
        # Ambil query parameter
        category_slug = request.query_params.get('categories__slug')
        tag_slug = request.query_params.get('tags__slug')
        search_query = request.query_params.get('search')
        
        # PARAMETER BARU UNTUK ARSIP
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        
        # Lakukan filter manual (logic yang terbukti bekerja)
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(markdown_content__icontains=search_query)
            )

        # LOGIC FILTER TAHUN DAN BULAN
        if year and month:
            # Menggunakan ExtractYear dan ExtractMonth untuk filter yang akurat
            queryset = queryset.annotate(
                article_year=ExtractYear('published_date'),
                article_month=ExtractMonth('published_date')
            ).filter(article_year=year, article_month=month) # Filter berdasarkan tahun dan bulan
        
        # Implementasi Pagination Manual
        paginator = PageNumberPagination()
        custom_page_size = request.query_params.get('page_size')
        if custom_page_size:
            try:
                # Pastikan nilai adalah integer yang valid
                paginator.page_size = int(custom_page_size) 
            except ValueError:
                # Jika nilai page_size salah, gunakan default
                pass 
        
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        # Serialisasi data
        serializer = ArticleSerializer(page, many=True, context={'request': request})
        
        # Kembalikan Respons Paginated
        return paginator.get_paginated_response(serializer.data)


# --- ARTICLE RETRIEVE APIVIEW (Custom Detail View) ---

class ArticleRetrieveAPIView(APIView):
    # API ini digunakan untuk DETAIL artikel (/articles/<slug>)
    def get(self, request, slug, format=None):
        try:
            article = Article.objects.get(slug=slug, is_published=True)
        except Article.DoesNotExist:
            raise NotFound(detail="Article not found or not published.")

        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)

class LatestArticlesAPIView(APIView):
    def get(self, request, format=None):
        latest_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:5]
        serializer = ArticleSerializer(latest_articles, many=True, context={'request': request})
        return Response(serializer.data)

# VIEW API BARU UNTUK ARTIKEL ACAK (Further Reading)
class RandomArticlesAPIView(APIView):
    def get(self, request, format=None):
        # Ambil slug artikel yang sedang dilihat dari query parameter (misal: ?exclude_slug=...)
        exclude_slug = request.query_params.get('exclude_slug')

        queryset = Article.objects.filter(is_published=True).exclude(slug=exclude_slug).order_by('?')[:3]
        
        serializer = ArticleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)