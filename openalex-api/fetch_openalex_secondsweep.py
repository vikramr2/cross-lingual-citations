import requests
import pandas as pd
from tqdm import tqdm

max_retries = 3
retry_delay = 5

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
df = pd.read_csv('remaining_dois.csv')

# Step 1: Remove NaNs and 'doi:' prefix from each entry
df = df.dropna(subset=['doi'])
df['doi'] = df['doi'].str.replace('doi:', '')

# Step 2: Split entries with multiple DOIs
df['doi'] = df['doi'].str.split()

# Step 3: Create the dictionary mapping each DOI to the corresponding 'id'
doi_dict = {doi: row['id'] for _, row in df.iterrows() for doi in row['doi']}

dois = list(doi_dict.keys())

# Make start_index a checkpoint for where we left off
start_index = 150000
slice_width = 50

n = len(dois)
works = pd.DataFrame()

print(n)

for i in tqdm(range(start_index, n, slice_width)):
    slice = dois[i:i+slice_width]
    pipe_separated_dois = "|".join(slice)
    url = f"https://api.openalex.org/works?filter=doi:{pipe_separated_dois}&per-page=50"

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            # Process the response here
            if response.status_code == 200:
                fetched_data = get_needed_data(response, doi_dict)
                works = pd.concat([works, fetched_data], ignore_index=True)

                if (i + slice_width) % 10000 == 0:
                    works.to_csv(f'../data/unprocessed/openalex_second_sweep/openalex_query_{start_index}_{i + slice_width - 1}.csv', index=False)
                    start_index = i + slice_width
                    works = pd.DataFrame()
            else:
                print(f"Failed to retrieve data for slice: {slice}, error {response.status_code}")
            break
        except (ConnectionError, Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

works.to_csv(f'../data/unprocessed/openalex_second_sweep/openalex_query_{start_index}_{n - 1}.csv', index=False)
