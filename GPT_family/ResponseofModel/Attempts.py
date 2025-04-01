import json

def load_classification_file(file_path):
    with open(file_path, 'r') as f:
        classification_data = json.load(f)
    
    classification_dict = {}
    for category in ['standard', 'specific']:
        for item in classification_data[category]:
            classification_dict[item['text']] = category
    
    return classification_dict

def process_level(level_data, classification_dict):
    standard = []
    specific = []
    for item in level_data:
        category = classification_dict.get(item['question'], 'unknown')
        if category == 'standard':
            standard.append(item)
        elif category == 'specific':
            specific.append(item)
        else:
            print(f"Warning: Question not found in classification file: {item['question']}")
    return standard, specific

classification_file_path = 'GPT3.5_classified_questions_with_index.json'

classification_dict = load_classification_file(classification_file_path)

input_file_path = 'filtered_questions.json'
with open(input_file_path, 'r') as f:
    data = json.load(f)

result = {}

for level, questions in data.items():
    standard, specific = process_level(questions, classification_dict)
    result[level] = {
        'standard': standard,
        'specific': specific
    }

output_file_path = 'classified_questions.json'
with open(output_file_path, 'w') as f:
    json.dump(result, f, indent=2)

print(f"Classification completed. Results saved in '{output_file_path}'")