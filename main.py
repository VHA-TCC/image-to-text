import base64
from io import BytesIO
import re
from vision import CloudVision

from image import Image

car_plate_regex = '^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$'

def main(request) -> None:
    data = request.get_json(force=True)
    image_b64 = data.get('vehicle_plate')
    buffer = BytesIO(base64.b64decode(image_b64))
    image = Image().set_image(buffer)
    
    vision = CloudVision()
    
    analysis = vision.extract_text(image=image)
    
    for block in analysis.blocks:
        text = block.text
        has_car_plate = re.search(car_plate_regex, text)
        if has_car_plate:
            return { "car_plate": text }, 200
        
    return { "error": "could not find any car plates" }, 400
