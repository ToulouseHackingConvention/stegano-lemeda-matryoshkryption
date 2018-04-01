#!/bin/bash


function die() {
    echo $@
    exit
}


echo "Creating mp3 file... Phase 2"
cp ./build/audio.mp3 ./build/mp3_file
python ./src/angecrypt.py -c ./build/hybrid -i ./build/mp3_file -o ./build/mp3_out -k ./config/mp3_key -a aes -p ./build/
python ./build/dec-mp3_file.py #|| die "Error while executing dec-mp3_file.py"
echo "Done!"



# pdf file
echo "Creating pdf file..."
echo -n "THCon 2018 - $(cat ./config/vc_passphrase | base64)" > ./build/pdf_tagline

# Generate file (1st round)
echo "AAAABBBBCCCCDDDD" > ./build/pdf_iv
python ./src/utils/gen_pdf_text.py --template ./config/pdf_template --output ./build/pdf_text


[ -f ./config/dict_t2m ] || python ./src/gen_t2m_dict.py -o ./build/dict_t2m -e ./build/dict_m2t.txt
[ -f ./config/dict_m2t.txt ] || python ./src/gen_t2m_dict.py -o ./build/dict_t2m -e ./build/dict_m2t.txt

python ./src/generate_music_score.py --input ./build/pdf_text --output ./build/score.ly --dict ./config/dict_t2m --title Stegophony --tagline ./build/pdf_tagline
lilypond -o ./build/score ./build/score.ly || die "You must install lilypond in order to build the challenge."
rm ./build/pdf_iv

python ./src/angecrypt.py -c ./build/dec-mp3_file.mp3 -i ./build/score.pdf -o /dev/null -k ./config/pdf_key -a aes -p ./build/ --ivfile pdf_iv

# Generate real file knowing actual iv
python ./src/utils/gen_pdf_text.py --template ./config/pdf_template --output ./build/pdf_text
python ./src/generate_music_score.py --input ./build/pdf_text --output ./build/score.ly --dict ./build/dict_t2m --title Stegophony --tagline ./build/pdf_tagline
lilypond -o ./build/score ./build/score.ly || die "You must install lilypond in order to build the challenge."

cp ./build/score.pdf ./build/pdf_file
python ./src/angecrypt.py -c ./build/dec-mp3_file.mp3 -i ./build/pdf_file -o ./build/pdf_out -k ./config/pdf_key -a aes -p ./build/
python ./build/dec-pdf_file.py
echo "Done!"




# png file
echo "Creating png file..."
python ./src/insert_lsb.py --text ./config/png_key --cover ./assets/matryoshka.png --output ./build/matryoshka_1.png --colors g --visual --asbytes --prefix "key: "
python ./src/insert_lsb.py --text ./build/dict_m2t.txt --cover ./build/matryoshka_1.png --output ./build/matryoshka_2.png --colors r

python ./src/angecrypt.py -c ./build/dec-pdf_file.pdf -i ./build/matryoshka_2.png -o /dev/null -k ./config/png_key -a aes -p ./build/ --ivfile png_iv
python ./build/dec-matryoshka2.png.py

python ./src/insert_lsb.py --text ./build/png_iv --cover ./build/matryoshka_2.png --output ./build/matryoshka_out.png --colors b --visual --asbytes --prefix "iv: "
cp ./build/matryoshka_out.png ./build/png_file
python ./src/angecrypt.py -c ./build/dec-pdf_file.pdf -i ./build/png_file -o ./build/png_out -k ./config/png_key -a aes -p ./build/ --ivfile png_iv
python ./build/dec-png_file.py
echo "Done!"
rm ./build/matryoshka_*

sum="$(shasum ./build/dec-png_file.png | awk '{print $1}')"

cp ./build/dec-png_file.png ./export/$sum.png
tar cvzf ./export/matryoshkryption.tar.gz --directory ./export/ $sum.png
rm ./export/$sum.png

echo -e "\nOutput file to give to the challenger written as \`./export/matryoshkryption.tar.gz\`"



