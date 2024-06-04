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
    "bigsize":  ['#FA8072', '#E74C3C', '#27629D'],
    "courier": ["#DA2424", "#faca00", "#77543e", ],
    "ecommerce":  ['#FF7224', '#f9ad33', '#0000a4'],
    "education": ['#a31a32', '#064a6b', '#cccccc', '#218d51'],
    "entertainment": ['#3395ac', '#1ed760', '#f40000', ],
    "gov": ['#FF7224', '#E74C3C', '#aaaaaa'],
    "healthcare": ['#628acf', '#102f5c', '#3fc3a5'],
    "mediumsize": ['#1ed760', '#f77933', '#194696'],
    "news": ['#e1b600', '#aaaaaa', '#f3080c'],
    "nonprofit": ['#339158', '#d71519', '#c8a200'],
    "smallsize": ['#d7b280', '#aaaaaa', '#8fdb59'],
    "socialmedia": ['#0647b3', '#218d51', '#f54200'],
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
critical_issue_counts = {}
serious_issue_counts = {}


for index, category in enumerate(categories):
    json_file_names = set()
    all_issues = set()
    file_issues = {}
    
    all_issues_counts.setdefault(category, {'critical': 0, 'serious': 0})
    all_issues_average.setdefault(category, {'critical': 0, 'serious': 0})

    with open(f"{category}.txt", "r") as file:
        data = file.read()

    sections = re.split(r"[\w]+\\", data)[1:]

    critical_counts_array = []
    serious_counts_array = []
    for section in sections:
        critical_count = 0;
        serious_count = 0;
        lines = section.split("\n")

        json_file_name = lines[0].split("_")[0]
        json_file_names.add(json_file_name);

        if "Critical Issues:" in lines:
            critical_index = lines.index("Critical Issues:") + 1
            end_critical_index = lines.index("Serious Issues:") if "Serious Issues:" in lines else len(lines)
            critical_issues_data = lines[critical_index:end_critical_index]

            if all(data == '' for data in critical_issues_data): 
                file_issues.setdefault(json_file_name, {})

            for issue_data in critical_issues_data:
                if ";" in issue_data:
                    issue, count, description = issue_data.strip().split(":")
                    all_issues.add(issue.strip())
                    all_issues_detail_counts.setdefault(issue, 0)
                    count = int(count.strip())
                    all_issues.add(issue.strip())
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('count', 0)
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('color', '#E74C3C')
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('hatch', 'xx')
                    file_issues[json_file_name][issue.strip()]["count"] += count
                    all_issues_detail_counts[issue] += count
                    all_issues_counts[category]['critical'] += count
                    critical_count += count
                    critical_issue_counts.setdefault(issue, 0)
                    critical_issue_counts[issue] += count

        if "Serious Issues:" in lines:
            serious_index = lines.index("Serious Issues:") + 1
            serious_issues_data = lines[serious_index:]

            for issue_data in serious_issues_data:
                if ";" in issue_data:
                    issue, count, description = issue_data.strip().split(":")
                    all_issues.add(issue.strip())
                    all_issues_detail_counts.setdefault(issue, 0)
                    count = int(count.strip())
                    all_issues.add(issue.strip())
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('count', 0)
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('color', 'orange')
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('hatch', '//')
                    file_issues[json_file_name][issue.strip()]["count"] += count
                    all_issues_detail_counts[issue] += count
                    all_issues_counts[category]['serious'] += count
                    serious_count += count
                    serious_issue_counts.setdefault(issue, 0)
                    serious_issue_counts[issue] += count
    
        critical_counts_array.append(critical_count)
        serious_counts_array.append(serious_count)
    
    all_issues_average[category]["critical"] = math.ceil(Average(critical_counts_array))
    all_issues_average[category]["serious"] = math.ceil(Average(serious_counts_array))

    all_issues = sorted(list(all_issues))
    max_total_count = max([sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues], default=0)
    max_total_count = math.ceil(max_total_count) + 5

    plt.figure(figsize=(12, 8))
    total_issue_counts = [sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues]

    colors_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("color", "") for json_file in file_issues.keys()] for issue in all_issues]
    colors = ['#E74C3C' if '#E74C3C' in subarr else 'orange' for subarr in colors_arrays]
    
    hatches_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("hatch", "") for json_file in file_issues.keys()] for issue in all_issues]
    hatches = ['xx' if 'xx' in subarr else '//' for subarr in hatches_arrays]

    if not all_issues:
        total_issue_counts = [0] * len(total_issue_counts)

    plt.bar(all_issues, total_issue_counts, color=colors, hatch=hatches, zorder=2)
    
    plt.title(f'Suma wystąpień naruszeń w kategorii {categories_pl[index]}')
    plt.xlabel('Naruszenie')
    plt.ylabel('Liczba wystąpień')
    plt.xticks(rotation=90)
    plt.ylim(0, max_total_count)
    plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
    plt.tight_layout()
    for i, count in enumerate(total_issue_counts):
        plt.text(i, count + 0.2, str(count), ha='center', va='bottom')
    plt.savefig(f'{category}_total_issues.png')  # Save total issues plot to a file in the current folder
    plt.close()


