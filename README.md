<!--
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (C) 2022-2023 Dyne.org foundation <foundation@dyne.org>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

# Interfacer-notebook

### Rapid prototyping data modeling for Zenflows

A notebook-based tool/examples for GraphQL calls to the Interfacer back-end.  
This tool is written in Python and it is based on [Jupyter notebooks](https://jupyter.org/).

</div>

<p align="center">
  <a href="https://dyne.org">
    <img src="https://files.dyne.org/software_by_dyne.png" width="170">
  </a>
</p>

## Building the digital infrastructure for Fab Cities

<br>
<a href="https://www.interfacerproject.eu/">
  <img alt="Interfacer project" src="https://dyne.org/images/projects/Interfacer_logo_color.png" width="350" />
</a>
<br>

### What is **INTERFACER?**

The goal of the INTERFACER project is to build the open-source digital infrastructure for Fab Cities.

Our vision is to promote a green, resilient, and digitally-based mode of production and consumption that enables the greatest possible sovereignty, empowerment and participation of citizens all over the world.
We want to help Fab Cities to produce everything they consume by 2054 on the basis of collaboratively developed and globally shared data in the commons.

To know more [DOWNLOAD THE WHITEPAPER](https://www.interfacerproject.eu/assets/news/whitepaper/IF-WhitePaper_DigitalInfrastructureForFabCities.pdf)

## Interfacer-notebook Features

This repository contains notebooks for several use cases:

1.  a [flow](https://github.com/interfacerproject/Interfacer-notebook/blob/main/isogowns.ipynb) defined during the [Reflow project](https://reflowproject.eu/) that focusses on making isolation gowns used in hospitals more circular. The use-case is described [here](https://reflowproject.eu/blog/the-development-of-circular-isolation-gowns-a-case-study/). The flow expressed according to Value Flows is represented by the following picture (taken from this [repo](https://github.com/reflow-project/Amsterdam-pilot/tree/main/graphviz)):
    ![Isolation Gowns Value Flows](/img/isogowns.png?raw=true "Isolation Gowns Value Flows")

        - The notebook implements a part of it which concerns the agents `hospital` and `Textile Company` (called the cleaner in the notebook).

2.  a [flow](https://github.com/interfacerproject/Interfacer-notebook/blob/main/gownshirt.ipynb) defined in this [file](https://github.com/interfacerproject/Interfacer-notebook/blob/main/gownshirt_flow.1.1.txt).
3.  a [flow](https://github.com/interfacerproject/Interfacer-notebook/blob/main/IFUsersFlows.ipynb) corresponding to the [Interfacer](https://www.interfacerproject.eu/) project's front-end [here](https://interfacer-gui-staging.dyne.org/).
4.  a flow corresponding to the [Libre Solar](https://libre.solar/) project (in progress).

# [LIVE DEMO](https://interfacerproject.github.io/Interfacer-notebo)

<br>

<div id="toc">

### 🚩 Table of Contents

- [💾 Install](#-install)
- [🎮 Quick start](#-quick-start)
- [🔧 Configuration](#-configuration)
- [😍 Acknowledgements](#-acknowledgements)
- [🌐 Links](#-links)
- [👤 Contributing](#-contributing)
- [💼 License](#-license)

</div>

---

## 💾 Install

**NOTE**: at the moment you need some credentials to create users, so this software cannot run without an appropriate `.credentials.json` of the form:

```
{
    "key": "<secret key>"
}
```

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

**[🔝 back to top](#toc)**

---

## 🎮 Quick start

In one of the first cells of each use case you can customise the data for your users. Subsequently, the notebook creates some JSON files in order to store information about the users that has been created, the locations, the resource specifications and the units used to quantify the resources.

This information is stored separately per use case and per endpoint on disk with a folder structure like \<use-case\>/\<endpoint\>/\<file\>.json.

When run again, the notebook will reuse info from existing files, avoiding recreating users,units,locations and specs that already exist. It will therefore not overwrite existing files, so if you want to reset the conf files you need to delete them manually.

**[🔝 back to top](#toc)**

---

## 🔧 Configuration

**NOTE**: at the moment you need some credentials to create users, so this software cannot run without an appropriate `.credentials.json` of the form:

```
{
    "key": "<secret key>"
}
```

**[🔝 back to top](#toc)**

---

## 😍 Acknowledgements

<a href="https://dyne.org">
  <img src="https://files.dyne.org/software_by_dyne.png" width="222">
</a>

Copyleft (ɔ) 2022 by [Dyne.org](https://www.dyne.org) foundation, Amsterdam

Designed, written and maintained by Stefano Bocconi

With contributions by Adam Burns & Puria Nafisi Azizi

**[🔝 back to top](#toc)**

---

## 🌐 Links

https://www.interfacer.eu/

https://dyne.org/

**[🔝 back to top](#toc)**

---

## 👤 Contributing

1.  🔀 [FORK IT](../../fork)
2.  Create your feature branch `git checkout -b feature/branch`
3.  Commit your changes `git commit -am 'Add some fooBar'`
4.  Push to the branch `git push origin feature/branch`
5.  Create a new Pull Request
6.  🙏 Thank you

**[🔝 back to top](#toc)**

---

## 💼 License

    Interfacer-notebook - Rapid prototyping data modeling for Zenflows
    Copyleft (ɔ) 2022 Dyne.org foundation

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

**[🔝 back to top](#toc)**
