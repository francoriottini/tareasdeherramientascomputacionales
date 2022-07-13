# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:52:22 2022

@author: Franco
"""

#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import os
os.chdir("/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 3/Data/Crimen")

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("odn.data.socrata.com", None)

# Example authenticated client (needed for non-public datasets):
client = Socrata("odn.data.socrata.com",
                  "nColKKrqJghxr2dgibNZm6W49",
                  username = "seminarioseconomia@udesa.edu.ar",
                  password="EconUdesa2020+")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("tt5s-y5fc", limit=100000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.to_csv('crime.csv', header = True, index = False)