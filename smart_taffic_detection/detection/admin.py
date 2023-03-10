from django.contrib import admin

# Register your models here.
from .models import Input, Result

admin.site.register([Input, Result])