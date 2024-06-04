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
    json_file_names = set()
    all_issues = set()
    file_issues = {}

    total_per_issue = 0;
 
    total_critical_in_country = 0;
    total_serious_in_country = 0;

    with open(f"{country}.txt", "r") as file:
        data = file.read()

    sections = re.split(r"[\w]+\\", data)[1:]

    for section in sections:
        lines = section.split("\n")

        json_file_name = lines[0].split("_")[0]
        json_file_names.add(json_file_name);

        if "Critical Issues:" in lines:
            critical_index = lines.index("Critical Issues:") + 1
            end_critical_index = lines.index("Serious Issues:") if "Serious Issues:" in lines else len(lines)
            critical_issues_data = lines[critical_index:end_critical_index]

            country_issues.setdefault(country, {})
            country_issues2.setdefault(country, {})
            if all(data == '' for data in critical_issues_data):
                file_issues.setdefault(json_file_name, {})

            total_per_issue = 0;
            for issue_data in critical_issues_data:
                if ";" in issue_data:
                    issue, count, description = issue_data.strip().split(":")
                    count = int(count.strip())
                    all_issues.add(issue.strip())
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('count', 0)
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('color', '#E74C3C')
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('hatch', 'xx')
                    file_issues[json_file_name][issue.strip()]["count"] += count

                    country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('count', total_per_issue)
                    country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('color', '#E74C3C')
                    country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('hatch', 'xx')
                    country_issues[country][issue.strip()]["count"] += count

                    country_issues2.setdefault(country, {}).setdefault('critical', {}).setdefault('count', 0)
                    country_issues2.setdefault(country, {}).setdefault('critical', {}).setdefault('color', '#E74C3C')
                    country_issues2[country]['critical']["count"] += count

                    total_per_issue += count;
                    total_critical_in_country += count;

        if "Serious Issues:" in lines:
            serious_index = lines.index("Serious Issues:") + 1
            serious_issues_data = lines[serious_index:]

            total_per_issue = 0;
            for issue_data in serious_issues_data:
                if ";" in issue_data:
                    issue, count, description = issue_data.strip().split(":")
                    count = int(count.strip())
                    all_issues.add(issue.strip())
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('count', 0)
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('color', 'orange')
                    file_issues.setdefault(json_file_name, {}).setdefault(issue.strip(), {}).setdefault('hatch', '/')
                    file_issues[json_file_name][issue.strip()]["count"] += count

                    country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('count', total_per_issue)
                    country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('color', 'orange')
                    country_issues.setdefault(country, {}).setdefault(issue.strip(), {}).setdefault('hatch', '/')
                    country_issues[country][issue.strip()]["count"] += count

                    country_issues2.setdefault(country, {}).setdefault('serious', {}).setdefault('count', 0)
                    country_issues2.setdefault(country, {}).setdefault('serious', {}).setdefault('color', 'orange')
                    country_issues2[country]['serious']["count"] += count

                    total_per_issue += count;
                    total_serious_in_country += count;
    





    ### total issues plot
    all_issues = sorted(list(all_issues))
    max_total_count = max([sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues], default=0)
    max_total_count = math.ceil(max_total_count) + 5

    plt.figure(figsize=(10, 7))
    total_issue_counts = [sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues]

    colors_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("color", "") for json_file in file_issues.keys()] for issue in all_issues]
    colors = [];
    for subarr in colors_arrays:
        if any(item == '#E74C3C' for item in subarr):
            colors.append('#E74C3C');
        else:
            colors.append('orange');
    
    hatches_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("hatch", "") for json_file in file_issues.keys()] for issue in all_issues]
    hatches = [];
    for subarr in hatches_arrays:
        if any(item == 'xx' for item in subarr):
            hatches.append('xx');
        else:
            hatches.append('//');

    if not all_issues:
        total_issue_counts = [0] * len(total_issue_counts)

    plt.bar(all_issues, total_issue_counts, color=colors, hatch=hatches, zorder=2)
    
    legend_handles = []
    legend_handles.append(mpatches.Patch(hatch='xx', facecolor='#E74C3C'))
    legend_handles.append(mpatches.Patch(hatch='//', facecolor='orange'))

    plt.legend(legend_handles, ['Naruszenie krytyczne', 'Naruszenie poważne'], loc='upper left')
    plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
    plt.title(f'Suma wystąpień naruszeń wg. obszaru geograficznego: {countries_pl[index]}')
    plt.xlabel('Rodzaj naruszenia')
    plt.ylabel('Liczba wystąpień')
    plt.xticks(rotation=90)
    plt.ylim(0, max_total_count + 6)  # Set the y-axis limits using the maximum total count
    plt.tight_layout()
    for i, count in enumerate(total_issue_counts):
        plt.text(i, count + 0.2, str(count), ha='center', va='bottom')
    plt.savefig(f'{country}_total_issues.png')  # Save total issues plot to a file in the current folder
    plt.close()




