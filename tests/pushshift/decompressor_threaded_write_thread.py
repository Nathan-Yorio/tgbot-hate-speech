#!/usr/bin/env python3

import zstandard as zstd
import time
import json
import sys
import threading
from queue import Queue, Empty
from collections import defaultdict

# Function to process the data in a thread
def process_data(data_queue, output_queue, encoding_errors, malformed_errors, counter_lock, counter, previous_lines):
    while True:
        try:
            chunk = data_queue.get(timeout=1)  # Get a chunk of data from the queue
        except Empty:
            break

        try:
            string_data = chunk.decode('utf-8')
        except UnicodeDecodeError as encoding_error:
            encoding_errors += 1
            print(encoding_error)
            continue

        lines = string_data.split("\n")
        for i, line in enumerate(lines[:-1]):
            if i == 0:
                line = previous_lines[threading.current_thread()] + line

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as malformed_json_error:
                malformed_errors += 1
                print(malformed_json_error)
                continue

            # Perform processing on the object here
            with counter_lock:
                counter += 1
                if counter == 100000:
                    output_queue.put(obj)  # Put the object in the output queue
                    counter = 0

        previous_lines[threading.current_thread()] = lines[-1]
        data_queue.task_done()

# Function for file writing in a separate thread
def write_to_file(output_queue, output_file, counter_lock):
    while True:
        obj = output_queue.get()  # Get an object from the output queue
        if obj is None:
            break

        with counter_lock:
            output_file.write(json.dumps(obj) + "\n")

        output_queue.task_done()

# Check that the script is running with the correct arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <filename.zst> [num_threads]")
    sys.exit(1)

input_filename = sys.argv[1]

# Number of threads (specify as an argument or default to 1)
num_threads = int(sys.argv[2]) if len(sys.argv) >= 3 else 1

encoding_errors = 0
malformed_errors = 0
counter = 0

# Maximum queue size for chunks (adjust as needed)
max_queue_size = 400

with open(input_filename, 'rb') as fh:
    dctx = zstd.ZstdDecompressor(max_window_size=2147483648)
    with dctx.stream_reader(fh) as reader:
        previous_lines = defaultdict(str)  # Initialize the dictionary with empty strings
        data_queue = Queue(max_queue_size)
        output_queue = Queue()

        # Create a lock for the counter
        counter_lock = threading.Lock()

        # Create and start the worker threads
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=process_data, args=(data_queue, output_queue, encoding_errors,
                                                            malformed_errors, counter_lock, counter, previous_lines))
            t.start()
            threads.append(t)

        # Create and start the file writing thread
        output_file = open("output.json", "a")
        file_writer_thread = threading.Thread(target=write_to_file, args=(output_queue, output_file, counter_lock))
        file_writer_thread.start()

        # Read and enqueue the data chunks
        while True:
            chunk = reader.read(2 ** 24)  # 16MB chunks
            if not chunk:
                break
            data_queue.put(chunk)

            # Wait if the queue is full
            while data_queue.qsize() >= max_queue_size:
                time.sleep(0.1)

        # Wait for all data to be processed
        data_queue.join()

        # Signal the worker threads and file writing thread to exit
        for _ in range(num_threads):
            data_queue.put(None)
        output_queue.put(None)

        # Wait for all threads to finish
        for t in threads:
            t.join()
        file_writer_thread.join()

output_file.close()

print('==========================Error Totals==========================')
print('Total UTF8 encoding errors:   ', encoding_errors)
print('Total JSON encoding errors:   ', malformed_errors)
