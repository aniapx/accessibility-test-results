import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import numpy as np

def Average(lst): 
    return sum(lst) / len(lst) 

categories = {
    "bigsize": "duże przedsiębiorstwa",
    "courier": "firmy kurierskie",
    "ecommerce": "firmy e-commerce",
    "education": "instytucje edukacyjne",
    "entertainment": "rozrywka",
    "gov": "strony rządowe",
    "healthcare": "instytucje zdrowia",
    "news": "wiadomości",
    "nonprofit": "non-profit",
    "mediumsize": "średnie przedsiębiorstwa",
    "smallsize": "małe przedsiębiorstwa",
    "socialmedia": "media społecznościowe"
}

category_colors = {
    "ecommerce": ["#fd581b", "#fdbc6e", "#0507a2"],
    "education": ["#a31a32", "#064a6b", "#cccccc", "#218d51"],
    "healthcare": ["#cccccc", "#005eb8", "#1bc3a5"],
    "entertainment": ["blue", "#2bd764", "red"],
    "gov": ["white", "red", "blue"],
    "nonprofit": ["#0f8e51", "white", "red"],
    "socialmedia": ["#1868fc", "white", "#ff4500"],
    "courier": ["#feca2a", "#6d5447", "#d40511"]
}

category_labels = {
    "ecommerce": ["Allegro", "Bol", "Amazon"],
    "education": ["Harvard", "Politechnika Warszawska", "Universiteit van Amsterdam", "Zachodniopomorski Uniwersytet Technologiczny w Szczecinie"],
    "healthcare": ["Mayo Clinic", "NHS", "Znany Lekarz"],
    "entertainment": ["YouTube", "Spotify", "Player.pl"],
    "gov": ["Francja", "Polska", "USA"],
    "nonprofit": ["Legambiente", "American Red Cross", "WOŚP"],
    "socialmedia": ["Facebook", "LinkedIn", "Reddit"],
    "courier": ["InPost", "UPS", "DHL"]
}

issue_settings = {
    "critical": {"color": "red", "hatch": "xx", "label": "Naruszenia krytyczne"},
    "serious": {"color": "orange", "hatch": "//", "label": "Naruszenia poważne"}
}


all_issues = set()
all_issues_detail_counts = {}
all_issues_counts = {'critical': 0, 'serious': 0}
critical_counts = {}
serious_counts = {}
all_issues_average = {}

def process_issues(category_data, color, hatch, counts, json_file_name, file_issues):
    total = 0;
    for issue_data in category_data:
        if ";" in issue_data:
            issue, count, description = issue_data.strip().split(":")
            issue = issue.strip()
            count = int(count.strip())

            all_issues.add(issue)
            all_issues_detail_counts.setdefault(issue, 0)
            file_issues.setdefault(json_file_name, {}).setdefault(issue, {}).setdefault('count', 0)
            file_issues.setdefault(json_file_name, {}).setdefault(issue, {}).setdefault('color', color)
            file_issues.setdefault(json_file_name, {}).setdefault(issue, {}).setdefault('hatch', hatch)

            file_issues[json_file_name][issue]["count"] += count
            all_issues_detail_counts[issue] += count
            counts.setdefault(issue, 0)
            counts[issue] += count
            total += count
    return total


def process_section():
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
            if "Serious Issues:" in lines:
                serious_index = lines.index("Serious Issues:") + 1
                serious_issues_data = lines[serious_index:]

            critical_count = process_issues(critical_issues_data, 'red', 'xx', critical_counts, json_file_name, file_issues)
            serious_count = process_issues(serious_issues_data, 'orange', '//', serious_counts, json_file_name, file_issues)
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
        colors = ['red' if 'red' in subarr else 'orange' for subarr in colors_arrays]
        
        hatches_arrays = [[file_issues.get(json_file, {}).get(issue, {}).get("hatch", "") for json_file in file_issues.keys()] for issue in all_issues]
        hatches = ['xx' if 'xx' in subarr else '//' for subarr in hatches_arrays]

        if not all_issues:
            total_issue_counts = [0] * len(total_issue_counts)

        plt.bar(all_issues, total_issue_counts, edgecolor='black', color=colors, hatch=hatches, alpha=0.7)

        plt.title(f'Suma wystąpień naruszeń w kategorii {categories[category]}')
        plt.xlabel('Naruszenie')
        plt.ylabel('Liczba wystąpień')
        plt.xticks(rotation=90)
        plt.ylim(0, max_total_count)  # Set the y-axis limits using the maximum total count
        plt.tight_layout()
        for i, count in enumerate(total_issue_counts):
            plt.text(i, count + 0.1, str(count), ha='center', va='bottom')
        plt.savefig(f'{category}_total_issues.png')  # Save total issues plot to a file in the current folder
        plt.close()

    return all_issues, file_issues


