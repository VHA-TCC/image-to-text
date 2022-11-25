from PIL import Image as PilImage, ImageDraw, ImageFont


class Pillow:
    def convert_to_rgb(self, image: PilImage) -> ImageDraw:
        return image.convert('RGBA')