# Plot individual issues for each file
    fig, ax1 = plt.subplots(figsize=(13, 8))
    X_axis = np.arange(len(all_issues))
    max_count = 0
    bar_width = 0.17
    idx = np.arange(len(json_file_names)) * bar_width
    colors = category_colors.get(category)
    legend_handles = []
    json_file_names = sorted(json_file_names)
    pie_numbers = [];

    j = 0
    for idx_offset, json_file_name in zip(idx, json_file_names):
        individual_issue_counts = [file_issues[json_file_name].get(issue, {}).get("count", 0) for issue in all_issues]
        max_count = max(max(individual_issue_counts), max_count)

        # plt.bar(X_axis + idx_offset, individual_issue_counts, bar_width, edgecolor='black', color=colors, hatch=hatches)
        ax1.bar(X_axis + idx_offset, individual_issue_counts, bar_width, color=colors[j], hatch=hatches, zorder=2)
        legend_handles.append(mpatches.Patch(facecolor=colors[j], ))
        
        colors_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("color", "") for json_file in file_issues.keys()] for issue in all_issues]
    
        critical_count = sum(inner_dict['count'] for inner_dict in file_issues[json_file_name].values() if inner_dict.get('color') == '#E74C3C')
        serious_count = sum(inner_dict['count'] for inner_dict in file_issues[json_file_name].values() if inner_dict.get('color') == 'orange')
        pie_numbers.append(critical_count)
        pie_numbers.append(serious_count)

        j = (j + 1) % len(colors)
        for i, count in enumerate(individual_issue_counts):
            # plt.text(i + idx_offset, count + 0.1, f"{json_file_name[0]}{str(count)}", ha='center', va='bottom')
            ax1.text(i + idx_offset, count + 0.2, f"{str(count)}", ha='center', va='bottom', fontsize=8.5)

    ax1.set_title(f"Suma wystąpień naruszeń w kategorii {categories_pl[index]}")
    ax1.set_ylabel('Liczba wystąpień')
    ax1.set_xlabel('Naruszenie')
    ax1.set_xticks(X_axis + bar_width * (len(json_file_names) - 1) / 2, all_issues, rotation=90)

    legend_handles.append(mpatches.Patch(facecolor='white', edgecolor='black', hatch='xx'))
    legend_handles.append(mpatches.Patch(facecolor='white', edgecolor='black', hatch='//'))
    companies = category_labels.get(category)
    ax1.legend(legend_handles, companies + ['Naruszenie krytyczne', 'Naruszenie poważne'], loc='upper left')
    ax1.set_ylim(0, max_count + 7)
    
    # ax2 = fig.add_axes([0.815, 0.75, 0.2, 0.2])   # [left, bottom, width, height]
    ax2 = fig.add_axes([0.03, 0.575, 0.2, 0.2])   # [left, bottom, width, height]
    wedges, texts = ax2.pie(
        pie_numbers, labels=['' if x == 0 else x for x in pie_numbers], 
        colors=[color for color in colors for _ in range(2)], 
        hatch=['xx','//', 'xx','//', 'xx','//']
    )

    for w in wedges:
        w.set_linewidth(1)
        w.set_edgecolor('#222222')
        w.set_alpha(0.7)

    ax1.set_axisbelow(True)
    ax1.yaxis.grid(True, color='#EEEEEE')
    ax1.xaxis.grid(False)

    plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
    plt.tight_layout()
    plt.savefig(f'{category}_issues.png')
    plt.close()


