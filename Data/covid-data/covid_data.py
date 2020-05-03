# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 15:32:30 2020

@author: joell
"""

import pandas as pd 

csv_files = ['covid19_Confirmed.csv','covid19_Deaths.csv','covid19_Recovered.csv']

def prepare_data(source):
    data_raw = pd.read_csv(source)
    
    #if no province is given name the province 'country'
    data_raw['Province/State'] = data_raw['Province/State'].fillna(value='country')
    
    #create Multicolumn layer
    country_tuples = list(zip(data_raw['Country/Region'],data_raw['Province/State']))
    cols = pd.MultiIndex.from_tuples(country_tuples, names=['country', 'province'])
    
    #create datetime index
    dates = pd.to_datetime(data_raw.columns[4:],infer_datetime_format=True)
    df = pd.DataFrame(data_raw.iloc[:,4:].transpose().values, index=dates, columns=cols)
    return df

#prepare_data(csv_files[0])
