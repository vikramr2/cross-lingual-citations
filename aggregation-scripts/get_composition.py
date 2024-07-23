from sys import argv
import pandas as pd
import json
from tqdm import tqdm

file = argv[1]

# Get file without the folder and the extension
filename = file.split('/')[-1].split('.')[0]

# Load the tsv file
df = pd.read_csv(file, sep='\t', header=None)
df.columns = ['id', 'cluster_id']

# Load the csv file
langdata = pd.read_csv('../data/cleaned/oc_corroborated_langdata.csv')

# Merge the dataframes on the 'id' column
merged_df = pd.merge(df, langdata, on='id')

# Group by cluster_id and aggregate the percentages for field, subfield, and language
def get_composition(group):
    total = len(group)
    field = (group['field'].value_counts(normalize=True) * 100).to_dict()
    subfield = (group['subfield'].value_counts(normalize=True) * 100).to_dict()
    language = (group['language'].value_counts(normalize=True) * 100).to_dict()
    return pd.Series({'field': field, 'subfield': subfield, 'language': language})

# Get unique cluster IDs
unique_cluster_ids = merged_df['cluster_id'].unique()

# Initialize an empty dictionary to store the cluster composition
cluster_composition = {}

# Iterate over the unique cluster IDs with a progress bar
for cluster_id in tqdm(unique_cluster_ids, desc="Processing clusters"):
    group = merged_df[merged_df['cluster_id'] == cluster_id]
    cluster_composition[cluster_id] = get_composition(group).to_dict()

# Save the cluster composition to a json file
with open(f'../data/{filename}_cluster_composition.json', 'w') as f:
    json.dump(cluster_composition, f, indent=4)

