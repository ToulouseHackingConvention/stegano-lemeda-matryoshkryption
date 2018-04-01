#!/bin/bash


function die() {
    echo $@
    exit
}

# hybrid vc volume / mp4 file
python ./src/mp42HV.py ./assets/video.mp4 ./build/vc_volume ./build/hybrid
./src/utils/embed_2nd_flag.sh


# mp3 file
python ./src/text_to_morse.py -i ./config/mp3_key -o ./build/morse.mp3 --samples ./assets/samples/ --asbytes --prefix "key "
python ./src/angecrypt.py -c ./build/hybrid -i ./assets/morse_sample.mp3 -o /dev/null -k ./config/mp3_key -a aes -p ./build/ --ivfile mp3_iv
rm ./build/dec-morse.mp3.py
python ./src/text_to_pic.py -i ./build/mp3_iv -o ./build/spectro.png --asbytes --prefix "iv: "
# The next step takes a while to complete (about 7min)
python ./src/spectrology/spectrology.py -o ./build/spectro.wav -m 0 -M 8000 ./build/spectro.png

echo -e "\nNext step:"
echo -e "\t open ./build/spectro.wav in Audacity"
echo -e "\t File > Import > browse to ./build/morse.mp3"
echo -e "\t Select all, then Tracks > Mix > Mix and Render"
echo -e "\t File > Export > Export as MP3 > export as ./build/audio.mp3"
echo -e "\nYou can now proceed to the second building phase by running \`make phase2\`"

