# FMAPS(q)

FMAPS(q) is a code for calculating the structure factor, S(q), of a protein solution, by extending our fast Fourier transform-based modeling of atomistic protein-protein interactions (FMAP) approach. It takes the potential of mean force W(R) along the center-center distance of a pair of protein molecules and the protein diameter d as input. Both W(R) and d can be obtained from our [FMAPB2 web server](https://pipe.rcc.fsu.edu/fmapb2/).

We have implemented FMAPS(q) into a [FMAPSq web server](https://zhougroup-uic.github.io/FMAPSq/). 
The fmapsq.js file is a stand-alone versions of FMAPS(q) for using in command line.


#### Usage

    nodejs fmapsq.js Bltz.txt diam qstrt qstep Nq Cmol

    nodejs fmapsq.js Bltz.txt diam qstrt qstep Nq Cmas MW

#### References:

* S. Qin and H.-X. Zhou (2019), Calculation of Second Virial Coefficients of
    Atomistic Proteins Using Fast Fourier Transform, J Phys Chem B 123,
    8203-8215.
* S. Qin and H.-X. Zhou (2024), Calculating Structure Factors of Protein
    Solutions by Atomistic Modeling of Protein-Protein Interactions, [biorxiv](https://www.biorxiv.org/content/10.1101/2024.03.27.587040v1)
