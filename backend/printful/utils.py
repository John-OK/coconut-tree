from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
from django.conf import settings
import logging
import re

# max_width_ratio adjusts ratio of total text width to image width
# max_height adjusts ratio of total text height to image height
# start_y adjusts height from top of shirt/image
# spacing_ratio adjust space between lines as ratio of font height

def generate_text_image(
    user_text,
    image_size=(1800, 2400),
    text_color=(255, 255, 255),
    bg_color=(0, 0, 0, 0),
    max_line_length=10,
    max_width_ratio=1,
    max_height_ratio=1,
    spacing_ratio=0.4
    ):
    try:
        # Create a new image with transparent background
        image = Image.new('RGBA', image_size, color=bg_color)
        draw = ImageDraw.Draw(image)

        # Load the font
        font_path = settings.FONTS_DIR / 'outfit' / 'Outfit-Medium.ttf'

        def split_text(text):
            words = []
            warning_needed = False
            
            # Split by spaces and hyphens, keeping hyphens
            parts = re.split(r'(\s+|-)', text.upper())
            current_word = ''
            
            for part in parts:
                part = part.strip()
                if part:
                    if part == '-':
                        current_word += part
                    elif len(current_word + part) <= max_line_length:
                        current_word += (' ' if current_word and current_word[-1] != '-' else '') + part
                    else:
                        if current_word:
                            words.append(current_word)
                        current_word = part
                    
                    if len(part) > max_line_length:
                        warning_needed = True
            
            if current_word:
                words.append(current_word)

            return words, warning_needed

        def group_words(words):
            lines = []
            current_line = []
            current_length = 0

            for word in words:
                word_length_with_space = len(word) + (1 if current_line else 0)
                if len(word) > max_line_length:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = []
                        current_length = 0
                    lines.append(word)
                elif current_length + word_length_with_space <= max_line_length:
                    current_line.append(word)
                    current_length += word_length_with_space
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)

            if current_line:
                lines.append(' '.join(current_line))

            return lines

        # Split and group the user input text
        words, warning_needed = split_text(user_text)
        user_lines = group_words(words)

        # Prepare all lines of text
        lines = user_lines + ["TRUMPS", "Trump"]

        # Function to calculate text size
        def get_text_size(text, font_size):
            font = ImageFont.truetype(str(font_path), max(1, font_size))
            bbox = draw.textbbox((0, 0), text, font=font)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Find the maximum font size that fits the width and height for all lines
        max_width = int(image_size[0] * max_width_ratio)
        max_height = int(image_size[1] * 1)  # 100% of image height
        font_size = 1
        max_font_size = 1000  # Set a reasonable upper limit
        while font_size < max_font_size:
            fits = True
            total_height = 0
            for i, line in enumerate(lines):
                if i == len(user_lines):  # "TRUMPS" line
                    test_font_size = max(1, int(font_size * 0.8))
                elif i == len(user_lines) + 1:  # "Trump" line
                    test_font_size = max(1, int(font_size * 0.6))
                else:
                    test_font_size = font_size

                width, height = get_text_size(line, test_font_size)
                if width > max_width:
                    fits = False
                    break
                total_height += height

            # Calculate spacing based on the current font size
            spacing = max(1, int(font_size * spacing_ratio))
            total_height += (len(lines) - 1) * spacing

            if total_height > max_height:
                fits = False

            if not fits:
                break
            font_size += 1

        font_size = max(1, font_size - 1)  # Ensure font_size is at least 1

        # Calculate heights for each line
        line_heights = [font_size] * len(user_lines) + [max(1, int(font_size * 0.8)), max(1, int(font_size * 0.6))]

        # Calculate spacing based on the final font size
        spacing = max(1, int(font_size * spacing_ratio))
        
        # Calculate total height of all text
        total_height = sum(line_heights) + (len(lines) - 1) * spacing

        # Calculate starting Y position to center all text vertically
        start_y = max(100, (image_size[1] - total_height) // 2)

        current_y = start_y

        for line, height in zip(lines, line_heights):
            font = ImageFont.truetype(str(font_path), height)
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((image_size[0] - text_width) // 2, current_y)
            draw.text(position, line, font=font, fill=text_color)
            current_y += text_height + spacing

        return image, warning_needed

    except Exception as e:
        logging.error(f"Error generating image: {str(e)}")
        raise

def get_image_as_base64(user_text):
    try:
        image, warning = generate_text_image(user_text)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        logging.error(f"Error in get_image_as_base64: {str(e)}")
        raise

def save_text_image(user_text, filename):
    image, warning = generate_text_image(user_text)
    image.save(filename, format='PNG')
    return filename