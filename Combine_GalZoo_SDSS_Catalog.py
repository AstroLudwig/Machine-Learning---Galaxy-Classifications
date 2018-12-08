# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    Combine GalZoo SDSS Catalog
PURPOSE:
    Take all the newly aquired data and put it in one spread sheet.
NOTE: 
      
"""
import numpy as np 
from astropy.io import fits
from astropy.coordinates import SkyCoord
#from astroquery.sdss import SDSS
import astropy.units as u
import pandas as pd 

# The paper: https://academic.oup.com/mnras/article/406/1/342/1073212 

# Load Data From Galaxy Zoo
df_GZ = pd.read_csv("GalaxyZoo/GalaxyZoo1_DR_table2.csv")
# Load Data From SDSS
dfs = [];
for i in range(0,10):
	dfs.append(pd.read_csv("SDSS/result_"+str(i)+".csv"))

# Insert Column of Object Names in Galaxy Zoo Catalog 
names = []
for i in range(len(df_GZ)):
	names.append("A"+str(i))
df_GZ.insert(0,"Name",names)

# Go through each name, check to see if it is the SDSS catalog
# If it is, add to dictionary
for i in range(len(names)):
	if len(dfs[0][dfs[0]["Name"].str.match("A"+str(i))].shape) == 1:
		# STOPPED HERE 
		
# Retrieve coordinates and dummy name in some increment
def get_coords(dataframe,start,stop):
	ra = df["RA"].iloc[start:stop]
	dec = df["DEC"].iloc[start:stop]

	# Get Sky Coordinate
	coordinates = SkyCoord(ra,dec,unit=u.deg,frame="icrs")

	names = []
	# Dummy Names
	for i in range(start,stop):
		names.append("A"+str(i))

	return coordinates, names


