# MyITBlog/core/urls.py (Kode Final dan Lengkap)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleListAPIView, 
    ArticleRetrieveAPIView, 
    LatestArticlesAPIView,      # View untuk /latest/
    RandomArticlesAPIView,      # View untuk /random_articles/
    CategoryViewSet,
    ImageViewSet,
    TagViewSet,
    ArchiveViewSet
)

# 1. Router untuk ViewSets (Category, Tag, Image, Archive)
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'archives', ArchiveViewSet, basename='archive')


# 2. Path Kustom untuk Artikel (Harus Didefinisikan Manual)
urlpatterns = [
    # PENTING: Path kustom yang lebih panjang harus di atas path dinamis
    
    # Path API KUSTOM (Latest dan Random)
    path('articles/latest/', LatestArticlesAPIView.as_view(), name='article-latest'),
    path('articles/random_articles/', RandomArticlesAPIView.as_view(), name='article-random'), 

    # Path Detail Artikel (Harus berada di urutan berikutnya untuk menangkap slug)
    path('articles/<slug:slug>/', ArticleRetrieveAPIView.as_view(), name='article-detail'),

    # Path List Artikel (Harus berada di urutan berikutnya setelah path dinamis)
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),

    # 3. Masukkan semua router ViewSet
    path('', include(router.urls)),
]