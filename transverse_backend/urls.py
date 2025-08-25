"""
URL configuration for transverse_backend project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from .file_upload_views import upload_file, translate_pdf_pages, translate_text, download_translated_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', upload_file, name='upload_file'),
    path('api/translate-pdf/', translate_pdf_pages, name='translate_pdf'),
    path('api/translate/', translate_text, name='translate_text'),
    path('api/download-pdf/<str:filename>', download_translated_pdf, name='download_pdf'),
    path('api/translation-services/', lambda request: JsonResponse({'services': ['gemini']}), name='translation_services'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
