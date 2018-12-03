# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    Convert Galaxy Zoo Coordinates
PURPOSE:
    SDSS Needs a list of ra/dec coordinates in degrees to pull the right table. 
"""
import numpy as np 
import pandas as pd 

# Converstion Functions
def RA_to_Decimal(hour,minute,second):
	return 15 * (hour+minute/60+second/3600)
def DEC_to_Decimal(deg,minute,second):
	return deg+minute/60+second/3600

# Load Data
df_1 = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table2.csv")
df_2 = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table3.csv")	

# Split hms 
split_ra = df_1["RA"].str.split(":")
split_dec = df_1["RA"].str.split(":")

# Convert and store
ra_deg = []; dec_deg = []
for i in range(len(split_ra)):
	ra_deg.append(RA_to_Decimal(float(split_ra[i][0]),float(split_ra[i][1]),float(split_ra[i][2])))
	dec_deg.append(DEC_to_Decimal(float(split_dec[i][0]),float(split_dec[i][1]),float(split_dec[i][2])))