import openai

import json

#
openai.api_key = 'sk-'

with open('RawQuestion.json', 'r', encoding='utf-8') as f:
    question_data= json.load(f)

key_list=[]    
for key in question_data.keys():
    key_list.append(key)

question_data=key_list


with open('SeparatedAnswers.json', 'r', encoding='utf-8') as file:
    units_data = json.load(file)
    units = units_data[0].get('units', 'unknown')



def get_ai_generated_answer(question, units):
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
                {"role": "user", "content": f"Question: {question}"}
            ],
            max_tokens=4096,  
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating AI answer: {e}")
        return None


#
generated_answers = []

#
for i in range(len(question_data)):
    question = question_data[i]  #

    
    #
    answer = get_ai_generated_answer(question, units)
    
    #
    generated_answers.append({
        'question_index': i,
        'question': question,
        'answer': answer
    })
    
    print(f"Finish {i+1}/{len(question_data)} generation ")

with open('generated_answers_level0.json', 'w', encoding='utf-8') as f:
    json.dump(generated_answers, f, ensure_ascii=False, indent=4)