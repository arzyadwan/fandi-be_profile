# from django.shortcuts import render

# # Create your views here.

# # MyITBlog/articles/views.py

# from rest_framework import viewsets
# from .models import Article
# from .serializers import ArticleSerializer

# class ArticleViewSet(viewsets.ModelViewSet):
#     # Mengambil artikel yang is_published=True untuk daftar publik
#     # Untuk admin, Anda mungkin ingin melihat semua, tapi untuk API publik, filter ini baik.
#     queryset = Article.objects.filter(is_published=True).order_by('-published_date')
#     serializer_class = ArticleSerializer
#     lookup_field = 'slug' # Menggunakan slug artikel di URL

#     # Override method get_serializer_context untuk meneruskan 'request' ke serializer
#     # Ini diperlukan agar ArticleSerializer bisa membuat URL absolut untuk featured_image_url
#     def get_serializer_context(self):
#         return {'request': self.request}