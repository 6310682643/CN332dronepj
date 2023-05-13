# from django.urls import path
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('', views.loginPage, name="loginPage"),
#     path('upload/', views.uploadPage, name="uploadPage"),
#     path('delete/<int:id>', views.delete, name='delete'),
#     path('home/', views.home, name="home"),
# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loginPage, name="loginPage"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('home/', views.home, name="home"),
    path('upload/', views.uploadPage, name="uploadPage"),
    path('generalInfo/<int:id>', views.generalInfo, name='generalInfo'),
    path('createLoop/<int:id>', views.createLoop, name='createLoop'),
    path("edit_loop/<int:id>", views.edit_loop, name='edit_loop'),
    path('preview/', views.preview, name='preview'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
