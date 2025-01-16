import logging
from PIL import Image
from super_image import EdsrModel, ImageLoader


class ImageUpscaler:

    __allowed_models = [
        "drln-bam",
        "edsr",
        "msrn",
        "mdsr",
        "msrn-bam",
        "edsr-base",
        "mdsr-bam",
        "awsrn-bam",
        "a2n",
        "carn",
        "carn-bam",
        "pan",
        "pan-bam"
    ]

    @staticmethod
    def is_upscaling_model_valid(model_name: str):
        return model_name in ImageUpscaler.__allowed_models

    @staticmethod
    def upscale_image(image_path, output_path, upscaling_model: str = 'edsr-base'):
        image = Image.open(image_path)
        if not ImageUpscaler.is_upscaling_model_valid(upscaling_model):
            logging.warning(f"Unknown upscaling model: {upscaling_model}")
            logging.warning("Using default upscaling model edsr-base")
            upscaling_model = 'edsr-base'
        model = EdsrModel.from_pretrained(f'eugenesiow/{upscaling_model}', scale=2)
        inputs = ImageLoader.load_image(image)
        predictions = model(inputs)
        ImageLoader.save_image(predictions, output_path)
