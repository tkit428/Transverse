#!/usr/bin/env python3
"""
Advanced PDF translator using redaction approach for better text replacement.
Based on PyMuPDF best practices from GitHub discussions.
"""

import fitz  # PyMuPDF
from pathlib import Path
import uuid
import html
import time
import logging

# Set up logging for debug output
logging.basicConfig(
    level=logging.DEBUG,
    format='[PDF_TRANSLATOR] %(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('pdf_translator')

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
            logger.info("=== STARTING PDF TRANSLATION ===")
            logger.info(f"📁 Input file: {Path(file_path).name}")
            logger.info(f"🌐 Target language: {target_language}")
            logger.info(f"🔧 Translation service: {getattr(translation_service, 'service_name', 'Unknown')}")

            # Open original document
            doc = fitz.open(file_path)
            total_pages = len(doc)
            logger.info(f"📄 Total pages in document: {total_pages}")

            if page_numbers is None:
                page_numbers = list(range(1, len(doc) + 1))
                logger.info(f"📄 Processing all pages: {page_numbers}")
            else:
                logger.info(f"📄 Processing selected pages: {page_numbers}")

            # Process each specified page
            for page_idx in page_numbers:
                if page_idx < 1 or page_idx > len(doc):
                    logger.warning(f"⚠️ Skipping invalid page {page_idx} (out of range 1-{len(doc)})")
                    continue

                logger.info(f"📄 STARTING PAGE {page_idx}")
                page_start_time = time.time()

                page = doc[page_idx - 1]  # Convert to 0-based
                page_size = f"{page.rect.width:.1f}x{page.rect.height:.1f}"
                logger.info(f"📄 Page {page_idx} dimensions: {page_size}")

                # Extract text with detailed formatting information
                logger.info(f"📄 Page {page_idx}: Extracting text blocks...")
                text_dict = page.get_text("dict")
                total_blocks = len(text_dict.get("blocks", []))
                logger.info(f"📄 Page {page_idx}: Found {total_blocks} blocks in document")

                # Collect text blocks for translation
                translation_blocks = []

                for block in text_dict.get("blocks", []):
                    if "lines" in block:  # Text block
                        block_info = self._extract_block_info(block)
                        if block_info and block_info['text'].strip():
                            translation_blocks.append(block_info)

                logger.info(f"📄 Page {page_idx}: Found {len(translation_blocks)} text blocks to translate")

                # Batch translate all text blocks in one API call
                logger.info(f"📄 Page {page_idx}: Batch translating {len(translation_blocks)} blocks in one request...")

                if translation_blocks:
                    try:
                        # Combine all text blocks with markers to identify them
                        combined_text = ""
                        block_markers = []

                        for block_idx, block_info in enumerate(translation_blocks, 1):
                            block_marker = f"__BLOCK_{block_idx}__"
                            combined_text += f"{block_marker}\n{block_info['text']}\n\n"
                            block_markers.append(block_marker)

                        logger.info(f"📄 Page {page_idx}: Combined text length: {len(combined_text)} characters")

                        # Make single API call for entire page
                        page_translate_start = time.time()
                        translated_combined = translation_service.translate(
                            combined_text,
                            target_language
                        )
                        translate_time = time.time() - page_translate_start

                        if not translated_combined or translated_combined.strip() == "":
                            logger.warning(f"📄 Page {page_idx}: Empty translation received, using original texts")
                            # Use original texts as fallback
                            for block_info in translation_blocks:
                                block_info['translated_text'] = block_info['text']
                        else:
                            logger.info(f"📄 Page {page_idx}: Batch translation completed ({len(translated_combined)} chars) in {translate_time:.2f}s")

                            # Split the translated text back using markers
                            translated_blocks = self._split_translated_text(translated_combined, block_markers)

                            # Assign translated text to each block
                            for i, block_info in enumerate(translation_blocks):
                                if i < len(translated_blocks) and translated_blocks[i].strip():
                                    block_info['translated_text'] = translated_blocks[i].strip()
                                    logger.debug(f"📄 Page {page_idx}, Block {i+1}: Assigned translated text ({len(block_info['translated_text'])} chars)")
                                else:
                                    logger.warning(f"📄 Page {page_idx}, Block {i+1}: No translated text found, using original")
                                    block_info['translated_text'] = block_info['text']

                    except Exception as e:
                        logger.error(f"📄 Page {page_idx}: Batch translation error: {str(e)}")
                        # Fallback to original texts
                        for block_info in translation_blocks:
                            block_info['translated_text'] = block_info['text']

                # Add redaction annotations for all blocks
                logger.info(f"📄 Page {page_idx}: Adding {len(translation_blocks)} redaction annotations...")
                for block_idx, block_info in enumerate(translation_blocks, 1):
                    try:
                        page.add_redact_annot(
                            block_info['bbox'],
                            text="",  # Remove text
                            fill=(1, 1, 1)  # White fill
                        )
                        logger.debug(f"📄 Page {page_idx}, Block {block_idx}: Redaction annotation added")
                    except Exception as e:
                        logger.error(f"📄 Page {page_idx}, Block {block_idx}: Error adding redaction: {str(e)}")

                # Apply all redactions
                logger.info(f"📄 Page {page_idx}: Applying {len(translation_blocks)} redaction annotations...")
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                logger.info(f"📄 Page {page_idx}: Redactions applied successfully")

                # Insert translated text using HTML for better Unicode support
                logger.info(f"📄 Page {page_idx}: Inserting {len(translation_blocks)} translated text blocks...")
                successful_insertions = 0
                for block_idx, block_info in enumerate(translation_blocks, 1):
                    if 'translated_text' in block_info:
                        try:
                            success = self._insert_translated_text(page, block_info)
                            if success:
                                successful_insertions += 1
                                logger.debug(f"📄 Page {page_idx}, Block {block_idx}: Text insertion successful")
                            else:
                                logger.warning(f"📄 Page {page_idx}, Block {block_idx}: Text insertion failed")
                        except Exception as e:
                            logger.error(f"📄 Page {page_idx}, Block {block_idx}: Text insertion error: {str(e)}")

                logger.info(f"📄 Page {page_idx}: Text insertion completed ({successful_insertions}/{len(translation_blocks)} successful)")

                # Calculate page processing time
                page_time = time.time() - page_start_time
                logger.info(f"📄 PAGE {page_idx} COMPLETED in {page_time:.2f}s")

            # Save the translated document
            logger.info("💾 Saving translated document...")
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

            logger.info("✅ PDF TRANSLATION COMPLETED SUCCESSFULLY")
            logger.info(f"📄 Total pages processed: {len(page_numbers)}")
            logger.info(f"💾 Output file: {output_filename}")

            return {
                'success': True,
                'output_path': str(output_path),
                'filename': output_filename,
                'translated_pages': len(page_numbers)
            }

        except Exception as e:
            logger.error(f"❌ PDF TRANSLATION FAILED: {str(e)}")
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
    
    def _split_translated_text(self, translated_text, block_markers):
        """Split translated text back into individual blocks using markers."""
        translated_blocks = []
        current_text = translated_text

        for marker in block_markers:
            if marker in current_text:
                # Split at the marker
                parts = current_text.split(marker, 1)
                if len(parts) > 1:
                    # Everything before the marker is the previous block's text
                    if parts[0].strip():
                        translated_blocks.append(parts[0].strip())
                    # Continue with the rest
                    current_text = parts[1]
                else:
                    # Marker not found, add empty text
                    translated_blocks.append("")
            else:
                # Marker not found, add empty text
                translated_blocks.append("")

        # Add any remaining text after the last marker
        if current_text.strip():
            translated_blocks.append(current_text.strip())

        logger.debug(f"Split {len(translated_blocks)} blocks from translated text")
        return translated_blocks

    def _insert_translated_text(self, page, block_info):
        """Insert translated text with proper formatting."""
        translated_text = block_info['translated_text']
        bbox = block_info['bbox']

        # Create HTML content for better Unicode support
        html_content = self._create_html_for_text(block_info)

        try:
            # Try HTML insertion first (best for Unicode)
            logger.debug(f"Attempting HTML insertion for text ({len(translated_text)} chars)")
            result = page.insert_htmlbox(bbox, html_content)

            if result[0] >= 0:  # Success
                logger.debug("HTML insertion successful")
                return True
            else:
                logger.debug(f"HTML insertion failed with result: {result}")

        except Exception as e:
            logger.debug(f"HTML insertion failed: {e}")

        # Fallback to textbox with appropriate font
        try:
            fontname = self._get_font_for_language(block_info)
            color = self._convert_color(block_info['color'])

            logger.debug(f"Attempting textbox insertion with font: {fontname}")
            result = page.insert_textbox(
                bbox,
                translated_text,
                fontname=fontname,
                fontsize=max(8, min(block_info['font_size'], 20)),
                color=color,
                align=0
            )

            if result >= 0:
                logger.debug("Textbox insertion successful")
                return True

            # Try with smaller font sizes
            for scale in [0.8, 0.6, 0.4]:
                smaller_size = block_info['font_size'] * scale
                if smaller_size < 6:
                    break

                logger.debug(f"Retrying with smaller font size: {smaller_size}")
                result = page.insert_textbox(
                    bbox,
                    translated_text,
                    fontname=fontname,
                    fontsize=smaller_size,
                    color=color,
                    align=0
                )

                if result >= 0:
                    logger.debug(f"Textbox insertion successful with font size {smaller_size}")
                    return True

        except Exception as e:
            logger.debug(f"Textbox insertion failed: {e}")

        # Ultimate fallback
        try:
            logger.debug("Attempting ultimate fallback text insertion")
            page.insert_text(
                bbox.tl,
                translated_text,
                fontsize=12,
                color=(0, 0, 0)
            )
            logger.debug("Ultimate fallback successful")
            return True
        except Exception as e:
            logger.debug(f"Ultimate fallback failed: {e}")
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
