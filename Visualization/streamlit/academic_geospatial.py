import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import plotly.express as px
import math
import inspect
import ast

def to_list(data_cell):
    return ast.literal_eval(data_cell)

def to_string(data_cell):
    return str(data_cell)

def to_float(data_cell):
    return float(data_cell)

def get_year(data_cell):
    data_cell = str(data_cell)
    return data_cell.split()[-1]

def lowercasing(data_cell):
    data_cell = str(data_cell)
    return data_cell.lower()

def main() :

    ## ---------------------------------------------------------------------------- ##
    ## Initial Part ##
    renamedScraped = {
        'articleTitle': 'title',
        'authorsAffilationCountry': 'affiliation_country',
    }

    # Main Title
    st.title('Chula Academic Paper Analysis in 2018-2023 (Scopus Data)')

    # Load main dataset
    df = pd.read_csv('../cleaned_test.csv')
    df['publish_year'] = df['publish_year'].apply(to_string)
    df['index'] = df['Unnamed: 0']
    df = df[['index', 'title', 'extracted_class', 'affiliation_country', 'publish_year']]

    # Load scraped dataset
    scraped_df = pd.read_csv('../../WebScraping/RESTAPI/scraped_data.csv')
    scraped_df = pd.DataFrame(scraped_df[['articleTitle', 'authorsAffilationCountry', 'extracted_class', 'publicationDate']])
    scraped_df['publish_year'] = scraped_df['publicationDate'].apply(get_year)
    scraped_df = scraped_df.drop(columns=['publicationDate'])
    scraped_df = scraped_df.rename(columns=renamedScraped)
    scraped_df['affiliation_country'] = scraped_df['affiliation_country'].apply(to_list)
    scraped_df = scraped_df.explode('affiliation_country')
    scraped_df['affiliation_country'] = scraped_df['affiliation_country'].apply(lowercasing)
    scraped_df = scraped_df[scraped_df['affiliation_country'].str.len() == 3]
    scraped_df = scraped_df[scraped_df['affiliation_country'] != 'chn']
    scraped_df = scraped_df.drop_duplicates()

    # Load countrycode coordination dataset
    coor_df = pd.read_csv('../countrycode_coor.csv')

    # Classification Dataset
    class_df = df[['title', 'extracted_class', 'publish_year']]
    class_df['extracted_class'] = class_df['extracted_class'].apply(to_list)
    class_df['publish_year'] = df['publish_year']
    class_df = class_df.explode('extracted_class')

    # Country Affiliation Dataset
    country_df = df[['title', 'affiliation_country', 'publish_year']]
    country_df['affiliation_country'] = country_df['affiliation_country'].apply(to_list)
    country_df = country_df.explode('affiliation_country')
    country_df = country_df[country_df['affiliation_country'] != 'tha']
    country_df = country_df.drop_duplicates()

    # Prepare Classification Dataset
    # Classification Data
    class_data = class_df['extracted_class'].unique()
    class_data.sort()
    class_data = np.concatenate((['Any'], class_data), axis=0)

    # Published Year Data
    published_year_data = df['publish_year'].unique()
    published_year_data.sort()
    published_year_data = np.concatenate((['Any'], published_year_data), axis=0)

    st.sidebar.header('Variable Control')

    # Classification Type Selection
    class_selected = st.sidebar.selectbox('Choose Classification Type', class_data)

    # Published Year Selection
    published_year_selected = st.sidebar.selectbox('Choose Published Year', published_year_data)

    # Generate histogram depends on Province
    def generate_histogram(isAll: bool, type: str): 

        text_header = ''
        if(not isAll):
            if(type == 'class') :
                new_df = class_df[class_df['extracted_class'] == class_selected]
                text_header = f'Academic Paper based on {class_selected} class'
            elif(type == 'date') :
                new_df = class_df[class_df['publish_year'] == published_year_selected]
                text_header = f'Academic Paper in {published_year_selected}'
        else:
            new_df = class_df
            text_header = f'Academic Paper Type from 2018-2023'

        if(type == 'date') :
            sum_by_class = new_df['extracted_class'].value_counts().reset_index(name="class_count")
            his = px.histogram(sum_by_class, x ="class_count", y="extracted_class")
            his.update_layout(title=text_header, 
                            height = 700, width = 700, xaxis_title = "Count", 
                            yaxis_title = "Class Type",
                            yaxis={'categoryorder':'total ascending'} 
                            )
            return his

        elif(type == 'class') :
            sum_by_year = new_df.groupby('publish_year').size().reset_index(name="class_count")
            his = px.histogram(sum_by_year, x ="publish_year", y="class_count", nbins=6)
            his.update_layout(title=text_header, 
                            height = 350, width = 700, xaxis_title = "Year",
                            bargap=0.2, 
                            yaxis_title = "Count",
                            )
            return his

    # Generate Map function
    def generate_map(type: str):

        if(type == 'scopus') :
            country_df_ready = country_df[['title', 'affiliation_country', 'publish_year']]
        elif(type == 'scraped') :
            country_df_ready = scraped_df[['title', 'affiliation_country', 'publish_year', 'extracted_class']]

        if(published_year_selected != 'Any') :
            country_df_ready = country_df_ready[country_df_ready['publish_year'] == published_year_selected]
        if(class_selected != 'Any') :
            if(type == 'scopus') :
                country_df_ready = pd.merge(country_df_ready, class_df.drop(columns=['publish_year']), on='title', how='inner')
            country_df_ready = country_df_ready[country_df_ready['extracted_class'] == class_selected]
        
        
        country_freq = country_df_ready['affiliation_country'].value_counts()
        country_freq = country_freq.reset_index()
        country_freq['affiliation_country'] = country_freq['affiliation_country']
        country_freq = pd.merge(country_freq, coor_df, left_on='affiliation_country', right_on='country_code', how='inner')
        country_freq = country_freq.drop(columns=['Unnamed: 0', 'country_code'])
        radius_factor = 1000000 / country_freq['count'].max()
        country_freq['paper_radius'] = country_freq['count'].apply(lambda count: count * radius_factor)
        
        

        layer = pdk.Layer("ScatterplotLayer",
                        country_freq,
                        get_position=['longitude', 'latitude'],
                        get_color=[255, 219, 230, 220],
                        get_radius="paper_radius",
                        radius_scale=1,
                        opacity=1,
                        pickable=True
                        )
        view_state = pdk.ViewState(longitude=country_freq['longitude'].mean(),
                                latitude=country_freq['latitude'].mean(),
                                zoom=0.7
                                )
        map_style = "mapbox://styles/mapbox/dark-v11"
        return pdk.Deck(layers=[layer],
                        initial_view_state=view_state,
                        map_style=map_style,
                        tooltip={'text': '{code}'}
                        )

    ## ---------------------------------------------------------------------------- ##

    ## Main Contents ##
    # Histogram on Classification and Year
    st.subheader('Histogram of Academic Paper Analysis')
    if(published_year_selected == 'Any') :
        st.plotly_chart(generate_histogram(True, 'date'))
    else :
        st.plotly_chart(generate_histogram(False, 'date'))
    if(class_selected == 'Any') :
        st.plotly_chart(generate_histogram(True, 'class'))
    else :
        st.plotly_chart(generate_histogram(False, 'class'))

    # Geospatial Analysis on Country
    st.subheader('Collaboration Analysis on Scopus Data (Geospatial)')
    st.pydeck_chart(generate_map('scopus'))

    st.subheader('Foreign Scraped Data')
    st.pydeck_chart(generate_map('scraped'))


main()