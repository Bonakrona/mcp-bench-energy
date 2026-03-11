
import json
import os

def calculate_weighted_average(file_task_pairs):
    """
    Calculate weighted averages for each score key across multiple JSON files.
    :param file_task_pairs: List of tuples (file_path, task_count)
    :return: Dictionary with weighted averages for each key.
    """
    cumulative_sums = {}
    total_tasks = 0

    for file_path, task_count in file_task_pairs:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Update cumulative sums weighted by task count
        for key, value in data.items():
            cumulative_sums[key] = cumulative_sums.get(key, 0) + value * task_count

        total_tasks += task_count

    # Compute weighted averages
    weighted_averages = {key: cumulative_sums[key] / total_tasks for key in cumulative_sums}
    return weighted_averages


file_task_pairs = [

    #Layup for the most overviewable table ever, one block of 2 at a time brother
    ('average-script\\Claude_sonnet_4\\internal_vs_external_multiserver.json', 12),
    ('average-script\\Claude_sonnet_4\\internal_vs_external.json', 103), 

    ('average-script\\gpt-4o-mini\\internal_vs_external_multiserver.json', 12),
    ('average-script\\gpt-4o-mini\\internal_vs_external.json', 103), 

    ('average-script\\Phi-4-mini-instruct\\internal_vs_external_multiserver.json', 12),
    ('average-script\\Phi-4-mini-instruct\\internal_vs_external.json', 103), 
]

# Check if files exist before proceeding
for file_path, _ in file_task_pairs:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Please make sure the file exists.")

if all(os.path.exists(file_path) for file_path, _ in file_task_pairs):
    result = calculate_weighted_average(file_task_pairs)
    print("Weighted averages across all batches:")
    for key, value in result.items():
        print(f"{key}: {value}")
