from typing import Any
from google.cloud import vision

from image import Image
from ocr_analysis import OCRAnalysis, TextBlock

class CloudVision:
    _client: vision.ImageAnnotatorClient = None

    def __init__(self, service_account_path: str = None):
        self._client = self._get_client_authenticated(service_account_path=service_account_path)
    
    @property
    def client(self) -> vision.ImageAnnotatorClient:
        return self._client

    def _get_client_authenticated(self, service_account_path: str) -> vision.ImageAnnotatorClient:
        if service_account_path is not None:
            return vision.ImageAnnotatorClient.from_service_account_json(filename=service_account_path)
        return vision.ImageAnnotatorClient()
    
    def extract_text(self, image: Image) -> OCRAnalysis:
        vision_image = vision.Image(content=bytes(image.content.getbuffer()))
        response = self.client.text_detection(image=vision_image)
        text_blocks = response.full_text_annotation
        imageToText = OCRAnalysis()
        
        if not text_blocks: return OCRAnalysis()
        
        for text_block in text_blocks.pages[0].blocks:
            current_text_block = TextBlock(text=self.extract_text_from_paragraphs(paragraphs=text_block.paragraphs),
                                           position=self.extract_text_left_top_coords(bounding_box=text_block.bounding_box),
                                           area=self.extract_text_area(bounding_box=text_block.bounding_box))
            imageToText.blocks.append(current_text_block)
        
        return imageToText
