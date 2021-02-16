"""
Minimum longitude: 2.54154°
Maximum longitude: 5.92°
Minimum latitude: 50.6756°
Maximum latitude: 51.51°
"""


import rasterio
from rasterio.plot import show
import geopandas as gpd
fp = r'C:\Users\simon\PycharmProjects\3D_houses\data\data1\GeoTIFF\DHMVIIDSMRAS1m_k43.tif'
img = rasterio.open(fp)
show(img)


print(img)

Stationsstraat 205
2910 Essen
51,462935° - 4,453936°