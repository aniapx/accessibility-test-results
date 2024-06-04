import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import numpy as np  

def Average(lst): 
    return sum(lst) / len(lst) 

categories = [
    'ecommerce', 
    'courier', 
    'education', 
    'healthcare', 
    'socialmedia',
    'entertainment', 
    'news', 
    'gov', 
    'nonprofit', 
    'bigsize', 
    'mediumsize', 
    'smallsize', 
]
categories_pl = [
    'firmy e-commerce', 
    'firmy kurieskie', 
    'instytucje edukacyjne', 
    'instytucje zdrowia', 
    'media społecznościowe',
    'rozrywka', 
    'wiadomości', 
    'strony rządowe', 
    'non-profit', 
    'duże przedsiębiorstwa', 
    'średnie przedsiębiorstwa', 
    'małe przedziębiorstwa', 
]
# categories = ['gov']
# categories_pl = ['strony rządowe']

category_colors = {
    "bigsize":  ['#85C1E9', '#E74C3C', '#27629D'],
    "courier": ["#DA2424", "#faca00", "#77543e", ],
    "ecommerce":  ['#FF7224', '#f9ad33', '#0000a4'],
    "education": ['#a31a32', '#064a6b', '#cccccc', '#218d51'],
    "entertainment": ['#5DADE2', '#46DD85', '#E74C3C', ],
    "gov": ['#5499C7', '#E74C3C', '#aaaaaa'],
    "healthcare": ['#628acf', '#102f5c', '#3fc3a5'],
    "mediumsize": ['#1ed760', '#f77933', '#2980B9'],
    "news": ['#E74C3C', '#aaaaaa', '#F4D03F'],
    "nonprofit": ['#52BE80', '#E74C3C', '#F4D03F'],
    "smallsize": ['#d7b280', '#aaaaaa', '#8fdb59'],
    "socialmedia": ['#3498DB', '#52BE80', '#FF9E48'],
}

category_labels = {
    "bigsize": ["Microsoft", "Orlen", "Volkswagen"],
    "courier": ["DHL", "InPost", "UPS"],
    "ecommerce": ["Allegro", "Amazon", "Bol"],
    "education": ['Harvard', 'Politechnika Warszawska', 'Universiteit van Amsterdam', 'Zachodniopomorski Uniwersytet Technologiczny w Szczecinie'],
    "entertainment": ["Player", "Spotify", "YouTube"],
    "gov": ['Francja', 'Polska', 'USA'],
    "healthcare": ['Mayo Clinic', 'NHS', 'Znany Lekarz'],
    "mediumsize": ['Uber Eats', 'CCC', 'Booking'],
    "news": ['CNN', 'ElPais', 'WP'],
    "nonprofit": ['Legambiente', 'American Red Cross', 'WOŚP'],
    "smallsize": ['Bagietka', 'Nomad Playhouse', 'Osnabrueck Halle'],
    "socialmedia": ['Facebook', 'LinkedIn', 'Reddit'],
}

all_issues = set()
all_issues_counts = {}
all_issues_average = {}
all_issues_detail_counts = {}

for index, category in enumerate(categories):
    json_file_names = set()
    all_issues = set()
    file_issues = {}
    
    all_issues_counts.setdefault(category, 0)
    all_issues_average.setdefault(category, 0)

    with open(f"{category}.txt", "r") as file:
        data = file.read()

    sections = re.split(r"[\w]+\\", data)[1:]

    counts_array = []
    for section in sections:
        total = 0;
        lines = section.split("\n")

        json_file_name = lines.pop(0).split("_")[1]
        json_file_names.add(json_file_name);

        file_issues.setdefault(json_file_name, {})

        for issue_data in lines:
            if ";" in issue_data:
                issue, count, description = issue_data.strip().split(":")
                all_issues.add(issue.strip())
                all_issues_detail_counts.setdefault(issue, 0)
                count = int(count.strip())
                all_issues.add(issue.strip())
                file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), 0)
                file_issues[json_file_name][issue.strip()] += count
                all_issues_detail_counts[issue] += count
                all_issues_counts[category] += count
                total += count
    
        counts_array.append(total)
    
    all_issues_average[category] = math.ceil(Average(counts_array))

    all_issues = sorted(list(all_issues))
    max_count = max([sum(file_issues.get(json_file, {}).get(issue, 0) for json_file in file_issues.keys()) for issue in all_issues], default=0)
    max_count = math.ceil(max_count) + 5

    plt.figure(figsize=(12, 8))
    total_issue_counts = [sum(file_issues.get(json_file, {}).get(issue, 0) for json_file in file_issues.keys()) for issue in all_issues]

    if not all_issues:
        total_issue_counts = [0] * len(total_issue_counts)

    plt.bar(all_issues, total_issue_counts, color='#2E86C1', zorder=2)
    
    plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
    plt.title(f'Suma wystąpień naruszeń w kategorii {categories_pl[index]}')
    plt.xlabel('Naruszenie')
    plt.ylabel('Liczba wystąpień')
    plt.xticks(rotation=90)
    plt.ylim(0, max_count + (max_count/10))  # Set the y-axis limits using the maximum total count
    plt.tight_layout()
    for i, count in enumerate(total_issue_counts):
        plt.text(i, count + 0.2, str(count), ha='center', va='bottom', fontsize=8.5)
    plt.savefig(f'{category}_total_issues.png')  # Save total issues plot to a file in the current folder
    plt.close()


