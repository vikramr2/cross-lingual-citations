import pandas as pd
import glob
import os
import multiprocessing as mp

CORES = 8

# Path to the directory containing folders of CSVs. Adjust this path to your specific directory structure.
base_folder_path = "/scratch/users/vikramr2/cross-lingual-data/oc_citations_zips"

# Using glob to find all CSV files within subdirectories of the base folder
csv_file_paths = glob.glob(os.path.join(base_folder_path, "*/*.csv"))

def par_task(paths):
    # Initialize an empty list to store individual dataframes
    df_list = []

    for file_path in paths:
        # Read each CSV file
        temp_df = pd.read_csv(file_path, usecols=['citing', 'cited', 'creation'])

        # Convert the "creation" column to datetime
        temp_df['creation'] = pd.to_datetime(temp_df['creation'], errors='coerce')

        # Filter rows where "creation" is after January 1, 2019
        filtered_df = temp_df[temp_df['creation'] >= '2019-01-01']

        # Append the dataframe to the list
        df_list.append(filtered_df)

    # Concatenate all dataframes into one
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df

path_split = [[] for _ in range(CORES)]

for i, path in enumerate(csv_file_paths):
    path_split[i % CORES].append(path)

# (VR) Map the algorithm to each partition
with mp.Pool(CORES) as p:
    out = p.starmap(par_task, zip(path_split))

final = pd.concat(out, ignore_index=True)

outname = 
final.to_csv('oc_indices_preprocessed1.csv', index=False)
