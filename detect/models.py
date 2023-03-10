from django.db import models
from .validators import file_size

# Create your models here.

class Video(models.Model):
    intersection_name = models.CharField(max_length=256)
    video = models.FileField(upload_to="video/%y", validators=[file_size])
    def __str__(self):
        return self.intersection_name
