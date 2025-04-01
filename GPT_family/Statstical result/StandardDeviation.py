import json
import math 

file_paths = [
    #Change to your dataset file path.
]

score_data_list = []

# Read file
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as f:
        score_data = json.load(f)
        score_data_list.append(score_data)

def calculate_standard_deviation(scores):
    if len(scores) == 0:
        return 0
    mean = sum(scores) / len(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    return math.sqrt(variance)

standard_deviations_list = []
for scores in score_data_list:
    std_dev = calculate_standard_deviation(scores)
    standard_deviations_list.append(std_dev)

# Store the deviation.
standard_deviations_dict = {str(i): std_dev for i, std_dev in enumerate(standard_deviations_list)}

# output file path.
output_file_path = ""
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(standard_deviations_dict, outfile, ensure_ascii=False, indent=4)

print(f" {output_file_path}")