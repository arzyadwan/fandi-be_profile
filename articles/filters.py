# MyITBlog/articles/filters.py

import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    categories__slug = django_filters.CharFilter(field_name='categories__slug')
    tags__slug = django_filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Article
        fields = ['categories__slug', 'tags__slug']