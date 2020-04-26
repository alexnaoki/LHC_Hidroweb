# LHC_Hidroweb
---------------------

![](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/gifs/inventario01.gif)


# Instalation GUIDE
**Follow** the process in order to utilize the Interactive Tool.

#### It is **necessary** to use Anaconda for the following steps. The use of Anaconda facilitate the download and aplication of the following programs.

-----------------------------------------
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
  - `conda install numpy`
  - `conda install pandas`
  - `conda install -c conda-forge geopandas`
  - `conda install -c conda-forge ipywidgets`
  - `conda install -c conda-forge nodejs`
  - `conda install -c conda-forge ipyleaflet`
  
5. **Add** the newly created Virtual Environment to **Jupyter**
  - `pip install --user ipykernel`
  - `python -m ipykernel install --user --name=LHC_Hidroweb`
  
6. **Install/Activate** the widgets for **Jupyter-lab**
  - `jupyter labextension install @jupyter-widgets/jupyterlab-manager`
  - `jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet`

7. **Opening Jupyter-lab**
  - `jupyter-lab`
  
  - After opened the **Jupyter Lab**, you need to make sure to use the **correct kernel**.

![alt text](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/imgs/fig03.jpg)

  - And, if the selected kernel is other than the one just created, selected the **correct kernel**.

![alt text](https://github.com/alexnaoki/LHC_Hidroweb/blob/master/imgs/fig02.PNG)

8. **Open** the **View_Map01.ipynb** in Jupyter-lab and **Run the cells**

9. **Enjoy the interactive map!**
