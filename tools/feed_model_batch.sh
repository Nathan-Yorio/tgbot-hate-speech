#!/bin/bash

input_file="$1"

#echo "input file is $input_file"
#echo "Message,Hateful"

# Function to process a batch of lines
process_batch() {
    local batch=("$@")
    python3 model.py "${batch[@]}"
}

# Process the input file line by line
while IFS= read -r line; do
  if [[ -n $line ]]; then
    lines+=("$line")
    # Process in batches to prevent memory issues
    if (( ${#lines[@]} % 1000 == 0 )); then
      process_batch "${lines[@]}"
      unset lines
    fi
  fi
done < "$input_file"

# Process any remaining lines
if [ ${#lines[@]} -gt 0 ]; then
  process_batch "${lines[@]}"
fi

#echo "Done running analysis"
