#!/bin/bash

function die() {
    echo $@
    exit
}

function generate() {
    echo "File config/$1 missing."
    echo "Creating file..."
    head /dev/urandom -c 16 > config/$1
    echo "Done!"
}

[ -f ./config/flag1 ] || die "Missing intermediate flag. Please write\
    intermediate flag to ./config/flag1"
[ -f ./config/flag2 ] || die "Missing final flag. Please write final flag to \
    ./config/flag2"
[ -f ./config/vc_passphrase ] || die "Missing passphrase for VeraCrypt Volume.\
    Please write is to ./config/vc_passphrase"
[ -f ./config/pdf_template ] || die "Missing template for music score. Please\
    write it into ./config/pdf_template"

[ -f ./config/png_key ] || generate png_key
[ -f ./config/pdf_key ] || generate pdf_key
[ -f ./config/mp3_key ] || generate mp3_key
