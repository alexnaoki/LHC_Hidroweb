# LHC_Hidroweb

[![DOI](https://zenodo.org/badge/245466190.svg)](https://zenodo.org/badge/latestdoi/245466190)

---------------------
# Introduction

LHC_Hidroweb is a Jupyter application for visualize ANA's Inventory and download Rainfall or Flow data from ANA's API.

# Usage

You can use a ".csv" file from ANA's website, or you can get the latest Inventory file from ANA's API (and later save in your local). Don't forget to add 'Inventario.csv' at the end.
![](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/gifs/inventario01_v2.gif)

After uploading the Inventory data you can **visualize** the columns in the inventory.
![](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/gifs/tables01_v2.gif)

And, check a few basic **stats**.
![](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/gifs/stats01_v2.gif)

And finally you can easily **download** the **Rainfall** or **Flow** data with a **self drawn contour** or use a **Shapefile**. If you use the **Shapefile**, the file should be in **WGS84**.
![](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/gifs/download01_v2.gif)

A quick graph visualization can be done by checking the date period with some data in the Downloaded data.
![](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/gifs/graphs01_v2.gif)

--------------------------------------

# Instalation GUIDE
**Follow** the process in order to utilize the Interactive Tool.

#### It is **necessary** to use Anaconda for the following steps. The use of Anaconda facilitate the download and aplication of the following programs.

1. **First**, you need to open **Anaconda Prompt**.

2. **Create** a new **Virtual Environment** for avoid possible conflict of packages.
  - Deactivate the current environment by `conda deactivate`.
  - Check the possible environment by `conda env list`.
  - Create by `conda create --name LHC_Hidroweb python=3.7`.
  - Check again the environment to make sure the Environment was created `conda env list`.
  - Activate the environment `conda activate LHC_Hidroweb`.


3. **Core packages** for the **Batch download**.
  - Install `conda install requests`.
  
4. **Core packages** for the **Interactive Map**.
  - `conda install -c conda-forge jupyterlab geopandas ipywidgets nodejs ipyleaflet bqplot`
  - `conda install numpy pandas`
  
5. **Add** the newly created Virtual Environment to **Jupyter**
  - `pip install --user ipykernel`
  - `python -m ipykernel install --user --name=LHC_Hidroweb`
  
6. **Install/Activate** the widgets for **Jupyter-lab**
  - `jupyter labextension install @jupyter-widgets/jupyterlab-manager`
  - `jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet`
  - `jupyter labextension install bqplot`

7. **Opening Jupyter-lab**
  - `jupyter-lab`
  
  - After opened the **Jupyter Lab**, you need to make sure to use the **correct kernel**.

![alt text](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/imgs/fig03.jpg)

  - And, if the selected kernel is other than the one just created, selected the **correct kernel**.

![alt text](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/imgs/fig02.PNG)

8. **Open** the **View_Map01.ipynb** in Jupyter-lab and **Run the cells**

9. **Enjoy the interactive map!**
