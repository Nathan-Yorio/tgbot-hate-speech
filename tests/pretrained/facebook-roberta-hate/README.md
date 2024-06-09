Rough order that these are being used in

1. Run `pip install -r reqs.txt`
2. If dataset != JSON, run `python3 csv_to_json.py dataset_in dataset_out.json`
3. Run `extract_field_json.sh dataset_out.json dataset_messages.txt`
4. Run `python3 model_combined.py dataset_messages.txt dataset_results.json`
5. Run `python3 compare_results.py dataset_out.json dataset_results.json`

Then observe output and check incorrect_pairs.json to see which lines failed against model

Test Results:

- HateSpeechDetection.csv  
```
Number of Correct Sentiments: 2796
Number of Incorrect Sentiments: 204
Percentage of Incorrect Sentiment: 6.80%
Count of false positives: 101
Count of false negatives: 103
Percentage of False Positives: 3.37%
Percentage of False Negatives: 3.43%
```
