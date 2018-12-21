# -*- Copyright (c) 2018, Bethany Ann Ludwig, All rights reserved. -*-
"""
NAME:
    Match GalZoo to SDSS
PURPOSE:
    Combine and Reduce Galaxy Zoo Data. Upload to CASJOBS. Merge with SDSS Data
NOTE: 
	I found the more efficient SQL method because I had to. Download 10,000 objects and then 
	reducing gives me 37 objects. :) So I figured out how to use CAS JOBS and I'm going to 
	reduce that data and match by cross id.    
"""
import numpy as np 
from astropy.io import fits
from astropy.coordinates import SkyCoord
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
  p.objID, 
  p.ra, 
  p.dec, 
  p.run, 
  p.field,
  dbo.fPhotoTypeN(p.type) as type,
  p.dered_g, 
  p.dered_r, 
  p.dered_i, 
  p.deVAB_i, 
  p.expAB_i,
  p.lnLExp_i, 
  p.lnLDeV_i, 
  p.lnLStar_i, 
  p.petroR90_i, 
  p.petroR50_i,
  p.mRrCc_i, 
  p.mCr4_i,
  p.texture_i
INTO mydb.MatchedByOBJID
FROM mydb.FullOBJID as o
JOIN PhotoObjAll AS p ON p.objid=o.objid
"""
############
# Switches #
############

phase_1 = False # Merges Galaxy Zoo Table 2 and 3, Reduces, Saves
phase_2 = False # Combines Galaxy Zoo Reduced Table with Object ID Matched SDSS Catalog
phase_3 = True  # Reduces to only what's absolutely required for machine learning code
#######################
# Galaxy Zoo Handling #
#######################
# Once this phase is complete, upload object ids to casjobs, download sdss info, load into phase 2 and merge. 
if phase_1:
	# Load Galaxy Zoo Data, Join Tables
	gz2 = pd.read_csv("GalaxyZoo/GalaxyZoo1_DR_table2.csv")
	gz3 = pd.read_csv("GalaxyZoo/GalaxyZoo1_DR_table3.csv")
	gz = pd.concat([gz2,gz3],axis=0, join='outer', ignore_index=True,sort=False)

	# Remove rows where none of the votes exceed 0.8
	gz = gz.drop(gz[(gz.P_EL < 0.8) & (gz.P_CW < 0.8) & 
	 				(gz.P_ACW < 0.8) & (gz.P_EDGE < 0.8) & 
	 				(gz.P_DK < 0.8) & (gz.P_MG < 0.8)].index)

	# Remove mergers
	gz = gz.drop(gz[gz.P_MG > 0.8].index)

	# Seperate out Object Ids
	OBJID = gz[["OBJID"]].copy()

	# Convert to strings
	OBJID["OBJID"] = OBJID["OBJID"].apply(lambda x: '{:d}'.format(x))

	# Save as it's own dataframe, this is uploaded to casjobs
	OBJID.to_csv("GalaxyZoo/GalaxyZoo_Table2And3_Reduced_ObjectID_Only.csv",index=False)
	print(("Galaxy Zoo Reduced Catalog {} Object IDs Saved.").format(OBJID.shape[0]))

	# Save Catalog
	gz.to_csv("GalaxyZoo/GalaxyZoo_Table2And3_Reduced.csv",index=False)

##############################
# Galaxy Zoo and SDSS Merger #	
##############################
if phase_2:
	# Load Reduced Galaxy Zoo Data
	gz = pd.read_csv("GalaxyZoo/GalaxyZoo_Table2And3_Reduced.csv")
	sdss = pd.read_csv("SDSS/MatchedByOBJID_AstroLudwig.csv")

	# Rename objid to match
	sdss = sdss.rename(columns={"objID":"OBJID"})

	# Merge both tables
	FinalCatalog = pd.merge(gz,sdss,on="OBJID")

	# More Data Reduction, Remove anything that is not a galaxy
	FinalCatalog = FinalCatalog.drop(FinalCatalog[(FinalCatalog.type == "STAR") | (FinalCatalog.type == "UNKNOWN")].index)
	# Remove any spurious Values, -9999
	FinalCatalog = FinalCatalog[FinalCatalog != -9999]
	# Save 
	FinalCatalog.to_csv("CombinedCatalog/Merged_Reduced_SDSS_GZ_Catalog.csv",index=False)

	print(("Catalogs Merged {} Objects Saved.").format(FinalCatalog.shape[0]))

#######################
# Strip For Training  #	
#######################	
# Create simplistic case where we just use spiral, elliptical, and uncertain votes of 1 or 0.
if phase_3: 
	# Load Merged Catalog 
	FC = pd.read_csv("CombinedCatalog/Merged_Reduced_SDSS_GZ_Catalog.csv")
	# Drop everything we're not feeding into the machine.
	FC = FC.drop(labels=["RA","DEC","P_CW","P_ACW","P_EDGE",
						  "P_MG","P_EL_DEBIASED","P_CS_DEBIASED",
						  "run","field","type","UNCERTAIN","ELLIPTICAL","SPIRAL"],axis=1)
	# Only keep bright objects to try to even out what types are left
	FC = FC.drop(FC[FC.dered_r > 16].index)
	# Create Color Columns
	FC["dered_g-dered_r"] = FC["dered_g"] - FC["dered_r"]
	FC["dered_r-dered_i"] = FC["dered_r"] - FC["dered_i"]
	# Create Distance Ratios
	FC["petroR90_i/petroR50_i"] = FC["petroR90_i"] / FC["petroR50_i"]
	
	# Combine types into a single column with 
	# 0 = Unknown/Artefact/PointSource, 1 = Elliptical, 2 = Spiral
	def f(row):
		probability = [row["P_DK"],row["P_EL"],row["P_CS"]]
		if row["P_DK"] == np.max(probability):
			val = 0
		elif row["P_EL"] == np.max(probability):
			val = 1
		elif row["P_CS"] == np.max(probability):
			val = 2 
		return val
	FC["type"] = FC.apply(f,axis=1)

	# Drop more columns
	FC = FC.drop(labels=["dered_g","dered_r","dered_i","petroR90_i","petroR50_i",
						  "P_DK","P_EL","P_CS"],axis=1)
	# Reorder 
	FC = FC[['OBJID', 'ra', 'dec', 'NVOTE', 'type','deVAB_i', 'expAB_i', 'lnLExp_i', 'lnLDeV_i', 'lnLStar_i', 'mRrCc_i', 'mCr4_i', 'texture_i', 'dered_g-dered_r', 'dered_r-dered_i', 'petroR90_i/petroR50_i']]

	# Remove Nan's or missing data
	FC = FC.dropna(axis=0,how='any')
	print(("{} Objects Saved").format(FC.shape[0]))
	# SAVE 
	FC.to_csv("ML_Ready_Catalog.csv",index=False)
