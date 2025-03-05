import os
from PIL import Image
from PIL.ExifTags import TAGS
import magic
import PyPDF2
from datetime import datetime

class MetadataExtractor:
    def __init__(self):
        self.supported_types = {
            'image': ['.jpg', '.jpeg', '.png', '.tiff'],
            'document': ['.pdf', '.doc', '.docx'],
            'audio': ['.mp3', '.wav'],
            'video': ['.mp4', '.avi']
        }
        
    def extract_metadata(self, file_path):
        """Extract metadata dari file"""
        try:
            file_type = magic.from_file(file_path, mime=True)
            ext = os.path.splitext(file_path)[1].lower()
            
            results = {
                "timestamp": datetime.now().isoformat(),
                "file_path": file_path,
                "file_type": file_type,
                "file_size": os.path.getsize(file_path),
                "metadata": {}
            }
            
            if ext in self.supported_types['image']:
                results["metadata"] = self.extract_image_metadata(file_path)
            elif ext in self.supported_types['document']:
                results["metadata"] = self.extract_document_metadata(file_path)
                
            return results
        except Exception as e:
            return {"error": str(e)}
            
    def extract_image_metadata(self, image_path):
        """Extract metadata dari gambar"""
        try:
            image = Image.open(image_path)
            exif = {}
            
            if hasattr(image, '_getexif'):
                info = image._getexif()
                if info:
                    for tag, value in info.items():
                        decoded = TAGS.get(tag, tag)
                        exif[decoded] = str(value)
                        
            return {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "exif": exif
            }
        except Exception as e:
            return {"error": str(e)}
            
    def extract_document_metadata(self, doc_path):
        """Extract metadata dari dokumen"""
        try:
            if doc_path.endswith('.pdf'):
                with open(doc_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    info = pdf.metadata
                    return {
                        "author": info.get('/Author', ''),
                        "creator": info.get('/Creator', ''),
                        "producer": info.get('/Producer', ''),
                        "subject": info.get('/Subject', ''),
                        "title": info.get('/Title', ''),
                        "pages": len(pdf.pages)
                    }
            return {"error": "Format tidak didukung"}
        except Exception as e:
            return {"error": str(e)} 