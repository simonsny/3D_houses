requirements:
py3.7
rasterio
geopy
matplotlib
requests

conda install -c conda-forge jupyterlab-plotly-extension
https://anaconda.org/conda-forge/jupyterlab-plotly-extension

data:
formatted:
Coordinate reference system: CRS.from_epsg(31370)

use gitignore to leave out the big files in data/


to save a file:
conda install psutil
conda install -c plotly plotly-orca
