import json

# Read Json File 
file_paths = [

]
results={}

for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count_zeros = 0
    count_invalid_values = 0

    for item in data:
        if item == 0:
            count_zeros += 1
        elif item == "Invalid value for score calculation.":
            count_invalid_values += 1
            
    level=file_path.split('Level')[1].split('.')[0]
    results[f'Level{level}']={
        'zeros':count_zeros,
        'invalid_values': count_invalid_values
    }



output_file_path = '/count_results.json'
print(f'Successfully Download')
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)