# FMAPB2

FMAPB2 implements FMAP, a method based on fast Fourier transform (FFT), to calculate second virial coefficients (B2) for proteins represented at the all-atom level in implicit solvent. FMAP stands for FFT-based Modeling of Atomistic Protein-protein interactions. In FMAPB2, we express terms of the protein-protein inteaction energy as correlation functions, and evaluate them by FFT. These terms include steric repulsion, nonpolar attraction (in the form of a Lennard-Jones potential), and electrostatic interactions (in the form of a Debye-Hückel potential).

The input to FMAPB2 is the structure of the protein, in PQR format. The user also sets the solvent condition, including ionic strength (ionc, in M) and temperature (temp, in celcius).

We have implemented FMAPB2 into a [FMAPB2 web server](https://pipe.rcc.fsu.edu/fmapb2/). The FMAPB2 package released here is a stand-alone version for using in command line.

### Requirements
FFTW3, OPENMP, python2, and numpy are required; gnuplot and ghostscript are optional for graphics.

* For Centos 7

    $ yum -y install fftw-libs-double libgomp python2 python2-numpy gnuplot ghostscript

* For ubuntu 18.04

    $ apt-get -y install libfftw3-double3 python python-numpy gnuplot ghostscript
    
### Usage and example

#### Usage

    $ [dir/]fmapb2 pro.pqr ionc temp [nthrd]

### run directly in Linux

To reproduce the values in parms.txt.bak in example, go to example directory

    $ cd example
    $ ../fmapb2 subA.pqr 0.1 25
    $ diff parms.txt parms.txt.bak

Use a web browser to open the index.html to show a similar page as in the web sever.

### run with apptainer/singularity

#### prepare fmapsys image file using fmapsys.def for centos 7 or fmapsys.ubuntu18.def for ubuntu 18.04

    $ apptainer build --fakeroot fmapsys.sif fmapsys.def

#### run in example directory

    $ cd example
    $ apptainer exec ../fmapsys.sif ../fmapb2 subA.pqr 0.1 25

#### References:

* S. Qin and H.-X. Zhou (2019), Calculation of second virial coefficients of atomistic proteins using fast Fourier transform. J. Phys. Chem. B 123, 8203-8215.
* S. Qin and H.-X. Zhou (2024), Calculating Structure Factors of Protein Solutions by Atomistic Modeling of Protein-Protein Interactions, [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.03.27.587040v1).
* S. Qin and H.-X. Zhou (2014), Further development of the FFT-based method for atomistic modeling of protein folding and binding under crowding: optimization of accuracy and speed, J. Chem. Theory Comput. 10, 2824-2835
