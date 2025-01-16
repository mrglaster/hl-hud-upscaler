import os
import shutil
import numpy as np
from PIL import Image
from colortrans import colortrans
from modules.image_processing.image_upscaler import ImageUpscaler
from modules.sprite_processing.sprite_extractor import SpriteExtractor
from modules.sprite_processing.sprite_writer import SpriteWriter


class ImageProcessor:

    @staticmethod
    def transmit_color(image, reference):
        with Image.open(image) as img:
            content = np.array(img.convert('RGB'))
        with Image.open(reference) as img:
            reference = np.array(img.convert('RGB'))
        output_reinhard = colortrans.transfer_reinhard(content, reference)
        Image.fromarray(output_reinhard).quantize(colors=256, method=2).save(image)

    @staticmethod
    def process_raw_image(raw_image_path, upscaling_model: str = 'edsr-base'):
        width, height = Image.open(raw_image_path).size
        new_size = width * 2
        sizes_dirs_create = {
            128: 256,
            256: 512,
            512: 1280,
            1024: 2560
        }
        sprite_dir = os.path.dirname(raw_image_path)
        if new_size in sizes_dirs_create:
            new_resolution_dir = os.path.join(sprite_dir, str(sizes_dirs_create[new_size]))
            os.makedirs(new_resolution_dir, exist_ok=True)
            upscaled_path = os.path.join(new_resolution_dir, os.path.basename(raw_image_path))
            ImageUpscaler.upscale_image(raw_image_path, f"{upscaled_path}", upscaling_model=upscaling_model)
            ImageProcessor.transmit_color(upscaled_path, raw_image_path)
            SpriteWriter.img_to_spr(upscaled_path, upscaled_path.replace('.png', '.spr'))

            os.remove(raw_image_path)
            shutil.copy(upscaled_path, raw_image_path)
            return ImageProcessor.process_raw_image(raw_image_path)
        else:
            return True

    @staticmethod
    def process_sprite(sprite_path, upscaling_model: str = 'edsr-base'):
        raw_image_path = sprite_path.replace('.spr', '.png')
        SpriteExtractor.extract_image(sprite_path, raw_image_path)
        ImageProcessor.process_raw_image(raw_image_path, upscaling_model)
