# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    Convert Galaxy Zoo Coordinates
PURPOSE:
    SDSS Needs a list of ra/dec coordinates in degrees to pull the right table. 
"""
import numpy as np 
import pandas as pd 
from astropy import units as u
from astropy.coordinates import SkyCoord

# Conversion Functions
# I'm not gonna use these, but I'll leave them here for future reference. 
def RA_to_Decimal(hour,minute,second):
	return 15 * (hour+minute/60+second/3600)
def DEC_to_Decimal(deg,minute,second):
	return np.sign(deg)*(np.abs(deg)+minute/60+second/3600)
# Convert using sky coord because Astropy is probably safer than me.
def convert(dataframe):
	ra_string = []; dec_string = []
	for i in range(len(dataframe)):
		h,m,s = dataframe["RA"][i].split(":")
		D,M,S = dataframe["DEC"][i].split(":")
		ra_string.append(h+'h'+m+'m'+s+'s')
		dec_string.append(D+'d'+M+'m'+S+'s')
	coord = SkyCoord(ra_string,dec_string,frame='icrs')
	ra_deg = coord.ra.value
	dec_deg = coord.dec.value
	return ra_deg,dec_deg

# Load Data
df_1 = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table2.csv")
df_2 = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table3.csv")	

# Save Coordinates
np.savetxt("../GalaxyZoo/GalaxyZoo1_DR_table2_coordinates.txt",convert(df_1))
np.savetxt("../GalaxyZoo/GalaxyZoo1_DR_table3_coordinates.txt",convert(df_2))