### countries plot
idx = -0.4
plt.figure(figsize=(18, 7))
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

    plt.bar(X_axis + idx, individual_issue_counts, 0.2, color=country_colors, hatch=hatches, zorder=2)
    legend_handles.append(mpatches.Patch(facecolor=country_colors[0] ))
    for i, count in enumerate(individual_issue_counts):
        plt.text(i + idx, count + 0.1, str(count), ha='center', va='bottom')
    idx += 0.2

legend_handles.append(mpatches.Patch(facecolor='white', hatch='xx', edgecolor='black'))
legend_handles.append(mpatches.Patch(facecolor='white', hatch='//', edgecolor='black'))

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title(f"Liczba wystąpień poszczególnych naruszeń wg. obszaru geograficznego")
plt.ylabel('Liczba wystapień')
plt.xlabel('Rodzaj naruszenia')
plt.xticks(X_axis-idx, all_issues, rotation=60)
plt.ylim(0, max_count + (max_count/10))  # Set the y-axis limits using the maximum total count
plt.legend(legend_handles, ['USA', 'Unia Europejska', 'Polska', 'Naruszenie krytyczne', 'Naruszenie poważne'], title='Obszar geograficzny', loc='upper right')
plt.tight_layout()
plt.savefig(f'countries_issues.png')  # Save individual file issues plot to a file in the current folder
plt.close()






### countries2 plot
idx = -0.4
plt.figure(figsize=(10, 7))
X_axis = np.arange(2)
max_count = 0
legend_handles = []

for country in countries: 
    individual_issue_counts = [country_issues2.get(country, {}).get(severity, {}).get("count", 0) for severity in ['critical', 'serious']]

    if country == 'usa':
        country_colors = ["#cccccc" for _ in range(2)]
    elif country == 'eu':
        country_colors = ["#2980B9" for _ in range(2)]   
    else:
        country_colors = ["#E74C3C" for _ in range(2)]

    maxtemp = max(individual_issue_counts)
    if maxtemp > max_count:
        max_count = maxtemp

    for i, count in enumerate(individual_issue_counts):
        plt.text(i + idx, count + 0.1, str(count), ha='center', va='bottom')

    plt.bar(X_axis + idx, individual_issue_counts, 0.2, color=country_colors, zorder=2)
    legend_handles.append(mpatches.Patch(facecolor=country_colors[0]))
    idx += 0.2

plt.grid(True, axis = 'y', linewidth=0.3, zorder=1)
plt.title(f"Ilość naruszeń poważnych i krytycznych wg. obszaru geograficznego")
plt.ylabel('Liczba wystąpień')
plt.xlabel('Rodzaj naruszeń')
plt.xticks(X_axis-idx, ['Krytyczne', 'Poważne']) 
plt.legend(legend_handles, ['USA', 'Unia Europejska', 'Polska'], title='Obszar geograficzny', loc='upper left')

plt.ylim(0, max_count + (max_count/25))  # Set the y-axis limits using the maximum total count
plt.tight_layout()
plt.savefig(f'countries_issues_by_severity.png')  # Save individual file issues plot to a file in the current folder
plt.close()