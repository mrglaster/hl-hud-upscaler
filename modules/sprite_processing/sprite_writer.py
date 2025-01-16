import math
import struct
from PIL import Image


class SpriteWriter:

    @staticmethod
    def write_spr_header(spr_file, width, height, numframes, sprite_type=2, texture_format=1, synctype=0):
        bounding_radius = 32
        if width > 0 and height > 0:
            bounding_radius = math.sqrt(((width / 2) ** 2) + ((height / 2) ** 2))

        spr_file.write(b'IDSP')  # Identifier
        spr_file.write(struct.pack('<i', 2))  # Version (2 for Half-Life)
        spr_file.write(struct.pack('<i', sprite_type))  # Sprite type
        spr_file.write(struct.pack('<i', texture_format))  # Texture Format (0 = SPR_NORMAL)
        spr_file.write(struct.pack('<f', bounding_radius))
        spr_file.write(struct.pack('<i', width))  # Width
        spr_file.write(struct.pack('<i', height))  # Height
        spr_file.write(struct.pack('<i', numframes))  # Number of frames
        spr_file.write(struct.pack('<f', 0.0))  # Beamlength (not used)
        spr_file.write(struct.pack('<i', synctype))  # Synctype (0 for synchronized)

    @staticmethod
    def write_palette_data(spr_file, image, palette):
        spr_file.write(struct.pack('<h', 256))
        # palette = image.getpalette()#[:768]  # 256 colors * 3 (R, G, B)
        spr_file.write(bytearray(palette))

    @staticmethod
    def closest_color_index(rgb, color_list):
        """Find the index of the closest color in the list."""
        distances = [SpriteWriter.euclidean_distance(rgb, color) for color in color_list]
        return distances.index(min(distances))

    @staticmethod
    def euclidean_distance(c1, c2):
        """Calculate the Euclidean distance between two colors."""
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

    @staticmethod
    def write_indexed_data(spr_file, image, palette):
        img_data = list(image.getdata())
        indexed_data = []

        palette_colors = []
        for i in range(0, len(palette) - 4, 3):
            palette_colors.append(palette[i:i + 3])

        img_colors = []
        for i in range(0, len(img_data), 1):
            col = img_data[i]
            img_colors.append(list(col))

        num_prints = 0

        for p in img_colors:
            idx = 0
            if p in palette_colors:
                # print(f"found {p} in palette_colors")
                idx = palette_colors.index(p)
            else:
                num_prints = num_prints + 1
                if num_prints < 30:
                    pass

            indexed_data.append(idx)

        spr_file.write(bytearray(indexed_data))

    @staticmethod
    def next_power_of_two(n):
        """Return the next power of two for given n."""
        return 2 ** (n - 1).bit_length()

    @staticmethod
    def pad_image_to_power_of_two(image):
        """Pad image dimensions to the next power of two."""
        width, height = image.size
        new_width = SpriteWriter.next_power_of_two(width)
        new_height = SpriteWriter.next_power_of_two(height)

        # Create a new blank image with the padded size
        padded_image = Image.new("RGB", (new_width, new_height), 0)
        padded_image.paste(image, (0, 0))
        return padded_image

    @staticmethod
    def create_palette(img):
        """Extract unique colors from the image and create a palette."""
        # Get the list of all colors in the image
        colors = list(img.getdata())
        # Deduplicate the colors
        unique_colors = sorted(list(set(colors)))
        # print( f"unique_colors: {unique_colors}" )

        # Create a palette
        palette = []
        for color in unique_colors:
            palette.extend(color[:3])  # We only want RGB, not RGBA

        # Fill the rest of the 256-color palette with black
        while len(palette) < 256 * 3:
            palette.extend((0, 0, 0))

        # print( f"palette: {palette}" )

        return unique_colors, palette

    @staticmethod
    def palettize_image(img, unique_colors, palette):
        # Create a palette image whose size does not matter
        arbitrary_size = 16, 16
        palimage = Image.new('P', arbitrary_size)
        palimage.putpalette(palette)

        img_p = img.convert("P", 0, palimage.im)
        img_p.putpalette(palette)
        return img_p

    @staticmethod
    def img_to_spr(img_path, spr_path):
        # 1. Read the image file and convert to indexed color
        image = Image.open(img_path).convert("RGBA")

        # 1.1. Pad image to power of two dimensions
        image = SpriteWriter.pad_image_to_power_of_two(image)
        width, height = image.size

        # Extract unique colors and create a palette
        unique_colors, palette = SpriteWriter.create_palette(image)

        # Palettize the image
        # image.save(spr_path + "_PALETTETIME.png")

        # print("\n\n\n")

        with open(spr_path, 'wb') as spr_file:
            # 2. Write SPR header
            SpriteWriter.write_spr_header(spr_file, width, height, 1)

            # 3. Write the palette data
            SpriteWriter.write_palette_data(spr_file, image, palette)

            # 4. Write the frame header
            spr_file.write(struct.pack('<i', 0))  # frame group
            spr_file.write(struct.pack('<i', int(-width / 2)))  # frame_origin_x
            spr_file.write(struct.pack('<i', int(-height / 2)))  # frame_origin_y
            spr_file.write(struct.pack('<i', width))  # frame_width
            spr_file.write(struct.pack('<i', height))  # frame_height

            # 4.1 Write the indexed data
            SpriteWriter.write_indexed_data(spr_file, image, palette)
