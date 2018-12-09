# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    GalZoo to SDSS
PURPOSE:
    Transform RanDec coordinates from h:m:s to decimal and save in order to upload them to SDSS
    and retrieve cross matched Galaxy Zoo and SDSS data.  
NOTE: 
    I downloaded the sdss data by hand using a web interface sql search.
    There is likely a more efficient method out there but I was running into
    indecipherable error messages with astroquery. Future Bethany will want to 
    learn how to automate sql queries.         
"""
import numpy as np 
from astropy.io import fits
from astropy.coordinates import SkyCoord
#from astroquery.sdss import SDSS
import astropy.units as u
import pandas as pd 

# The paper: https://academic.oup.com/mnras/article/406/1/342/1073212 
# SDSS: http://skyserver.sdss.org/dr7/en/tools/crossid/crossid.asp

# Desired Fields:    p.dered_g, p.dered_r, p.dered_i, p.deVAB_i, p.expAB_i,
#					 p.lnLExp_i, p.lnLDeV_i, p.lnLStar_i, p.petroR90_i, p.petroR50_i,
#					 p.mRrCc_i, p.mCr4_i, p.texture_i
# Note: I did not include p.aE_i because it doesn't exist in the table.
# It may be possible to calculate it from other parameters but since
# We already have so many nodes/parameters, I neglected it. 

""" SQL COMMAND:
SELECT 
   p.objID, p.ra, p.dec, p.run, p.rerun, p.camcol, p.field,
   dbo.fPhotoTypeN(p.type) as type,
   p.dered_g, p.dered_r, p.dered_i, p.deVAB_i, p.expAB_i,
   p.lnLExp_i, p.lnLDeV_i, p.lnLStar_i, p.petroR90_i, p.petroR50_i,
   p.mRrCc_i, p.mCr4_i, p.texture_i
FROM #x x, #upload u, PhotoObjAll p
WHERE u.up_id = x.up_id and x.objID=p.objID and dbo.fPhotoTypeN(p.type)="galaxy"
ORDER BY x.up_id
"""
# Load Data
df = pd.read_csv("GalaxyZoo/GalaxyZoo1_DR_table2.csv")

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
# SQL will only let me upload 1000 coordinates at a time before crashing
# Saving text files to upload manually at the SDSS link above.
for i in range(0,10000,1000):
	# Create Dictionary 
	coordinates,names = get_coords(df,i,i+1000)
	Dict = {"Name":names,"RA":coordinates.ra.value,"DEC":coordinates.dec.value}
	new_df = pd.DataFrame(data=Dict)
	# Dictionary columns are not explicitly ordered and have to be reordered
	new_df = new_df[["Name","RA","DEC"]]
	
	# Save File
	new_df.to_csv("GalaxyZoo/DecimalCoordinates/Decimal_Coordinates_1000increment_"+str(i)+".txt",sep='\t',index=False)

# Save everything in one file to try to use with CASJOBS
allC, allN = get_coords(df,0,df.shape[0])
allDict = {"RA":allC.ra.value,"DEC":allC.dec.value}
all_df = pd.DataFrame(data=allDict)
all_df = all_df[["RA","DEC"]]
all_df.to_csv("GalaxyZoo/DecimalCoordinates/Decimal_Coordinates_Table2_NoName.csv",index=False)