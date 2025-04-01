import json
import scipy.stats as stats
import numpy as np

def extract_scores_by_level(group, level):
    scores = []
    for key, levels in data[group].items():
        if level in levels:
            score = levels[level]
            if isinstance(score, (int, float)):
                scores.append(score)
    return scores

# Load the data,specific and standard together.
with open('classified_Rawscore.json', 'r') as file:
    data = json.load(file)

levels=['Level_0','Level_2','Level_4']
#Extract scores for 'specific' and 'standard'
# def extract_scores(group):
#     scores = []
#     for key, levels in data[group].items():
#         for level, score in levels.items():
#             if isinstance(score, (int, float)):
#                 scores.append(score)
#     return scores
for level in levels:
    specific_scores = extract_scores_by_level('specific',level)
    standard_scores = extract_scores_by_level('standard',level)

    # Remove invalid or NaN scores
    specific_scores = [s for s in specific_scores if not np.isnan(s)]
    standard_scores = [s for s in standard_scores if not np.isnan(s)]

    # print(specific_scores)
    # print(standard_scores)
    # Perform t-test
    stat, p_value = stats.ttest_ind(specific_scores, standard_scores, equal_var=False)  # t-test

# Print results
    print(f"For level {level}:")

    print("T-statistic:", stat)
    print("P-value:", p_value)

    # if p_value < 0.05:
    #     print("The difference between the groups is statistically significant.")
    # else:
    #     print("The difference between the groups is not statistically significant.")
