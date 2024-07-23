import requests
import pandas as pd
from tqdm import tqdm


def get_needed_data(r, doi_dict):
    results = r.json().get('results', [])
    results_proc = []

    for result in results:
        doi = result.get('doi', '').replace('https://doi.org/', '')
        title = result.get('title', None)
        publication_year = result.get('publication_year', None)
        language = result.get('language', None)
        pub_type = result.get('type', None)
        type_crossref = result.get('type_crossref', None)
        open_access = result.get('open_access', {}).get('is_oa', None)
        accepted = result.get('primary_location', {}).get('is_accepted', None)
        published = result.get('primary_location', {}).get('is_published', None)
        cited_by_count = result.get('cited_by_count', None)

        if len(result['authorships']) == 0 or len(result['authorships'][0]['countries']) == 0:
            country = None
        else:
            country = result['authorships'][0]['countries'][0]

        cited_by_count = result['cited_by_count']

        if len(result['topics']) == 0:
            field = None
            subfield = None
        else:
            field = result['topics'][0]['field']['display_name']
            subfield = result['topics'][0]['subfield']['display_name']

        if doi in doi_dict:
            results_proc.append({
                'id': doi_dict[doi],
                'doi': doi,
                'title': title,
                'publication_year': publication_year,
                'language': language,
                'type': pub_type,
                'type_crossref': type_crossref,
                'open_access': open_access,
                'accepted': accepted,
                'published': published,
                'country': country,
                'cited_by_count': cited_by_count,
                'field': field,
                'subfield': subfield
            })

    return pd.DataFrame(results_proc)


# Fetch the retrieved dois from OpenCitations
df = pd.read_csv('integer_doi_mapping.csv')

# Step 1: Remove NaNs and 'doi:' prefix from each entry
df = df.dropna(subset=['doi'])
df['doi'] = df['doi'].str.replace('doi:', '')

# Step 2: Split entries with multiple DOIs
df['doi'] = df['doi'].str.split()

# Step 3: Create the dictionary mapping each DOI to the corresponding 'id'
doi_dict = {doi: row['id'] for _, row in df.iterrows() for doi in row['doi']}

dois = list(doi_dict.keys())

# Make start_index a checkpoint for where we left off
start_index = 7470000

n = len(dois)
works = pd.DataFrame()

for i in tqdm(range(start_index, n, 100)):
    slice = dois[i:i+100]
    pipe_separated_dois = "|".join(slice)
    
    response = requests.get(f"https://api.openalex.org/works?filter=doi:{pipe_separated_dois}&per-page=100")
    
    if response.status_code == 200:
        fetched_data = get_needed_data(response, doi_dict)
        works = pd.concat([works, fetched_data], ignore_index=True)

        if (i + 100) % 10000 == 0:
            works.to_csv(f'root/openalex_query_{start_index}_{i + 99}.csv', index=False)
            start_index = i + 100
            works = pd.DataFrame()
    else:
        print(f"Failed to retrieve data for slice: {slice}")

works.to_csv(f'root/openalex_query_{start_index}_{n - 1}.csv', index=False)
