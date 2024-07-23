import pandas as pd
import os


# Define the directory
first = "../data/unprocessed/openalex_first_sweep/"

# List all CSV files in the directory
csv_files1 = [f for f in os.listdir(first) if f.endswith('.csv') and not f.startswith('._')]

second = "../data/unprocessed/openalex_second_sweep/"

# List all CSV files in the directory
csv_files2 = [f for f in os.listdir(second) if f.endswith('.csv') and not f.startswith('._')]

# Concatenate all CSV files in the directory
df1 = pd.concat([pd.read_csv(first + f) for f in csv_files1])
df2 = pd.concat([pd.read_csv(second + f) for f in csv_files2])

# Concatenate the two dataframes
df = pd.concat([df1, df2])

# Sort by id
df = df.sort_values('id')

# Save the concatenated dataframe
df.to_csv("../data/cleaned/oc_openalex_langdata.csv", index=False)
