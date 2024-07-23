import pandas as pd

# Go through the csvs in ../data/unprocessed/fetched-crossref-metadata/ and combine them into one df, only get rows where language isnt null
df = pd.DataFrame(columns=['doi', 'date', 'title', 'language'])

for i in range(0, 750, 100):
    try:
        df = pd.concat([df, pd.read_csv(f'../data/unprocessed/fetched-crossref-metadata/oc_omid_doi_mapping_5yrs.crossref{i}.csv')], ignore_index=True)
    except:
        pass

df = pd.concat([df, pd.read_csv(f'../data/unprocessed/fetched-crossref-metadata/oc_omid_doi_mapping_5yrs.crossref75035.csv')], ignore_index=True)

df = df[df['language'].notnull()]
df.to_csv('../data/cleaned/oc_crossref_langdata.csv', index=False)
