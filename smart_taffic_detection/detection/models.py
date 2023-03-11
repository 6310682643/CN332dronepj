from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class Input(models.Model):
    choices = (
        ('sunny', 'Sunny'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
        ('snow', 'Snow'),
        ('windy', 'Windy'),
        ('partly cloudy', 'Partly cloudy'),
        ('fog', 'Fog'),
        ('null', 'Null')
    )
    ownerName = models.CharField(max_length=999, default="")
    time_record = models.TimeField('time', default=timezone.now, null=True)
    # time_record =models.DateTimeField(auto_now_add=True, default=timezone.now)
    date_record = models.DateTimeField('date', default=timezone.now, null=True)
    video = models.FileField(upload_to='uploads/video', blank=True)
    location = models.TextField(max_length=9999, default="", null=True)
    traffic_status = models.IntegerField(default=0, null=True, validators=[MinValueValidator(0)])
    note = models.TextField(max_length=9999, default="", null=True)
    weather = models.CharField(max_length=999, choices=choices, default="null")

    def __str__(self):
        return f"{self.video}"
    
class Result(models.Model):
    input_video = models.ForeignKey(Input, null=True, on_delete=models.SET_NULL)
    video = models.FileField(upload_to='uploads/video', blank=True)  
    loop = models.FileField(upload_to='uploads/files', blank=True)

    def __str__(self):
        return f"{self.video}"
    
class Intersection(models.Model):
    name = models.CharField(max_length=9999, default="")

    def __str__(self):
        return f"{self.name}"

