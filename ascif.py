import os
import time
from PIL import Image
import shutil
import platform
import argparse


def get_mapper(more_detailed=False):
    """
    Get dictionary mapping pixel brightness to ascii symbols.
    :param more_detailed: bool, determines number of colors in ballet.
    :return: mapping dictionary.
    """
    return {
        0.00: "@", 0.05: "@", 0.10: "#", 0.15: "%",
        0.20: "$", 0.25: "£", 0.30: "&", 0.35: "0",
        0.40: "O", 0.45: "o", 0.50: "?", 0.55: "*",
        0.60: "<", 0.65: ">", 0.70: "-", 0.75: "'",
        0.80: "'", 0.85: ".", 0.90: "´", 0.95: " ",
        1.00: " "
    } if more_detailed else {
        1.0: ' ', 0.9: '.', 0.8: '+', 0.7: '>',
        0.6: '?', 0.5: '*', 0.4: '&', 0.3: '$',
        0.2: '#', 0.1: '%', 0.0: "@"}


def calculate_ascii_image_size(size, aspect_ratio):
    """
    Calculate max size of ascii gif with suitable aspect ratio.
    :param size: size of terminal
    :param aspect_ratio: size of original gif (used to get aspect ratio).
    :return: calculated ascii gif size.
    """
    x, y = size
    x_, y_ = aspect_ratio

    # Because terminal single symbol space has larger height than weight
    y_ = y_ * 0.7

    # Calculate the width based on the height (maintaining aspect ratio)
    width = int(y * (x_ / y_))

    # If the calculated width fits within the available width, use it
    if width <= x:
        return width, y
    else:
        # Calculate the height based on the width (maintaining aspect ratio)
        height = int(x * (y_ / x_))
        return x, height


def format_additional_text(text, width):
    """
    Format string to fit terminal window.
    :param text: text to be formatted.
    :param width: max width.
    :return: formatted text.
    """
    rows = text.split("\n")
    new_txt = ""
    for row in rows:
        if len(row) > width:
            sliced = [row[i:i + width] for i in range(0, len(row), width)]
            row = "\n".join(sliced)
        new_txt += row + "\n"
    return new_txt[:-1]


def round_to_specific(x, more_detailed=False, reverse=False):
    """
    Round given number to wanted lengths.
    :param x: number to be rounded.
    :param more_detailed: sets rounding length to more detailed.
    :param reverse: flips black and white meaning returns 1- result instead of result.
    :return: rounded number.
    """
    base = 0.05 if more_detailed else 0.1
    return round(1 - base * round(x / base), 2) if reverse else round(base * round(x / base), 2)


def gif_to_ascii(file_path, reverse_colors=False, loop=False, t=0.01, more_detailed=False):
    """
    Main logic function. Takes in path to gif and prints out gif in ascii format.
    :param file_path: path to GIF file.
    :param reverse_colors: reverses colors, black turns white and white turns black etc.
    :param loop: if True keeps ascii GIF looping.
    :param t: determines time between frames.
    :param more_detailed: if True sets number of colors in color ballet to 21 instead od default 11.
    """
    # Open the GIF file
    gif_image = Image.open(file_path)
    mapper = get_mapper(more_detailed=more_detailed)
    # Start looping, break after first iteration if loop is False
    while True:
        for frame_number in range(gif_image.n_frames):
            gif_image.seek(frame_number)

            grayscale_frame = gif_image.convert("L")
            window_size = shutil.get_terminal_size()  # os.get_terminal_size()

            # Add additional text
            extra_text = format_additional_text(
                (f"\n{' File':<20}: {file_path}\n{' Reverse Colors':<20}: {reverse_colors}\n"
                 f"{' Loop':<20}: {loop}\n{' T parameter':<20}: {t}\n"
                 f"{' More detailed':<20}: {more_detailed}\n"), window_size.columns)

            # Text makes animation smaller. The hard coded 3 is the following: one for the line under the animation,
            # one for the extra empty line between animation and extra text and one for the title.
            additional_lines = 3 + extra_text.count("\n")

            # Get terminal image size and resize image
            x_new, y_new = calculate_ascii_image_size((window_size.columns, window_size.lines - additional_lines),
                                                      gif_image.size)
            grayscale_frame = grayscale_frame.resize((int(x_new), y_new))

            # Create ascii string
            res_str = "\033[1mVERY NICE ANIMATION\033[0m".center(window_size.columns) + "\n"
            for y in range(grayscale_frame.size[1]):

                row_str = ""
                for x in range(grayscale_frame.size[0]):
                    pixel_value = grayscale_frame.getpixel((x, y))
                    val = round_to_specific(pixel_value / 255, reverse=reverse_colors, more_detailed=more_detailed)
                    row_str += mapper[val]

                res_str += row_str.center(window_size.columns) + f"\n"
            # Print out GIF frame as ascii using .center() to format animation to the center of the window and use ANSI
            # escape codes to clear terminal between frames.
            print(f"{res_str}\033[1m{window_size.columns * '='}\n\033[0m{extra_text}", end='\033[H\033[J')

            time.sleep(t)
        # Break out of while loop if loop is set to False
        if not loop:
            break


def main():
    # Needed to enable using ANSI escape codes
    if platform.system() == "Windows":
        os.system("")

    parser = argparse.ArgumentParser(description="GIF file to ascii animation")

    # Positional arguments
    parser.add_argument("GIF_file", help="Path to the GIF file")

    # Optional arguments
    parser.add_argument("--reverse_colors", action="store_true", help="Reverse the colors")
    parser.add_argument("--loop", action="store_true", help="Enable looping")
    parser.add_argument("--t", type=float, default=0.01, help="Time parameter")
    parser.add_argument("--more_detailed", action="store_true", help="More detailed")

    # Parse the command-line arguments
    args = parser.parse_args()

    gif_to_ascii(args.GIF_file, args.reverse_colors, args.loop, args.t, args.more_detailed)


if __name__ == "__main__":
    main()
