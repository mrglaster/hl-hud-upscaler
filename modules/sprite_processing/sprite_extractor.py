# Code for image data extraction was borrowed from: https://github.com/ValveSoftware/halflife/blob/master/devtools/image_to_spr.py
# Check the .spr format structure here: https://developer.valvesoftware.com/wiki/SPR

import struct
from PIL import Image


class SpriteExtractor:

    @staticmethod
    def read_sprite_data(sprite_path) -> tuple:
        with open(sprite_path, 'rb') as f:
            # Read the SPR header
            id = f.read(4).decode()
            if id != 'IDSP':
                raise ValueError("Not a valid SPR file")

            version, = struct.unpack('<i', f.read(4))
            type, = struct.unpack('<i', f.read(4))

            if type != 2:  # 2 = VP_PARALLEL
                raise ValueError(f"Only VP_PARALLEL type supported, got {type}")

            # other header info...
            format, = struct.unpack('<i', f.read(4))
            bounding_radius, = struct.unpack('<f', f.read(4))
            width, = struct.unpack('<i', f.read(4))
            height, = struct.unpack('<i', f.read(4))
            num_frames, = struct.unpack('<i', f.read(4))
            beam_len, = struct.unpack('<f', f.read(4))
            sync_type, = struct.unpack('<i', f.read(4))

            # For simplicity, assume a single frame
            if num_frames != 1:
                raise ValueError(f"Only single frame SPRs supported, got {num_frames}")

            palette_len, = struct.unpack('<h', f.read(2))

            # Read the palette (256 RGB entries)
            palette = [(ord(f.read(1)), ord(f.read(1)), ord(f.read(1))) for _ in range(256)]

            # Read the frame
            frame_group, = struct.unpack('<i', f.read(4))
            frame_origin_x, = struct.unpack('<i', f.read(4))
            frame_origin_y, = struct.unpack('<i', f.read(4))
            frame_width, = struct.unpack('<i', f.read(4))
            frame_height, = struct.unpack('<i', f.read(4))

            data = f.read(width * height)

        return width, height, palette, data

    @staticmethod
    def save_as_png(filename, width, height, palette, data):
        img_data = [palette[byte] for byte in data]
        img = Image.new('RGB', (width, height))
        img.putdata(img_data)
        img.save(filename)

    @staticmethod
    def extract_image(sprite_path, image_path):
        width, height, palette, data = SpriteExtractor.read_sprite_data(sprite_path=sprite_path)
        SpriteExtractor.save_as_png(filename=image_path, width=width, height=height, palette=palette, data=data)
