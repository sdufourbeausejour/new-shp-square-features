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
# from this project
import new_shp

# Band in image raster, and its name
band_index = [1,"HH"] # Rasterio starts counting at 1, not 0
no_data_value = 0

# Paths (add your raster and your shapefile to example/data)
image_path = "example/data/image.tif"
shapefile_path = "example/data/shapefile.shp"
results_dir = "examples/results"

# Create new shp
new_shapefile_path = os.path.join(results_dir, "square_AOIs.shp")
new_shp.square_polygons(image_path, shapefile_path, results_dir, new_shapefile_path)

# Plot shapefile over image
new_shp.plot_shp_over_tiff(image_path, shapefile_path, results_dir, band_index, convert_to_dB=1)
new_shp.plot_shp_over_tiff(image_path, new_shapefile_path, results_dir, band_index, convert_to_dB=1)
