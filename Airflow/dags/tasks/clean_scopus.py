import pandas as pd
import os
import json

country_coordinates = {
    "tha": {"Latitude": 13.75, "Longitude": 100.5167},
    "usa": {"Latitude": 37.0902, "Longitude": -95.7129},
    "gbr": {"Latitude": 51.509865, "Longitude": -0.118092},
    "deu": {"Latitude": 51.1657, "Longitude": 10.4515},
    "jpn": {"Latitude": 36.2048, "Longitude": 138.2529},
    "nor": {"Latitude": 60.472, "Longitude": 8.4689},
    "bel": {"Latitude": 50.5039, "Longitude": 4.4699},
    "swe": {"Latitude": 60.1282, "Longitude": 18.6435},
    "aus": {"Latitude": -25.2744, "Longitude": 133.7751},
    "idn": {"Latitude": -0.7893, "Longitude": 113.9213},
    "chn": {"Latitude": 35.8617, "Longitude": 104.1954},
    "chl": {"Latitude": -35.6751, "Longitude": -71.543},
    "ind": {"Latitude": 20.5937, "Longitude": 78.9629},
    "pak": {"Latitude": 30.3753, "Longitude": 69.3451},
    "mex": {"Latitude": 23.6345, "Longitude": -102.5528},
    "nld": {"Latitude": 52.1326, "Longitude": 5.2913},
    "twn": {"Latitude": 23.6978, "Longitude": 120.9605},
    "btn": {"Latitude": 27.5142, "Longitude": 90.4336},
    "mmr": {"Latitude": 21.9162, "Longitude": 95.956},
    "bra": {"Latitude": -14.235, "Longitude": -51.9253},
    "bgr": {"Latitude": 42.7339, "Longitude": 25.4858},
    "ita": {"Latitude": 41.8719, "Longitude": 12.5674},
    "can": {"Latitude": 56.1304, "Longitude": -106.3468},
    "arm": {"Latitude": 40.0691, "Longitude": 45.0382},
    "aut": {"Latitude": 47.5162, "Longitude": 14.5501},
    "blr": {"Latitude": 53.7098, "Longitude": 27.9534},
    "col": {"Latitude": 4.5709, "Longitude": -74.2973},
    "hrv": {"Latitude": 45.1, "Longitude": 15.2},
    "cyp": {"Latitude": 35.1264, "Longitude": 33.4299},
    "cze": {"Latitude": 49.8175, "Longitude": 15.473},
    "ecu": {"Latitude": -1.8312, "Longitude": -78.1834},
    "egy": {"Latitude": 26.8206, "Longitude": 30.8025},
    "est": {"Latitude": 58.5953, "Longitude": 25.0136},
    "fin": {"Latitude": 61.9241, "Longitude": 25.7482},
    "geo": {"Latitude": 42.3154, "Longitude": 43.3569},
    "grc": {"Latitude": 39.0742, "Longitude": 21.8243},
    "hun": {"Latitude": 47.1625, "Longitude": 19.5033},
    "irn": {"Latitude": 32.4279, "Longitude": 53.688},
    "irl": {"Latitude": 53.1424, "Longitude": -7.6921},
    "kor": {"Latitude": 35.9078, "Longitude": 127.7669},
    "ltu": {"Latitude": 55.1694, "Longitude": 23.8813},
    "mys": {"Latitude": 4.2105, "Longitude": 101.9758},
    "nzl": {"Latitude": -40.9006, "Longitude": 174.886},
    "pol": {"Latitude": 51.9194, "Longitude": 19.1451},
    "prt": {"Latitude": 39.3999, "Longitude": -8.2245},
    "rus": {"Latitude": 61.524, "Longitude": 105.3188},
    "srb": {"Latitude": 44.0165, "Longitude": 21.0059},
    "esp": {"Latitude": 40.4637, "Longitude": -3.7492},
    "che": {"Latitude": 46.8182, "Longitude": 8.2275},
    "tur": {"Latitude": 38.9637, "Longitude": 35.2433},
    "ukr": {"Latitude": 48.3794, "Longitude": 31.1656},
    "lva": {"Latitude": 56.8796, "Longitude": 24.6032},
    "isl": {"Latitude": 64.9631, "Longitude": -19.0208},
    "hkg": {"Latitude": 22.3193, "Longitude": 114.1694},
    "phl": {"Latitude": 12.8797, "Longitude": 121.774},
    "sgp": {"Latitude": 1.3521, "Longitude": 103.8198},
    "vnm": {"Latitude": 14.0583, "Longitude": 108.2772},
    "isr": {"Latitude": 31.0461, "Longitude": 34.8516},
    "pan": {"Latitude": 8.537, "Longitude": -80.7821},
    "are": {"Latitude": 23.4241, "Longitude": 53.8478},
    "irq": {"Latitude": 33.2232, "Longitude": 43.6793},
    "khm": {"Latitude": 12.5657, "Longitude": 104.991},
    "bgd": {"Latitude": 23.685, "Longitude": 90.3563},
    "nga": {"Latitude": 9.082, "Longitude": 8.6753},
    "dnk": {"Latitude": 56.2639, "Longitude": 9.5018},
    "sau": {"Latitude": 23.8859, "Longitude": 45.0792},
    "bhr": {"Latitude": 25.9304, "Longitude": 50.6378},
    "moz": {"Latitude": -18.6657, "Longitude": 35.5296},
    "arg": {"Latitude": -38.4161, "Longitude": -63.6167},
    "bol": {"Latitude": -16.2902, "Longitude": -63.5887},
    "lao": {"Latitude": 19.8563, "Longitude": 102.4955},
    "cub": {"Latitude": 21.5218, "Longitude": -77.7812},
    "lka": {"Latitude": 7.8731, "Longitude": 80.7718},
    "svk": {"Latitude": 48.669, "Longitude": 19.699},
    "eth": {"Latitude": 9.145, "Longitude": 40.4897},
    "rou": {"Latitude": 45.9432, "Longitude": 24.9668},
    "zaf": {"Latitude": -30.5595, "Longitude": 22.9375},
    "npl": {"Latitude": 28.3949, "Longitude": 84.124},
    "tun": {"Latitude": 33.8869, "Longitude": 9.5375},
    "qat": {"Latitude": 25.3548, "Longitude": 51.1839},
    "brn": {"Latitude": 4.5353, "Longitude": 114.7277},
    "ken": {"Latitude": -0.0236, "Longitude": 37.9062},
    "sdn": {"Latitude": 12.8628, "Longitude": 30.2176},
    "som": {"Latitude": 5.1521, "Longitude": 46.1996},
    "pri": {"Latitude": 18.2208, "Longitude": -66.5901},
    "uga": {"Latitude": 1.3733, "Longitude": 32.2903},
    "mwi": {"Latitude": -13.2543, "Longitude": 34.3015},
    "lux": {"Latitude": 49.8153, "Longitude": 6.1296},
    "svn": {"Latitude": 46.1512, "Longitude": 14.9955},
    "sle": {"Latitude": 8.4606, "Longitude": -11.7799},
    "per": {"Latitude": -9.19, "Longitude": -75.0152},
    "mar": {"Latitude": 31.7917, "Longitude": -7.0926},
    "pry": {"Latitude": -23.4425, "Longitude": -58.4438},
    "cri": {"Latitude": 9.7489, "Longitude": -83.7534},
    "gha": {"Latitude": 7.9465, "Longitude": -1.0232},
    "mdv": {"Latitude": 3.2028, "Longitude": 73.2207},
    "ssd": {"Latitude": 6.8769, "Longitude": 31.306},
    "png": {"Latitude": -6.3146, "Longitude": 143.9555},
    "zwe": {"Latitude": -19.0154, "Longitude": 29.1549},
    "zmb": {"Latitude": -13.1339, "Longitude": 27.8493},
    "ven": {"Latitude": 6.4238, "Longitude": -66.5897},
    "cod": {"Latitude": -4.0383, "Longitude": 21.7587},
    "civ": {"Latitude": 7.54, "Longitude": -5.5471},
    "mkd": {"Latitude": 41.6086, "Longitude": 21.7453},
    "tza": {"Latitude": -6.369, "Longitude": 34.8888},
    "kwt": {"Latitude": 29.3759, "Longitude": 47.9774},
    "dom": {"Latitude": 18.7357, "Longitude": -70.1627},
    "mac": {"Latitude": 22.1987, "Longitude": 113.5439},
    "dza": {"Latitude": 28.0339, "Longitude": 1.6596},
    "mne": {"Latitude": 42.7087, "Longitude": 19.3744},
    "lbn": {"Latitude": 33.8547, "Longitude": 35.8623},
    "pse": {"Latitude": 31.9522, "Longitude": 35.2332},
    "rwa": {"Latitude": -1.9403, "Longitude": 29.8739},
    "cmr": {"Latitude": 7.3697, "Longitude": 12.3547},
    "sen": {"Latitude": 14.4974, "Longitude": -14.4524},
    "hnd": {"Latitude": 15.2, "Longitude": -86.2419},
    "mng": {"Latitude": 46.8625, "Longitude": 103.8467},
    "kaz": {"Latitude": 48.0196, "Longitude": 66.9237},
    "omn": {"Latitude": 21.4735, "Longitude": 55.9754},
    "mco": {"Latitude": 43.7384, "Longitude": 7.4246},
    "bwa": {"Latitude": -22.3285, "Longitude": 24.6849},
    "syr": {"Latitude": 34.8021, "Longitude": 38.9968},
    "tto": {"Latitude": 10.6918, "Longitude": -61.2225},
    "gtm": {"Latitude": 15.7835, "Longitude": -90.2308},
    "ury": {"Latitude": -32.5228, "Longitude": -55.7658},
    "eri": {"Latitude": 15.1794, "Longitude": 39.7823},
    "guf": {"Latitude": 3.9339, "Longitude": -53.1258},
    "mrt": {"Latitude": 21.0079, "Longitude": -10.9408},
    "bih": {"Latitude": 43.9159, "Longitude": 17.6791},
    "ner": {"Latitude": 17.6078, "Longitude": 8.0817},
    "aze": {"Latitude": 40.1431, "Longitude": 47.5769},
    "ben": {"Latitude": 9.3077, "Longitude": 2.3158},
    "hti": {"Latitude": 18.9712, "Longitude": -72.2852},
    "yem": {"Latitude": 15.5527, "Longitude": 48.5164},
    "alb": {"Latitude": 41.1533, "Longitude": 20.1683},
    "lby": {"Latitude": 26.3351, "Longitude": 17.2283},
    "bfa": {"Latitude": 12.2383, "Longitude": -1.5616},
    "nic": {"Latitude": 12.8654, "Longitude": -85.2072},
    "jam": {"Latitude": 18.1096, "Longitude": -77.2975},
    "slv": {"Latitude": 13.7942, "Longitude": -88.8965},
    "afg": {"Latitude": 33.9391, "Longitude": 67.71},
    "tgo": {"Latitude": 8.6195, "Longitude": 0.8248},
    "caf": {"Latitude": 6.6111, "Longitude": 20.9394},
    "kgz": {"Latitude": 41.2044, "Longitude": 74.7661},
    "jor": {"Latitude": 30.5852, "Longitude": 36.2384},
    "gab": {"Latitude": -0.8037, "Longitude": 11.6094},
    "ago": {"Latitude": -11.2027, "Longitude": 17.8739},
    "bdi": {"Latitude": -3.3731, "Longitude": 29.9189},
    "swz": {"Latitude": -26.5225, "Longitude": 31.4659},
    "mdg": {"Latitude": -18.7669, "Longitude": 46.8691},
    "tls": {"Latitude": -8.8742, "Longitude": 125.7275},
    "mli": {"Latitude": 17.5707, "Longitude": -3.9962},
    "tcd": {"Latitude": 15.4542, "Longitude": 18.7322},
    "uzb": {"Latitude": 41.3775, "Longitude": 64.5853},
    "mus": {"Latitude": -20.3484, "Longitude": 57.5522},
    "gmb": {"Latitude": 13.4432, "Longitude": -15.3101},
    "fji": {"Latitude": -17.7134, "Longitude": 178.065},
    "reu": {"Latitude": -21.1151, "Longitude": 55.5364},
    "nam": {"Latitude": -22.9576, "Longitude": 18.4904},
    "mda": {"Latitude": 47.4116, "Longitude": 28.3699},
    "guy": {"Latitude": 4.8604, "Longitude": -58.9302},
    "brb": {"Latitude": 13.1939, "Longitude": -59.5432},
    "fsm": {"Latitude": 7.4256, "Longitude": 150.5508},
    "cpv": {"Latitude": 16.5388, "Longitude": -23.0418},
    "lbr": {"Latitude": 6.4281, "Longitude": -9.4295},
    "mlt": {"Latitude": 35.9375, "Longitude": 14.3754},
}


