# Matryoshkryption - Write-up


## First Part

### Challenge Statement
Wow! I heard about that conf from 31C3 on file formats tweaks and the result is
pretty impressive.

Will you find what is hidden inside that matryoshka?

### Solving Process
* Decompress `matryoshkryption.tar.gz`
* One gets a (malformed) png file (thereafter referred to as `png_file`)

### Handling the png file
* To get a proper png file, one can for instance open it in Gimp and export it to
  a new png file. This is useful because otherwise, software
  such as stegsolve would not be able to open the file. In case you prefer to
  use homemade scripts to extract concealed data, you probably don't need to
  carry out this step.
* Let's look for concealed data. For example, with stegsolve:
    * Analyse → Data Extract: by ticking only the box corresponding to Bit Plan 0 of the red component, we get something that looks like a dictionary or an alphabet.
    * Using the arrows at the bottom of the window to navigate between the successive components' plans:
        * One finds a key in Green Plan 0
        * One finds an IV in Blue Plan 0
* We've got a key and an iv. Let's find out how to use them:
    * Let's try to do so using the statement of the chall. Looking up something
      like "31c3 file formats tweaks", one of the first result we get is the
      slides of a conference hold by Ange Albertini during 31C3, called "Funky
      file formats".
    * Searching for "IV" or "key", we can identify that what
      seems to have been used here is Angecryption.
* Let's try to "de-angecrypt" out png file:
    * To do so, one just needs to use the key/IV pair previously found to
      decrypt the png file, assuming the corresponding plaintext/data has been
      encrypted using AES-128 CBC with that key/IV pair (since this is what is
      done in Angecryption).
    * The resulting data appears to be a PDF file.
    
    
### Handling pdf file - Part 1
* The content is a music score. One can use the dictionary found previously to decode the notes into actual text.
    * Note: at that stage, a hint was given to the participants, stating that
      the interesting data for that step can be found within bars 84 to 215.
* One thus gets a message giving a new key, a new IV and a flag.

__The flag one gets from the music score validates the first part of the challenge__.


## Second Part

### Handling pdf file - Part 2
* The Copyright line of the music score also contains base64-encoded data,
  which once decoded gives what appears to be some passphrase.
* De-angecrypt the pdf file with the new key/iv pair.
* `file pdf_decrypted` → `MPEG ADTS, layer III, v1, 128 kbps, 44.1 kHz, Monaural`.
* This looks like some kind of malformed mp3 file.
    
### Handling the mp3 file
* Listening to the mp3 file lets one hear a morse-encoded message and some additional noise.
* Open the file in Audacity: this allows to "visualize the sound" and decode the morse message more easily.
* Opening the file in Audacity, one thus gets a new key.
* Using the Spectrogram view, one also gets a new IV.
* De-angecrypt again, using the newly found key/IV pair.
* One thus gets a mp4 file.

### Handling the mp4 file
* The video shows nothing particular.
* The passphrase from earlier has not been used yet, it is time to do so.
* The passphrase suggests TrueCrypt has been used. Looking up for "TrueCrypt mp4", one sees that TrueCrypt volumes can be hidden within mp4 ones so that both files are still readable.
* However, TrueCrypt is deprecated and a common alternative for it is VeraCrypt, so let's use VeraCrypt instead: `veracrypt -p <passphrase> --mount <mp4_file> <some_mounting_point>`.
* There is a single file in the volume, called `flag`.

__The flag one gets from the eponym file validates the second part of the challenge__.
