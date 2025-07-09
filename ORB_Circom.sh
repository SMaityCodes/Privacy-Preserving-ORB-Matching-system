#!/bin/bash

# Get arguments
n=$1
file1=$2
file2=$3

# Check if all required arguments are provided
if [ -z "$n" ] || [ -z "$file1" ] || [ -z "$file2" ]; then
  echo "Usage: ./ORB_Python.sh <n> <file1.jpg> <file2.jpg>"
  exit 1
fi

# Construct output filenames
out1="./tmp/Features1.pkl"
out2="./tmp/Features2.pkl"

# Run feature extraction
python3 ./Python_Progs/featureExtracter.py -i "$file1" -o "$out1" -n "$n"
python3 ./Python_Progs/featureExtracter.py -i "$file2" -o "$out2" -n "$n"

# Generate Circom Input from Feature files

python3 ./Python_Progs/circomPreprocessor.py "$out1" "$out2" "$n" "$n"

# Attach Merkle Roots
node ./MerkelRootCal/calMerkleRoot.js

# Run comparison
node ./Circom_Circuits/ORB_Matcher_js/generate_witness.js ./Circom_Circuits/ORB_Matcher_js/ORB_Matcher.wasm circomInputWithHash.json witness.wtns


