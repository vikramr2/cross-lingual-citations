import pandas as pd
import os
from collections import Counter
import json


def get_fn_only(file_path):
    # Use os.path.basename to get 'file.txt' from the full path
    filename_with_extension = os.path.basename(file_path)

    # Use os.path.splitext to split the filename and its extension
    filename_without_extension, _ = os.path.splitext(filename_with_extension)

    return filename_without_extension

def calculate_freq(arr):
    element_counts = Counter(arr)
    total_elements = len(arr)

    frequency_ratios = {element: count / total_elements for element, count in element_counts.items()}

    return frequency_ratios

def get_lang_comp(cluster_nodes, langmap):
    lang_entries = [langmap[node] for node in cluster_nodes]
    return calculate_freq(lang_entries)


METADATA = '/scratch/users/vikramr2/cross-lingual-data/ocmeta_last_5yrs_langtag.csv'
CLUSTERING = '/scratch/users/vikramr2/cross-lingual-data/cm_pipeline/oc-batch/oc-last5yrs-pipeline-20240417-10:24:30/leiden_res0.5_i2/S1_oc_leiden.0.5_i2_clustering.tsv'

outname = f'{get_fn_only(CLUSTERING)}_langdetect_comp.json'

# Load the TSV file
# Adjust 'path_to_file.tsv' to the path of your TSV file
df = pd.read_csv(CLUSTERING, header=None, sep='\t', names=['node_id', 'cluster_id'])

# Create a dictionary where each cluster_id maps to a list of node_ids
cluster_dict = df.groupby('cluster_id')['node_id'].apply(list).to_dict()

metadata_df = pd.read_csv(METADATA)
langmap = metadata_df['langdetect'].to_list()

cluster_langcomp = {cluster: get_lang_comp(nodes, langmap) for cluster, nodes in cluster_dict.items()}

with open(outname, 'w') as json_file:
    json.dump(cluster_langcomp, json_file, indent=4)
