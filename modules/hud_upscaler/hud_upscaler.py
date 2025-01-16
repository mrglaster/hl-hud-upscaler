import logging
import os

from modules.hud_text_processor.hud_text_processor import HudTextProcessor
from modules.image_processing.image_processor import ImageProcessor


class HudUpscaler:

    @staticmethod
    def upscale_hud(content_dir_path: str, upscaling_model: str = 'edsr-base'):
        dir_content = os.listdir(content_dir_path)
        weapon_txt = ''
        found_sprites = []
        for file in dir_content:
            if file.endswith('.spr'):
                found_sprites.append(os.path.join(content_dir_path, file))
                logging.info(f"Found sprite: {file}")
            elif file.startswith('weapon_') and file.endswith('.txt') and 'upscaled' not in file:
                logging.info(f"Weapon TXT description found: {file}")
                weapon_txt = os.path.join(content_dir_path, file)

        if weapon_txt == '':
            logging.critical("Weapon TXT file NOT FOUND!")
            return False

        if not len(found_sprites):
            logging.critical("No sprites found in the provided directory!")
            return False

        HudTextProcessor.upscale_txt(weapon_txt)

        txt_data = HudTextProcessor.read_sprite_text_data(weapon_txt)
        max_res = HudTextProcessor.get_max_resolution(txt_data)
        sprites_data = HudTextProcessor.get_selected_resolution_rows(txt_data, max_res)
        sprites_for_upscaling = [i[2] for i in sprites_data]
        for sprite in sprites_for_upscaling:
            sprite_path = os.path.join(content_dir_path, f'{sprite}.spr')
            if sprite_path not in found_sprites:
                logging.warning(f"Sprite {sprite_path} not found!")
                continue
            ImageProcessor.process_sprite(sprite_path, upscaling_model)
        logging.info("The converting process is DONE!")
        return True
