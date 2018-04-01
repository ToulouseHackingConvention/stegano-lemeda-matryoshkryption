# matryoshkryption
* Author: lemeda
* Type: steganography

## Statement

### Part 1
Wow! I heard about that conf from 31C3 on file formats tweaks and the result is pretty impressive.

Will you find what is hidden inside that matryoshka?


### Part 2
You need to solve the first part of the challenge first.


## File provided to the challenger
* `./export/matryoshkryption.tar.gz`

## Hints
* Part 1: none
* Part 2: Don't use deprecated software!

## Build the challenge
* `make phase1`
* In Audacity:
    * Open `./build/spectro.wav`
    * File > Import > Audio > browse to `./build/morse.mp3`
    * Select All, Tracks > Mix > Mix and Render
    * File > Export > Export as MP3 → `./build/audio.mp3`
* `make phase2`

## Update flags or config files
Update `config/flag1` (intermediate flag), `config/flag2` (final flag) or another file in `config/` and rebuild the chall (see above for rebuilding).

List of files in `config`:
* `flag1`: intermediate flag (flag of 1st part)
* `flag2`: final flag (flag of 2nd part)
* `pdf_template`: template text used for generating the music score (pdf document)
* `vc_passphrase`: decryption passphrase for the VeraCrypt volume

Some more files can be provided in `config/` and are created if not already present:
* `png_key`: key to use to decrypt png file into pdf file
* `pdf_key`: key to use to decrypt pdf file into mp3 file
* `mp3_key`: key to use to decrypt mp3 file into mp4/VC hybrid file


## Organization of the repo

* directory `assets/` contains the resources which are necessary to build the
    challenge
* directory `config/` contains the config files necessary to build the challenge
    as well as both flag files
* directory `solution/` contains a write-up of the challenge..
* directory `src/` contains the core of the challenge, that is to say its
    code and more generally any file required to make it work properly
