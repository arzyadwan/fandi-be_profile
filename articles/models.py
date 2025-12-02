from django.db import models

# Create your models here.

# myitblog_backend/articles/models.py

from django.db import models
from django.contrib.auth.models import User # Mengimpor model User bawaan Django
from django.utils.text import slugify
from categories.models import Category # Mengimpor model Category
from tags.models import Tag # Mengimpor model Tag
from images.models import Image # Mengimpor model Image

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    # Konten Markdown akan disimpan di sini
    markdown_content = models.TextField()
    # Ringkasan singkat artikel
    summary = models.TextField(blank=True, null=True, help_text="A short summary for article listings.")

    published_date = models.DateTimeField(auto_now_add=True) # Otomatis set saat dibuat
    updated_date = models.DateTimeField(auto_now=True)     # Otomatis update setiap disimpan
    is_published = models.BooleanField(default=True)

    # Penulis: Hubungan ke User bawaan Django
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Kategori: Hubungan many-to-many atau many-to-one (sesuai kebutuhan Anda)
    # Kita akan gunakan ManyToManyField untuk fleksibilitas (satu artikel bisa di banyak kategori)
    # Jika Anda hanya ingin satu kategori per artikel, gunakan models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='articles')

    # Tag: Hubungan Many-to-Many
    tags = models.ManyToManyField(Tag, related_name='articles')

    # Featured Image: Hubungan satu-ke-satu atau satu-ke-banyak ke model Image
    # Kita gunakan ForeignKey, agar satu gambar bisa digunakan oleh banyak artikel sebagai featured
    featured_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_articles'
    )

    class Meta:
        ordering = ['-published_date'] # Default order: artikel terbaru di atas

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title