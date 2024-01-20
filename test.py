import pandas as pd
import streamlit as st
import plotly.express as px



df=pd.read_csv('sensor_data_przedtreningiem.csv')


fig = px.line(df, x='Timestamp', y="ECG")
fig.update_layout(title={
    'text': 'Wykres EKG dla zarejestrowanego treningu',
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
fig.update_traces(line={'width': 0.25})
with st.container():
    st.plotly_chart(fig, theme="streamlit")