def plot_issues(category, all_issues, file_issues, json_file_names, index):
    plt.figure(figsize=(12, 8))
    idx = np.arange(len(all_issues))
    max_total_count = max([sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues], default=0)
    max_total_count = math.ceil(max_total_count) + 5

    total_issue_counts = [sum(file_issues.get(json_file, {}).get(issue, {}).get("count", 0) for json_file in file_issues.keys()) for issue in all_issues]

    colors = ["red" if any(file_issues.get(json_file, {}).get(issue, {}).get("color", "") == "red" for json_file in file_issues.keys()) else "orange" for issue in all_issues]
    hatches = ["xx" if any(file_issues.get(json_file, {}).get(issue, {}).get("hatch", "") == "xx" for json_file in file_issues.keys()) else "//" for issue in all_issues]

    plt.bar(all_issues, total_issue_counts, edgecolor="black", color=colors, hatch=hatches, alpha=0.7)

    plt.title(f"Suma występień naruszeń w kategorii {category_labels.get(category)}")
    plt.xlabel("Naruszenie")
    plt.ylabel("Liczba wystąpień")
    plt.xticks(rotation=90)
    plt.ylim(0, max_total_count)

    for i, count in enumerate(total_issue_counts):
        plt.text(i, count + 0.1, str(count), ha="center", va="bottom")

    plt.savefig(f"{category}_total_issues.png")
    plt.close()

    # Plot individual issues for each file
    fig, ax1 = plt.subplots(figsize=(13, 8))
    X_axis = np.arange(len(all_issues))
    max_count = 0
    bar_width = 0.17
    idx = np.arange(len(json_file_names)) * bar_width

    cols = category_colors.get(category, [])
    legend_handles = []
    json_file_names = sorted(json_file_names)
    pie_numbers = []

    j = 0
    for idx_offset, json_file_name in zip(idx, json_file_names):
        individual_issue_counts = [file_issues[json_file_name].get(issue, {}).get("count", 0) for issue in all_issues]
        max_count = max(max(individual_issue_counts), max_count)

        ax1.bar(X_axis + idx_offset, individual_issue_counts, bar_width, edgecolor="black", alpha=0.7, color=category_colors[j % len(cols)], hatch=hatches)
        legend_handles.append(mpatches.Patch(facecolor=cols[j % len(cols)], edgecolor="black", alpha=0.7))

        critical_count = sum(inner_dict["count"] for inner_dict in file_issues[json_file_name].values() if inner_dict.get("color") == "red")
        serious_count = sum(inner_dict["count"] for inner_dict in file_issues[json_file_name].values() if inner_dict.get("color") == "orange")
        pie_numbers.extend([critical_count, serious_count])

        j += 1
        for i, count in enumerate(individual_issue_counts):
            ax1.text(i + idx_offset, count + 0.1, f"{str(count)}", ha="center", va="bottom", fontsize=9)

    ax1.set_title(f"Suma naruszeń w kategorii {categories[index]}")
    ax1.set_ylabel("Liczba wystąpień")
    ax1.set_xlabel("Naruszenie")
    ax1.set_xticks(X_axis + bar_width * (len(json_file_names) - 1) / 2, all_issues, rotation=90)
    legend_handles.append(mpatches.Patch(facecolor="white", edgecolor="black", hatch="xx"))
    legend_handles.append(mpatches.Patch(facecolor="white", edgecolor="black", hatch="//"))
    xx = category_labels.get(category, [])
    ax1.legend(legend_handles, xx + ["Naruszenie krytyczne", "Naruszenie poważne"], loc="upper left")
    ax1.set_ylim(0, max_count + 10)

    ax2 = fig.add_axes([0.035, 0.575, 0.2, 0.2])  # [left, bottom, width, height]
    wedges, texts = ax2.pie(pie_numbers, labels=["" if x == 0 else x for x in pie_numbers], colors=[color for color in xx for _ in range(2)], hatch=["xx", "//", "xx", "//", "xx", "//"])
    for w in wedges:
        w.set_linewidth(1)
        w.set_edgecolor("black")
        w.set_alpha(0.7)

    plt.tight_layout()
    plt.savefig(f"{category}_issues.png")
    plt.close()


