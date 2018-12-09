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
import astropy.units as u
import pandas as pd 

#############
# Functions #
#############

# Retrieve coordinates and compare
def check_coords(dataframe,index):
	# Get Galaxy Zoo Coordinates
	Ra = dataframe.loc[index]["RA"]
	Dec = dataframe.loc[index]["DEC"]

	# Create Sky Coordinate For Galaxy Zoo
	Coord = SkyCoord(Ra,Dec,unit=u.deg,frame="icrs")
	Ra = Coord.ra.value; Dec = Coord.dec.value

	# Get SDSS Coordinates
	ra = dataframe.loc[index]["ra"]
	dec = dataframe.loc[index]["dec"]
	
	# Create Sky Coordinate for SDSS
	coord = SkyCoord(ra,dec,unit=u.deg,frame="icrs")
	
	print(Coord)
	print(coord)

	Delta_ra = Ra - ra
	Delta_dec = Dec - dec 

	return Delta_ra, Delta_dec

########
# Main #
########

# The paper: https://academic.oup.com/mnras/article/406/1/342/1073212 

# Load Data From Galaxy Zoo
gz = pd.read_csv("GalaxyZoo/GalaxyZoo1_DR_table2.csv")

# Load Data From SDSS
dfs = [];
for i in range(0,10):
	dfs.append(pd.read_csv("SDSS/result_"+str(i)+".csv"))

# Add all the SDSS data together
sdss = pd.concat(dfs) 

# Insert Column of Object Names in Galaxy Zoo Catalog 
names = []
for i in range(len(gz)):
	names.append("A"+str(i))
gz.insert(0,"Name",names)

# Merge DataFrames
both = pd.merge(gz,sdss,on="Name")

# Compare Ra/Dec coordinates to make sure this was done correctly
DelRA, DelDEC = check_coords(both,0)

# Something's a little off with the coordinates
# Dec is fine but ra is strange. I ruled out it being an issue of 
# converting to radian. 

# The object ID's are the same, I think it's possible SDSS
# Is using a weird coordinate scheme like great circles
# and that's the issue. They have IDL functions to convert
# between great circle and celestial but I'm not sure what the eq for that is
# to put in python.

# Here are some links that may help with this 
# http://www.astropy.org/astropy-tutorials/Coordinates.html
# http://www.sdss3.org/svn/repo/idlutils/tags/v5_5_5/pro/coord/munu_to_radec.pro
# http://www.sdss3.org/dr8/algorithms/surveycoords.php

# Since the object id's match and Aladdin has no problem finding 
# objects in SDSS filter with GALZOO coordinates, I'm going to move on. 

# Save our new dataframe
both.to_csv("CombinedCatalog/MergedCatalog.csv",index=False)

