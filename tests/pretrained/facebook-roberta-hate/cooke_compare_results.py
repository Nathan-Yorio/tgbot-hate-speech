import json
import sys

def compare_jsons(json1, json2):
    # Load JSON data from files
    with open(json1, 'r') as file:
        data1 = json.load(file)

    with open(json2, 'r') as file:
        data2 = json.load(file)

    # Compare the two JSONs
    incorrect_count = 0
    false_positives = 0
    false_negatives = 0
    incorrect_pairs = []
    correct_count   = 0


    for entry1, entry2 in zip(data1, data2):
        if entry1.get("Hateful") != entry2.get("Hateful"):
            incorrect_count += 1
            #incorrect_pairs.append(entry1)
            incorrect_pairs.append(entry2)
        if entry1.get("Hateful") == "0" and entry2.get("Hateful") == "1":
            false_positives += 1
        if entry1.get("Hateful") == "1" and entry2.get("Hateful") == "0":
            false_negatives += 1

    # Calculate percentage of incorrect entries
    total_entries = len(data1)
    percentage_incorrect = (incorrect_count / total_entries) * 100
    correct_count = len(data1) - incorrect_count


    # Calculate false positives and false negatives
    percent_false_positive = (false_positives / total_entries) * 100
    percent_false_negative = (false_negatives / total_entries) * 100

    # Write incorrect pairs to a separate file
    with open('incorrect_pairs.json', 'w') as file:
        json.dump(incorrect_pairs, file, indent=2)

    return {
        'Number of Correct Sentiments': correct_count,
        'Number of Incorrect Sentiments': incorrect_count,
        'Percentage of Incorrect Sentiment': f'{percentage_incorrect:.2f}%',
        'Count of false positives': f'{false_positives:d}',
        'Count of false negatives': f'{false_negatives:d}',
        'Percentage of False Positives': f'{percent_false_positive:.2f}%',
        'Percentage of False Negatives': f'{percent_false_negative:.2f}%',
        'View which dict pairs are incorrect in': 'incorrect_pairs.json'
    }

if len(sys.argv) != 3:
    print("Usage: python3 csv_to_json.py first_json second_json")
    sys.exit(1)

first_json = sys.argv[1]
second_json = sys.argv[2]

result = compare_jsons(first_json, second_json)

# Print the result
for key, value in result.items():
    print(f'{key}: {value}')
