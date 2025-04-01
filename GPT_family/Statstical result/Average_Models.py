import json
import math 
import statistics

file_path='xxx'

# Read the JSON file
with open(file_path, 'r', encoding='utf-8') as f:
    all_scores = json.load(f)

results_dict = {}

for level, scores in all_scores.items():
    # Use zero to replace null or invalid scores
    valid_scores = [0 if not isinstance(score, (int, float)) or math.isnan(score) else score for score in scores]
    
    if valid_scores:
        average_score = sum(valid_scores) / len(valid_scores)
        std_dev = statistics.stdev(valid_scores) if len(valid_scores) > 1 else 0
    else:
        average_score = 0
        std_dev = 0
    
    results_dict[level] = {
        "average": average_score,
        "std_dev": std_dev
    }

# Write results to a new JSON file
output_file_path = 'xxx//newscores_stats.json'
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(results_dict, outfile, ensure_ascii=False, indent=4)

print(f"Results have been saved to {output_file_path}")