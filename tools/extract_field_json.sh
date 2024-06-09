#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Please run this script with arguments"
    exit 1
fi

input_file=$1
output_file=$2

jq -r '.[].Comment' "$input_file" > $output_file

echo "Fields extracted and saved to '$output_file'"
