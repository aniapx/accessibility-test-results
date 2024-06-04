import matplotlib.pyplot as plt
import re
import numpy as np

def read_data(country_name):
    country_issues = {}
    with open(f'{country_name}.txt', 'r') as file:
        data = file.read()
        sections = re.split(r"[\w]+\\", data)[1:]

        for section in sections:
            lines = section.split("\n")
            
            if "Critical Issues:" in lines:
                critical_index = lines.index("Critical Issues:") + 1
                end_critical_index = lines.index("Serious Issues:") if "Serious Issues:" in lines else len(lines)
                critical_issues_data = lines[critical_index:end_critical_index]

                for issue_data in critical_issues_data:
                    if ";" in issue_data:
                        issue, count, description = issue_data.strip().split(":")
                        count = int(count.strip())
                        country_issues.setdefault(issue.strip(), {}).setdefault('count', 0)
                        country_issues[issue]['count'] += count
                        country_issues.setdefault(issue.strip(), {}).setdefault('color', 'red')
                        country_issues.setdefault(issue.strip(), {}).setdefault('hatch', 'xx')

            if "Serious Issues:" in lines:
                serious_index = lines.index("Serious Issues:") + 1
                serious_issues_data = lines[serious_index:]

                for issue_data in serious_issues_data:
                    if ";" in issue_data:
                        issue, count, description = issue_data.strip().split(":")
                        count = int(count.strip())
                        country_issues.setdefault(issue.strip(), {}).setdefault('count', 0)
                        country_issues[issue]['count'] += count
                        country_issues.setdefault(issue.strip(), {}).setdefault('color', 'orange')
                        country_issues.setdefault(issue.strip(), {}).setdefault('hatch', '/')

    return country_issues

def plot_severity_issues(issues_data):
    countries = list(issues_data.keys())
    critical_counts = [issues_data[country]['critical'] for country in countries]
    serious_counts = [issues_data[country]['serious'] for country in countries]

    X_axis = np.arange(3)

    plt.figure(figsize=(10, 6))

    idx = -0.2
    for severity_issues in [
        {'issues': critical_counts, 'color': 'red', 'hatch': 'xx'}, 
        {'issues': serious_counts, 'color': 'orange', 'hatch': '/'}
    ]:
        plt.bar(X_axis + idx, severity_issues['issues'], 0.2, alpha=0.7, edgecolor='black', color=severity_issues['color'], hatch=severity_issues['hatch'])
        for i, count in enumerate(severity_issues['issues']):
            plt.text(i + idx, count + 0.1, str(count), ha='center', va='bottom')
        idx += 0.2

    # plt.bar(list(X_axis), critical_counts, color='red', label='Critical')
    # plt.bar(list(X_axis + 1), serious_counts, color='orange', label='Serious', bottom=critical_counts)

    plt.ylabel('Liczba naruszeń')
    plt.title('Suma naruszeń krytycznych i poważnych')
    plt.legend(['Krytyczne', 'Poważne'])
    plt.xticks(X_axis-0.1, ['Unia Europejska', 'USA', 'Polska']) 
    plt.tight_layout()
    plt.savefig(f'countries_issues_per_country.png')  # Save individual file issues plot to a file in the current folder
    plt.close()

 

def plot_detailed_issues(issues_data):
    countries = list(issues_data.keys())
    issues_array = [issues_data[country] for country in countries]

    all_issues = set()
    for issues in issues_array:
        all_issues.update(issues.keys())

    all_issues = sorted(all_issues)

    X_axis = np.arange(len(all_issues))

    plt.figure(figsize=(30, 8))

    hatches = ['*', '/', '-']

    bar_width = 0.25

    idx = bar_width * -2
    for i, issues in enumerate(issues_array):
        for j, issue_name in enumerate(all_issues):
            issue_props = issues.get(issue_name)

            if issue_props != None:
                plt.bar(X_axis[j] + idx, issue_props['count'], bar_width, alpha=0.7, edgecolor='black', color=issue_props.get('color'), hatch=hatches[i])
                plt.text(X_axis[j] + idx, issue_props['count'] + 0.2, str(issue_props['count']), ha='center', va='bottom')
            else:
                plt.text(X_axis[j] + idx, 0.2, '0', ha='center', va='bottom')
            
        idx += bar_width

    plt.ylabel('Liczba naruszeń')
    plt.title('Suma naruszeń krytycznych i poważnych')
    # plt.legend(['Krytyczne', 'Poważne', 'mm', 's'])
    plt.xticks(X_axis-bar_width / 2, all_issues, rotation=90) 
    plt.tight_layout()
    plt.savefig(f'countries_detailed_issues.png')  # Save individual file issues plot to a file in the current folder
    plt.close()



# Combine data from all countries
countries = ['usa', 'eu', 'pl']
# countries = ['pl']
countries_issues = {}
countries_severities = {}
for country in countries:
    data = read_data(country)

    countries_severities.setdefault(country, {'critical': 0, 'serious': 0})

    for issue_name, issue_props in data.items():
        countries_issues.setdefault(country, {})
        countries_issues[country].setdefault(issue_name, {'count': 0})
        countries_issues[country][issue_name]['count'] += issue_props.get('count', 0)
        countries_issues[country][issue_name]['color'] = issue_props.get('color', 'red')
        countries_issues[country][issue_name]['hatch'] = issue_props.get('hatch', 'xx')

        if issue_props['color'] == 'red':
            countries_severities[country]['critical'] += issue_props.get('count', 0)
        elif issue_props['color'] == 'orange':
            countries_severities[country]['serious'] += issue_props.get('count', 0)


# Plot the sum of serious and critical issues for each country
# plot_severity_issues(countries_severities)
plot_detailed_issues(countries_issues)
