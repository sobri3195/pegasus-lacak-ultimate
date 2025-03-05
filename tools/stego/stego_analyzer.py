from PIL import Image
import numpy as np
from scipy.fftpack import dct
import cv2
from datetime import datetime
import os

class StegoAnalyzer:
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.bmp']
        
    def analyze_image(self, image_path):
        """Analisis steganografi pada gambar"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "file": image_path,
            "analysis": {}
        }
        
        try:
            # Basic Analysis
            results["analysis"]["basic"] = self.basic_analysis(image_path)
            
            # Statistical Analysis
            results["analysis"]["statistical"] = self.statistical_analysis(image_path)
            
            # LSB Analysis
            results["analysis"]["lsb"] = self.lsb_analysis(image_path)
            
            # Visual Analysis
            results["analysis"]["visual"] = self.visual_analysis(image_path)
            
            return results
        except Exception as e:
            return {"error": str(e)}
            
    def basic_analysis(self, image_path):
        """Analisis dasar"""
        img = Image.open(image_path)
        return {
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "file_size": os.path.getsize(image_path)
        }
        
    def statistical_analysis(self, image_path):
        """Analisis statistik"""
        img = cv2.imread(image_path)
        return {
            "mean": img.mean(),
            "std": img.std(),
            "entropy": self.calculate_entropy(img)
        }
        
    def lsb_analysis(self, image_path):
        """Analisis LSB (Least Significant Bit)"""
        img = np.array(Image.open(image_path))
        lsb = img & 1
        return {
            "lsb_mean": lsb.mean(),
            "lsb_std": lsb.std(),
            "suspicious": self.check_suspicious_patterns(lsb)
        }
        
    def visual_analysis(self, image_path):
        """Analisis visual"""
        img = cv2.imread(image_path)
        edges = cv2.Canny(img, 100, 200)
        return {
            "edge_density": edges.mean(),
            "suspicious_regions": self.detect_suspicious_regions(img)
        } 