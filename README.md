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
This notebook implements a use-case defined during the [Reflow project](https://reflowproject.eu/) that focusses on making isolation gowns used in hospitals more circular. The use-case is described [here](https://reflowproject.eu/blog/the-development-of-circular-isolation-gowns-a-case-study/).  

The flow expressed according to Value Flows is represented by the following picture (taken from this [repo](https://github.com/reflow-project/Amsterdam-pilot/tree/main/graphviz)):
![Isolation Gowns Value Flows](/img/isolation_gowns.png?raw=true "Isolation Gowns Value Flows")

The notebook implements a part of it which concerns the agents `hospital` and `Textile Company` (called the cleaner in the notebook).

# Installation
Here the step by step installation:

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

Then proceed to install jupyter notebook:
```
pip install notebook
```
 and the required packages:
 ```
 pip install requests zenroom
 
 ```
 
start jupyter notebook with:
```
jupyter notebook
```
A browser should open (or you should open it with the url indicated on the command line output).  
Clicking on `interfacer.ipynb` will open the notebook in another tab.

# Running the code
The notebook reads some JSON files in order to have information about the users that need to be created, the locations, the resource specifications and the units used to quantify the resources. In the repo we provide template files called `*_example.json`.  

First, you should copy the file `cred_users_example.json` to `.cred_users.json` and edit it to change the data of your 2 users.  

Then you should copy or rename each example file to the same name without example:
```
cp cred_users_example.json .cred_users.json
cp loc_users_example.json loc_users.json
cp res_spec_data_example.json res_spec_data.json
cp units_data_example.json units_data.json
```

At this point you should be able to run all the notebook and inspect the data it generates.
