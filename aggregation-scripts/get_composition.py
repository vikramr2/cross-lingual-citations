from sys import argv
import pandas as pd
import json
from tqdm import tqdm

def get_comp(df):
    # Calculate total counts per cluster
    total_counts = df.groupby('cluster_id').size().reset_index(name='total_count')

    # Calculate counts of each field and language for each cluster
    field_counts = df.groupby(['cluster_id', 'field']).size().unstack(fill_value=0)
    language_counts = df.groupby(['cluster_id', 'language']).size().unstack(fill_value=0)

    # Combine field and language counts
    combined_counts = pd.concat([field_counts, language_counts], axis=1).reset_index()

    # Merge with total counts to calculate percentages
    combined_counts = combined_counts.merge(total_counts, on='cluster_id')

    # Calculate percentages for each column
    for column in combined_counts.columns[1:-1]:
        combined_counts[column] = (combined_counts[column] / combined_counts['total_count']) * 100

    # Drop the total_count column as it's not needed in the final output
    combined_counts = combined_counts.drop(columns=['total_count'])

    return combined_counts

file = argv[1]

# Get file without the folder and the extension
filename = file.split('/')[-1].split('.tsv')[0]

# Load the tsv file
df = pd.read_csv(file, sep='\t', header=None)
df.columns = ['id', 'cluster_id']

# Load the csv file
langdata = pd.read_csv('../../data/cleaned/oc_corroborated_langdata.csv')

# Merge the dataframes on the 'id' column
merged_df = pd.merge(df, langdata, on='id')
merged_df = merged_df[['id', 'cluster_id', 'language', 'field']]

comp_df = get_comp(merged_df)
comp_df.to_csv(f'{filename}_cluster_comp.csv', index=False)
