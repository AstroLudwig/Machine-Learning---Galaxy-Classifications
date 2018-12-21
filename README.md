# Machine learning galaxy classifications
This project was done as a requirement of the graduate Cosmology 2018 course with Dr. Renée Hložek. In it, I
recreate the results from [Banerji, 2010](https://academic.oup.com/mnras/article/406/1/342/1073212) (here after Banerji) on classifying galaxies using machine learning techniques. I follow their strategies for data reduction but may be using different packages and solvers. My goal is to learn some machine learning techniques and experiment with a very cool data set.

## Code
#### Data_Acquisition.py
Aquire, reduce, and combine the data sets.
#### Machine_Learning.py
Create a neural net to classify galaxies.
## Download Data
### Galaxy Zoo
> The Galaxy Zoo catalogue that we use in this paper is the combined weighted sample of [Lintott et al. (2008)](http://adsabs.harvard.edu/abs/2008MNRAS.389.1179L). This contains morphological classifications for 893,212 objects into four morphological classes – ellipticals, spirals, mergers and point sources/artefacts.  
  
This corresponds to table 2 and table 3 of the [Galaxy Zoo 1 Data Release](https://data.galaxyzoo.org/).  
This data set is very straight forward to download. Table 2 has 667,944 galaxies; Table 3 has 225,269 galaxies. The table contains the SDSS object id, the equatorial coordinates, the number of votes and the percent of votes that went to a particular category of galaxy including elliptical, clockwise spiral, anticlockwise spiral, edge on spiral galaxy, don't know, merger, or combined spirals. The catalogs and reduced versions can be found in the Galaxy Zoo folder of this repository. 
  
### SDSS
> We match the Galaxy Zoo catalogue to the SDSS DR7 PhotoObjAll catalogue in order to obtain input parameters for the neural
network code 

To download this data I used an SQL Search with [CasJobs](https://skyserver.sdss.org/casjobs/). You have to create an account to use this tool. After combining table 2 and 3 from galaxy zoo, and doing some minor reduction (removing things without a consensus on galactic morphology, i.e. no vote column had a value higher than 0.8) I uploaded a csv of object ids as strings (it wont work if the csv transforms the 18 digit number to scientific notation!).  
This is the SQL search I wrote for this:  
```
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
```  
## Data Reduction
Banerji defines a gold sample of galaxies to train their net on and I decided to follow along and make the same cuts that they did. I removed all potential galactic mergers and galaxies without a consensus (vote fraction < 0.8). I removed rows that did not have all of the parameters or had spurious values (=-9999). I removed objects that were categorized as stars by SDSS. I removed objects that had an apparent magnitude in the corrected R band greater than 16 mag.

Banerji's gold sample contained 315,000 objects. After my initial data reduction of galaxy zoo data I have 264,327 objects. After matching these objects by object id to SDSS's PhotoObjAll DR7 catalog and making further reductions I have 50,753 objects. The combined and reduced data set is labeled ML_Ready_Catalog.csv.   
## Identify Parameters
### First Set
Because we do not have distances to all of our sources, and to avoid making further cuts, Banerji defines parameters that are correlated with galactic type but that do not dependence on distance, such as color, smoothness, or ratio of radii. Similarly, while the magnitudes have been corrected for dust reddening, they have not been corrected for redshift.
> ![Table](https://i.imgur.com/IV8KSlD.png) 
  
Color is used because ellipticals tend to be redder and spirals more blue. However, this isn't necessarily always true. In fact it was discovered using galaxy zoo data that blue ellipticals and red spirals [exist](http://adsabs.harvard.edu/abs/2013MNRAS.432..359T).  
Other parameters in the first set include the de Vaucouleurs profile and the exponential profile which map to elliptical and spiral galaxies, respectively. Both by describing their light profiles.
### Second Set
> ![Table2](https://i.imgur.com/PpDJenG.png)  
   The concentration is given by the ratios of radii containing 90 and 50 per cent of the Petrosian flux in a given band.  
   mRrCc is the second moment of the object intensity in the CCD row and column directions 
## Train Neural Net 
### Software Resourcces
To create the neural net, I used Sci-Kit learn on the advice of Dr. Renée Hložek. Sci-Kit learn comes with the anaconda installation and was happily already on my computer. Specifically, I used the [MLPClassifier](https://scikit-learn.org/stable/modules/neural_networks_supervised.html#classification) which 'implements a multi-layer perceptron (MLP) algorithm that trains using Backpropagation.'
### Architecture 
> The architecture of the network is therefore N:2N:2N:3.  
  
Keeping with this scheme, I had 11 parameters so I used 22 by 22 hidden layers.

## Evaluate Results

