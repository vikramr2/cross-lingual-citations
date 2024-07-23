import pandas as pd

# Load ../data/cleaned/oc_corroborated_langdata.csv
corroborated_df = pd.read_csv("../data/cleaned/oc_corroborated_langdata.csv")

# Get the list of ids
ids = corroborated_df['id'].tolist()

# Load ../data/cleaned/oc_citation_events_last_5_years_int_el.cleaned.tsv. There are no column names
citation_events_df = pd.read_csv("../data/cleaned/oc_citation_events_last_5yrs_int_el.cleaned.tsv", header=None, sep='\t')

# Rename the columns to 'citing' and 'cited'
citation_events_df.columns = ['citing', 'cited']

# Get only rows in citation_events_df where both columns are in ids
filtered_citation_events_df = citation_events_df[citation_events_df['citing'].isin(ids) & citation_events_df['cited'].isin(ids)]

# Ensure both columns are ints
filtered_citation_events_df['citing'] = filtered_citation_events_df['citing'].astype(int)

# Save the filtered DataFrame to ../data/cleaned/oc_citation_events_last_5_years_int_el.cleaned.filtered.tsv. Save without index or header
filtered_citation_events_df.to_csv("../data/cleaned/oc_citation_events_last_5_years_int_el.cleaned.filtered.tsv", index=False, header=False, sep='\t')
