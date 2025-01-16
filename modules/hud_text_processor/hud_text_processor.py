import logging
import os.path
import re


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
    def generate_upscaled_txt(hud_txt_file: str,  max_resolution=2560):
        sprite_rows = HudTextProcessor.read_sprite_text_data(hud_txt_file)
        start_resolution = HudTextProcessor.get_max_resolution(sprite_rows)
        current_resolution = start_resolution * 2
        sprite_data_set = HudTextProcessor.get_selected_resolution_rows(sprite_rows, start_resolution)
        all_upscaled_data = []
        all_upscaled_data.extend(sprite_rows)
        while current_resolution <= max_resolution:
            upscaled = HudTextProcessor.upscale_sprite_offsets(sprite_data_set, current_resolution)
            all_upscaled_data.extend(upscaled)
            sprite_data_set = upscaled
            current_resolution *= 2
        all_upscaled_data[0][0] = str(len(all_upscaled_data) - 1)
        return all_upscaled_data

    @staticmethod
    def upscale_txt(hud_txt_file: str, max_resolution: int = 2560):
        generated_data = HudTextProcessor.generate_upscaled_txt(hud_txt_file, max_resolution)
        output_file_name = os.path.join(os.path.dirname(hud_txt_file),
                                        os.path.basename(hud_txt_file).replace('.txt', '_upscaled.txt'))
        with open(output_file_name, 'w', encoding='utf-8') as file:
            for i in generated_data:
                file.write("\t".join(i) + '\n')

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
