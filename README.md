# Machine learning galaxy classifications
Recreating results from [Banerji, 2010](https://academic.oup.com/mnras/article/406/1/342/1073212) on classifying galaxies using machine learning. To be clear, most of the information below is from this paper. The focus of this project is to learn some machine learning techniques for the first time rather than to improve or alter the information in this paper.
## Download Data
### Galaxy Zoo
> The Galaxy Zoo catalogue that we use in this paper is the combined weighted sample of Lintott et al. (2008). This contains morphological classifications for 893,212 objects into four morphological classes – ellipticals, spirals, mergers and point sources/artefacts.  
  
This corresponds to table 2 and table 3 of the [Galaxy Zoo 1 Data Release](https://data.galaxyzoo.org/).  
Time permitting, I could try this methodology on the galaxy zoo 2 data release. 
  
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
This leaves me with 264,327 objects, which is somewhat close to the paper's gold sample of 315,000 objects.  
## Data Reduction
>[W]e apply cuts to our sample and remove objects that are not detected in the g, r and i bands and those that have spurious values and large errors for some of the other parameters used in this study ... We ... also remove the few well classified mergers with a fraction of vote of being a merger greater than 0.8 from the sample as we are not attempting to classify the mergers in this work.  
> This leads to a sample of ∼800 000 objects. Further cuts are then applied to define a gold sample where the fraction of vote for each object belonging to any one of three morphological classes – ellipticals, spirals and point sources/artefacts – is always greater than 0.8. This gold sample contains ∼315 000 objects and is essentially equivalent to the clean sample of Lintott et al. (2008). The neural network is run on the gold sample as well as the entire sample.  

Removing rows where no votes > 0.8 removed most non galaxy items but I did some more cuts looking for rows that had types equal to unknown, or to stars. I also removed spurious values = -9999. This left me with 264,044 objects remaining. I'm both impressed and confused how the authors managed to retain 315,000 objects. 
## Identify Parameters
### First Set
It is useful to define parameters that are independent of distance to the object. 
> ![Table](https://i.imgur.com/IV8KSlD.png)  
The colours are corrected for reddenning but not for redshift since that would reduce the sample. 
> The other parameters considered are the axial ratios and log likelihoods associated with both a de Vaucouleurs and an exponential fit to the two-dimensional galaxy image. The de Vaucouleurs profile is commonly used to describe the variation in surface brightness of an elliptical galaxy as a function of radius whereas the exponential profile is used to describe the disc component of a spiral galaxy. In addition, the log likelihood of the object being well fitted by a point spread function (PSF), lnLstar, helps in distinguishing extended galaxies from more point-like sources.
How parameters map to physical classifications:
> Different parameters allow us to distinguish between different morphological classes. As expected, early types are found to be redder than spirals whereas the point sources and artefacts have a wide range of colours. The axial ratio obtained from a de Vaucouleurs fit to the galaxy images is closer to unity for early type systems (typically ∼0.8) compared to spirals (typically ∼0.3) and has a bimodal distribution for the point sources and artefacts. The log likelihood associated with the de Vaucouleurs fit is also larger for the early types than the spirals and largest for the point sources and artefacts.
### Second Set
> ![Table2](https://i.imgur.com/PpDJenG.png)  
   The concentration is given by the ratios of radii containing 90 and 50 per cent of the Petrosian flux in a given band.  
   mRrCc is the second moment of the object intensity in the CCD row and column directions ![eq](https://latex.codecogs.com/gif.latex?\inline&space;mRrCc&space;=&space;\langle&space;y^2\rangle&space;&plus;&space;\langle&space;x^2\rangle) where ![eq](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Clangle%20y%5E2%5Crangle%20%3D%20%5Cfrac%7B%5Csum%20I%28y%2Cx%29w%28y%2Cx%29y%5E2%7D%7B%5Csum%20I%28y%2Cx%29w%28y%2Cx%29%29%7D)
## Train Neural Net 
### Software Resourcces
[ANNZ](https://arxiv.org/abs/astro-ph/0311058)  
[ANN](https://arxiv.org/abs/astro-ph/9503001)
### Cost function
> ![eq](https://latex.codecogs.com/gif.latex?\inline&space;E=\sum_k(T_{NN}(w_{ij},p_k)-T_{eye,k})^2)  
> T_NN is the neural network probability of the object belonging to a particular morphological type, p_k are the input parameters to the network and T eye,k are the fractional weighted votes in the training set in this case assigned by Galaxy Zoo users.  
> A training set is used to minimize the cost function wrt the free parameters w_ij
### Architecture 
> During the initial set-up, one has to specify the architecture of the neural network – the number of hidden layers and nodes in each hidden layer. We choose a neural network with two hidden layers with 2N nodes each, where N is the number of input parameters. The architecture of the network is therefore N:2N:2N:3. Note that increasing the number of nodes further either by adding nodes to existing hidden layers or by adding more hidden layers to the network does not result in any substantial improvement to the classifications.  
> The three nodes in the output layer give the probability of the galaxy being an early type, spiral and point source/artefact, respectively, between 0 and 1. Neural nets with this type of output are statistical Bayesian estimators and therefore the sum of all three outputs is roughly, although rarely, exactly equal to 1. 
> [T]his differs from the Galaxy Zoo fractional votes which always add up to exactly 1 over all four morphological classes – early types, spirals, point sources/artefacts and mergers. As mentioned earlier, the mergers are not classified by the neural network in this paper.
## Evaluate Results
# Bookmark
Stopped at describing the second set of parameters. 
