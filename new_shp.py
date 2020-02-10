# -*- coding: utf-8 -*-

# Sophie Dufour-Beauséjour
# s.dufour.beausejour@gmail.com
# Université INRS
# Québec, Canada

# From a shapefile and a raster, create a new shapefile with square features in
# the image projection, centered on shapefile features
# Requirements: fiona, rasterio, descartes, shapely
# Other files:
# - main.py

from __future__ import print_function

import os
import fiona
import rasterio
from descartes import PolygonPatch
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def plot_shp_over_tiff(image_path, shapefile_path, results_dir, band_index, convert_to_dB=0):
    """From a tiff image (path: image_path) and shapefile (path: shapefile_path),
    plot features over raster and save as png."""
    preffix = os.path.basename(image_path)[0:12]+"_"+band_index[1]+"_"+os.path.basename(shapefile_path)

    figures_path = os.path.join(results_dir,preffix+".pdf")
    fig = plt.figure(figsize=(6, 3))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.05,
                        wspace=0.05)  # adjust the box of axes regarding the figure s
    gs = mpl.gridspec.GridSpec(1, 1,
                               width_ratios=[1],
                               height_ratios=[1])
    axes = list()
    axes.append(plt.subplot(gs[0]))
    ax = axes[0]
    ax = fig.gca()

    # Plot image
    src = rasterio.open(image_path)
    array = src.read(band_index[0])
    array[array == 0.0] = np.nan
    if convert_to_dB:
        array = 10 * np.log10(array)
        ax.imshow(array, cmap='gray', vmin=-30, vmax=-5, zorder=0)
    else:
        ax.imshow(array, cmap='gray', zorder=0)

    # Convert features in long/lat to pixel coordinates and plot
    with fiona.open(shapefile_path, "r") as shapefile:
        features = [feature["geometry"] for feature in shapefile]
    pixel_polygons = list()
    for feature in features:
        pix_long_lat = [src.index(x[0],x[1]) for x in feature["coordinates"][0]]
        # long / lat is y / x; invert
        pix_x_y = [(x[1], x[0]) for x in pix_long_lat]
        pixel_polygon = Polygon(pix_x_y)
        pixel_polygons.append(pixel_polygon)
    patches = [PolygonPatch(feature, facecolor="pink", linewidth=0.5, zorder=2) for feature in pixel_polygons]
    ax.add_collection(mpl.collections.PatchCollection(patches, match_original=True))

    # Annotate feature number
    for j, pol in enumerate(pixel_polygons):
        x, y = pol.exterior.coords.xy
        ax.annotate(str(j+1), xy=(x[0]+20, y[0]-20), xycoords="data", ha="center", color="orange", fontsize=4)

    # Hide axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])

    # fig.savefig(figures_path)
    fig.savefig(figures_path[0:-4]+".png",transparent=False, dpi=300)
    plt.close()


def square_polygons(image_path, shapefile_path, results_dir, new_shp_path):
    """From a tiff image (path: image_path) and shapefile (path: shapefile_path),
    create new square features centered on the original shapes"""

    # Raster
    src = rasterio.open(image_path)
    array = src.read(1)
    array[array == 0.0] = np.nan

    # Convert features in long/lat to pixel coordinates
    with fiona.open(shapefile_path, "r") as source:
        sink_schema = source.schema
        with fiona.open(
                new_shp_path, 'w',
                crs=source.crs,
                driver=source.driver,
                schema=sink_schema,
        ) as sink:
            print(source.crs)
            for j, f in enumerate(source):
                g = f['geometry']
                # from long / lat to y / x
                p_coords = [src.index(x[0], x[1]) for x in g["coordinates"][0]]
                # Get center of polygon, in y / x coordinates
                x = [p[0] for p in p_coords]
                y = [p[1] for p in p_coords]
                center_x, center_y = (sum(x) / len(p_coords), sum(y) / len(p_coords))
                # Create 22 pixels large square centered on centroid
                half = 11
                rectangle = [(center_x-half, center_y+half), (center_x+half, center_y+half),
                             (center_x+half, center_y-half), (center_x-half, center_y-half), (center_x-half, center_y+half)]
                # from y / x to long / lat
                l_coords = [src.xy(x[0], x[1]) for x in rectangle]
                # pixel_polygon = Polygon(l_coords)
                g["coordinates"][0] = l_coords
                f['geometry'] = g
                sink.write(f)
                # sink.write({'geometry': mapping(poly), 'properties': {'Id': j}})