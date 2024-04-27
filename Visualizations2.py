import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# load the data
data_path = 'Cleaned_UK_Mental_Health.csv'
data = pd.read_csv(data_path)


# Is treatment acceptance related to family history?
def plot_family_history_vs_treatment(data):
    family_treatment = pd.crosstab(data['family_history'], data['treatment'], )
    family_treatment = family_treatment .reindex(index=['Yes', 'No'], columns=['Yes','No'])
    (family_treatment .div(family_treatment .sum(1), axis=0)*100).plot(kind='bar', stacked=True, figsize=(7, 10))
    plt.title('Family History vs Treatment')
    plt.xlabel('Family History')
    plt.ylabel('Percentage')
    plt.xticks(rotation=0)
    # Add percentage labels to the bars
    for p in plt.gca().patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        plt.gca().annotate(f'{height:.1f}%', (x + width / 2, y + height / 2), ha='center', va='center', fontsize=8)
    plt.show()


# Do different levels of indoor living have an effect on increased stress?
def plot_indoors_growing_stress(data):
    # Integrate two columns of data
    indoors_stress_counts = data.groupby(['Days_Indoors', 'Growing_Stress']).size().reset_index(name='Count')
    # Calculated percentage
    indoors_counts = data['Days_Indoors'].value_counts().reset_index(name='Total_Count')
    indoors_counts.columns = ['Days_Indoors', 'Total_Count']
    indoors_stress_counts = pd.merge(indoors_stress_counts, indoors_counts, on='Days_Indoors')
    indoors_stress_counts['Percentage'] = (indoors_stress_counts['Count'] / indoors_stress_counts['Total_Count']) * 100
    # Set an order we want
    order = ['Go out Every day', '1-14 days', '15-30 days', '31-60 days', 'More than 2 months']
    # Create a bar plot
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=indoors_stress_counts, x='Percentage', y='Days_Indoors', hue='Growing_Stress', palette='deep', order=order)
    # Set labels and title
    plt.xlabel('Percentage', fontsize=12)
    plt.ylabel('Days Indoors', fontsize=12)
    plt.title('Percentage of Growing Stress by Days Indoors', fontsize=14)
    # Rotate y-axis labels for better readability
    plt.yticks(rotation=0, ha='right')
    # Add legend
    plt.legend(title='Growing Stress', bbox_to_anchor=(1.05, 1), loc='upper left')
    # Add percentage labels to the bars
    for p in ax.patches:
        width = p.get_width()
        if width > 2:
            ax.text(width, p.get_y() + p.get_height() / 2.,
                    '{:.1f}%'.format(width),
                    ha='left', va='center', fontsize=8, color='black')
    plt.tight_layout()
    plt.show()


# Are people experiencing increased stress facing difficult times?
def plot_growing_stress_coping_struggles(data):
    stress_struggles_counts = data.groupby(['Growing_Stress', 'Coping_Struggles']).size().reset_index(name='Count')
    stress_counts = data['Growing_Stress'].value_counts().reset_index(name='Total_Count')
    stress_counts.columns = ['Growing_Stress', 'Total_Count']
    stress_struggles_counts = pd.merge(stress_struggles_counts, stress_counts, on='Growing_Stress')
    stress_struggles_counts['Percentage'] = (stress_struggles_counts['Count'] / stress_struggles_counts['Total_Count']) * 100
    g = sns.FacetGrid(stress_struggles_counts, col='Growing_Stress', height=4, aspect=1.5)
    g.set_axis_labels('Coping_Struggles', 'Percentage')
    g.set_titles('Coping Struggles: {col_name}')

    # Add percentage labels to the bars
    def add_percentage_labels(x, y, **kwargs):
        ax = plt.gca()
        for index, value in enumerate(y):
            ax.annotate(f'{value:.1f}%', xy=(index, value), xytext=(0, 3), textcoords='offset points', ha='center', fontsize=8, color='black')
    g.map_dataframe(sns.barplot, 'Coping_Struggles', 'Percentage', palette='deep').map(add_percentage_labels, 'Coping_Struggles', 'Percentage')
    g.set_axis_labels('Coping Struggles', 'Percentage')
    g.set_titles('Growing_Stress: {col_name}')
    plt.tight_layout()
    plt.show()


# Will people who feel stressed choose to seek psychological counseling?
def plot_growing_stress_mental_health_inter(data):
    stress_inter_counts = data.groupby(['Growing_Stress', 'mental_health_interview']).size().reset_index(name='Count')
    stress_counts = data['Growing_Stress'].value_counts().reset_index(name='Total_Count')
    stress_counts.columns = ['Growing_Stress', 'Total_Count']
    stress_inter_counts = pd.merge(stress_inter_counts, stress_counts, on='Growing_Stress')
    stress_inter_counts['Percentage'] = (stress_inter_counts['Count'] / stress_inter_counts['Total_Count']) * 100
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=stress_inter_counts, x='Growing_Stress', y='Percentage', hue='mental_health_interview', palette='deep')
    plt.xlabel('Growing Stress', fontsize=12)
    plt.ylabel('Percentage', fontsize=12)
    plt.title('Percentage of Mental Health Interview by Growing Stress', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    # Add legend
    plt.legend(title='Mental Health Interview', bbox_to_anchor=(1.05, 1), loc='upper left')
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., height,
                '{:.1f}%'.format(height),
                ha='center', va='bottom', fontsize=8, color='black')
    plt.tight_layout()
    plt.show()


plot_family_history_vs_treatment(data)
plot_indoors_growing_stress(data)
plot_growing_stress_coping_struggles(data)
plot_growing_stress_mental_health_inter(data)

