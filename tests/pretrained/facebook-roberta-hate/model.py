import transformers
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import sys
import json

# HuggingFace model parent directory and name
model_name = "facebook/roberta-hate-speech-dynabench-r4-target"
local_dir  = "./roberta"

# Store the model, cache directory, and tokenizer to local vars
model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=local_dir)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Read input data from stdin arguments
# Dataset prep fundamental example, texts can be extrapolated to an entire dataset file
if len(sys.argv) > 1:
    dataset_array = sys.argv[1:]
else:
    dataset_array = ["Text 1.", "Text 2."]

tokenized_inputs = tokenizer(dataset_array, return_tensors='pt', padding=True, truncation=True)

# Run inference, sentiment from the pre-trained model
with torch.no_grad():
    outputs = model(**tokenized_inputs)

predictions = torch.argmax(outputs.logits, dim=1)

# Create a list of dictionaries for each result
results_list = []
for i, data_line in enumerate(dataset_array):
    result_dict = {
        "Comment": data_line,
        "Hateful": str(predictions[i].item())
    }
    results_list.append(result_dict)

# Print the results list in JSON format
json_output = json.dumps(results_list, indent=2)
print(json_output)
