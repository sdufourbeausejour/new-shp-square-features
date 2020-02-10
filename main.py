# -*- coding: utf-8 -*-

# Sophie Dufour-Beauséjour
# s.dufour.beausejour@gmail.com
# Université INRS
# Québec, Canada

# From a shapefile and a raster, create a new shapefile with square features in
# the image projection, centered on shapefile features
# Requirements: fiona, rasterio, descartes, shapely
# Other files:
# - new_shp.py

from __future__ import print_function
__author__ = "Sophie Dufour-Beauséjour"

import os
import re
# from this project
import new_shp
import utils

# Band in image raster, and its name
band_index = [1,"HH"] # Rasterio starts counting at 1, not 0
no_data_value = 0

# Paths (add your raster and your shapefile to example/data)
image_path = "example/data/image.tif"
shapefile_path = "example/data/shapefile.shp"
results_dir = "examples/results"
exp_file_name_pattern = re.compile("RS2.*(2015).*")

for bay in ["Salluit", "DeceptionBay", "Kangiqsujuaq"]:
    image_dir = "/Volumes/Crabe/Doctorat/BaieDeception/Donnees/Imagerie/RS2_subAOIs/" + bay
    shapefile_path = "/Volumes/Crabe/Doctorat/BaieDeception/Donnees/Imagerie/VectorData/RS2paper/" + \
                     bay[0] + "_AOIs_RS2_WGS84_square.shp"
    results_dir = "/Users/sdufourbeausejour/Desktop/Doctorat/0. Analyse/" \
                  "data_analyzed/image_statistics/RS2paper/" + bay
    image_folders = utils.find_matching_file_list(image_dir, exp_file_name_pattern, print_list=0)
    for i, image_folder in enumerate(image_folders):
        print("Image "+str(i+1)+ " out of "+str(len(image_folders))+"...")
        image_path = os.path.join(image_dir, image_folder, image_folder+"_sub_cal_spk_rat_TC.tif")
        new_shp.plot_shp_over_tiff(image_path, shapefile_path, results_dir, band_index, convert_to_dB=1)

# # Create new shp
# new_shapefile_path = os.path.join(results_dir, "square_AOIs.shp")
# new_shp.square_polygons(image_path, shapefile_path, results_dir, new_shapefile_path)
#
# # Plot shapefile over image
# new_shp.plot_shp_over_tiff(image_path, shapefile_path, results_dir, band_index, convert_to_dB=1)