# Plot detailed issues count
hatches = ['xx', '//']
plt.figure(figsize=(12, 8))
bar_width = 0.35
idx = np.arange(len(all_issues_detail_counts))  # Array to hold the indices for each category
max_count = max(max(critical_issue_counts.values()), max(serious_issue_counts.values()))  # Find maximum count for setting y-axis limit

# Plotting critical issues
critical_bars = plt.bar(idx, [critical_issue_counts.get(label, 0) for label in all_issues_detail_counts.keys()], color='#E74C3C', hatch=hatches[0], label='Naruszenia krytyczne', zorder=2)

# Plotting serious issues
serious_bars = plt.bar(idx, [serious_issue_counts.get(label, 0) for label in all_issues_detail_counts.keys()], bottom=[critical_issue_counts.get(label, 0) for label in all_issues_detail_counts.keys()], color='orange', hatch=hatches[1], label='Naruszenia poważne', zorder=2)

# Add values above bars
for bars in [critical_bars, serious_bars]:
    for bar in bars:
        height = bar.get_height()
        if height != 0:  # Check if the height is not zero
            plt.text(bar.get_x() + bar.get_width() / 2, height, '%d' % int(height), ha='center', va='bottom')

plt.title("Suma wystąpień poszczególnych naruszeń we wszystkich kategoriach")
plt.xlabel('Naruszenie')
plt.ylabel('Liczba wystąpień')
plt.xticks(idx, all_issues_detail_counts.keys(), rotation=90)
plt.legend()
plt.ylim(0, max_count + 20)
plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.tight_layout()
plt.savefig(f'all_categories_detailed_issues.png')
plt.close()


# Plot aggregated issues for all categories
severities = ['critical', 'serious']
colors = ['#E74C3C', 'orange'] 
hatches = ['xx', '//'] 
plt.figure(figsize=(12, 8))
bar_width = 0.35
idx = np.arange(len(categories))  # Array to hold the indices for each category
max_count = 0

for j, severity in enumerate(severities):
    individual_issue_counts = [all_issues_counts[category].get(severity, 0) for category in categories]
    max_count = max(max(individual_issue_counts), max_count)

    plt.bar(idx + j * bar_width, individual_issue_counts, bar_width, label=['Naruszenia krytyczne', 'Naruszenia poważne'][j], color=colors[j], hatch=hatches[j], zorder=2)
    
    for i, count in enumerate(individual_issue_counts):
        plt.text(idx[i] + j * bar_width, count + 0.1, str(count), ha='center', va='bottom')

plt.title("Suma wystąpień naruszeń dla wszystkich kategorii")
plt.xlabel('Kategoria')
plt.ylabel('Liczba wystąpień')
plt.xticks(idx + bar_width / 2, categories_pl)  # Adjusting xticks position
plt.xticks(rotation=60)
plt.legend()
plt.ylim(0, max_count + 15)
plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.tight_layout()
plt.savefig(f'all_categories_issues.png')
plt.close()


# Plot average issues (critical and serious) per file
severities = ['critical', 'serious']
colors = ['#E74C3C', 'orange'] 
hatches = ['xx', '//'] 
plt.figure(figsize=(12, 8))
bar_width = 0.35
idx = np.arange(len(categories))  # Array to hold the indices for each category
max_count = 0

for j, severity in enumerate(severities):
    individual_issue_counts = [all_issues_average[category].get(severity, 0) for category in categories]
    max_count = max(max(individual_issue_counts), max_count)

    plt.bar(idx + j * bar_width, individual_issue_counts, bar_width, label=['Naruszenia krytyczne', 'Naruszenia poważne'][j], color=colors[j], hatch=hatches[j], zorder=2)
    
    for i, count in enumerate(individual_issue_counts):
        plt.text(idx[i] + j * bar_width, count + 0.1, str(count), ha='center', va='bottom')

plt.title("Średnia liczba wystąpień naruszeń dla pojedynczych stron we wszystich kategoriach")
plt.xlabel('Kategoria')
plt.ylabel('Liczba wystąpień')
plt.xticks(idx + bar_width / 2, categories_pl)  # Adjusting xticks position
plt.xticks(rotation=60)
plt.legend()
plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.ylim(0, max_count + 5)
plt.tight_layout()
plt.savefig(f'all_categories_issues_avg.png')
plt.close()
