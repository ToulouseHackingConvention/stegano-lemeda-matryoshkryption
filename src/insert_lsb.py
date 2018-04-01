#!/usr/bin/env python

"""
insert_lsb.py

Inserts data in the LSBs of a picture, either directly in the bytes or visually.
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


def colors2mask(colors):
    mask = list()
    mask.append('r' in colors.lower())
    mask.append('g' in colors.lower())
    mask.append('b' in colors.lower())

    return mask


def insert_lsb(content, cover, output, colors):
    content = open(content, "rb").read()
    logger.debug(content)

    cover = Image.open(cover)

    mask = colors2mask(colors)
    logger.debug(mask)
    nb_comp = sum(mask)  # Number of components which will undergo modifications

    import bitarray
    ba = bitarray.bitarray()
    ba.frombytes(content)
    bits = list(map(int, ba))
    bits += (len(bits) % nb_comp) * [0]   # Pad list so its length is a multiple of nb_comp

    #logger.debug(bits)
    #logger.debug(len(bits))

    width, height = cover.size
    if len(bits) > nb_comp * width * height:
        raise RuntimeError("Message is too long and cannot be embedded in the provided cover file")

    pixels = cover.load()
    for index in range(0, len(bits), nb_comp):
        row = index // (width * nb_comp)
        col = (index // nb_comp) % width

        p = pixels[col, row]
        try:
            if nb_comp == 3:
                pixels[col, row] = ((p[0] | 1) - (1 - bits[index]) if mask[0] else p[0],
                                    (p[1] | 1) - (1 - bits[index + 1]) if mask[1] else p[1],
                                    (p[2] | 1) - (1 - bits[index + 2]) if mask[2] else p[2])
            elif nb_comp == 2:
                pixels[col, row] = ((p[0] | 1) - (1 - bits[index]) if mask[0] else p[0],
                                    (p[1] | 1) - (1 - bits[(index + 1) if mask[0] else index]) if mask[1] else p[1],
                                    (p[2] | 1) - (1 - bits[index + 1]) if mask[2] else p[2])
            elif nb_comp == 1:
                pixels[col, row] = ((p[0] | 1) - (1 - bits[index]) if mask[0] else p[0],
                                    (p[1] | 1) - (1 - bits[index]) if mask[1] else p[1],
                                    (p[2] | 1) - (1 - bits[index]) if mask[2] else p[2])

            #logger.debug(pixels[col, row])
        except IndexError as e:     # All bits have been embedded
            break

    cover.save(output, format="png")


def insert_lsb_visual(content, cover, output, color, asbytes, prefix):

    if asbytes:
        content = open(content, "rb").read()
        content = ''.join("{:02x}".format(c) for c in content)
    else:
        content = open(content, "r").read()

    content = prefix + content

    cover = Image.open(cover)
    logger.debug(cover)

    width, height = cover.size

    aux = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(aux)
    font = ImageFont.truetype("/usr/share/fonts/TTF/Inconsolata-Regular.ttf", 48)
    w, h = draw.textsize(content, font=font)
    draw.text(((width - w) // 2, height - 60), content, (254, 254, 254), font=font)

# Decomment next 2 lines if result is not clean enough
#    aux.save("aux.png")
#    aux = Image.open("aux.png")

    mask = colors2mask(color)
    logger.debug(mask)
    pixels = cover.load()
    pixels_aux = aux.load()
    for i in range(width):
        for j in range(height):
            p = pixels[i, j]
            if pixels_aux[i, j] != (0, 0, 0):
                # Set LSB of each component to 1
                pixels[i, j] = (p[0] | 1 if mask[0] else p[0],
                                p[1] | 1 if mask[1] else p[1],
                                p[2] | 1 if mask[2] else p[2])
            else:
                # Set LSB of each component to 0
                pixels[i, j] = (p[0] ^ (p[0] & 1) if mask[0] else p[0],
                                p[1] ^ (p[1] & 1) if mask[1] else p[1],
                                p[2] ^ (p[2] & 1) if mask[2] else p[2])

    cover.save(output)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():

    parser = argparse.ArgumentParser(description="Inserts data in the LSBs of a picture, either directly in the bytes\
                                                 or visually")
    parser.add_argument("--text", "-t", required=True, help="File containing the data to insert")
    parser.add_argument("--cover", "-c", required=True, help="Image file in which to insert data")
    parser.add_argument("--output", "-o", required=False, default="lsb_output.png", help="Output file")
    parser.add_argument("--colors", required=False, default="rgb",
                        help="Colors in which to hide content")
    parser.add_argument("--visual", "-v", required=False, type=str2bool, nargs='?', const=True, default=False,
                        help="Use visual LSB instead of traditional LSB")
    parser.add_argument("--asbytes", "-b", required=False, type=str2bool, nargs='?', const=True, default=False,
                        help="Embed the hexadecimal representation of each byte rather than the data itself.\
                             Available only for visual LSB.")
    parser.add_argument("--prefix", "-p", required=False, default="", help="Add prefix to data to embed (visual LSB only)")

    args = parser.parse_args()
    logger.debug(args)

    if args.visual:
        insert_lsb_visual(args.text, args.cover, args.output, args.colors.lower(), args.asbytes, args.prefix)
    else:
        insert_lsb(args.text, args.cover, args.output, args.colors.lower())


if __name__ == "__main__":
    main()
