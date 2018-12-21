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
  
Rather than using distances, we can use the ratio of the radii to understand how concentrated the sources are. The radii is measured to contain some percent of the flux in a given band. The other parameters are variations of moments of object intensity on the detector.    
## Train Neural Net 
### Software Resourcces
To create the neural net, I used Sci-Kit learn on the advice of Dr. Renée Hložek. Sci-Kit learn comes with the anaconda installation and was happily already on my computer. Specifically, I used the [MLPClassifier](https://scikit-learn.org/stable/modules/neural_networks_supervised.html#classification) which 'implements a multi-layer perceptron (MLP) algorithm that trains using Backpropagation.'
### Multi Layer Perceptron Classifier
This is a type of neural net considered to be feed forward as the layers do not circle back to each other. The simplest, most "vanilla", neural network you can have is an input layer, one hidden layer, and an output layer. The weights of the parameters are calculated by the neural net using back propagation which is shorthand for backward propagation of errors since the errors are computed at the output and distributed backwards throughout the network's layers. These errors are optimized using a solver. I used a solver called ["Adam"](https://arxiv.org/pdf/1412.6980.pdf) which is a stochastic gradient based optimizer that works really well for giant data sets. I tried other solvers as well such as "lbfgs" which converges quickly and is similar to the Newton method but gave me poor results. 
### Architecture N:2N:2N:3   
I use 11 parameters as opposed to Banerji who uses 12. This means that I additionally have 2 hidden layers, each with 22 neurons, and 3 output neurons. 
## Evaluate Results
In comparing my results to Banerji I achieve accuracies listed in the table below.

![Table3](https://github.com/AstroLudwig/machine-learning-galaxy/blob/master/Results/Results_Accuracy.png?raw=true)

In probing the probability that the galactic classification is correct, it seems that for the types that are or are not correct, the neural net is very confident of their type. There are galaxies that fall within confidences of 20 - 80 % but they are comparatively quite small in number. Although I am very happy with my results, I wanted to see why the net is so sure that galaxies are a different type than how they've been classified by online users. Below are images of 2 galaxies I checked at random that the net was wrong about. I did not check all of the incorrectly labeled galaxies but I immediately found some interesting things. 

![WrongGalaxies](https://github.com/AstroLudwig/machine-learning-galaxy/blob/master/Results/WronglyClassifiedGalaxies.png?raw=true)

The image on the left appears, to me (a non expert), to be a blue elliptical. As blue ellipticals seemed to evade astronomers prior to Galaxy Zoo I think it's fair that it managed to also evade my neural net. The image on the right seems to have a bright spot within the galaxy (possibly a dwarf galaxy? supernova? foreground star? merger?). Since we measure the concentration as the ratio of radii (which I believe are measured by how much light they contain) it makes sense to me that the petroR90_i/petroR50_i parameter could have been misleading. These were the first two wrongly labeled galaxies I looked at. It would definitely be interesting to probe this further and see what strategies could be employed to account for various artefacts.
## Future Work
* Given time it would definitely be interesting to see how this machinery would stand against the entire data set, as opposed to the reduced. It would also be interesting to apply it to more recent data releases.  

* With many amazing surveys coming online it would be useful to match these objects to other catalogs and correct for redshift and also include distances in the parameters.  

* This has been my first step in machine learning, I am definitely excited to try out various architectures, solvers, and techniques in the future!  
