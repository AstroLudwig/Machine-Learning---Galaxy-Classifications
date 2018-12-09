# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    GalZoo to SDSS
PURPOSE:
    
NOTE: 
	I found the more efficient SQL method because I had to. Download 10,000 objects and then 
	reducing gives me 37 objects. :) So I figured out how to use CAS JOBS and I'm going to 
	reduce that data and match by cross id.    
"""
import numpy as np 
from astropy.io import fits
from astropy.coordinates import SkyCoord
#from astroquery.sdss import SDSS
import astropy.units as u
import pandas as pd 

# The paper: https://academic.oup.com/mnras/article/406/1/342/1073212 
# SDSS: CASJOB
# GALAXY ZOO: https://data.galaxyzoo.org/ Table 2

# Desired Fields:    p.dered_g, p.dered_r, p.dered_i, p.deVAB_i, p.expAB_i,
#					 p.lnLExp_i, p.lnLDeV_i, p.lnLStar_i, p.petroR90_i, p.petroR50_i,
#					 p.mRrCc_i, p.sdssr4_i, p.texture_i
# Note: I did not include p.aE_i because it doesn't exist in the table.
# It may be possible to calculate it from other parameters but since
# We already have so many nodes/parameters, I neglected it. 

""" SQL COMMAND:
SELECT 
   p.objID, p.ra, p.dec, p.run, p.rerun, p.casdssol, p.field,
   dbo.fPhotoTypeN(p.type) as type,
   p.dered_g, p.dered_r, p.dered_i, p.deVAB_i, p.expAB_i,
   p.lnLExp_i, p.lnLDeV_i, p.lnLStar_i, p.petroR90_i, p.petroR50_i,
   p.mRrCc_i, p.sdssr4_i, p.texture_i into mydb.MyTable_0 from MyDB.MyTable AS m
CROSS APPLY dbo.fGetNearestObjEq( m.ra, m.dec, 0.5) AS n
JOIN PhotoObjAll AS p ON n.objid=p.objid
"""
# Load Data
gz = pd.read_csv("GalaxyZoo/GalaxyZoo1_DR_table2.csv")
sdss = pd.read_csv("SDSS/Table2CasJob.csv")

# Remove stars from sdss table
sdss = sdss.drop(sdss[sdss.type == "STAR"].index)

# Remove rows where none of the votes exceed 0.8
gz = gz.drop(gz[(gz.P_EL < 0.8) & (gz.P_CW < 0.8) & 
 				(gz.P_ACW < 0.8) & (gz.P_EDGE < 0.8) & 
 				(gz.P_DK < 0.8) & (gz.P_MG < 0.8)].index)
# Remove mergers
gz = gz.drop(gz[gz.P_MG > 0.8].index)

## Merge the data based on object id
# Rename objID to OBJID so both have the same key
sdss = sdss.rename(index=str,columns={"objID":"OBJID"})

catalog = pd.merge(sdss,gz,on="OBJID")