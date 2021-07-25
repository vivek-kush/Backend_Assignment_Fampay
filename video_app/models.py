from django.db import models

# Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=500, unique=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    published_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    thumbnail_url = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['-published_datetime']),
        ]
