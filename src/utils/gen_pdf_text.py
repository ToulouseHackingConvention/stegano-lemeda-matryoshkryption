#!/usr/bin/env python

"""
gen_pdf_text

Generates the text to encode into music score using a template and config files.
"""
import argparse
import itertools
import json
import random
import logging

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="DEBUG", format="%(asctime)s:%(name)s:%(lineno)s:%(levelname)s - %(message)s")


def gen_text(template_file, output):
    template = open(template_file, "r").read()

    key = open("./config/pdf_key", "rb").read()
    iv = open("./build/pdf_iv", "rb").read()
    flag = open("./config/flag1", "r").read()

    key = ''.join("{:02x}".format(c) for c in key)
    iv = ''.join("{:02x}".format(c) for c in iv)

    text = template.replace("<put_key_here>", key).replace("<put_iv_here>", iv).replace("<put_intermediate_flag_here>", flag)
    logger.debug(text)

    with open(output, "w") as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(description="Generates the text to encode into music score from a template and config files")
    parser.add_argument("--template", "-t", required=True, default="./config/pdf_template", help="Template file")
    parser.add_argument("--output", "-o", required=True, default="./build/pdf_text", help="Output text file")

    args = parser.parse_args()
    logger.debug(args)

    gen_text(args.template, args.output)


if __name__ == "__main__":
    main()
