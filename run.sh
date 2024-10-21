#!/bin/bash

# Name of the output file
OUTPUT_FILE="./large_39_forward.txt"

# Run the Python script and redirect output to the file
python3 KNN.py > $OUTPUT_FILE 2>&1

# Optionally, you can print a message indicating where the output has been stored
echo "Output has been redirected to $OUTPUT_FILE"

