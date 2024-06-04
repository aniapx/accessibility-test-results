import os
import glob
import re
from bs4 import BeautifulSoup

def parse_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        failed_instances = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') and (tag['class'][0].startswith('failed-instances-container')))

        results = []
        for instance in failed_instances:
            tables = instance.find_all(lambda tag: tag.get('class') and (tag['class'][0].startswith('collapsible-container')))

            for table in tables:
                instance_data = {}
                
                # Extracting failed instances count
                h3_element = instance.find('h3')
                failed_count = h3_element.find('span', class_='count').text.strip() if h3_element else "Failed instances count not found"
                instance_data['failed_count'] = failed_count
                
                # Extracting failure id
                failure_id_span = table.find('span', class_='rule-details-id')
                failure_id = failure_id_span.text.strip().replace('\n', ' ') if failure_id_span else None
                failure_id = re.sub(r'\s+', ' ', failure_id) if failure_id else None
                instance_data['failure_id'] = failure_id
                
                # Extracting failure title
                failure_title_span = table.find('span', class_='rule-details-description')
                failure_title = failure_title_span.text.strip().replace('\n', ' ') if failure_title_span else None
                failure_title = re.sub(r'\s+', ' ', failure_title) if failure_title else None
                instance_data['failure_title'] = failure_title
                
                # Extracting failure count
                failure_count_span = table.find('span', class_='count')
                failure_count = failure_count_span.text.strip() if failure_count_span else None
                instance_data['failure_count'] = failure_count

                results.append(instance_data)

        return results
    
def print_to_file(file, data):
        for instance in data:
            file.write("{}: {}: {};\n".format(instance['failure_id'], instance['failed_count'], instance['failure_title']))

folders = ['bigsize', 'courier', 'ecommerce', 'education', 'entertainment', 'gov', 'healthcare', 'news', 'nonprofit', 'mediumsize', 'smallsize', 'socialmedia']
# folders = ['socialmedia']

for folder in folders:
    folder_path = os.path.join('.', folder)
    html_files = glob.glob(os.path.join(folder_path, '*.html'))  # Adjust pattern to match all HTML files

    # Create a file with the folder name
    output_file_name = f"{folder}.txt"
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(f"")

    for html_file in html_files:
        print("Parsing file:", html_file)
        parsed_data = parse_html(html_file)

        # Append the parsed data to the output file
        with open(output_file_name, 'a', encoding='utf-8') as output_file:
            output_file.write(f"{html_file}\n")
            print_to_file(output_file, parsed_data)
            output_file.write("\n")
            
