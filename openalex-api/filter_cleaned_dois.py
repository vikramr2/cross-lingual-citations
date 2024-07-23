import pandas as pd

df = pd.read_csv('oc_omid_doi_mapping_5yrs.csv')

dois = df['doi'].to_list()

# Load oc_citation_events_last_5yrs_int_el.cleaned.tsv. The tsv doesnt have column names, so we need to specify them.
# The columns are: 'citing', 'cited'
# Make sure the numbers are int and not float
df = pd.read_csv('oc_citation_events_last_5yrs_int_el.cleaned.tsv', sep='\t', names=['citing', 'cited'], dtype=int)

# Get all unique integer ids across both columns
unique_ids = list(set(df['citing'].to_list() + df['cited'].to_list()))

# Use the unique ids as an array of indices to filter the dois
dois = [dois[i] for i in unique_ids]

# zip unique ids with dois into a two column dataframe and save it as integer_doi_mapping.csv
df = pd.DataFrame(list(zip(unique_ids, dois)), columns=['id', 'doi'])
df.to_csv('integer_doi_mapping.csv', index=False)
