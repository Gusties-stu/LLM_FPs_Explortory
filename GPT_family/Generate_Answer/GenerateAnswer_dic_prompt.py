import json
import openai

openai.api_key = 'sk'


with open('', 'r', encoding='utf-8') as f:
    question_data = json.load(f)

with open('xxx//Promptslevel4.json', 'r', encoding='utf-8') as g:
    prompt_data = json.load(g)

#
with open('xxx//units.json', 'r', encoding='utf-8') as file:
    units_data = json.load(file)
    units = units_data[0].get('units', 'unknown')

#The prompt to generate the AI answer.
def get_ai_generated_answer(question, prompt, units):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a helpful assistant. "
                        "Please Don't use scientific notation in your answer. "
                        "Use another form to replace it and please give your answer "
                        "in a value to the question in the last sentence, make sure "
                        "the last number appear in your answer is the final answer! "
                        f"My answer should be in the form 'units(string)' in units X. Units: {units}"
                    )
                },
                {"role": "user", "content": f"Question: {question}\nPrompt: {prompt}"}
            ],
            max_tokens=4096,  #
            temperature=0.7  # Randomness
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating AI answer: {e}")
        return None

# Use a list to store
generated_answers = []


for question in question_data:

    prompt = prompt_data.get(question, '')
    
    #
    answer = get_ai_generated_answer(question, prompt, units)
    
    #
    generated_answers.append({
        'question': question,
        'answer': answer
    })
    
    print(f"Finish {len(generated_answers)}/{len(question_data)}  generation")

# Save
with open('xxx//generated_answers_AI4.json', 'w', encoding='utf-8') as f:
    json.dump(generated_answers, f, ensure_ascii=False, indent=4)
