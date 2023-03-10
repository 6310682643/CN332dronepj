from django.urls import path, include
from . import views
from django.conf .urls.static import static
from django.conf import settings
from .views import Video

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('upload/', views.uploaddata, name='uploaddata'),
    path('information/', views.clip_detect, name='clip_detect'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)