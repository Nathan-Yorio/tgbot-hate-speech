import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import sys
import json

# HuggingFace model parent directory and name
model_name = "Andrazp/multilingual-hate-speech-robacofi"
local_dir = "./roberta"

# Store the model, cache directory, and tokenizer to local vars
model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=local_dir)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Read input data from the input file
input_file = sys.argv[1]
with open(input_file, 'r') as file:
    dataset_array = [line.strip() for line in file.readlines() if line.strip()]

# Function to process a batch of lines
def process_batch(batch):
    tokenized_inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**tokenized_inputs)
    predictions = torch.argmax(outputs.logits, dim=1)

    results_list = []
    for i, data_line in enumerate(batch):
        result_dict = {
            "Comment": data_line,
            "Hateful": str(predictions[i].item())
        }
        results_list.append(result_dict)

    return results_list

# Process the input file line by line in batches
batch_size = 1000
all_results = []
lines_batch = []
for line in dataset_array:
    lines_batch.append(line)
    if len(lines_batch) == batch_size:
        batch_results = process_batch(lines_batch)
        all_results.extend(batch_results)
        lines_batch = []

# Process any remaining lines
if lines_batch:
    batch_results = process_batch(lines_batch)
    all_results.extend(batch_results)

# Print the results list in JSON format
json_output = json.dumps(all_results, indent=2)
print(json_output)
