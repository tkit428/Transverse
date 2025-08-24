"""
URL configuration for transverse_backend project.
"""

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from . import file_upload_views

def home_view(request):
    """Simple home view for testing."""
    return JsonResponse({"message": "Transverse Backend API", "status": "running"})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints for file processing
    path('api/upload/', file_upload_views.upload_file, name='upload_file'),
    path('api/extract-pdf-pages/', file_upload_views.extract_pdf_pages, name='extract_pdf_pages'),
    path('api/translate-pdf/', file_upload_views.translate_pdf_pages, name='translate_pdf_pages'),

    # Text translation endpoint
    path('api/translate/', file_upload_views.translate_text, name='translate_text'),
    path('api/download-pdf/<str:filename>/', file_upload_views.download_translated_pdf, name='download_translated_pdf'),
    
    # Translation service management
    path('api/translation-services/', file_upload_views.get_translation_services, name='get_translation_services'),
    path('api/translation-services/set/', file_upload_views.set_translation_service, name='set_translation_service'),
    path('api/translation-services/load/', file_upload_views.load_translation_service, name='load_translation_service'),
    
    # Utility endpoints
    path('api/supported-types/', file_upload_views.get_supported_types, name='get_supported_types'),
    
    # Root endpoint
    path('', home_view, name='home'),
]
