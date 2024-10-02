# utils.py

import colorsys

class ColorUtils:
    @staticmethod
    def get_color_name_from_hex(hex_code):
        """
        Convert a hex color code to a common color name.
        """
        # Remove the hash symbol if present
        hex_code = hex_code.lstrip('#')

        # Convert hex to RGB
        r, g, b = tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

        # Convert RGB to HSV
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

        # Define broad categories for common colors based on Hue
        if s < 0.1 and v > 0.9:
            return "White"
        elif s < 0.1:
            return "Gray"
        elif v < 0.1:
            return "Black"

        # Map hue ranges to color names
        hue = h * 360
        if 0 <= hue < 15 or 345 <= hue <= 360:
            return "Red"
        elif 15 <= hue < 45:
            return "Orange"
        elif 45 <= hue < 75:
            return "Yellow"
        elif 75 <= hue < 165:
            return "Green"
        elif 165 <= hue < 195:
            return "Cyan"
        elif 195 <= hue < 255:
            return "Blue"
        elif 255 <= hue < 285:
            return "Purple"
        elif 285 <= hue < 345:
            return "Pink"
        else:
            return "Unknown"
