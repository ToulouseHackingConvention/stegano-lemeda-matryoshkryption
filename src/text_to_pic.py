#!/usr/bin/env python

"""
text_to_pic.py

Creates a picture containing the text given as input
"""
import argparse
import logging
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile
from PIL import ImageFont
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")


def create_picture(input_file, output_file, asbytes=False, prefix="", width=600, height=200):
    if asbytes:
        text = open(input_file, "rb").read()
        text = ''.join("{:02x}".format(c) for c in text)
    else:
        text = open(input_file, "r").read()

    text = prefix + text
    logger.debug(text)

    pic = Image.new("RGB", (600, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype("/usr/share/fonts/TTF/Inconsolata-Bold.ttf", 32)
    w, h = draw.textsize(text, font=font)
    draw.text(((width - w) // 2, (height - h) // 2), text, (0, 0, 0), font=font)

    #pic.show()
    pic.save(output_file)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    parser = argparse.ArgumentParser(description="Creates a picture containing the text given as input")
    parser.add_argument("--input", "-i", required=True, help="File containing the text")
    parser.add_argument("--output", "-o", required=False, default="text.png", help="Output file")
    parser.add_argument("--asbytes", "-b", required=False, type=str2bool, nargs='?', const=True, default=False,
                        help="Embed the hexadecimal representation of each byte rather than the data itself.")
    parser.add_argument("--prefix", "-p", required=False, default="", help="Add prefix to data.")

    args = parser.parse_args()
    logger.debug(args)

    create_picture(args.input, args.output, args.asbytes, args.prefix)


if __name__ == "__main__":
    main()
