#!/usr/bin/env python3

import zstandard as zstd
import time
import json
import sys
import datetime

counter = 0
output_file = open("output.json", "a")

# Check that the script is running with the correct arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <filename.zst>")
    sys.exit(1)

input_filename = sys.argv[1]

encoding_errors = 0
malformed_errors = 0

with open(input_filename, 'rb') as fh:
    dctx = zstd.ZstdDecompressor(max_window_size=2147483648)
    with dctx.stream_reader(fh) as reader:
        previous_line = ""
        while True:
            chunk = reader.read(2**24)  # 16mb chunks
            if not chunk:
                break
            try:
                string_data = chunk.decode('utf-8')
            # Handle decoding errors (e.g., incomplete or corrupted data)
            except UnicodeDecodeError as encoding_error:
                encoding_errors += 1
                #print(encoding_error)
                continue
            #string_data = chunk.decode('utf-8')
            lines = string_data.split("\n")
            for i, line in enumerate(lines[:-1]):
                if i == 0:
                    line = previous_line + line

                # Malformed JSON error handling
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as malformed_json_error:
                    malformed_errors += 1
                    #print(malformed_json_error)
                    continue

                # Perform processing on the object here
                if counter == 100000:
                    #print(obj)
                    # Store the object in the output file
                    output_file.write(json.dumps(obj) + "\n")
                    counter = 0
                else:
                    counter += 1
                    #print(counter)

            previous_line = lines[-1]

output_file.close()

print('==========================Error Totals==========================')
print('Total UTF8 encoding errors:   ',encoding_errors,'\n')
print('Total JSON encoding errors:   ',encoding_errors,'\n')

now = datetime.datetime.now()
print('Decompressed completed at :\n',now)
