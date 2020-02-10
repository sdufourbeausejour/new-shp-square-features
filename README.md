# new_shp

new_shp is a Python script for creating a custom shapefile based on a reference shapefile schema, and using the pixel space of a georeferenced raster.

Using square_polygons, create a shapefile with square features (in the image projection)
Using plot_shp_over_tiff, plot a shapefile over the image raster in a png format

## Usage

```python
import new_shp

new_shp.plot_shp_over_tiff(image_path, shapefile_path, results_dir) # writes a png image of the raster overlaid with shapefile features
new_shp.square_polygons(image_path, shapefile_path, results_dir, new_shapefile_path) # creates a shapefile with square features in the image projection centered on shapefile features
```

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
