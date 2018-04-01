#!/bin/bash

function die() {
    echo $@
    exit
}

# Make outer volume
veracrypt -t -c -k '' --pim=0 --encryption=aes --hash=sha-512 --random-source=/dev/urandom --volume-type=normal --filesystem=ext4 -p 0000 --size=1M ./build/vc_volume || die "You must install VeraCrypt in order to use this script"

# Make inner volume
veracrypt -t -c -k "" --pim=0 --encryption=aes --hash=sha-512 --random-source=/dev/urandom --volume-type=hidden --filesystem=ext4 -p $(cat config/vc_passphrase) --size=512K ./build/vc_volume

echo -e "Hybrid volume successfully created.\n\n"
