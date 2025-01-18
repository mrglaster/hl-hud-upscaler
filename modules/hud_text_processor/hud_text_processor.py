import re
import json
import logging
import os.path


class HudTextProcessor:

    @staticmethod
    def read_sprite_text_data(hud_txt_file: str):
        logging.info(f"Reading content of file: {hud_txt_file}")
        with open(hud_txt_file, 'r', encoding='utf-8') as file:
            data = file.read()
            lines = data.strip().split('\n')
            file_data = []
            for line in lines:
                values = re.findall(r'\S+', line)
                if len(values) and (len(values) == 7 or len(values) == 1):
                    file_data.append(values)
            return file_data

    @staticmethod
    def get_selected_resolution_rows(sprite_rows: list, selected_resolution: int):
        logging.info(f"Getting rows for resolution: {selected_resolution}")
        values_set = []
        for line in sprite_rows:
            if len(line) < 2:
                continue
            if line[1] == str(selected_resolution):
                values_set.append(line)
        return values_set

    @staticmethod
    def upscale_sprite_offsets(sprite_data_set: list, current_resolution: int):
        upscaled_sprite_data = [row[:] for row in sprite_data_set]
        for i in range(len(upscaled_sprite_data)):
            upscaled_sprite_data[i][1] = str(current_resolution)

            if 'crosshairs' in upscaled_sprite_data[i][2]:
                continue
            slash_pos = upscaled_sprite_data[i][2].find('/')
            if slash_pos != -1:
                clean_name = upscaled_sprite_data[i][2][slash_pos + 1:]
                upscaled_sprite_data[i][2] = clean_name
            upscaled_sprite_data[i][2] = f"{current_resolution}/{upscaled_sprite_data[i][2]}"
            for j in range(3, len(upscaled_sprite_data[i])):
                upscaled_sprite_data[i][j] = str(int(upscaled_sprite_data[i][j]) * 2)
        return upscaled_sprite_data

    @staticmethod
    def fix_default_sprites_usage(sprite_rows, replacements_dict: dict):
        replacements_found = {}
        updated_rows = sprite_rows
        for i in range(1, len(updated_rows)):
            if 'ammo' in updated_rows[i][0] or 'crosshair' in updated_rows[i][0] or 'zoom' in updated_rows:
                if updated_rows[i][1] == '640':
                    if " ".join(updated_rows[i]) in replacements_dict:
                        replacements_found[updated_rows[i][0]] = " ".join(updated_rows[i])
                elif updated_rows[i][1] == '1280' and updated_rows[i][0] in replacements_found:
                    updated_rows[i] = replacements_dict[replacements_found[updated_rows[i][0]]]['1280']
                elif updated_rows[i][1] == '2560' and updated_rows[i][0] in replacements_found:
                    updated_rows[i] = replacements_dict[replacements_found[updated_rows[i][0]]]['2560']
        return updated_rows

    @staticmethod
    def get_replacements_dict() -> dict:
        replacements_path = 'data/auto_replacements.json'
        if not os.path.exists(replacements_path):
            logging.warning("Replacements dict was not opened!")
            return {}
        with open('data/auto_replacements.json') as file:
            logging.info("Replacements dictionary was opened")
            return json.load(file)

    @staticmethod
    def generate_upscaled_txt(hud_txt_file: str, max_resolution=2560):
        sprite_rows = HudTextProcessor.read_sprite_text_data(hud_txt_file)
        start_resolution = HudTextProcessor.get_max_resolution(sprite_rows)
        current_resolution = start_resolution * 2
        sprite_data_set = HudTextProcessor.get_selected_resolution_rows(sprite_rows, start_resolution)
        all_upscaled_data = []
        all_upscaled_data.extend(sprite_rows)
        replacements_dict = HudTextProcessor.get_replacements_dict()
        while current_resolution <= max_resolution:
            upscaled = HudTextProcessor.upscale_sprite_offsets(sprite_data_set, current_resolution)
            all_upscaled_data.extend(upscaled)
            sprite_data_set = upscaled
            current_resolution *= 2
        all_upscaled_data[1:] = HudTextProcessor.sort_txt(all_upscaled_data[1:])
        all_upscaled_data[0] = str(len(all_upscaled_data) - 1)
        return HudTextProcessor.fix_default_sprites_usage(all_upscaled_data, replacements_dict)

    @staticmethod
    def sort_txt(sprite_data):
        return sorted(sprite_data, key=lambda x: int(x[1]))

    @staticmethod
    def upscale_txt(hud_txt_file: str, max_resolution: int = 2560):
        generated_data = HudTextProcessor.generate_upscaled_txt(hud_txt_file, max_resolution)
        output_file_name = os.path.join(os.path.dirname(hud_txt_file),
                                        os.path.basename(hud_txt_file).replace('.txt', '_upscaled.txt'))
        with open(output_file_name, 'w', encoding='utf-8') as file:
            for i in generated_data:
                if len(i) > 2:
                    file.write("\t".join(i) + '\n')
                else:
                    file.write(i + '\n')

    @staticmethod
    def get_max_resolution(sprite_rows: list):
        previous_max = 320
        for row in sprite_rows:
            if len(row) != 7:
                continue
            if int(row[1]) > previous_max:
                previous_max = int(row[1])
        logging.info(f"Max sprite resolution found: {previous_max}")
        return previous_max
