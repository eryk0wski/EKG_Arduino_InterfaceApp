import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
#import streamlit.components.v1 as components
import plotly.express as px
#from streamlit_extras.add_vertical_space import add_vertical_space 


##String in special format that lets you connect to SQL in format like user:password@server:port/database 
connection_str = 'postgresql://jfgjgcfx:wQkwp_ImzFgYOBSkvzDgAFnAYr0ej5ML@snuffleupagus.db.elephantsql.com/jfgjgcfx'

##creates connection with database using string above
engine = create_engine(connection_str)

## Sending query
#query = f"select * from {table_name}"

#df=pd.read_sql_query(query,con=engine)

df = pd.DataFrame()


##################################### Streamlit functions ##################33

def draw_stats():
    col1, col2, col3 = st.columns(3)
    col1.metric("Średnie tętno", "144 BPM", "+13")
    col2.metric("Najwyższe tętno", "186 BPM", "-8%")
    col3.metric("Najniższe tętno", "99 BPM", "-4%")


def draw_chart_ekg():
    if not df.empty:
        fig = px.line(df, x='timestamp', y="ecg")
        fig.update_layout(title={
            'text': 'Wykres EKG dla zarejestrowanego treningu',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
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


st.write("# EKG Visualization App")

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
        df=pd.read_sql_query(query,con=engine)

        form1.empty()

        if not df.empty:
            draw_stats()
            draw_chart_ekg()
        else:
            st.warning("No data available for plotting")

except pd.errors.EmptyDataError as e:
    st.error(f"Error: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")



