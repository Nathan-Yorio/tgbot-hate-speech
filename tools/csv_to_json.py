import csv
import json
import sys

def convert_csv_to_json(csv_file_path, json_file_path):
    # Read CSV file and convert to JSON
    data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    # Write JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 csv_to_json.py csv_file output_file")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_json_file = sys.argv[2]
    convert_csv_to_json(input_csv_file, output_json_file)
