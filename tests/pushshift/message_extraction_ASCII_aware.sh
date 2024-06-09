#!/bin/bash

#input_file="test-text.ndjson"
input_file="$1"
#output_file="isolated-messages.ndjson"
output_file="$2"

# Remove output file if it already exists
rm -f "$output_file"

clearcnt=0
asciicnt=0
messagecnt=0
# Read the input file line by line
while IFS= read -r json_line; do
  # Extract the "message" field using jq
  message=$(echo "$json_line" | jq -r '.message')
  ((messagecnt++))
  # Check if the message field is not empty, and write the line to an output file
  if [[ -n $message ]]; then
    if [[ $message = *[![:ascii:]]* ]]; then
        echo "$message Contains Non-ASCII"
        ((clearcnt++))
        ((asciicnt++))
        echo $clearcnt
    else
        echo "$message" >> "$output_file"
    fi
  fi
  if [[ "$clearcnt" -gt 9 ]]; then
    clearcnt=0
    clear
  fi
done < "$input_file"

# Calculate a ratio for how many of the messages didn't make it through
messageratio=$(echo "scale=3; $asciicnt / $messagecnt" | bc)


printf "Messages extracted and saved to '$output_file' file. \n"
printf "Messages in dataset containing non-ascii characters:    $asciicnt \n"
printf "Total Messages in dataset -------------------------:   $messagecnt \n"
printf "Ratio of ASCII to non-ASCII messages --------------: $messageratio \n"
