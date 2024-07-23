import pandas as pd
import urllib.parse
import requests
import json
import time
from requests.exceptions import ChunkedEncodingError, RequestException


df = pd.read_csv('../data/cleaned/oc_omid_doi_mapping_5yrs.cleaned.csv')
doi_list = df['doi'].tolist()

# get rid of nan values in doi_list and print the number of dois removed
doi_list = [doi for doi in doi_list if str(doi) != 'nan']
print('Number of DOIs removed:', len(df['doi']) - len(doi_list))

def get_url_from_batch(doi_batch):
    dois_s = 'doi:' + ',doi:'.join(doi_batch)
    dois_s = urllib.parse.quote(dois_s)
    url = r'https://api.crossref.org/works/?filter={}&rows={}'.format(dois_s, batch_size)

    return url

def process_batch(doi_batch, retries=5):
    url = get_url_from_batch(doi_batch)
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # Set a timeout for 10 seconds
            response.raise_for_status()  # Raise an error for bad HTTP responses
            response_json = response.json()
            return response_json
        except ChunkedEncodingError as e:
            print(f'ChunkedEncodingError on attempt {attempt + 1}/{retries}: {e}')
        except RequestException as e:
            print(f'RequestException on attempt {attempt + 1}/{retries}: {e}')
        except ValueError as e:
            print(f'ValueError on attempt {attempt + 1}/{retries} (likely JSON decode error): {e}')
        
        time.sleep(2 ** attempt)  # Exponential backoff

    print('Failed to process batch after multiple retries')
    return {}

def compress_batch(json):
    items = json['message']['items']

    # Get a dataframe of doi, date, title, and language
    date = [item['created']['date-time'] for item in items]
    
    try:
        title = [item['title'][0] for item in items]
    except:
        title = "No title found"

    # Handle if language isn't present
    language = []
    for item in items:
        if 'language' in item:
            language.append(item['language'])
        else:
            language.append(None)
    doi = [item['DOI'] for item in items]

    df = pd.DataFrame({'doi': doi, 'date': date, 'title': title, 'language': language})
    return df

batch_size = 100
doi_batches = [doi_list[i:i+batch_size] for i in range(0, len(doi_list), batch_size)]

df = pd.DataFrame(columns=['doi', 'date', 'title', 'language'])

checkpoint = 75001
doi_batches = doi_batches[checkpoint:]

for i, batch in zip(range(checkpoint, len(doi_batches)+checkpoint), doi_batches):
    print('Processing batch {} of {}'.format(i+1, len(doi_batches)+checkpoint))
    response_json = process_batch(batch)

    if 'message' in response_json:
        df = pd.concat([df, compress_batch(response_json)], ignore_index=True)

    if i % 100 == 0:
        df.to_csv(f'../data/unprocessed/fetched-crossref-metadata/oc_omid_doi_mapping_5yrs.crossref{i}.csv', index=False)
        df = pd.DataFrame(columns=['doi', 'date', 'title', 'language'])

df.to_csv(f'../data/unprocessed/fetched-crossref-metadata/oc_omid_doi_mapping_5yrs.crossref{i}.csv', index=False)
df = pd.DataFrame(columns=['doi', 'date', 'title', 'language'])
