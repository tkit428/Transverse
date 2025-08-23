#!/usr/bin/env python3
"""
Advanced PDF translator using redaction approach for better text replacement.
Based on PyMuPDF best practices from GitHub discussions.
"""

import fitz  # PyMuPDF
from pathlib import Path
import uuid
import html

class AdvancedPdfTranslator:
    
    def __init__(self):
        self.temp_dir = Path(__file__).parent.parent / "uploads" / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def translate_pdf_with_redaction(self, file_path, page_numbers, target_language, translation_service):
        """
        Translate PDF using redaction approach for better format preservation.
        This method follows PyMuPDF best practices.
        """
        try:
            # Open original document
            doc = fitz.open(file_path)
            
            if page_numbers is None:
                page_numbers = list(range(1, len(doc) + 1))
            
            # Process each specified page
            for page_idx in page_numbers:
                if page_idx < 1 or page_idx > len(doc):
                    continue
                    
                page = doc[page_idx - 1]  # Convert to 0-based
                
                # Extract text with detailed formatting information
                text_dict = page.get_text("dict")
                
                # Collect text blocks for translation
                translation_blocks = []
                
                for block in text_dict.get("blocks", []):
                    if "lines" in block:  # Text block
                        block_info = self._extract_block_info(block)
                        if block_info and block_info['text'].strip():
                            translation_blocks.append(block_info)
                
                # Translate all text blocks
                for block_info in translation_blocks:
                    try:
                        # Translate the text
                        translated_text = translation_service.translate(
                            block_info['text'], 
                            target_language
                        )
                        
                        if not translated_text or translated_text.strip() == "":
                            translated_text = block_info['text']  # Fallback
                        
                        # Use redaction to remove original text
                        page.add_redact_annot(
                            block_info['bbox'], 
                            text="",  # Remove text
                            fill=(1, 1, 1)  # White fill
                        )
                        
                        # Store translation info for later insertion
                        block_info['translated_text'] = translated_text
                        
                    except Exception as e:
                        print(f"Translation error for block: {e}")
                        block_info['translated_text'] = block_info['text']
                
                # Apply all redactions
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                
                # Insert translated text using HTML for better Unicode support
                for block_info in translation_blocks:
                    if 'translated_text' in block_info:
                        self._insert_translated_text(page, block_info)
            
            # Save the translated document
            output_filename = f"translated_{uuid.uuid4().hex[:8]}.pdf"
            output_path = self.temp_dir / output_filename
            
            # Save with optimal settings
            doc.save(
                str(output_path),
                garbage=4,  # Maximum garbage collection
                clean=True,  # Clean content streams
                deflate=True,  # Compress streams
                ascii=False  # Allow Unicode
            )
            doc.close()
            
            return {
                'success': True,
                'output_path': str(output_path),
                'filename': output_filename,
                'translated_pages': len(page_numbers)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Advanced PDF translation error: {str(e)}'}
    
    def _extract_block_info(self, block):
        """Extract comprehensive information from a text block."""
        block_text = []
        block_bbox = None
        font_info = {
            'sizes': [],
            'fonts': [],
            'colors': [],
            'flags': []
        }
        
        for line in block["lines"]:
            for span in line["spans"]:
                if span["text"].strip():
                    block_text.append(span["text"])
                    
                    # Collect font information
                    font_info['sizes'].append(span.get('size', 12))
                    font_info['fonts'].append(span.get('font', 'Times-Roman'))
                    font_info['colors'].append(span.get('color', 0))
                    font_info['flags'].append(span.get('flags', 0))
                    
                    # Calculate bounding box
                    bbox = fitz.Rect(span['bbox'])
                    if block_bbox is None:
                        block_bbox = bbox
                    else:
                        block_bbox = block_bbox | bbox
        
        if not block_text or not block_bbox:
            return None
        
        # Get most common/average font properties
        avg_size = sum(font_info['sizes']) / len(font_info['sizes']) if font_info['sizes'] else 12
        most_common_font = max(set(font_info['fonts']), key=font_info['fonts'].count) if font_info['fonts'] else 'Times-Roman'
        avg_color = font_info['colors'][0] if font_info['colors'] else 0
        avg_flags = font_info['flags'][0] if font_info['flags'] else 0
        
        return {
            'text': " ".join(block_text),
            'bbox': block_bbox,
            'font_size': avg_size,
            'font_name': most_common_font,
            'color': avg_color,
            'flags': avg_flags,
            'is_bold': bool(avg_flags & 2**4),
            'is_italic': bool(avg_flags & 2**6)
        }
    
    def _insert_translated_text(self, page, block_info):
        """Insert translated text with proper formatting."""
        translated_text = block_info['translated_text']
        bbox = block_info['bbox']
        
        # Create HTML content for better Unicode support
        html_content = self._create_html_for_text(block_info)
        
        try:
            # Try HTML insertion first (best for Unicode)
            result = page.insert_htmlbox(bbox, html_content)
            
            if result[0] >= 0:  # Success
                return True
                
        except Exception as e:
            print(f"HTML insertion failed: {e}")
        
        # Fallback to textbox with appropriate font
        try:
            fontname = self._get_font_for_language(block_info)
            color = self._convert_color(block_info['color'])
            
            result = page.insert_textbox(
                bbox,
                translated_text,
                fontname=fontname,
                fontsize=max(8, min(block_info['font_size'], 20)),
                color=color,
                align=0
            )
            
            if result >= 0:
                return True
                
            # Try with smaller font sizes
            for scale in [0.8, 0.6, 0.4]:
                smaller_size = block_info['font_size'] * scale
                if smaller_size < 6:
                    break
                    
                result = page.insert_textbox(
                    bbox,
                    translated_text,
                    fontname=fontname,
                    fontsize=smaller_size,
                    color=color,
                    align=0
                )
                
                if result >= 0:
                    return True
                    
        except Exception as e:
            print(f"Textbox insertion failed: {e}")
        
        # Ultimate fallback
        try:
            page.insert_text(
                bbox.tl,
                translated_text,
                fontsize=12,
                color=(0, 0, 0)
            )
            return True
        except:
            return False
    
    def _create_html_for_text(self, block_info):
        """Create HTML content with proper styling."""
        text = block_info['translated_text']
        font_size = max(8, min(block_info['font_size'], 24))
        
        # Convert color
        color = self._convert_color(block_info['color'])
        color_hex = f"#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}"
        
        # Check if text contains Chinese characters for font selection
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
        
        # Build CSS style with appropriate font families
        if has_chinese:
            # Use Chinese-compatible font stack
            font_family = "'SimSun', 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', 'Source Han Sans SC', sans-serif"
        else:
            # Use general Unicode font stack
            font_family = "'DejaVu Sans', 'Noto Sans', 'Arial Unicode MS', sans-serif"
        
        styles = [
            f"font-size: {font_size}px",
            f"color: {color_hex}",
            f"font-family: {font_family}",
            "line-height: 1.1",
            "margin: 0",
            "padding: 0"
        ]
        
        if block_info['is_bold']:
            styles.append("font-weight: bold")
        if block_info['is_italic']:
            styles.append("font-style: italic")
        
        style_str = "; ".join(styles)
        
        # Escape HTML but preserve Unicode
        escaped_text = html.escape(text, quote=False)
        
        return f'<div style="{style_str}">{escaped_text}</div>'
    
    def _get_font_for_language(self, block_info):
        """Get appropriate font based on content and language."""
        # For Chinese text, we need to use appropriate Chinese fonts
        text = block_info.get('translated_text', '')
        
        # Check if text contains Chinese characters
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
        
        if has_chinese:
            # Use Chinese-compatible fonts
            return "china-s"  # Simplified Chinese font that also works for Traditional
        else:
            # Use more Unicode-friendly fonts for other languages
            if block_info['is_bold'] and block_info['is_italic']:
                return "helv"  # Helvetica handles most cases well
            elif block_info['is_bold']:
                return "helv"
            elif block_info['is_italic']:
                return "helv"
            else:
                return "helv"  # Helvetica is generally good for Unicode
    
    def _convert_color(self, color_value):
        """Convert color to RGB tuple."""
        if isinstance(color_value, int):
            r = (color_value >> 16) & 255
            g = (color_value >> 8) & 255
            b = color_value & 255
            return (r/255, g/255, b/255)
        elif isinstance(color_value, (list, tuple)) and len(color_value) >= 3:
            return tuple(color_value[:3])
        else:
            return (0, 0, 0)

# Global instance
advanced_pdf_translator = AdvancedPdfTranslator()
