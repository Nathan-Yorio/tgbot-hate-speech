#!/bin/bash

input_file="$1"

echo "input file is $input_file"

# Read the input file line by line
while IFS= read -r line; do
  # Check if the line is not empty and send to model if not
 if [[ -n $line ]]; then
    python3 model.py "$line"
  fi
done < "$input_file"

echo "Done running analysis"
