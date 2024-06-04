import os
import json
from collections import defaultdict

# Define a function to process a single file
def process_file(file_path, output_file):
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
        print(f"{sorted_errors}")
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
# folders = ['education']
for folder in folders:
    if os.path.isdir(folder):
        output_file = f"{folder}.txt"
        with open(output_file, 'w') as out:
            out.write(f"")
        
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.json'):
                    print(f"Parsing: {file}")
                    file_path = os.path.join(root, file)
                    process_file(file_path, output_file)
