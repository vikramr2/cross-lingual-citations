import pandas as pd

df = pd.read_csv("oc_omid_doi_mapping_5yrs.csv")
df.to_csv("oc_omid_doi_mapping_5yrs.csv", index_label="index")