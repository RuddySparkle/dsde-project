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

def main() :

    ## ---------------------------------------------------------------------------- ##
    ## Initial Part ##

    # Main Title
    st.title('Chula Academic Paper Analysis in 2018-2023')

    # Load main dataset
    df = pd.read_csv('../cleaned_test.csv')
    df['publish_year'] = df['publish_year'].apply(to_string)
    df['index'] = df['Unnamed: 0']
    df = df[['index', 'title', 'extracted_class', 'affiliation_country', 'publish_year']]
    st.write(df)

    # Load countrycode coordination dataset
    coor_df = pd.read_csv('../countrycode_coor.csv')
    st.write(coor_df)

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
    st.write(country_df)

    # Prepare Classification Dataset
    # Classification Data
    class_data = class_df['extracted_class'].unique()
    class_data.sort()

    # Published Year Data
    published_year_data = df['publish_year'].unique()
    published_year_data.sort()
    

    # # Date Data 
    # date_data = df['date'].unique()
    # date_data.sort()

    # # Code Data and map data prepare
    # rain_by_coor = df.groupby('code')['rain'].mean()
    # coor_data = pd.DataFrame(df['code'].unique()).rename(columns={0: 'code'}).merge(df[['code', 'latitude', 'longitude']], on='code', how='outer')
    # coor_data = df.apply(lambda row: f"{row['code']}, {row['latitude']}, {row['longitude']}", axis=1)
    # coor_data = coor_data.unique()
    # coor_data.sort()
    # coor_data = pd.DataFrame(coor_data).rename(columns={0: 'value'})
    # coor_data = coor_data['value'].str.split(', ', expand=True)
    # coor_data.columns = ['code', 'latitude', 'longitude']
    # coor_data = coor_data.merge(rain_by_coor, on='code', how='inner')
    # coor_data['rain_radius'] = coor_data['rain'].apply(lambda rain_data: math.sqrt(rain_data))
    # coor_data[['latitude', 'longitude']] = coor_data[['latitude', 'longitude']].astype(float)
    # coor_data['date'] = df['date']

    ## ---------------------------------------------------------------------------- ##
    ## Sidebar ##

    st.sidebar.header('Variable Control')

    # Classification Type Selection
    st.sidebar.subheader('Classification Visualize')
    class_selected = st.sidebar.selectbox('Choose Classification Type', class_data)

    # Published Year Selection
    published_year_selected = st.sidebar.selectbox('Choose Published Year', published_year_data)

    # # Province Selection
    # st.sidebar.subheader('Rain by Date Control')
    # province_selected = st.sidebar.selectbox('Choose Province', class_data)

    ## ---------------------------------------------------------------------------- ##
    ## Function to generate the graph

    # Generate histogram depends on Province
    def generate_histogram(isAll: bool, type: str): 

        text_header = ''
        if(not isAll):
            if(type == 'class') :
                new_df = class_df[class_df['extracted_class'] == class_selected]
                text_header = f'Count by year on {class_selected} class'
            elif(type == 'date') :
                new_df = class_df[class_df['publish_year'] == published_year_selected]
                text_header = f'Paper Count in {published_year_selected}'
        else:
            new_df = class_df
            text_header = f'Academic Paper Type from 2018-2023'

        if(isAll or type == 'date') :
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

    # Generate histogram depends on Date
    # def generate_line(isAll: bool):

    #     text_header = ''
    #     if(not isAll):
    #         new_df = df[df['province'] == province_selected]
    #         text_header = f'Average of rain by Province ({province_selected})'
    #     else:
    #         new_df = df
    #         text_header = f'Average of rain by Province (All Date)'

    #     sum_by_date = new_df.groupby('date')['rain'].mean().reset_index(name="avg_rain")
    #     line = px.line(sum_by_date, x="date", y="avg_rain", title='Average of rain by Date')
    #     line.update_layout(title=text_header, 
    #                     height = 500, width = 700, xaxis_title = "Average of rain", 
    #                     yaxis_title = "Province",
    #                     yaxis={'categoryorder':'total ascending'} 
    #                     )
    #     return line

    def generate_map(isAll: bool):
        if(not isAll):
            coor_data_ready = coor_data[coor_data['date'] == date_selected]
        else:
            country_df_ready = country_df[['title', 'affiliation_country']]
        
        country_freq = country_df_ready['affiliation_country'].value_counts()
        country_freq = country_freq.reset_index()
        country_freq['affiliation_country'] = country_freq['affiliation_country']
        country_freq = pd.merge(country_freq, coor_df, left_on='affiliation_country', right_on='country_code', how='inner')
        country_freq = country_freq.drop(columns=['Unnamed: 0', 'country_code'])
        country_freq['paper_radius'] = country_freq['count'].apply(lambda count: math.sqrt(count))
        # country_freq['paper_radius'] = country_freq['count']
        # country_freq['latitude'] = country_freq['latitude'].apply(to_float)
        # country_freq['longitude'] = country_freq['longitude'].apply(to_float)
        st.write(country_freq)
        
        layer = pdk.Layer("ScatterplotLayer",
                        country_freq,
                        get_position=['longitude', 'latitude'],
                        get_color=[255, 219, 230, 220],
                        get_radius="paper_radius",
                        radius_scale=12000,
                        opacity=1,
                        pickable=True
                        )
        view_state = pdk.ViewState(longitude=country_freq['longitude'].mean(),
                                latitude=country_freq['latitude'].mean(),
                                zoom=0.5
                                )
        map_style = "mapbox://styles/mapbox/dark-v11"
        return pdk.Deck(layers=[layer],
                        initial_view_state=view_state,
                        map_style=map_style,
                        tooltip={'text': '{code}'}
                        )

    ## ---------------------------------------------------------------------------- ##

    ## Main Contents ##
    # Rain by Province
    st.subheader('Chula all years classification')
    st.plotly_chart(generate_histogram(True, 'any'))
    st.plotly_chart(generate_histogram(False, 'class'))
    st.plotly_chart(generate_histogram(False, 'date'))

    # Rain by Date
    # st.subheader('Rain by Date')
    # st.plotly_chart(generate_line(True))
    # st.plotly_chart(generate_line(False))

    # Map on Date
    st.subheader('Rain Map Analysis')

    st.markdown('Rain Map (All Date)')
    st.pydeck_chart(generate_map(True))

    # st.markdown(f'Rain Map {date_selected}')
    st.pydeck_chart(generate_map(False))

    # Summary Block
    st.subheader('Summary')
    st.text('We can conclude that ระนอง and สุพรรณบุรี are the provinces \
            \nthat have the highest and lowest rainfall in August 2017, respectively. \
            \nAnd, we can also conclude that Aug 27, 2017 and Aug 22, 2017 are the dates that \
            \nhave the highest and lowest rainfall in August 2017.')


    # Block of Code
    st.subheader('Code')
    code = inspect.getsource(main)
    st.code(code, language='python')
    # st.write(df)
    # st.write(coor_data)

main()