import json

# This is a file to count the attempt times. 
file_path = r"classified_questions_GPT4.json"


with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

attempts = {
    "Level0": {"standard": 0, "specific": 0},
    "Level2": {"standard": 0, "specific": 0},
    "Level4": {"standard": 0, "specific": 0},
}

for level in ["Level0", "Level2", "Level4"]:
    if level in data:
        for question_type in ["standard", "specific"]:
            if question_type in data[level]:
                for item in data[level][question_type]:
                    attempts[level][question_type] += item['attempts']
                    

# Print result
for level in ["Level0", "Level2", "Level4"]:
    print(f"{level}:")
    print(f"  Standard questions attempts: {attempts[level]['standard']}")
    print(f"  Specific questions attempts: {attempts[level]['specific']}")
    print()