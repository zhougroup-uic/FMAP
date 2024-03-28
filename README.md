# FMAPS(q)

FMAPS(q) is a code for calculating the structure factor, S(q), of a protein solution, by extending our fast Fourier transform-based modeling of atomistic protein-protein interactions (FMAP) approach. It takes the potential of mean force W(R) along the center-center distance of a pair of protein molecules and the protein diameter d as input. Both W(R) and d can be obtained from our [FMAPB2 web server](https://pipe.rcc.fsu.edu/fmapb2/).

We have implemented FMAPS(q) into a [FMAPSq web server](https://zhougroup-uic.github.io/FMAPSq/). 
The fmapsq.js file released here is a stand-alone for using in command line.


#### Usage

If you directly enter protein concentration in molarity (mM):

    $ nodejs fmapsq.js Bltz.txt diam qstrt qstep Nq Cmol

Alternatively, if you enter mass concentration (in mg/mL), then you need to also enter the protein molecular mass (in kDa):

    $ nodejs fmapsq.js Bltz.txt diam qstrt qstep Nq Cmas MW


#### References:

1. S. Qin and H.-X. Zhou (2019), Calculation of Second Virial Coefficients of Atomistic Proteins Using Fast Fourier Transform, J Phys Chem B 123,
    8203-8215.
2. S. Qin and H.-X. Zhou (2024), Calculating Structure Factors of Protein Solutions by Atomistic Modeling of Protein-Protein Interactions, [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.03.27.587040v1)
