import os
import time
from PIL import Image
import shutil
import platform
import argparse


def get_more_detailed_mapper(more_detailed=False):
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
    x, y = size
    x_, y_ = aspect_ratio

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
    rows = text.split("\n")
    new_txt = ""
    for row in rows:
        if len(row) > width:
            sliced = [row[i:i + width] for i in range(0, len(row), width)]
            row = "\n".join(sliced)
        new_txt += row + "\n"
    return new_txt[:-1]


def round_to_specific(x, more_detailed=False, reverse=False):
    base = 0.05 if more_detailed else 0.1
    return round(1 - base * round(x / base), 2) if reverse else round(base * round(x / base), 2)


def gif_to_ascii(file_path, reverse_colors=False, loop=False, t=0.01, more_detailed=False):
    # Open the GIF file
    gif_image = Image.open(file_path)

    mapper = get_more_detailed_mapper(more_detailed=more_detailed)
    while True:
        for frame_number in range(gif_image.n_frames):
            gif_image.seek(frame_number)

            grayscale_frame = gif_image.convert("L")
            window_size = shutil.get_terminal_size()  # os.get_terminal_size()

            # add additional text
            extra_text = format_additional_text(
                (f"\n{' File':<20}: {file_path}\n{' Reverse Colors':<20}: {reverse_colors}\n"
                 f"{' Loop':<20}: {loop}\n{' T parameter':<20}: {t}\n"
                 f"{' T more_detailed':<20}: {more_detailed}\n"), window_size.columns)

            # text makes animation smaller. the hard coded 2 is the following: one for the line and one for title
            additional_lines = 4 + extra_text.count("\n")

            # get terminal image size and resize image
            x_new, y_new = calculate_ascii_image_size((window_size.columns, window_size.lines - additional_lines),
                                                      gif_image.size)
            grayscale_frame = grayscale_frame.resize((int(x_new), y_new))

            # create ascii string
            res_str = "\033[1mVERY NICE ANIMATION\033[0m".center(window_size.columns) + "\n"
            for y in range(grayscale_frame.size[1]):

                row_str = ""
                for x in range(grayscale_frame.size[0]):
                    pixel_value = grayscale_frame.getpixel((x, y))
                    val = round_to_specific(pixel_value / 255, reverse=reverse_colors, more_detailed=more_detailed)
                    row_str += mapper[val]

                res_str += row_str.center(window_size.columns) + f"\n"

            print(f"{res_str}\033[1m{window_size.columns * '='}\n\n\033[0m{extra_text}", end='\033[H\033[J')

            time.sleep(t)
        if not loop:
            break


def main():
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

    if platform.system() == "Windows":
        os.system("")
    gif_to_ascii(args.GIF_file, args.reverse_colors, args.loop, args.t, args.more_detailed)


if __name__ == "__main__":
    main()
