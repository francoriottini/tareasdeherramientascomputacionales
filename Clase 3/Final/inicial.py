# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:01:32 2022

@author: Franco
"""

from wwo_hist import retrieve_hist_data

#### Set working directory to store output csv file(s)
import os
os.chdir("C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 3/Data")


#### Example code
frequency=24
start_date = '01-JAN-2015'
end_date = '31-DEC-2015'
api_key = '35b7a88fa68046849a6210511221107'
location_list = ['20637', '20653','20688','20742','20871','21040',
                 '21043','21158','21220','21240','21502','21601',
                 '21638','21639','21643','21651','21701','21742',
                 '21804','21811','21853','21902']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)