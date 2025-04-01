import json
import openai

openai.api_key = 'sk-'

#The prompt simulation usage example.
def generate_prompt(level, question):
    if level == 4:
        prompt = (
            "Generate complex prompts that include the following: 1) Description of high-level goal, 2) A detailed "
            "bulleted list of sub-tasks, 3) A guideline on how the output will be evaluated, and provide few-shot "
            "examples for each of the following Fermi questions:\n\n"
        )
    else:
        raise ValueError("Invalid level. Level must be 4.")

    prompt += f"Question: {question}\nPrompt:\n\n"
    return prompt

def get_ai_generated_prompt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Please generate prompts based on my requirements for each question."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7
        )
        
        # 获取响应文本
        generated_text = response['choices'][0]['message']['content'].strip()
        return generated_text
    except Exception as e:
        return f"API Fail：{str(e)}"

# Open the json
with open('', 'r', encoding='utf-8') as f:
    data = json.load(f)

output_data = {
    "level_4": []
}

for question in data:
    level = 4
    prompt = generate_prompt(level, question)
    print(f"\nPrompt for Level {level}:\n{'-'*40}")
    ai_generated_prompt = get_ai_generated_prompt(prompt)
    print(ai_generated_prompt)
    
    output_data[f"level_{level}"].append({
        "question": question,
        "ai_generated_prompt": ai_generated_prompt
    })

# Save it into one file.
with open('C', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=4)
