import pandas as pd

# Fetch the OMID series
omid_doi_df = pd.read_csv('oc_omid_doi_mapping_5yrs.csv')
omids = omid_doi_df['omid']

# Get the edgelist and filter it
edgelist = pd.read_csv('oc_citation_events_last_5yrs.csv')
filtered = edgelist[edgelist['citing'].isin(omids) & edgelist['cited'].isin(omids)]

# Calculate the number of rows removed
original_rows = len(edgelist)
rows_removed = original_rows - len(filtered)

# Print the number of rows removed
print("Number of rows removed:", rows_removed)

filtered.to_csv('oc_citation_events_last_5yrs_filtered.csv', index=False)