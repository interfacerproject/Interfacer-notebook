# Interfacer-notebook
A notebook-based tool/examples for GraphQL calls to the Interfacer back-end.  
This tool is written in Python and it is based on [Jupyter notebooks](https://jupyter.org/).

**NOTE**: at the moment you need some credentials to create users, so this software cannot run without an appropriate `.credentials.json` of the form:
```
{
    "key": "<secret key>"
}
```
# Introduction
This repository contains notebooks for several use cases: 
1. a [flow](https://github.com/interfacerproject/Interfacer-notebook/blob/main/isogowns.ipynb) defined during the [Reflow project](https://reflowproject.eu/) that focusses on making isolation gowns used in hospitals more circular. The use-case is described [here](https://reflowproject.eu/blog/the-development-of-circular-isolation-gowns-a-case-study/). The flow expressed according to Value Flows is represented by the following picture (taken from this [repo](https://github.com/reflow-project/Amsterdam-pilot/tree/main/graphviz)):
![Isolation Gowns Value Flows](/img/isogowns.png?raw=true "Isolation Gowns Value Flows")

    - The notebook implements a part of it which concerns the agents `hospital` and `Textile Company` (called the cleaner in the notebook).
2. a [flow](https://github.com/interfacerproject/Interfacer-notebook/blob/main/gownshirt.ipynb) defined in this [file](https://github.com/interfacerproject/Interfacer-notebook/blob/main/gownshirt_flow.1.1.txt).
3. a [flow](https://github.com/interfacerproject/Interfacer-notebook/blob/main/IFUsersFlows.ipynb) corresponding to the [Interfacer](https://www.interfacerproject.eu/) project's front-end [here](https://interfacer-gui-staging.dyne.org/).
4. a flow corresponding to the [Libre Solar](https://libre.solar/) project (in progress).

# Installation
We assume you have python 3 installed on your system. Here the step by step installation:

```
git clone <this repo>
cd <cloned dir>
```
It is better to create a virtual environment (for example with [miniconda](https://docs.conda.io/en/latest/miniconda.html)), but it is not obligatory, thus the next step is optional:
```
conda create -n <name of env> python==3.9
conda activate <name of env>
```
Note that we use python 3.9 but we have not tested the code with other versions, the code should work also with other versions.  

If you have chosen not to install a virtual environment, use `pip3` instead of `pip` in the following commands.  

Proceed to install jupyter notebook:
```
pip install notebook
#or pip3 install notebook if not using conda
```
 and the required packages:
 ```
 pip install requests
 pip install -U zenroom --pre
 pip install plotly
 # or pip3 install requests, pip3 install -U zenroom --pre and pip3 install plotly if not using conda
 
 ```
The latter will install the latest version of zenroom.
 
start jupyter notebook with:
```
jupyter notebook
```
(if jupyer is not on your path, try search for it in your home directory, for example `~/.local/bin/jupyter notebook`)  

A browser should open (or you should open it with the url indicated on the command line output).  
Jupyter notebook opens in the directory you launched it from.  
![Notebook homepage](/img/homepage.png?raw=true "Notebook homepage")  

Make sure you are in the Interfacer-notebook folder and click on `interfacer.ipynb` to open the notebook in another tab.  
![notebook](/img/notebook.png?raw=true "Notebook start of page")  

# Running the code
In one of the first cells of each use case you can customise the data for your users. Subsequently, the notebook creates some JSON files in order to store information about the users that has been created, the locations, the resource specifications and the units used to quantify the resources.

This information is stored separately per use case and per endpoint on disk with a folder structure like \<use-case\>/\<endpoint\>/\<file\>.json.

When run again, the notebook will reuse info from existing files, avoiding recreating users,units,locations and specs that already exist. It will therefore not overwrite existing files, so if you want to reset the conf files you need to delete them manually.
