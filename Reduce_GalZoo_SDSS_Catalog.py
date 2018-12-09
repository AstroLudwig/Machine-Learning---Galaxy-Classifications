# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    Reduce GalZoo SDSS Catalog
PURPOSE:
    Get Gold Sample as Described by Banerji 2010
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

# Load Combined Data From Galaxy Zoo and SDSS
mc = pd.read_csv("CombinedCatalog/MergedCatalog.csv")

# Remove Rows where none of the votes exceed 0.8

# if P_EL or P_CW or P_ACW or P_EDGE or P_DK or P_MG is not > .8, drop 
mc = mc.drop(mc[(mc.P_EL < 0.8) & (mc.P_CW < 0.8) & 
				(mc.P_ACW < 0.8) & (mc.P_EDGE < 0.8) & 
				(mc.P_DK < 0.8) & (mc.P_MG < 0.8)].index)

# Remove Mergers
mc = mc.drop(mc[mc.P_MG > 0.8].index)