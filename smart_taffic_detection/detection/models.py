from django.db import models

# Create your models here.
class Input(models.Model):
    time_record = models.TimeField('time', auto_now_add=True)
    date_record = models.DateTimeField('date', auto_now_add=True)
    video = models.FileField(upload_to='uploads/video', blank=True)
    location = models.CharField(max_length=100, default="")
    def __str__(self):
        return f"{self.video}"
    
class Result(models.Model):
    video = models.FileField(upload_to='uploads/video', blank=True)  
    loop = models.FileField(upload_to='uploads/files', blank=True)

    def __str__(self):
        return f"{self.video}"