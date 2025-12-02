from django.db import models

# Create your models here.

# myitblog_backend/images/models.py

from django.db import models

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/') # Akan disimpan di MEDIA_ROOT/images/
    caption = models.CharField(max_length=255, blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True,
                                help_text="Text for screen readers, if image fails to load, etc.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption if self.caption else f"Image {self.id}"