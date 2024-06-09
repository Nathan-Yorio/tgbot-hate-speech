#!/bin/bash

#input_file="test-text.ndjson"
input_file="$1"
#output_file="isolated-messages.ndjson"
output_file="$2"

# Remove output file if it already exists
rm -f "$output_file"

# Read the input file line by line
while IFS= read -r json_line; do
  # Extract the "message" field using jq
  message=$(echo "$json_line" | jq -r '.message')
  
  # Check if the message field is not empty, and write the line to an output file
  if [[ -n $message ]]; then
    echo "$message" >> "$output_file"
  fi
done < "$input_file"

echo "Messages extracted and saved to '$output_file' file."
