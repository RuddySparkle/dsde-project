from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

country_mapper = pd.read_csv(
    "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
)
country_mapper["name"] = country_mapper["name"].str.upper()
country_mapper = country_mapper[["name", "alpha-3"]]
country_dict = country_mapper.set_index("name")["alpha-3"].to_dict()


memoization = dict()
all_records = []


def scrape_ieee(query, num_pages):
    url = "https://ieeexplore.ieee.org/rest/search"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "th-TH,th;q=0.9",
        "content-type": "application/json",
        "origin": "https://ieeexplore.ieee.org",
        "priority": "u=1, i",
        "referer": f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={query}",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "x-security-request": "required",
    }

    for page in range(1, num_pages + 1):
        data = {
            "newsearch": True,
            "queryText": query,
            "highlight": True,
            "returnFacets": ["ALL"],
            "returnType": "SEARCH",
            "matchPubs": True,
            "pageNumber": page,
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for unsuccessful requests

        data = response.json()
        records = data.get("records", [])
        all_records.extend(records)

    # Create DataFrame from all records
    df = pd.json_normalize(all_records)
    return df


# EDIT the search query here
queries = ["Medical", "Engineering", "Biochemical"]

# EDIT pagination here
num_pages = 40

selected_columns = [
    "authors",
    "publicationNumber",
    "publicationDate",
    "articleNumber",
    "articleTitle",
    "downloadCount",
    "abstract",
    "articleContentType",
]
for query in queries:
    df = scrape_ieee("query", num_pages)

selected_df = df[selected_columns]


def scrape_each_author(author):
    if "id" not in author:
        return None
    authorId = author["id"]
    global memoization
    if authorId in memoization.keys():
        return memoization[authorId]

    url = f"https://ieeexplore.ieee.org/rest/author/{authorId}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "th-TH,th;q=0.9",
        "content-type": "application/json",
        "origin": "https://ieeexplore.ieee.org",
        "priority": "u=1, i",
        "referer": "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=Engineering",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        memoization[authorId] = None
        return None
    response.raise_for_status()  # Raise an exception for unsuccessful requests

    data = response.json()
    if not len(data):
        memoization[authorId] = None
        return None
    currentAffilations = data[0].get("currentAffiliations", [])
    if not len(currentAffilations):
        memoization[authorId] = None
        return None
    currentAffilations = currentAffilations[0]
    country = currentAffilations.split(", ")
    if not len(country):
        memoization[authorId] = None
        return None
    country = country[-1]
    for k in country_dict.keys():
        if country.upper() in k or k in country.upper():
            memoization[authorId] = country_dict[k]
            return country_dict[k]
    if country.upper() in country_dict.values():
        memoization[authorId] = country.upper()
        return country.upper()
    memoization[authorId] = None
    return None


def scrape_data():
    selected_df["authors"]

    selected_df["authorsAffilationCountry"] = selected_df["authors"].apply(
        lambda x: [scrape_each_author(author) for author in x]
    )
    finished_df = selected_df
    finished_df["extracted_class"] = ""

    finished_df.loc[:999, "extracted_class"] = "MEDI"
    finished_df.loc[1000:1999, "extracted_class"] = "ENGI"
    finished_df.loc[2000:2999, "extracted_class"] = "BIOC"
    cur_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(cur_path, "scraped_data.csv")
    finished_df.to_csv(path)
