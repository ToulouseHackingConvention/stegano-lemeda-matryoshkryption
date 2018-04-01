#!/usr/bin/env python

"""
generate_music_score

Creates a music score from an arbitrary text given as an input.
"""
import json
import logging

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")

char2notes = {"\n": "d b b g",
              " ": "a e e g",
              "!": "e e c a",
              "\"": "g e g c",
              "#": "d e e g",
              "$": "g f f f",
              "%": "c b c d",
              "&": "a a g f",
              "'": "a c b c",
              "(": "d f f e",
              ")": "f d f d",
              "*": "e b f g",
              "+": "f g g d",
              ",": "e b a f",
              "-": "f d d b",
              ".": "c f f b",
              "/": "e f a c",
              "0": "b e d a",
              "1": "e f c a",
              "2": "e e f d",
              "3": "e g a a",
              "4": "f c g a",
              "5": "c g a a",
              "6": "g c d e",
              "7": "f b b e",
              "8": "d d c g",
              "9": "e g f a",
              ":": "a c a b",
              ";": "a g f g",
              "<": "e b e g",
              "=": "b a d d",
              ">": "f f f d",
              "?": "e a a c",
              "@": "c e b c",
              "A": "c a e a",
              "B": "g e g d",
              "C": "g b b b",
              "D": "d b c g",
              "E": "f d e c",
              "F": "b e f e",
              "G": "e c f b",
              "H": "e e a g",
              "I": "e d a e",
              "J": "g e b g",
              "K": "e b c a",
              "L": "a c b b",
              "M": "f a e a",
              "N": "g b e g",
              "O": "g e b d",
              "P": "a b f a",
              "Q": "f g b c",
              "R": "b e f b",
              "S": "b f e c",
              "T": "b e a g",
              "U": "b b g e",
              "V": "c g b f",
              "W": "f c e e",
              "X": "d f b e",
              "Y": "a g e c",
              "Z": "c a e e",
              "[": "g g g a",
              "\\": "d c f d",
              "]": "b d a d",
              "^": "c c g e",
              "_": "b g b f",
              "`": "f b f g",
              "a": "f c d e",
              "b": "f a g b",
              "c": "a b d c",
              "d": "a g b e",
              "e": "a a a c",
              "f": "d a c c",
              "g": "g e e d",
              "h": "a a g e",
              "i": "b c d f",
              "j": "f d b g",
              "k": "c d d c",
              "l": "d a g d",
              "m": "b b f a",
              "n": "g c g f",
              "o": "b f a e",
              "p": "e f d c",
              "q": "d e a f",
              "r": "b a d a",
              "s": "b a c b",
              "t": "d d f f",
              "u": "c d a b",
              "v": "a f b e",
              "w": "g d d f",
              "x": "d e b a",
              "y": "f d a g",
              "z": "d e a d",
              "{": "g a c f",
              "|": "f a f g",
              "}": "f c e f",
              "~": "d f b a"}


def encode(src_file, dst_file="output.ly", title="", dict=char2notes, tagline=""):
    header = ""
    header += '\\version "2.18.2"\n'
    header += "\header {\n"
    header += '  title = "{}"\n'.format(title)
    header += '  composer = "lemeda"\n'
    header += '  tagline = "{}"\n'.format(open(tagline, mode='r').read())
    header += "}\n"

    txt = open(src_file, "r").read()

    staff = "\n{\n\\new PianoStaff << \n"
    staff += "  \\new Staff { \clef alto "
    for i in txt:
        try:
            staff += dict[i] + " "
        except KeyError as e:  # Character not in dict: ignore
            logger.error("Unknown key {}, ignoring:\n".format(i, e))
            pass

    staff += '\\bar "|." }\n'
    staff += ">>\n}\n"

    dst_file = open(dst_file, "w")
    dst_file.write(header + staff)
    logger.debug(header + staff)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Encodes arbitrary text into a music score")
    parser.add_argument("--input", "-i", required=True, help="File containing the text to encode")
    parser.add_argument("--output", "-o", required=False, default="output.ly", help="Lilypond file in which to write.")
    parser.add_argument("--dict", required=False, help="File containing an alternative dictionary (written in \
                        the python dictionary format)")
    parser.add_argument("--title", "-t", required=False, default="", help="Title of the music score")
    parser.add_argument("--tagline", required=False, default="", help="File containing the tagline of the music score")

    args = parser.parse_args()

    d = json.loads(open(args.dict, "r").read(), strict=False) if args.dict is not None else char2notes
    encode(args.input, args.output, args.title, d, args.tagline)


if __name__ == "__main__":
    main()
