import pandas as pd
import numpy as np

def calculate_sgr(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)

def categorize_result(result, threshold):
    if result < threshold:
        return 0
    else:
        return 1

def categorize_activity(df,threshold_value = 9.5):

    # Oblicz sumę kwadratów pod pierwiastkiem dla każdego wiersza
    df['Sgr_result'] = df.apply(lambda row: calculate_sgr(row['x'], row['y'], row['z']), axis=1)

    #Uniform anomalies
    df['Sgr_result'] = np.where((df['Sgr_result'] > 28), np.random.uniform(10, 28, len(df['Sgr_result'])), df['Sgr_result'])

    #Categorize activity as 0 - no activity and 1 - activity
    df['Category'] = df['Sgr_result'].apply(lambda result: categorize_result(result, threshold_value))

