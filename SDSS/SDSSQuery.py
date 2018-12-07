# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    SDSS Query
PURPOSE:
    Pull photoobj all data from DR7 
"""
import numpy as np 
import pandas as pd 
from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.sdss import SDSS


# Get sky coordinates from data frame
# Including stop feature since there's so much data
def GetCoord(dataframe,stop):
	return SkyCoord(dataframe["RA"].iloc[0:stop],dataframe["DEC"].iloc[0:stop],unit=(u.deg),frame='icrs')
def GetImgs(dataframe,stop):
	for i in range(stop):
		region = SDSS.query_region(GetCoord(dataframe,stop))
		SDSS.get_photoobj(matches=region)
	return 
# Load Data
df_1 = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table2.csv")
df_2 = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table3.csv")	

