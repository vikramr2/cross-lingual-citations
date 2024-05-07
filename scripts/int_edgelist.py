import pandas as pd


# Example DataFrame: Mapping from OMID to DOI and Index
df_mapping = pd.read_csv('oc_omid_doi_mapping_5yrs.csv')

# Example DataFrame: Citations from OMID to OMID
df_citations = pd.read_csv('oc_citation_events_last_5yrs_filtered.csv')

# Merge to map citing omid to index
df_citations = df_citations.merge(df_mapping[['omid', 'index']], left_on='citing', right_on='omid', how='left')
df_citations.rename(columns={'index': 'citing_index'}, inplace=True)
df_citations.drop('omid', axis=1, inplace=True)

# Merge to map cited omid to index
df_citations = df_citations.merge(df_mapping[['omid', 'index']], left_on='cited', right_on='omid', how='left')
df_citations.rename(columns={'index': 'cited_index'}, inplace=True)
df_citations.drop('omid', axis=1, inplace=True)

df_citations = df_citations[['citing_index', 'cited_index']]

df_citations.to_csv('oc_citation_events_lats_5yrs_int_el.tsv', sep='\t', index=False, header=False)