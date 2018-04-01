#!/bin/bash

# Mount newly created veracrypt volume
echo "Embedding flag into hybrid volume..."
mkdir -p ./build/vol/
veracrypt -p $(cat config/vc_passphrase) --mount ./build/hybrid ./build/vol/
sudo cp ./config/flag2 ./build/vol/flag
veracrypt -d
echo "Done!"

