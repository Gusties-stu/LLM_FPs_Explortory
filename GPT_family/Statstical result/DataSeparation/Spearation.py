import openai
import json
import re 

openai.api_key = 'sk'

# Read File about question
with open('RawQuestion.json', 'r', encoding='utf-8') as f:
    question_data= json.load(f)
    
key_list=[]    
for key in question_data.keys():
    key_list.append(key)

question_data=key_list


# Read Prompt.json
with open('/Level4Prompt.json', 'r', encoding='utf-8') as g:
    prompt = json.load(g)


# Read File about units 
with open('Units_Value.json', 'r', encoding='utf-8') as file:
    units_data = json.load(file)
    units = units_data[0].get('units', 'unknown')

# print(units_data)

def extract_x_from_answer(answer):
    if not isinstance(answer, str):
        answer = str(answer)
    
    # Search all the numbers in the answer
    numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', answer)    

    if numbers:
        # Select the last number 
        last_number = numbers[-1]
        last_number = last_number.replace(',', '')
        try:
            return int(last_number) if last_number.isdigit() else float(last_number)
        except ValueError:
            print(f"Error converting the extracted value to float: {last_number}")
            return None
    else:
        #print("No valid numbers found in the answer.")
        return None
  
#2 and 3 variables are different   
def get_ai_generated_answer(question,units):
    try:
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",  # Model
            model="gpt-4-turbo",  # Model

            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a helpful assistant.I'd appreciate your assistance. "
                        "Please avoid using scientific notation or large numbers words like millions or trillions to represent the answer in your answer "
                        "Use another form to replace it and please give your answer "
                        "in a value to the question in the last sentence, make sure "
                        "I'd like the final answer to the question to be a specific value, not part of a sentence! "
                        "To clarify, the final answer should be a new number, not the one mentioned in the original question."
                        f"My answer should be in the form 'units(string)' in units X. Units: {units}"
                    )
                },
                {"role": "user", "content": f"Question: {question}\nPrompt: {prompt}"}
                #   {"role": "user", "content": f"Question: {question}"}

            ],
            max_tokens=4096, 
            temperature=0.7  
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating AI answer: {e}")
        return None


# Creat a list to store all the answers
generated_answers = []


# Make sure the question_data and prompt length are equal 
if len(question_data) != len(prompt):
    raise ValueError("question_data and the length of prompt are not match.")

# Loop question_data and prompt, Use function to generate answers, Add the answers into the list

results = []
max_attempts = 10

for i in range(len(question_data)):
    question = question_data[i]  # Direct get the string 
    current_prompt = prompt[i]
    attempts = 0
    x = None
    
    while x is None and attempts< max_attempts:
        # answer = get_ai_generated_answer(question, current_prompt, units)
        answer = get_ai_generated_answer(question, units)

        x = extract_x_from_answer(answer)
        attempts += 1
        
    results.append({
        'question': question,
        'extracted_value': x,
        'attempts': attempts
    })

    print(f"Completed {i+1}/{len(key_list)} questions. Attempts: {attempts}")


# Write it into new file
output_file_path = '.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# print(results)

print(f"Results have been saved to {output_file_path}")
