#!/usr/bin/env python

"""
generate_t2m_dict

Creates a python dictionary associating characters to music notes
that can later be used to produce a music score with Lilypond.
"""
import argparse
import itertools
import json
import random
import logging

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")


def gen_dict(output_file, export_file=None):
    l = list(map(' '.join, itertools.product("abcdefg", repeat=4)))
    random.shuffle(l)

    d = dict(zip([chr(i) for i in range(48, 127)] + ['\n'] + [chr(i) for i in range(32, 48)], l))
    logger.debug(d)
    logger.debug(len(str(d)))

    with open(output_file, 'w') as f:
        f.write(json.dumps(d))

    if export_file is not None:
        exp_dict = dict()
        for k, v in d.items():
            exp_dict[v.replace(' ', '')] = k

        logger.debug(exp_dict)
        with open(export_file,  'w') as f:
            s = str(exp_dict).replace("{'", "").replace("}", "").replace("': ", ":").replace(", '", ";")
            logger.debug(s)
            logger.debug(len(s))
            f.write(s)



def main():
    parser = argparse.ArgumentParser(description="Creates a picture containing the text given as input")
    parser.add_argument("--output", "-o", required=False, default="t2m_dict", help="Output file")
    parser.add_argument("--export", "-e", required=False, help="File in which to write a version of the dict more easily usable by the challenger")


    args = parser.parse_args()
    logger.debug(args)

    gen_dict(args.output, args.export)


if __name__ == "__main__":
    main()
