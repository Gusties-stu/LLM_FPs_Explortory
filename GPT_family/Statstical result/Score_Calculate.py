import math
import json

# This one is to get the fp_score from the results generated and gold standard.

# Function to calculate FP_score
def calculate_fp_score(A_prime, A):
    try:
        A_prime = float(A_prime)
        A = float(A)
        score = max(0, 1 - (1/3) * abs(math.log10(A_prime / A)))
        return score
    except ValueError:
        return "Invalid value for score calculation."
    
# FileList
file_paths = [

]

real_answers_path = '//Units_Value.json'

# Read the real answer 
with open(real_answers_path, 'r', encoding='utf-8') as real_answers:
    actual_data = json.load(real_answers)
    actual_values = [item['value'] for item in actual_data]

# Create lists for every level 
fp_scores_level0 = []
fp_scores_level2 = []
fp_scores_level4 = []

for file_path in file_paths:
    # Extract the levels from the files 
    file_name = file_path.split("//")[-1]  
    level = file_name.split("Level")[1].split(".json")[0]
    print(f"Processing level: {level}")
    
    with open(file_path, 'r', encoding='utf-8') as generate_answers:
        data = json.load(generate_answers)
    
    #  extracted_value
    extracted_values = [item['extracted_value'] if item['extracted_value'] is not None else 0 for item in data]
    
    fp_scores = []
    for i in range(len(actual_values)):
        A = actual_values[i]  # Standard 
        B = extracted_values[i]  # Generated answer
        fp_score = calculate_fp_score(B, A)
        fp_scores.append(fp_score)
    
    if level == '0':
        fp_scores_level0 = fp_scores
    elif level == '2':
        fp_scores_level2 = fp_scores
    elif level == '4':
        fp_scores_level4 = fp_scores

# Save the results
all_results = {
    "Level_0": fp_scores_level0,
    "Level_2": fp_scores_level2,
    "Level_4": fp_scores_level4
}

output_path = '//All_Updated_fp_scores.json'
with open(output_path, 'w') as f:
    json.dump(all_results, f, indent=2)

print("Successfully processed all files and saved results.")

