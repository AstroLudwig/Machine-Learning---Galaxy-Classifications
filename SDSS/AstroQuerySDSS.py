import numpy as np 
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astroquery.sdss import SDSS
import astropy.units as u
import pandas as pd 
import json
### Open GAl ZOO data frame and get coordinates
# How much data
start = 1000; stop = 1002
# Load Data
df = pd.read_csv("../GalaxyZoo/GalaxyZoo1_DR_table2.csv")
ra = df["RA"].iloc[start:stop]
dec = df["DEC"].iloc[start:stop]
# Get Sky Coordinate
coordinates = SkyCoord(ra,dec,unit=u.deg,frame="icrs")
# Save File
header = ["Names","Ra","Dec"]
names = []
for i in range(stop-start):
	names.append("A"+str(i))
Dict = {"Name":names,"RA":coordinates.ra.value,"DEC":coordinates.dec.value}
#np.savetxt("FirstThousand.txt",[names,coordinates.ra.value,coordinates.dec.value],fmt="{:0.4f} {:0.4f}", header="\t".join(header),delimiter="\t")
df = pd.DataFrame(data=Dict)
df.to_csv("Hope.txt",sep='\t',index=False)
print(df.head())
# Find the region in sdss with astroquery
#xid = SDSS.query_region(coordinates)#,radius=2*u.arcsecond,photoobj_fields=[type],data_release=7)
# Table list 
# https://skyserver.sdss.org/dr12/en/help/browser/browser.aspx?cmd=description+PhotoObjAll+U#&&history=description+PhotoObjAll+U
#xid = SDSS.query_region(coordinates,photoobj_fields=["dered_g","dered_r","dered_i","deVAB_i","expAB_i","lnLExp_i","lnLExp_i","lnLDeV_i","lnLStar_i"])
