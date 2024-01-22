import streamlit as st
from scipy.signal import find_peaks
from datetime import datetime, date
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import plotly.express as px
from heart_rate_fun import heart_rate_zones, heart_rate
from accelerometer_fun import categorize_activity, categorize_result, calculate_sgr
import plotly.graph_objects as go


connection_str = 'postgresql://jfgjgcfx:wQkwp_ImzFgYOBSkvzDgAFnAYr0ej5ML@snuffleupagus.db.elephantsql.com/jfgjgcfx'


engine = create_engine(connection_str)
dfb = pd.DataFrame()



##################################### Streamlit functions ##################33

def draw_stats(df):
    #typical set for user
    maxim= 195
    minim = 95
    avg = 145
    med = 137
    #average from value
    avg_puls = np.mean(df['heart_rate'].values)
    max_puls = max(df['heart_rate'].values)
    min_puls = min(df['heart_rate'].values)
    med_puls = np.median(df['heart_rate'].values)
    #delta
    change_avg = str(round(100*(avg_puls - avg)/(avg_puls))) 
    change_max = str(round(100*(max_puls - maxim)/(max_puls))) 
    change_min = str(round(100*(min_puls - minim)/(min_puls))) 
    change_med = str(round(100*(med_puls - med)/(med_puls))) 
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Średnie tętno", str(round(avg_puls)) ,change_avg + "%")
    col2.metric("Najwyższe tętno", str(round(max_puls)), change_max + "%")
    col3.metric("Najniższe tętno", str(round(min_puls)), change_min + "%")
    col4.metric("Mediana tętna", str(round(med_puls)), change_med + "%")


def plot_chart(df,x,y,title,x_title,y_title):
    if not df.empty:
        #fig = px.scatter(df, x=x, y=y, trendline = 'rolling', trendline_options=dict(function="median", window=5))
        fig = px.line(df, x=x, y=y)

        fig.update_layout(title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis_title=x_title,
            yaxis_title=y_title)
        fig.update_traces(line={'width': 0.25})

        with st.container():
            st.plotly_chart(fig, theme="streamlit")
    else:
        st.warning("No data available for the chart drawing.")

    
############################################### PAGE CONFIG ####################################
st.set_page_config(
    page_title="EKG data visualization",
    page_icon=":anatomical_heart:",
    initial_sidebar_state="collapsed",
)


st.write("# Analizator treningu")

form1 = st.empty()
with form1.form(key='my_form'):
    #Container with place to write text into it, when you click button
    #it submits the text and makes it as a variable named table_i, 
    # absolutely horrific name but dont wanna change'''

    table_name = st.text_input(label='Wpisz nazwę zapisanego treningu')
    submit_button =st.form_submit_button(label='Szukaj')

try:
    #''' It is the part which works when you type text and click button submit
    #it takes input name into box and looks for table with same name in the database,
    #then the table from database is imported into dataframe and used with PyGWalker module
    #which makes the chart
    if submit_button:

        query = "select * from \"" + table_name + "\""
        dfb=pd.read_sql_query(query,con=engine)

        form1.empty()
        if not dfb.empty:
            heart_db = heart_rate(dfb)
            categorize_activity(dfb)
            draw_stats(heart_db)
            plot_chart(dfb,'timestamp','ecg','Wykres EKG dla zarejestrowanego treningu',"Czas","EKG impuls")
            plot_chart(dfb,'timestamp',"Sgr_result",'Wypadkowa wartości z akcelerometru','Czas', 'Przyspieszenie [m/s^2]')
            plot_chart(heart_db, 'Date', 'heart_rate', 'Wykres tętna w czasie treningu', 'Czas', 'Tętno [BMP]')
            heart_rate_zones(np.mean(heart_db['heart_rate']))
        else:
            st.warning("No data available for plotting")

except pd.errors.EmptyDataError as e:
    st.error(f"Error: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")