# Plot individual issues for each file
    plt.figure(figsize=(13, 8))
    X_axis = np.arange(len(all_issues))
    max_count = 0
    bar_width = 0.17
    idx = np.arange(len(json_file_names)) * bar_width
    colors = category_colors.get(category)
    json_file_names = sorted(json_file_names)
    legend_handles = []

    j = 0
    for idx_offset, json_file_name in zip(idx, json_file_names):
        individual_issue_counts = [file_issues[json_file_name].get(issue, 0) for issue in all_issues]
        max_count = max(max(individual_issue_counts), max_count)

        # plt.bar(X_axis + idx_offset, individual_issue_counts, bar_width, edgecolor='black')
        plt.bar(X_axis + idx_offset, individual_issue_counts, bar_width, color=colors[j], zorder=2)
        legend_handles.append(mpatches.Patch(facecolor=colors[j]))
        
        j = (j + 1) % len(colors)
        for i, count in enumerate(individual_issue_counts):
            plt.text(i + idx_offset, count + 0.1, f"{str(count)}", ha='center', va='bottom', fontsize=8.5)

    plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
    plt.title(f"Suma wystąpień naruszeń w kategorii {categories_pl[index]}")
    plt.ylabel('Liczba wystąpień')
    plt.xlabel('Naruszenie')
    plt.xticks(X_axis + bar_width * (len(json_file_names) - 1) / 2, all_issues, rotation=90)

    plt.legend(legend_handles, category_labels.get(category), loc='upper left')
    plt.ylim(0, max_count + (max_count/15))

    plt.tight_layout()
    plt.savefig(f'{category}_issues.png')  # Save individual file issues plot to a file in the current folder
    plt.close()


# Plot aggregated issues for all categories
plt.figure(figsize=(12, 8))
bar_width = 0.4
idx = np.arange(len(categories))  # Array to hold the indices for each category
max_count = 0

individual_issue_counts = [all_issues_counts.get(category, 0) for category in categories]
max_count = max(max(individual_issue_counts), max_count)

plt.bar(idx + bar_width, individual_issue_counts, bar_width, color='#2E86C1', zorder=2)

for i, count in enumerate(individual_issue_counts):
    plt.text(idx[i] + bar_width, count + 0.2, str(count), ha='center', va='bottom', fontsize=8.5)

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title("Suma wystąpień naruszeń dla wszystkich kategorii")
plt.ylabel('Liczba wystąpień')
plt.xlabel('Kategoria')
plt.xticks(idx + bar_width, categories_pl, rotation=60)
plt.legend()  # Adding legend for severities
plt.tight_layout()
plt.ylim(0, max_count + (max_count/20))  # Set the y-axis limits using the maximum total count
plt.tight_layout()
plt.savefig(f'all_categories_issues.png')  # Save individual file issues plot to a file in the current folder
plt.close()


# Plot aggregated issues for all categories
plt.figure(figsize=(12, 8))
bar_width = 0.4
idx = np.arange(len(all_issues_detail_counts))  # Array to hold the indices for each category
max_count = max(all_issues_detail_counts.values())

bars = plt.bar(idx, [all_issues_detail_counts.get(label, 0) for label in all_issues_detail_counts.keys()], color='#2E86C1', zorder=2)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, '%d' % int(height), ha='center', va='bottom')

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title("Suma wystąpień poszczególnych naruszeń we wszystkich kategoriach")
plt.ylabel('Liczba wystąpień')
plt.xlabel('Narszenie')
plt.xticks(idx, all_issues_detail_counts.keys(), rotation=90)
plt.legend()  # Adding legend for severities
plt.tight_layout()
plt.ylim(0, max_count + (max_count/15))  # Set the y-axis limits using the maximum total count
plt.tight_layout()
plt.savefig(f'all_categories_detailed_issues.png')  # Save individual file issues plot to a file in the current folder
plt.close()


# Plot average issues (critical and serious) per file
plt.figure(figsize=(12, 8))
bar_width = 0.4  
idx = np.arange(len(categories))  # Array to hold the indices for each category
max_count = 0

individual_issue_counts = [all_issues_average[category] for category in categories]
max_count = max(max(individual_issue_counts), max_count)

plt.bar(idx +  bar_width, individual_issue_counts, bar_width, color='#2E86C1', zorder=2)

for i, count in enumerate(individual_issue_counts):
    plt.text(idx[i] +  bar_width, count + 0.1, str(count), ha='center', va='bottom', fontsize=8.5)

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title("Średnia liczba wystąpień naruszeń dla pojedynczych stron we wszystich kategoriach")
plt.ylabel('Liczba wystąpień')
plt.xlabel('Kategoria')
plt.xticks(idx + bar_width, categories_pl, rotation=60)
plt.legend()  # Adding legend for severities
plt.tight_layout()
plt.ylim(0, max_count + (max_count/15))  # Set the y-axis limits using the maximum total count
plt.tight_layout()
plt.savefig(f'all_categories_issues_avg.png')  # Save individual file issues plot to a file in the current folder
plt.close()
