# lkps_project/urls.py
from django.contrib import admin
from django.urls import path, include
from lkps_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lkps_app.urls')), # Menyambungkan rute dari lkps_app
    path('admin-db-explorer/', views.db_explorer, name='db_explorer'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)