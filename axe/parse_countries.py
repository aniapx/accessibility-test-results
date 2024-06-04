import os
import json
from collections import defaultdict

# Define a function to process a single file
def process_and_save_to_file(file_path, output_file):
    errors = defaultdict(lambda: defaultdict(int))
    with open(file_path, 'r') as f:
        data = json.load(f)
        
        for issue in data['allIssues']:
            rule_id = issue['ruleId']
            errors[issue['impact']][rule_id] += 1
    
    # Sort errors by level and count
    sorted_errors = {}
    for impact, error_dict in sorted(errors.items()):
        sorted_errors[impact] = sorted(error_dict.items(), key=lambda x: (-x[1], x[0]))
    
    # Write to output file
    with open(output_file, 'a') as out:
        # Write the filename
        # out.write(f"\nErrors in file: {file_path}\n")
        out.write(f"{file_path}\n")
        
        # Write sorted errors
        if len(sorted_errors):
            for impact, error_list in sorted_errors.items():
                out.write(f"{impact.capitalize()} Issues:\n")
                for error, count in error_list:
                    # Find the issue description by rule ID
                    description = next((issue['description'] for issue in data['allIssues'] if issue['ruleId'] == error), '')
                    out.write(f"{error}: {count}: {description};\n")
                out.write(f"\n")
        else:
            out.write(f"Critical Issues:\n\n")
            out.write(f"Serious Issues:\n")

            


# Iterate over the folders and files
folders = ['bigsize', 'courier', 'ecommerce', 'education', 'entertainment', 'gov', 'healthcare', 'news', 'nonprofit', 'mediumsize', 'smallsize', 'socialmedia']
folders = ['bigsize', 'courier', 'ecommerce', 'education', 'entertainment', 'gov', 'healthcare', 'news', 'nonprofit', 'mediumsize', 'smallsize']
# folders = ['courier','entertainment']
countries = ['usa', 'eu', 'pl']
# countries = ['usa']

countries_folder = "countries"
if not os.path.exists(countries_folder):
    os.makedirs(countries_folder)

for country in countries: 
    if os.path.isdir(countries_folder):
        output_file = os.path.join(countries_folder, f"{country}.txt")
        with open(output_file, 'w') as out:
            out.write(f"")
        
        for folder in folders:
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.endswith('.json') & file.startswith(country):
                        file_path = os.path.join(root, file)
                        output_file = os.path.join(countries_folder, f"{country}.txt")
                        process_and_save_to_file(file_path, output_file)

