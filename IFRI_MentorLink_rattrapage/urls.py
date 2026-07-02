from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/rechercher/', views.rechercher_mentors, name='rechercher_mentors'),
    path('api/mentors/', views.liste_mentors, name='liste_mentors'),
    path('upload/<int:mentor_id>/', views.upload_photo_page, name='upload_photo_page'),
    path('api/upload/<int:mentor_id>/', views.upload_photo, name='upload_photo'),
]

# Servir les médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)