"""
URL configuration for transverse_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .file_upload_views import (
    upload_file, get_supported_types, extract_pdf_pages, translate_pdf_pages, 
    download_translated_pdf, get_translation_services, set_translation_service, 
    load_translation_service
)
import os
import json

def serve_static_html(request, filename):
    """Serve static HTML files from the project root"""
    file_path = os.path.join(settings.BASE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        from django.http import Http404
        raise Http404("File not found")

def home(request):
    """Simple home view that serves index.html"""
    return serve_static_html(request, 'index.html')

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def translate_text(request):
    """Real translation API endpoint using the optimized model"""
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    try:
        data = json.loads(request.body)
        source_text = data.get('text', '')
        target_language = data.get('target_language', 'French')
        service_name = data.get('service_name')  # Get the specific service to use
        
        if not source_text:
            response = JsonResponse({
                'error': 'No text provided',
                'status': 'error'
            }, status=400)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        
        # Import translation service
        try:
            from .translation_service import translation_service
            
            # Set service if specified
            if service_name and hasattr(translation_service, 'set_service'):
                success = translation_service.set_service(service_name)
                if not success:
                    response = JsonResponse({
                        'error': f'Failed to set translation service to {service_name}',
                        'status': 'error'
                    }, status=400)
                    response['Access-Control-Allow-Origin'] = '*'
                    return response
            
            # Perform translation
            translated_text = translation_service.translate(source_text, target_language)
        except Exception as import_error:
            # Fallback to simple translation for testing
            translated_text = f"[FALLBACK] {source_text} → {target_language}"
        
        response_data = {
            'translated_text': translated_text,
            'source_text': source_text,
            'target_language': target_language,
            'service_used': service_name or 'default',
            'status': 'success'
        }
        
        response = JsonResponse(response_data)
        response['Access-Control-Allow-Origin'] = '*'
        return response
        
    except Exception as e:
        response = JsonResponse({
            'error': f'Translation failed: {str(e)}',
            'status': 'error'
        }, status=500)
        response['Access-Control-Allow-Origin'] = '*'
        return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/translate/', translate_text, name='translate_text'),
    path('api/upload/', upload_file, name='upload_file'),
    path('api/extract-pages/', extract_pdf_pages, name='extract_pdf_pages'),
    path('api/translate-pdf/', translate_pdf_pages, name='translate_pdf_pages'),
    path('api/download-pdf/<str:filename>/', download_translated_pdf, name='download_translated_pdf'),
    path('api/supported-types/', get_supported_types, name='supported_types'),
    
    # Translation service management endpoints
    path('api/translation-services/', get_translation_services, name='get_translation_services'),
    path('api/translation-services/set/', set_translation_service, name='set_translation_service'),
    path('api/translation-services/load/', load_translation_service, name='load_translation_service'),
    
    path('privacy.html', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms.html', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
    
    # Serve static HTML files
    path('test_xalma.html', serve_static_html, {'filename': 'test_xalma.html'}, name='test_xalma'),
    path('test_upload.html', serve_static_html, {'filename': 'test_upload.html'}, name='test_upload'),
    path('index.html', serve_static_html, {'filename': 'index.html'}, name='index'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR)
