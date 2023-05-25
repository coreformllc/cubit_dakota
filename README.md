## Prerequisites
### Python
* Tested on Python 3.10
* Required modules
    * numpy
### DAKOTA
* Tested on Dakota 6.18
* Install binary for your distribution from 
    * https://github.com/snl-dakota/dakota/releases/tag/v6.18.0
### SEACAS - Exodus
* Clone the SEACAS repository
* Follow instructions for building Exodus from
    * https://github.com/sandialabs/seacas#exodus
* After installation, determine the location of `exodus.py` (not `exodus.py.in`) as you will need to specify this path in the Python scripts to be able to use this module.
### Cubit
* Tested on Coreform Cubit 2023.4
* Download installer for your system from 
    * https://coreform.com/products/downloads/#Coreform-Cubit
* After installation, determine the location of your Cubit installation's `bin` subdirectory as you will need to specify this path in the Python scripts to be able to use the Cubit-Python functionality.
### MOOSE
* Follow instructions from:
    * https://mooseframework.inl.gov/getting_started/installation/index.html
### ParaView (optional for visualization)
* Download installer for your system from
    * https://www.paraview.org/download/