def plot_detailed_issues_count(critical_counts, serious_counts):
    # Plot detailed issues count
    plt.figure(figsize=(12, 8))
    idx = np.arange(len(all_issues_detail_counts))  # Array to hold the indices for each category
    max_count = max(max(critical_counts.values()), max(serious_counts.values()))  # Find maximum count for setting y-axis limit

    # Plotting critical issues
    critical_bars = plt.bar(
        idx,
        [critical_counts.get(label, 0) for label in all_issues_detail_counts.keys()],
        alpha=0.7,
        color=issue_settings["critical"]["color"],
        hatch=issue_settings["critical"]["hatch"],
        label=issue_settings["critical"]["label"],
        edgecolor="black"
    )

    # Plotting serious issues
    serious_bars = plt.bar(
        idx,
        [serious_counts.get(label, 0) for label in all_issues_detail_counts.keys()],
        alpha=0.7,
        edgecolor="black",
        bottom=[critical_counts.get(label, 0) for label in all_issues_detail_counts.keys()],
        color=issue_settings["serious"]["color"],
        hatch=issue_settings["serious"]["hatch"],
        label=issue_settings["serious"]["label"]
    )

    # Add values above bars
    for bars in [critical_bars, serious_bars]:
        for bar in bars:
            height = bar.get_height()
            if height != 0:  # Check if the height is not zero
                plt.text(bar.get_x() + bar.get_width() / 2, height, "%d" % int(height), ha="center", va="bottom")

    plt.title("Suma naruszeń poszczególnych naruszeń we wszystkich kategoriach")
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Naruszenie")
    plt.xticks(idx, all_issues_detail_counts.keys(), rotation=90)
    plt.legend()  # Adding legend for severities
    plt.tight_layout()
    plt.ylim(0, max_count + 20)  # Set the y-axis limits using the maximum total count
    plt.tight_layout()
    plt.savefig(f"all_categories_detailed_issues.png")  # Save individual file issues plot to a file in the current folder
    plt.close()


def plot_aggregated_issues_for_all_categories():
    severities = ["critical", "serious"]
    plt.figure(figsize=(12, 8))
    bar_width = 0.35  # Width of each bar
    idx = np.arange(len(categories))  # Array to hold the indices for each category
    max_count = 0

    for j, severity in enumerate(severities):
        individual_issue_counts = [all_issues_counts[category].get(severity, 0) for category in categories]
        max_count = max(max(individual_issue_counts), max_count)

        plt.bar(idx + j * bar_width, individual_issue_counts, bar_width, edgecolor="black", alpha=0.7, label=issue_settings[severity]["label"], color=issue_settings[severity]["color"], hatch=issue_settings[severity]["hatch"])
        
        for i, count in enumerate(individual_issue_counts):
            plt.text(idx[i] + j * bar_width, count + 0.1, str(count), ha="center", va="bottom")

    plt.title("Suma wystąpień naruszeń dla wszystkich kategorii")
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Kategoria")
    plt.xticks(idx + bar_width / 2, categories, rotation=60)  # Adjusting xticks position and rotation
    plt.legend()  # Adding legend for severities
    plt.tight_layout()
    plt.ylim(0, max_count + 15)  # Set the y-axis limits using the maximum total count
    plt.tight_layout()
    plt.savefig(f"all_categories_issues.png")  # Save individual file issues plot to a file in the current folder
    plt.close()


def plot_avg_issues_per_file():
    severities = ["critical", "serious"]
    plt.figure(figsize=(12, 8))
    bar_width = 0.35  # Width of each bar
    idx = np.arange(len(categories))  # Array to hold the indices for each category
    max_count = 0

    for j, severity in enumerate(severities):
        individual_issue_counts = [all_issues_average[category].get(severity, 0) for category in categories]
        max_count = max(max(individual_issue_counts), max_count)

        plt.bar(idx + j * bar_width, individual_issue_counts, bar_width, edgecolor="black", alpha=0.7, label=issue_settings[severity]['label'], color=issue_settings[severity]['color'], hatch=issue_settings[severity]['hatch'])
        
        for i, count in enumerate(individual_issue_counts):
            plt.text(idx[i] + j * bar_width, count + 0.1, str(count), ha="center", va="bottom")

    plt.title("Średnia liczba wystąpień naruszeń dla pojedynczych stron we wszystich kategoriach")
    plt.ylabel("Liczba wystąpień")
    plt.xlabel("Kategoria")
    plt.xticks(idx + bar_width / 2, categories, rotation=60)  # Adjusting xticks position and rotation
    plt.legend()  # Adding legend for severities
    plt.tight_layout()
    plt.ylim(0, max_count + 5)  # Set the y-axis limits using the maximum total count
    plt.tight_layout()
    plt.savefig(f"all_categories_issues_avg.png")
    plt.close()



process_section()

for category in enumerate(categories.keys):
    plot_issues(category)

plot_detailed_issues_count(critical_counts, serious_counts)
plot_aggregated_issues_for_all_categories()
plot_avg_issues_per_file()