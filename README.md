# 3d-houses

## Table of Contents

- [Introduction](#introduction)
- [Folder Structure](#folder-structure)

## Introduction

This project is created with the goal of visualising a building starting from only the address.

### Strategy
1. Use an API call to https://api.basisregisters.vlaanderen.be/v1/adresmatch 
get a polygon from a house when given an address
2. www.Geopunt.be has a digital height model. With the address we have we find the right files to download.
We want to download DTM and DSM data. These are digital height models of flanders which are created by LIDAR.
With the DTM and DSM we can create Canopy Height Model, which represent houeses in this case.

An example of DTM, DSM and CHM:

![Image](data/images/chm.png)

3. Finally we can plot this data to get a virtual representation of the building. Although this is not perfect. 
Since the data came from an LIDAR outside a plain we will only get the top down bird view.
As a result, a bridge will look like a wall.

An eample of a 3D plot (interactive when you run it yourself)

![Image](data/images/2000_bolivarplaats_20(0).png)

## Folder Structure

- **Data**: All dat will be stored in this folder
    - **GeoTIFF**: **tif** files that contain DTM and DSM data, from which we obtain the Canopy Height Model
    - **images**
        - Saved plots of 3D houess
    - **bounding_boxes_coordinates**: Pandas dataframe with coordinate pairs as index and column 
    and values as folder number in which the data can be found.
- **utils**: module with function we need to build 3D plots
    -**api.py**: Functions that use *requests* to make api calls to *https://api.basisregisters.vlaanderen.be/v1/adresmatch*
    to get the polygons of a house/building
    -**functions.py**: One function to match a coordinate in the indexes of **bounding_boxes_coordinates**
- **house.py**: Defining the house class in which most operations happen, connecting the code base: api calls, plots, ...
- **main.py**: The file to execute, just enter your address in the correct format and the program will do all the rest.
