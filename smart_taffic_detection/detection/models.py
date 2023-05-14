from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
# Create your models here.


class Intersection(models.Model):
    name = models.CharField(max_length=9999, default="")

    def __str__(self):
        return f"{self.name}"


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
    intersection = models.ForeignKey(
        Intersection, null=True, on_delete=models.SET_NULL, default=None)
    time_record = models.TimeField('time', default=timezone.now, null=True)
    # time_record =models.DateTimeField(auto_now_add=True, default=timezone.now)
    date_record = models.DateField('date', default=datetime.now, null=True)
    video = models.FileField(upload_to='uploads/video', blank=True)
    image = models.FileField(upload_to='uploads/images', blank=True, null=True)
    image_scale = models.FileField(upload_to='uploads/images', blank=True, null=True)
    location = models.TextField(max_length=9999, default="", null=True)
    traffic_status = models.IntegerField(
        default=0, null=True, validators=[MinValueValidator(0)])
    detect_status = models.IntegerField(
        default=0, null=True, validators=[MinValueValidator(0)])
    note = models.TextField(max_length=9999, default="", null=True)
    weather = models.CharField(max_length=999, choices=choices, default="null")
    date_upload = models.DateField(
        'date_upload', default=datetime.now, null=True)

    def __str__(self):
        return f"{self.video}"


class Result(models.Model):
    input_video = models.ForeignKey(
        Input, null=True, on_delete=models.SET_NULL)
    video = models.FileField(upload_to='uploads/video', blank=True)
    loop = models.FileField(upload_to='uploads/files', blank=True)

    def __str__(self):
        return f"{self.video}"

class CreateLoop(models.Model):
    fileName = models.CharField(max_length=999, default="")
    
    loopName1 = models.CharField(max_length=999, default="")
    x1 = models.IntegerField(default=0, null=True)
    y1 = models.IntegerField(default=0, null=True)
    width1 = models.IntegerField(default=0, null=True)
    height1 = models.IntegerField(default=0, null=True)
    angle1 = models.IntegerField(default=0, null=True)
    summary_location = models.JSONField(null=True, blank=True)

    loopName2 = models.CharField(max_length=999, default="")
    x2 = models.IntegerField(default=0, null=True)
    y2 = models.IntegerField(default=0, null=True)
    width2 = models.IntegerField(default=0, null=True)
    height2 = models.IntegerField(default=0, null=True)
    angle2 = models.IntegerField(default=0, null=True)

    loopName3 = models.CharField(max_length=999, default="")
    x3 = models.IntegerField(default=0, null=True)
    y3 = models.IntegerField(default=0, null=True)
    width3 = models.IntegerField(default=0, null=True)
    height3 = models.IntegerField(default=0, null=True)
    angle3 = models.IntegerField(default=0, null=True)

    loopName4 = models.CharField(max_length=999, default="")
    # points4 = models.JSONField(default=[], null=True)
    x4 = models.IntegerField(default=0, null=True)
    y4 = models.IntegerField(default=0, null=True)
    # orientation4 = models.CharField(max_length=20, default="")
    width4 = models.IntegerField(default=0, null=True)
    height4 = models.IntegerField(default=0, null=True)
    angle4 =models.IntegerField(default=0, null=True)