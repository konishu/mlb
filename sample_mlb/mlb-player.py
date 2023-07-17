#https://github.com/chrisf03/portfolio-projects/blob/main/Projects/app_1_MLB_eda/mlb-app.py

import streamlit as st
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt
import seaborn as sns

from pybaseball import team_batting_bref,team_pitching_bref,team_fielding_bref,team_ids

from PIL import Image
import requests
# import plotly.graph_objects as go
# import plotly.express as px

st.set_page_config(page_title='MLB Analysis', page_icon=':baseball:',layout="wide")

image = Image.open(r"/Users/s_koni/work_dir/python/mlb/src/sample_mlb/mlb-logo.png") #.open(r"Projects/app_1_MLB_eda/mlb-logo.png") on GitHub
st.image(image,width=300)

st.title('MLB チームごとのデータ表示')

st.markdown("""
以下を指定すると、自動で結果が表示されます。
- 開始年
- 終了年
- チーム名

---
pybaseballを用いて作成
""")
st.header('結果')
tab1, tab2, tab3 = st.tabs(["Hitting", "Pitching","Fielding"])

st.sidebar.title('入力してください。')
start_year = st.sidebar.selectbox('Select start Year', list((range(2021,2024))))
end_year = st.sidebar.selectbox('Select end Year', list(reversed(range(2021,2024))))

selected_team = st.sidebar.selectbox('Select Team', [None] + ['LAA', 'MIA','KC'])
## 昔のチームまで含まれるとエラー？
# selected_team = st.sidebar.selectbox('Select Team', [None] + list(team_ids()['teamID'].unique()))



if selected_team:

    ################### Web scraping of MLB player stats ##########################
    # Hitting Stats #
    with tab1:
        @st.cache_data
        def hit_data(team_name,start_year=None,end_year=None,player_name=None):
            df = team_batting_bref(team_name,start_year, end_year)
            if player_name:
                df = df[df['Name'] == player_name]
            
            return df

        hit_stats = hit_data(team_name=selected_team, start_year=start_year, end_year=end_year)


    # Pitching Stats #
    with tab2:
        @st.cache_data
        def pitch_data(team_name,start_year=None,end_year=None,player_name=None):
            df = team_pitching_bref(team_name, start_year, end_year)
            if player_name:
                df = df[df['Name'] == player_name]
            
            return df

        pitch_stats = pitch_data(team_name=selected_team, start_year=start_year, end_year=end_year)

    # Fielding Stats #
    with tab3:
        @st.cache_data
        def field_data(team_name,start_year=None,end_year=None,player_name=None):
            df = team_fielding_bref(team_name, start_year, end_year)
            if player_name:
                df = df[df['Name'] == player_name]
            
            return df
        
        def rename_duplicates(old_columns):
            seen = {}
            for i, column in enumerate(old_columns):
                if column not in seen:
                    seen[column] = 1
                else:
                    seen[column] += 1
                    old_columns[i] = column + str(seen[column])
            return old_columns

        field_stats = field_data(team_name=selected_team, start_year=start_year, end_year=end_year)
        field_stats.columns = rename_duplicates(field_stats.columns.tolist())

    # data = [hit_data, pitch_data,field_data]
    # mlb_df = pd.concat(data)

    # unique_team = sorted(mlb_df.Tm.unique())




    ################### data filter for each tab #####################
    # # hitting tab #
    # hit_selected_team = hit_stats[(hit_stats.Tm == selected_team)]

    # # pitching tab #
    # if selected_team is None :
    #     pitch_selected_team = pitch_stats
    # else :
    #     pitch_selected_team = pitch_stats[(pitch_stats.Tm == selected_team)]

    ##################### Data Display############################
    with tab1 :
        st.dataframe(hit_stats)

        # def filedownload(df):
        #      csv = df.to_csv(index=True)
        #      b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        #      href = f'<a href="data:file/csv;base64,{b64}" download="hitter-stats.csv">Download CSV File</a>'
        #      return href
        # st.markdown(filedownload(hit_selected_team), unsafe_allow_html=True)
    with tab2 :
        st.dataframe(pitch_stats)

    #  # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
    #     def filedownload(df) :
    #         csv = df.to_csv(index=True)
    #         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    #         href = f'<a href="data:file/csv;base64,{b64}"  download="pitcher-stats.csv">Download CSV File</a>'
    #         return href
    #     st.markdown(filedownload(pitch_selected_team), unsafe_allow_html=True)

    with tab3 :
        st.dataframe(field_stats)