def map_country_coordinates(country_code):
    return country_coordinates.get(country_code, {"Latitude": None, "Longitude": None})


def extract_affiliation_country(author_group):
    try:
        return [entry["affiliation"]["@country"] for entry in author_group]
    except KeyError:
        return None


def extract_class(cell_value):
    # print(isinstance(cell_value, str))
    if isinstance(cell_value, str):
        return cell_value
    else:
        return ", ".join([d["$"] for d in cell_value])


def to_str(cell_value):
    return str(cell_value)


def extract_values(row):
    tags = row["paper_type"][-1]
    return pd.Series({"tags": tags})


def clean_data():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    fp = os.path.join(cur_path, "scopus_data")
    years = ["2018", "2019", "2020", "2021", "2022", "2023"]
    dfs = []

    for year in years:
        folder_path = os.path.join(fp, year)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    try:
                        data = json.load(file)
                        df = pd.json_normalize(data)
                        dfs.append(df)
                        print(f"Successfully reading {file_path}")
                    except json.JSONDecodeError:
                        print(f"Skipping {file_path}. Not a valid JSON file.")
            # count_test += 1
            # if(count_test == 5) :
            #     break
    df = pd.concat(dfs, ignore_index=True)
    mapper = {
        "abstracts-retrieval-response.item.bibrecord.head.enhancement.classificationgroup.classifications": "paper_type",
        "abstracts-retrieval-response.item.bibrecord.head.author-group": "authors",
    }

    classification_df = pd.DataFrame(
        df[
            "abstracts-retrieval-response.item.bibrecord.head.enhancement.classificationgroup.classifications"
        ]
    )
    classification_df["paper_type"] = classification_df
    classification_df["authors"] = df[
        "abstracts-retrieval-response.item.bibrecord.head.author-group"
    ]
    classification_df = classification_df.drop(
        columns=[
            "abstracts-retrieval-response.item.bibrecord.head.enhancement.classificationgroup.classifications"
        ]
    )
    new_df = classification_df.dropna()

    new_df["affiliationCountry"] = new_df["authors"].apply(extract_affiliation_country)

    new_sample_columns_df = classification_df.apply(extract_values, axis=1)
    new_sample_columns_df

    new_sample_columns_df[["@type", "classification"]] = pd.json_normalize(
        new_sample_columns_df["tags"]
    )
    new_sample_columns_df["extracted_class"] = new_sample_columns_df[
        "classification"
    ].apply(extract_class)
    new_sample_columns_df["extracted_class"] = new_sample_columns_df[
        "extracted_class"
    ].str.split(", ")
    # new_sample_columns_df = new_sample_columns_df.explode('extracted_class')
    new_sample_columns_df = new_sample_columns_df.drop(
        columns=["classification", "@type", "tags"]
    )

    new_sample_columns_df["affiliation_country"] = new_df["affiliationCountry"]
    new_sample_columns_df = new_sample_columns_df.dropna(subset=["affiliation_country"])
    new_sample_columns_df["title"] = df[
        "abstracts-retrieval-response.item.bibrecord.head.citation-title"
    ]
    new_sample_columns_df["publish_year"] = df[
        "abstracts-retrieval-response.item.bibrecord.head.source.publicationdate.year"
    ].apply(to_str)
    # new_sample_columns_df['publish_month'] = df['abstracts-retrieval-response.item.bibrecord.head.source.publicationdate.month']
    # new_sample_columns_df['publish_month'] = new_sample_columns_df['publish_month'].fillna({'publish_month' : new_sample_columns_df['publish_month'].mode()})
    # new_sample_columns_df = new_sample_columns_df.drop(columns=['extracted_class', 'affiliation_country'])
    filename = os.path.join(cur_path, "cleaned_test.csv")
    new_sample_columns_df.to_csv(filename)
    affiliation = pd.DataFrame(new_sample_columns_df["affiliationCountry"])
    affiliation = affiliation.explode("affiliationCountry")
    affiliation["affiliationCountry"].unique()
    affiliation[["Latitude", "Longitude"]] = (
        affiliation["affiliationCountry"]
        .apply(map_country_coordinates)
        .apply(pd.Series)
    )
    mapper = {"Latitude": "latitude", "Longitude": "longitude"}

    coor_df = pd.DataFrame(country_coordinates).T
    coor_df = coor_df.rename(columns=mapper)
    coor_df.index.name = "country_code"
    coor_df = coor_df.reset_index()
    filename = os.path.join(cur_path, "countrycode_coor.csv")
    coor_df.to_csv(filename)
