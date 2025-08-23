#!/usr/bin/env python3
"""
File upload views for document processing.
"""

import os
import json
import tempfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pathlib import Path
from .file_extractor import file_extractor

@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    """
    Handle file upload and text extraction.
    
    Returns JSON with extracted text and file information.
    """
    try:
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No file provided'
            }, status=400)
        
        uploaded_file = request.FILES['file']

        # Check if file type is supported
        if not file_extractor.is_supported(uploaded_file.name):
            return JsonResponse({
                'success': False,
                'error': f'Unsupported file type. Supported types: {", ".join(file_extractor.supported_extensions)}'
            }, status=400)
        
        # Save file temporarily
        temp_dir = Path(__file__).parent.parent / "uploads" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique filename
        import uuid
        file_id = str(uuid.uuid4())
        file_extension = Path(uploaded_file.name).suffix
        temp_filename = f"{file_id}{file_extension}"
        temp_filepath = temp_dir / temp_filename
        
        # Save uploaded file
        with open(temp_filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Extract text from file
        extraction_result = file_extractor.extract_text(temp_filepath)
        
        # Clean up temporary file
        try:
            os.remove(temp_filepath)
        except:
            pass  # Ignore cleanup errors
        
        # Prepare response
        response_data = {
            'success': True,
            'file_info': {
                'original_name': uploaded_file.name,
                'size': uploaded_file.size,
                'extension': extraction_result.get('extension', ''),
                'pages': extraction_result.get('pages', 1),
                'metadata': extraction_result.get('metadata', {})
            },
            'extracted_text': extraction_result.get('text', ''),
            'error': extraction_result.get('error', None)
        }
        
        # If there was an extraction error, still return success but with error info
        if extraction_result.get('error'):
            response_data['success'] = True  # File was uploaded successfully
            response_data['extraction_error'] = extraction_result['error']
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def extract_pdf_pages(request):
    """Extract text from specific PDF pages."""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No file provided'
            }, status=400)
        
        uploaded_file = request.FILES['file']
        page_numbers = request.POST.get('pages', None)
        
        # Parse page numbers
        if page_numbers:
            try:
                page_numbers = [int(p.strip()) for p in page_numbers.split(',') if p.strip()]
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid page numbers format. Use comma-separated numbers (e.g., "1,3,5")'
                }, status=400)
        
        # Check if file is PDF
        if not uploaded_file.name.lower().endswith('.pdf'):
            return JsonResponse({
                'success': False,
                'error': 'Only PDF files are supported for page extraction'
            }, status=400)
        
        # Save file temporarily
        temp_dir = Path(__file__).parent.parent / "uploads" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        import uuid
        file_id = str(uuid.uuid4())
        temp_filename = f"{file_id}.pdf"
        temp_filepath = temp_dir / temp_filename
        
        # Save uploaded file
        with open(temp_filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Extract pages
        try:
            result = file_extractor.extract_pdf_pages(temp_filepath, page_numbers)
        except Exception as e:
            # Clean up temporary file on error
            try:
                os.remove(temp_filepath)
            except:
                pass
            return JsonResponse({
                'success': False,
                'error': f'PDF page extraction failed: {str(e)}'
            }, status=500)
        
        # Clean up temporary file
        try:
            os.remove(temp_filepath)
        except:
            pass
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'pages': result['pages'],
                'total_pages': result['total_pages'],
                'selected_pages': result['selected_pages']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def translate_pdf_pages(request):
    """Translate specific PDF pages and return a new PDF."""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No file provided'
            }, status=400)
        
        uploaded_file = request.FILES['file']
        page_numbers = request.POST.get('pages', None)
        target_language = request.POST.get('target_language', 'English')
        service_name = request.POST.get('service_name')  # Get the specific service to use
        
        # Parse page numbers
        if page_numbers:
            try:
                page_numbers = [int(p.strip()) for p in page_numbers.split(',') if p.strip()]
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid page numbers format. Use comma-separated numbers (e.g., "1,3,5")'
                }, status=400)
        
        # Check if file is PDF
        if not uploaded_file.name.lower().endswith('.pdf'):
            return JsonResponse({
                'success': False,
                'error': 'Only PDF files are supported for translation'
            }, status=400)
        
        # Save file temporarily
        temp_dir = Path(__file__).parent.parent / "uploads" / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        import uuid
        file_id = str(uuid.uuid4())
        temp_filename = f"{file_id}.pdf"
        temp_filepath = temp_dir / temp_filename
        
        # Save uploaded file
        with open(temp_filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Get translation service
        try:
            from .translation_service import translation_service
            
            # Set service if specified
            if service_name and hasattr(translation_service, 'set_service'):
                success = translation_service.set_service(service_name)
                if not success:
                    return JsonResponse({
                        'success': False,
                        'error': f'Failed to set translation service to {service_name}'
                    }, status=400)
            
        except ImportError:
            return JsonResponse({
                'success': False,
                'error': 'Translation service not available'
            }, status=500)
        
        # Translate PDF pages
        result = file_extractor.translate_pdf_pages(
            temp_filepath, 
            page_numbers, 
            target_language, 
            translation_service
        )
        
        # Clean up original temporary file
        try:
            os.remove(temp_filepath)
        except:
            pass
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'output_path': result['output_path'],
                'filename': result['filename'],
                'translated_pages': result['translated_pages'],
                'download_url': f'/api/download-pdf/{result["filename"]}',
                'service_used': service_name or 'default'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def download_translated_pdf(request, filename):
    """Download a translated PDF file."""
    try:
        temp_dir = Path(__file__).parent.parent / "uploads" / "temp"
        file_path = temp_dir / filename
        
        if not file_path.exists():
            return JsonResponse({
                'success': False,
                'error': 'File not found'
            }, status=404)
        
        from django.http import FileResponse
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=f'translated_{filename}'
        )
        
        # Schedule file deletion after a delay (optional cleanup)
        import threading
        import time
        
        def delayed_cleanup():
            time.sleep(300)  # Wait 5 minutes
            try:
                if file_path.exists():
                    os.remove(file_path)
            except:
                pass
        
        cleanup_thread = threading.Thread(target=delayed_cleanup)
        cleanup_thread.daemon = True
        cleanup_thread.start()
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Download error: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_supported_types(request):
    """Return list of supported file types."""
    return JsonResponse({
        'supported_extensions': list(file_extractor.supported_extensions),
        'supported_types': {
            'documents': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt'],
            'ebooks': ['.epub', '.mobi', '.fb2'],
            'comics': ['.cbz'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'other': ['.xps', '.svg', '.hwp']
        }
    })

# Translation Service Management Endpoints

@require_http_methods(["GET"])
def get_translation_services(request):
    """Get information about available translation services."""
    try:
        from .translation_service import translation_service
        
        if hasattr(translation_service, 'get_available_services'):
            available = translation_service.get_available_services()
            all_info = translation_service.get_service_info()
            
            return JsonResponse({
                'success': True,
                'available_services': available,
                'services_info': all_info,
                'current_service': getattr(translation_service.manager, 'current_service', None) if hasattr(translation_service, 'manager') else 'local_transformer'
            })
        else:
            # Legacy service
            return JsonResponse({
                'success': True,
                'available_services': ['local_transformer'],
                'services_info': {
                    'local_transformer': {
                        'name': 'Gemini API',
                        'description': 'Gemini API for advanced translation',
                        'available': True,
                        'loaded': translation_service.model_loaded
                    }
                },
                'current_service': 'local_transformer'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error getting translation services: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def set_translation_service(request):
    """Set the active translation service."""
    try:
        data = json.loads(request.body)
        service_name = data.get('service_name')
        
        if not service_name:
            return JsonResponse({
                'success': False,
                'error': 'service_name is required'
            }, status=400)
        
        from .translation_service import translation_service
        
        if hasattr(translation_service, 'set_service'):
            success = translation_service.set_service(service_name)
            if success:
                return JsonResponse({
                    'success': True,
                    'message': f'Translation service set to: {service_name}'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to set service to: {service_name}'
                }, status=400)
        else:
            # Legacy service only supports local_transformer
            if service_name == 'local_transformer':
                return JsonResponse({
                    'success': True,
                    'message': 'Using local transformer service'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Only local_transformer service is available in legacy mode'
                }, status=400)
                
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error setting translation service: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def load_translation_service(request):
    """Load/initialize the current translation service."""
    try:
        data = json.loads(request.body) if request.body else {}
        service_name = data.get('service_name')  # Optional - will use current if not specified
        
        from .translation_service import translation_service
        
        if service_name and hasattr(translation_service, 'set_service'):
            # Set service first if specified
            success = translation_service.set_service(service_name)
            if not success:
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to set service to: {service_name}'
                }, status=400)
        
        # Load the service
        if hasattr(translation_service, 'load_model'):
            translation_service.load_model()
            
            current_service = getattr(translation_service.manager, 'current_service', 'local_transformer') if hasattr(translation_service, 'manager') else 'local_transformer'
            
            return JsonResponse({
                'success': True,
                'message': f'Translation service loaded: {current_service}',
                'service': current_service
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Translation service not available'
            }, status=500)
                
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error loading translation service: {str(e)}'
        }, status=500)
