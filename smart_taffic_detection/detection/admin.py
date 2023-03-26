# from django.contrib import admin

# # Register your models here.
# from .models import Input, Result

# admin.site.register([Input, Result])

from django.contrib import admin

# Register your models here.
from .models import Input, Result, Intersection

admin.site.register([Input, Result, Intersection])
