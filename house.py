import os

import pandas as pd
import numpy as np
import psutil
import rasterio
import rasterio.mask
from rasterio.plot import show
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly
import requests, zipfile, io
from utils.api import get_polygon_from_adress_params
from utils.functions import find_index

class House:
    """
    A class used to find the coordinates of a house when given an address and display this house in 3D.
    """

    def __init__(self,
                 params=None,
                 polygons=None,
                 raster_file_number=None,
                 chms=None):
        """
        Initializes the House class.
        :param params: Address of the house.
        :param polygons: Polygons of coordinates that give boundaries to the buildings of the address.
        :param raster_file_number: The number of the file which has the LIDAR data of the house we want.
        :param chms: List of Conopy Height Models of our house.
        """
        if params is None:
            self.params = {}
            self.ask_input()
        else:
            self.params = params
        self.polygons = polygons
        self.raster_file_number = raster_file_number
        if chms is None:
            self.chms = []
        else:
            self.chms = chms


    def ask_input(self):
        """
        Asks the user for the address of the house we want to 3D-plot
        """
        self.params['street_name'] = input('Street name:')
        self.params['house_number'] = input('huisnummer:')
        self.params['postcode'] = input('Postcode:')

    def get_polygon(self):
        """
        Method that uses address parameters and an API call to get a list of polygons
        """
        _request_params = {}
        _request_params['straatnaam'] = self.params['street_name']
        _request_params['huisnummer'] = self.params['house_number']
        _request_params['postcode'] = self.params['postcode']
        self.polygons = get_polygon_from_adress_params(_request_params)

    def get_raster_file_number(self):
        """"
        Method that finds raster number corresponding to the coordinates.
        It does not handle edge cases in which the polygons go over the raster bounds.
        """
        _raster_coords = pd.read_csv('data/bounding_boxes_coordinates')
        _raster_coords.set_index('index', inplace=True)
        _x, _y = self.polygons[0].bounds[:2]
        ind = find_index(_y, _raster_coords.index)
        col = find_index(_x, _raster_coords.columns)
        self.raster_file_number = str(_raster_coords.loc[ind, col])

    def get_chm(self):
        """
        Load the DTM and DSM, mask them with the polygon and get the Canopy Height Model.
        """
        k = self.raster_file_number
        cwd = os.getcwd()
        data_dir = os.path.join(cwd, 'data')
        tif_folder = os.path.join(data_dir, 'GeoTIFF')
        k_tif_dsm = f'DHMVIIDSMRAS1m_k{k}.tif'
        k_tif_dtm = f'DHMVIIDTMRAS1m_k{k}.tif'
        k_DSM_tif_loc = os.path.join(tif_folder, k_tif_dsm)
        k_DTM_tif_loc = os.path.join(tif_folder, k_tif_dtm)
        for polygon in self.polygons:
            with rasterio.open(k_DSM_tif_loc) as src:
                out_image_dsm, out_transform = rasterio.mask.mask(src, [polygon], crop=True, filled=True, pad=True)
            with rasterio.open(k_DTM_tif_loc) as src:
                out_image_dtm, out_transform = rasterio.mask.mask(src, [polygon], crop=True, filled=True, pad=True)
            image_chm = out_image_dtm - out_image_dsm

            self.chms.append(image_chm)

    def show_chm(self, save=True):
        """
        Plots the canopy height models of the house in 3D.
        Most of the time there should be only 1 chm.
        """
        for i, chm in enumerate(self.chms):
            chm = chm[0] * -1
            chm = np.flip(chm, axis=1)
            fig = go.Figure(data=[go.Surface(z=chm)])
            title = f'{self.params["postcode"]} {self.params["street_name"]} {self.params["house_number"]}'
            fig.update_layout(title=f'3D plot of {title}', autosize=True)
            fig.show()

            fig.write_image(f'data/images/{self.params["postcode"]}_'
                            f'{self.params["street_name"]}_'
                            f'{self.params["house_number"]}({i}).png')

    def get_tif_files(self):
        """
        Methods that checks if the DSM and DTM tif files are in the correct folder, if not, it downloads them.
        """
        k = self.raster_file_number
        dsm = f'DHMVIIDSMRAS1m_k{k}.tif'
        dtm = f'DHMVIIDTMRAS1m_k{k}.tif'
        file_path = os.path.abspath(__file__)
        project_path = os.path.dirname(file_path)
        data_path = os.path.join(project_path, 'data')
        full_path_dsm = os.path.join(data_path, 'GeoTIFF', dsm)
        full_path_dtm = os.path.join(data_path, 'GeoTIFF', dtm)
        print(full_path_dsm)

        if not os.path.exists(full_path_dsm):
            print('DSM tif not in data folder, downloading zip file now...')
            dsm_url = f'https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/DHMVIIDSMRAS1m_k{k}.zip'
            r_dsm = requests.get(dsm_url, stream=True)
            print("Downloaded zip file, unpacking the tif file...")
            print(dsm_url)

            z_dsm = zipfile.ZipFile(io.BytesIO(r_dsm.content))
            z_dsm.extract(f'GeoTIFF/DHMVIIDSMRAS1m_k{k}.tif', path=data_path)
            print("Unpacked")
        else:
            print(f'{dsm} file found, no need to download.')
        if not os.path.exists(full_path_dtm):
            print('DTM tif not in data folder, downloading zip file now...')
            dtm_url = f'https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/DHMVIIDTMRAS1m_k{k}.zip'
            r_dtm = requests.get(dtm_url, stream=True)
            print("Downloaded zip file, unpacking the tif file...")
            z_dtm = zipfile.ZipFile(io.BytesIO(r_dtm.content))
            z_dtm.extract(f'GeoTIFF/DHMVIIDTMRAS1m_k{k}.tif', path=data_path)
            print("Unpacked")
        else:
            print(f'{dtm} file found, no need to download.')


if __name__ == '__main__':
    house = House()
    house.get_polygon()
    print(house.polygons)

    house.get_raster_file_number()
    print(house.raster_file_number)

    house.get_tif_files()

    house.get_chm()

    house.show_chm()