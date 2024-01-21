import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from datetime import datetime, timedelta
from sqlalchemy import create_engine


connection_str = 'postgresql://jfgjgcfx:wQkwp_ImzFgYOBSkvzDgAFnAYr0ej5ML@snuffleupagus.db.elephantsql.com/jfgjgcfx'

##creates connection with database using string above
engine = create_engine(connection_str)

table_name = "bieznia_easy1"
query = "select * from \"" + table_name + "\""
df=pd.read_sql_query(query,con=engine)


def heart_rate(df):

    ekg_signal = df['ecg'].values
# Znajdowanie pików --- wartość 600 wzięta z wykresu
    peaks, _ = find_peaks(ekg_signal, height=500)
# Oblicz różnice między kolejnymi pikami w jednostkach czasu
    rr_intervals_time = np.diff(pd.to_datetime(df['timestamp'][peaks]))

    #print("Dlugosc interval time:", len(rr_intervals_time))

    #deltat = df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]
    #deltat_sec = (deltat.total_seconds())/(len(rr_intervals_time))
    #print(deltat_sec)
    #print(df['timestamp'].dtype)

    #print("pierwsza data: ", np.datetime64(df['timestamp'].iloc[0]))

    #time = np.arange(df['timestamp'].iloc[0], df['timestamp'].iloc[-1], timedelta(seconds=deltat_sec)).astype(np.datetime64)
    #time = np.arange(np.datetime64(df['timestamp'].iloc[0]), np.datetime64(df['timestamp'].iloc[-1]),len(rr_intervals_time))
    time = pd.date_range(start = df['timestamp'].iloc[0], end = df['timestamp'].iloc[-1], periods = len(rr_intervals_time) )
    intervals_heart_rate = rr_intervals_time / 1_000_000
    puls =  60_000 / intervals_heart_rate.astype(float)

    #intervals =  rr_intervals_time.astype('timedelta64[s]').astype(float)
    heart_rate_db = pd.DataFrame()
    heart_rate_db['heart_rate'] = puls
    heart_rate_db['Date'] = time
    return heart_rate_db



def heart_rate_zones(average_pulse_bpm):
    max_heart_rate = 195.0

    # Klasyfikacja średniego tempa do odpowiedniej strefy
    if average_pulse_bpm <= 0.7 * max_heart_rate:
        training_zone = 'Strefy  1 - Łatwy trening (60-70% maksymalnego tętna)'
    elif average_pulse_bpm <= 0.76 * max_heart_rate:
        training_zone = 'Strefy 2 - Komfortowy trening (70-80% maksymalnego tętna)'
    elif average_pulse_bpm <= 0.8 * max_heart_rate:
        training_zone = 'Strefy 3 - Próg mleczanowy (80-90% maksymalnego tętna)'
    else:
        training_zone = 'Strefy 4 - Intensywny trening (90-100% maksymalnego tętna)'

    st.write (f'Średnie tempo treningowe klasyfikuje się do: {training_zone}')