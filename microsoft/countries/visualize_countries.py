import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import numpy as np  

countries = ['usa', 'eu', 'pl'];
countries_pl = ['USA', 'Unia Europejska', 'Polska'];
# countries = ['usa', 'pl'];

country_issues = {};
country_issues2 = {};

for index, country in enumerate(countries): 
    file_names = set()
    all_issues = set()
    file_issues = {}

    total_critical_in_country = 0;
    total_serious_in_country = 0;

    with open(f"{country}.txt", "r") as file:
        data = file.read()

    sections = re.split(r"[\w]+\\", data)[1:]

    for section in sections:
        lines = section.split("\n")

        file_name = lines.pop(0).split("_")[0]
        file_names.add(file_name);

        country_issues.setdefault(country, {})
        country_issues2.setdefault(country, 0)
        
        if all(data == '' for data in lines):
            file_issues.setdefault(file_name, {})

        total_per_issue = 0;
        for issue_data in lines:
            if ";" in issue_data:
                issue, count, description = issue_data.strip().split(":")
                count = int(count.strip())
                all_issues.add(issue.strip())
                file_issues.setdefault(file_name, {}).setdefault(issue.strip(), {}).setdefault('count', 0)
                file_issues[file_name][issue.strip()]["count"] += count

                country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('count', 0)
                country_issues[country][issue.strip()]["count"] += count

                country_issues2[country] += count

                total_critical_in_country += count;
                total_serious_in_country += count;

        
    ### total issues plot
    all_issues = sorted(list(all_issues))
    max_total_count = max([sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues], default=0)
    max_total_count = math.ceil(max_total_count) + 5

    plt.figure(figsize=(10, 7))
    total_issue_counts = [sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues]

    colors_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("color", "") for json_file in file_issues.keys()] for issue in all_issues]
    
    if not all_issues:
        total_issue_counts = [0] * len(total_issue_counts)

    plt.bar(all_issues, total_issue_counts, color='#2E86C1', zorder=2)
    plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
    plt.title(f'Suma wystąpień naruszeń wg. obrzaru geograficznego: {countries_pl[index]}')
    plt.xlabel('Naruszenie')
    plt.ylabel('Liczba wystąpień')
    plt.xticks(rotation=90, fontsize=8.5)
    plt.ylim(0, max_total_count + (max_total_count/20))  # Set the y-axis limits using the maximum total count
    plt.tight_layout()
    for i, count in enumerate(total_issue_counts):
        plt.text(i, count + 0.1, str(count), ha='center', va='bottom', fontsize=8.5)
    plt.savefig(f'{country}_total_issues.png')  # Save total issues plot to a file in the current folder
    plt.close()




### countries plot
idx = -0.4
plt.figure(figsize=(20, 7))
X_axis = np.arange(len(all_issues))
max_count = 0
legend_handles = []

for country in countries: 
    individual_issue_counts = [country_issues.get(country, {}).get(issue, {}).get("count", 0) for issue in all_issues]

    if country == 'usa':
        country_colors = ["#cccccc" for _ in range(len(all_issues))]
    elif country == 'eu':
        country_colors = ["#2980B9" for _ in range(len(all_issues))]    
    else:
        country_colors = ["#E74C3C" for _ in range(len(all_issues))]

    maxtemp = max(individual_issue_counts)
    if maxtemp > max_count:
        max_count = maxtemp

    plt.bar(X_axis + idx, individual_issue_counts, 0.2, color=country_colors, zorder=2)
    legend_handles.append(mpatches.Patch(facecolor=country_colors[0]))
    for i, count in enumerate(individual_issue_counts):
        plt.text(i + idx, count + 0.1, str(count), ha='center', va='bottom', fontsize=8.5)
    idx += 0.2

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title(f"Liczba wystąpień naruszeń wg. obszaru geograficznego")
plt.ylabel('Liczba wystąpień')
plt.xlabel('Naruszenie')
plt.xticks(X_axis-idx, all_issues, rotation=90)
plt.ylim(0, max_count + (max_count/20))  # Set the y-axis limits using the maximum total count
plt.legend(legend_handles, ['USA', 'Unia Europejska', 'Polska'], title='Obszar geograficzny', loc='upper right')
plt.tight_layout()
plt.savefig(f'countries_issues.png')  # Save individual file issues plot to a file in the current folder
plt.close()



### countries2 plot
plt.figure(figsize=(10, 7))
max_count = 0

for i, country in enumerate(countries): 
    count = country_issues2.get(country, 0)

    if country == 'usa':
        color = "#cccccc"
    elif country == 'eu':
        color = "#2980B9" 
    else:
        color = "#E74C3C"

    if count > max_count:
        max_count = count

    plt.bar(i, count, color=color, zorder=2)
    plt.text(i, count + 0.1, str(count), ha='center', va='bottom')

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title(f"Liczba wystąpień naruszeń wg. obszaru geograficznego")
plt.ylabel('Liczba wystąpień')
plt.xticks(range(3), labels=['USA', 'Unia Europejska', 'Polska'])
plt.ylim(0, max_count + (max_count/20))  # Set the y-axis limits using the maximum total count
plt.tight_layout()
plt.savefig(f'countries_issues_by_severity.png')  # Save individual file issues plot to a file in the current folder
plt.close()