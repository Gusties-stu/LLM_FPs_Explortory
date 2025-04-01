# Python program to read json and do the classification work. Include the prompts about classifying

import json
import openai 
from tqdm import tqdm

openai.api_key = 'sk-'

# Use API to implement these keys,classify them 

class QuestionClassfier:
    def __init__(self,api_key):
        self.api_key=api_key
        
    def classify_question(self,question):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that classifies questions as 'standard' or 'nonstandard', You should classify the questions to one of two classes."},
            {"role": "user", "content": f"""
            The following question needs to be classified as 'standard' or 'nonstandard' based on the following criteria:
            - Clarity: The question should have one intended meaning and be easy to understand without any ambiguity.
            - Neutrality: The question should not be biased towards any particular viewpoint.
            - Conciseness: The question should be concise and to the point.
            
            Question: {question}
            
            Based on the criteria, this question is:"""}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo", 
                messages=messages,
                max_tokens=10,
                temperature=0  
            )
            classification = response.choices[0].message['content'].strip().lower()
            return classification
        except Exception as e:
            return f"Error: {str(e)}"

    
with open('//IndexQuestion.json', 'r') as f:
    data = json.load(f)

classifier = QuestionClassfier(openai.api_key)

result = {"standard": [], "specific": []}

# Use tqdm
for item in tqdm(data, desc="Classifying questions", unit="question"):
    index = item["index"]
    question = item["question"]
    classification = classifier.classify_question(question)
    if classification == 'standard':
        result["standard"].append(index)
    else:
        result["specific"].append(index)

# Write into json
output_path = '//classified_questions.json'
with open(output_path, "w") as outfile:
    json.dump(result, outfile, indent=2)

print(f"\nSave: {output_path}")

# Print
total_questions = len(data)
standard_count = len(result["standard"])
specific_count = len(result["specific"])

# print(f"\nClassified result calculation:")
# print(f"Total: {total_questions}")
# print(f"Standard: {standard_count} ({standard_count/total_questions*100:.2f}%)")
# print(f"Specific: {specific_count} ({specific_count/total_questions*100:.2f}%)")

