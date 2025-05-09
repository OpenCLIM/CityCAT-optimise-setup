#from citycatio import Model, output
import geopandas as gpd
import pandas as pd
import os
import shutil
from zipfile import ZipFile
from glob import glob
import subprocess
import zipfile
import csv
#import rasterio as rio


# Set up paths
data_path = os.getenv('DATA_PATH', '/data')
inputs_path = os.path.join(data_path, 'inputs')
outputs_path = os.path.join(data_path, 'outputs')
if not os.path.exists(outputs_path):
    os.mkdir(outputs_path)
from pathlib import Path
from os.path import isfile, join, isdir

class GreenAreas:
    """Areas representing permeable land cover

    Args:
        data: Table containing green areas polygons

    """
    def __init__(self, data: gpd.GeoDataFrame):
        assert type(data) == gpd.GeoDataFrame
        self.data = data

    def write(self, path):
        with open(os.path.join(path, 'GreenAreas.txt'), 'w') as f:
            f.write(geoseries_to_string(self.data.geometry))
        with open(os.path.join(path, 'GreenAreas_0.txt'), 'w') as f:
            f.write(geoseries_to_string(self.data.geometry))
 
class Buildings:
    """Areas representing Buildings

    Args:
        data: Table containing buildings polygons

    """
    def __init__(self, data: gpd.GeoDataFrame):
        assert type(data) == gpd.GeoDataFrame
        self.data = data

    def write(self, path):
        with open(os.path.join(path, 'Buildings.txt'), 'w') as f:
            f.write(geoseries_to_string(self.data.geometry))

def geoseries_to_string(geoseries: gpd.GeoSeries, value= None, index=False, index_first=True):
    """GeoSeries to CityCAT string representation

    Args:
        geoseries: Polygons to convert
        index: Whether or not to include the index
        index_first: Whether or not to place the index before the number of points
    Returns:
        s (str): String representation readable by CityCAT

    """
    assert (geoseries.geom_type == 'Polygon').all(), 'Geometries must be of type Polygon'

    s = '{}\n'.format(len(geoseries))

    for idx, geometry in geoseries.items():
        if not index:
            s += '{}'.format(len(geometry.exterior.coords))
        elif index_first:
            s += '{} {}'.format(value[idx], len(geometry.exterior.coords))
        else:
            s += '{} {}'.format(len(geometry.exterior.coords), value[idx])
        x, y = geometry.exterior.coords.xy
        for x_val in x:
            s += ' {}'.format(x_val)
        for y_val in y:
            s += ' {}'.format(y_val)
        s += '\n'

    return s



def read_geometries(path, bbox=None):
    paths = glob(os.path.join(inputs_path, path, '*.gpkg'))
    paths.extend(glob(os.path.join(inputs_path, path, '*.shp')))
    print(f'Files in {path} directory: {[os.path.basename(p) for p in paths]}')
    
    # set a default value
    geometries = None
    
    if len(paths) > 0:
        geometries = gpd.read_file(paths[0], bbox=bbox)
              
    if len(paths) > 1:
        for path in paths[1:]:
            geometries = geometries.append(gpd.read_file(path))
    return geometries


# Read and write DEM
dem_path = os.path.join(inputs_path, 'dem')
dem_out_path = os.path.join(outputs_path, 'dem')
if not os.path.exists(dem_out_path):
    os.mkdir(dem_out_path)
for demfilename in glob(os.path.join(dem_path, '*.asc')):
#three similar files needed for CityCAt optimisation
    destination_file = os.path.join(dem_out_path, 'Baseline_DEM.asc')
    shutil.copy(demfilename, destination_file)
    destination_file = os.path.join(dem_out_path, 'DEM.asc')
    shutil.copy(demfilename, destination_file)
    destination_file = os.path.join(dem_out_path, 'Domain_DEM.asc')
    shutil.copy(demfilename, destination_file)
    print (demfilename)

#read green-areas gemetry
green_areas = read_geometries('green_areas')
green_out_path = os.path.join(outputs_path, 'green-areas')
if not os.path.exists(green_out_path):
    os.mkdir(green_out_path)
GreenAreas(green_areas).write(green_out_path)

#read buildings gemetry
buildings = read_geometries('buildings')
buildings_out_path = os.path.join(outputs_path, 'buildings')
if not os.path.exists(buildings_out_path):
    os.mkdir(buildings_out_path)
Buildings(buildings).write(buildings_out_path)


# buildings_path = os.path.join(inputs_path, 'buildings')
# buildings_out_path = os.path.join(outputs_path, 'buildings')
# if not os.path.exists(buildings_out_path):
#     os.mkdir(buildings_out_path)
# for buildingsfilename in glob(os.path.join(buildings_path, '*.gpkg')):
#     data = gpd.read_file(buildingsfilename)
#     destination_file = os.path.join(buildings_out_path, 'Buildings.shp')
#     data.to_file(destination_file, driver='ESRI Shapefile')

#green_areas2 = GreenAreas(green_areas)

#Model(green_areas=green_areas).write(outputs_path)
# with open(os.path.join(outputs_path, 'GreenAreas.txt'), 'w') as f:
#     assert type(green_areas) == gpd.GeoDataFrame
#     green_areas = GreenAreas(green_areas)
#     #green_areas.data=green_areas
#     f.write(geoseries_to_string(green_areas.geometry))


# array, transform = merge(dem_datasets, bounds=bounds, precision=50, nodata=nodata)
# assert array[array != nodata].size > 0, "No DEM data available for selected location"

# # Read buildings
# logger.info('Reading buildings')
# buildings = read_geometries('buildings', bbox=bounds)

# # Look to see if a spatial infiltration/green nareas is being used
# greenAreas_path = os.path.join(inputs_path, 'green_areas')
# infiltration_file = glob(greenAreas_path + "/*.csv", recursive = True)
# print('infiltration_file:', infiltration_file)
# if len(infiltration_file) == 1 :
#     file_path = os.path.splitext(infiltration_file[0])
#     print('Filepath:',file_path)
#     if os.name=='nt':
#         filename=file_path[0].split("\\")
#     else:
#         filename=file_path[0].split("/")
#     #filename=file_path[0].split("\")
#     #filename=file_path[0].split("\\")
#     print('Filename:',filename[-1])

#     infiltration_parameters = pd.read_csv(os.path.join(greenAreas_path + '/' + filename[-1] + '.csv'), header=None)
# else:
#     infiltration_parameters = None    
    
    
# #read green-areas gemetry
# logger.info('Reading green areas')
# green_areas = read_geometries('green_areas', bbox=bounds)
# if green_areas is not None:
#     if("Value" in green_areas.columns):
#         assert infiltration_file, 'if spatial green areas exist, an infiltration.csv file must be provided'


# # Read friction coeffs
# logger.info('Reading friction coeffs areas')
# friction = read_geometries('friction_coeffs', bbox=bounds)


# # Read reservoir
# logger.info('Reading reservoir areas')
# reservoir = read_geometries('reservoirs', bbox=bounds)


# # Read spatial rainfall
# logger.info('Reading rainfall polygons')
# rainfall_polygons = read_geometries('rainfall_polygons', bbox=bounds)

# logger.info('Reading rainfall depths for rainfall polygons')
# if rainfall_polygons is not None:
#     rainfall_polygons_path = os.path.join(inputs_path, 'rainfall_polygons')
#     rainfall_depth = glob(rainfall_polygons_path + "/*.csv") + glob(rainfall_polygons_path + "/*.txt")
#     if len(rainfall_depth) == 1 :
#         spatial_depths = np.loadtxt(rainfall_depth[0],skiprows=1)
#         rain_array = np.zeros(shape=(len(unit_profile)+2,len(spatial_depths)))
#         for x1 in range(len(unit_profile)):
#             for y1 in range(len(spatial_depths)):
#                 rain_array[x1,y1]=unit_profile[x1]*spatial_depths[y1]
#         for y1 in range(len(spatial_depths)):
#             rain_array[x1+1,y1]=0.0
#             rain_array[x1+2,y1]=0.0
#         rainfall = pd.DataFrame(list(rain_array/unit_total/1000),
#                         index=list(rainfall_times) + [duration*3600+1, duration*3600+2] )




# total_duration = 3600*duration+3600*post_event_duration

# # Create discharge timeseries
# print('discharge_parameter:',discharge_parameter)
# logger.info('Creating discharge timeseries')
# if discharge_parameter != None:
#     if discharge_parameter >0:
#         discharge = pd.Series([discharge_parameter, discharge_parameter], index=[0, total_duration])

#         # Divide by the length of each cell
#         if dtm_size >0:
#             discharge = discharge.divide(dtm_size)
#             print('actual discharge per m = input discharge divided by cell size:',discharge[0])
#         else:
#             discharge = discharge.divide(5)
#             print('actual discharge per m = input discharge divided by cell size:',discharge[0])
#             print('cell size not defined set to 5 meters')

# #        flow_polygons = gpd.read_file(glob(os.path.join(inputs_path, 'flow_polygons', '*'))[0]).geometry
#         flow_polygons = read_geometries('flow_polygons', bbox=bounds)
#     else:
#         discharge = None
#         flow_polygons = None

# logger.info('Creating DEM dataset and boundary dataset')
# dem = MemoryFile()
# with dem.open(driver='GTiff', transform=transform, width=array.shape[2], height=array.shape[1], count=1,
#               dtype=rio.float32, nodata=nodata) as dataset:
#     bounds = dataset.bounds
#     dataset.write(array)

# # if boundary is not None:
# #     array, transform = mask(dem.open(), boundary.geometry, crop=True)
# #     dem = MemoryFile()
# #     with dem.open(driver='GTiff', transform=transform, width=array.shape[2], height=array.shape[1], count=1,
# #                   dtype=rio.float32, nodata=nodata) as dataset:
# #         bounds = dataset.bounds
# #         dataset.write(array)

# # Create input files
# logger.info('Creating input files')
# Model(
#     dem=dem,
#     rainfall=rainfall,
#     rainfall_polygons=rainfall_polygons,
#     duration=total_duration,
#     output_interval=output_interval,
#     open_external_boundaries=open_boundaries,
#     buildings=buildings,
#     green_areas=green_areas,
#     friction=friction,
#     reservoir=reservoir,
#     use_infiltration=True,
#     permeable_areas={'polygons': 0, 'impermeable': 1, 'permeable': 2}[permeable_areas],
#     roof_storage=roof_storage,
#     flow=discharge,
#     flow_polygons=flow_polygons,
#     infiltration_parameters=infiltration_parameters

# ).write(run_path)

# # Copy executable
# logger.info('Preparing CityCat')
# shutil.copy('citycat.exe', run_path)

# start_timestamp = pd.Timestamp.now()

# # Run executable
# logger.info('Running CityCat......')
# if os.name == 'nt':
#     subprocess.call('cd {run_path} & citycat.exe -r 1 -c 1'.format(run_path=run_path), shell=True)
# else:
#     subprocess.call('cd {run_path} && wine64 citycat.exe -r 1 -c 1'.format(run_path=run_path), shell=True)

# end_timestamp = pd.Timestamp.now()

# logger.info('....CityCat completed!')

# # Delete executable
# logger.info('Deleting CityCAT model')
# os.remove(os.path.join(run_path, 'citycat.exe'))

# # Archive results files
# logger.info('Archiving results')
# surface_maps = os.path.join(run_path, 'R1C1_SurfaceMaps')
# shutil.make_archive(surface_maps, 'zip', surface_maps)

# # Create geotiff
# logger.info('Creating outputs')
# geotiff_path = os.path.join(run_path, 'max_depth.tif')
# netcdf_path = os.path.join(run_path, 'R1C1_SurfaceMaps.nc')

# output.to_geotiff(os.path.join(surface_maps, 'R1_C1_max_depth.csv'), geotiff_path, srid=int(projection))
            
# if x != None:
#     output.to_netcdf(surface_maps, out_path=netcdf_path, srid=int(projection),
#                      attributes=dict(
#                         rainfall_mode=rainfall_mode,
#                         rainfall_total=float(rainfall_total),
#                         size=size,
#                         duration=duration,
#                         post_event_duration=post_event_duration,
#                         x=int(x),
#                         y=int(y),
#                         open_boundaries=str(open_boundaries),
#                         permeable_areas=str(permeable_areas)))
# else:
#     output.to_netcdf(surface_maps, out_path=netcdf_path, srid=int(projection),
#                  attributes=dict(
#                     rainfall_mode=rainfall_mode,
#                     rainfall_total=float(rainfall_total),
#                     duration=duration,
#                     post_event_duration=post_event_duration,
#                     open_boundaries=str(open_boundaries),
#                     permeable_areas=str(permeable_areas)))

# a = xr.open_dataset(netcdf_path)

# dst_crs='EPSG:'+ projection
# print('dts_crs:',dst_crs)

# #velocity = xr.ufuncs.sqrt(a.x_vel**2+a.y_vel**2).astype(np.float64)
# velocity = np.sqrt(a.x_vel**2+a.y_vel**2).astype(np.float64)
# #print(velocity)
# max_velocity = velocity.max(dim='time').round(3)
# #print(max_velocity)
# max_velocity = max_velocity.where(np.isfinite(max_velocity), other=output.fill_value)
# #max_velocity = max_velocity.where(xr.ufuncs.isfinite(max_velocity), other=output.fill_value)
# #print(type(max_velocity.rio))
# #max_velocity.rio.set_crs('EPSG:27700')
# max_velocity.rio.write_crs('EPSG:27700')
# max_velocity.rio.set_nodata(output.fill_value)
# max_velocity.rio.to_raster(os.path.join(run_path, 'max_velocity.tif'))

# print('Stage 1')

# vd_product = velocity * a.depth
# max_vd_product = vd_product.max(dim='time').round(3)
# max_vd_product = max_vd_product.where(np.isfinite(max_vd_product), other=output.fill_value)
# #max_vd_product = max_vd_product.where(xr.ufuncs.isfinite(max_vd_product), other=output.fill_value)
# #max_vd_product.rio.set_crs('EPSG:27700')
# max_vd_product.rio.write_crs('EPSG:27700')
# max_vd_product.rio.set_nodata(output.fill_value)
# max_vd_product.rio.to_raster(os.path.join(run_path, 'max_vd_product.tif'))

# print('Stage 2')

# # # Create depth map
# # with rio.open(geotiff_path) as ds:
# #     f, ax = plt.subplots()

# #     cmap = ListedColormap(['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c',
# #                            '#08306b', 'black'])
# #     cmap.set_bad(color='lightgrey')
# #     cmap.colorbar_extend = 'max'

# #     im = show(ds, ax=ax, cmap=cmap, vmin=0, vmax=1).get_images()[0]

# #     ax.set_xticks([])
# #     ax.set_yticks([])

# #     ax.add_artist(ScaleBar(1, frameon=False))
# #     f.colorbar(im, label='Water Depth (m)')
# #     f.savefig(os.path.join(run_path, 'max_depth.png'), dpi=200, bbox_inches='tight')

# # Create a depth map, with the boundary and max water levels

# dpi = 300
# print('dpi:',dpi)

# #Plotting the Raster and the ShapeFile together
# fig, ax = plt.subplots(1, 1, dpi = dpi)
# cmap = mpl.cm.Blues

# plt.subplots_adjust(left = 0.10 , bottom = 0, right = 0.90 , top =1)

# print('Stage 3')

# #Bounds for the raster
# bounds_depth =  [0.01, 0.05, 0.10, 0.15, 0.30, 0.50, 0.80, 1.00] #you could change here the water depth of your results
# norm = mpl.colors.BoundaryNorm(bounds_depth, cmap.N)

# axins = inset_axes(ax,
#                    width="2%", # width of colorbar in % of plot width
#                    height="45%", # height of colorbar in % of plot height
#                    loc=2, #topright location
#                    bbox_to_anchor=(1.01, 0, 1, 1), #first number: space relative to plot (1.0 = no space between cb and plot)
#                    bbox_transform=ax.transAxes,
#                    borderpad=0) 

# print('Stage 4')

# if len(boundary) != 0:
#     boundary.boundary.plot(edgecolor = 'black', lw = 0.5, ax = ax) #lw = 0.05 -> entire area #0.2 #0.80 for zoom

# citycat_outputs = rio.open(geotiff_path, mode ='r')
# #The line below correspond to the raster
# show(citycat_outputs, ax = ax, title = 'max_water_depth', cmap = 'Blues', norm = norm)

# print('Stage 5')

# #Plotting the colorbar for the raster file Water Depth:
# plt.colorbar(mpl.cm.ScalarMappable(cmap = cmap, norm = norm),
#              ax = ax,
#              cax = axins,
#              extend = 'both',
#              format='%.2f',
#              ticks = bounds_depth,
#              spacing = 'uniform',
#              orientation = 'vertical',
#              label = 'Water Depth in m')

# plt.savefig(os.path.join(run_path, 'max_depth.png'), dpi=dpi, bbox_inches='tight')

# print('Stage 6')

# # Create interpolated GeoTIFF
# with rio.open(geotiff_path) as ds:
#     with rio.open(os.path.join(run_path, 'max_depth_interpolated.tif'), 'w', **ds.profile) as dst:
#         dst.write(fillnodata(ds.read(1), mask=ds.read_masks(1)), 1)

# print('Stage 6a')

# title = 'CityCat'
# description = 'Testing'

# print('Stage 6b')

# if rainfall_mode == 'return_period':
#     description += f'The {return_period}yr {duration}hr event was extracted from the UKCP18 baseline (1980-2000)'
#     if time_horizon != 'baseline':
#         description += f' and uplifted by {row["Uplift_50"]}%'
#     description += '. '

#     title += f' {time_horizon} {return_period}yr'

# print('Stage 7')

# description += f'Total depth of rainfall was {int(round(rainfall_total, 0))}mm. '
# title += f' {int(round(rainfall_total, 0))}mm'
# if post_event_duration > 0:
#     description += f'Following the {duration}hr event, the simulation continued for {post_event_duration}hrs. '

# if buildings is not None and len(buildings) > 0:
#     description += f'{len(buildings)} buildings were extracted from the domain. '

# if green_areas is not None and len(green_areas) > 0:
#     description += f'{len(green_areas)} green areas where infiltration can take place were defined. '

# print('Stage 8')

# description += f'The boundaries of the domain were set to {"open" if open_boundaries else "closed"}.'

# if roof_storage > 0:
#     description += f' There was {roof_storage}m of roof storage.'
#     title += f' storage={roof_storage}m'

# if discharge is not None:
#     description += f' A flow of {discharge_parameter} cumecs was used as a boundary condition.'
#     title += f' {discharge_parameter}m3/s'

# udm_para_out_path = os.path.join(outputs_path, 'udm_parameters')
# if not os.path.exists(udm_para_out_path):
#     os.mkdir(udm_para_out_path)

# print('Stage 9')

# meta_data_txt = glob(udm_para_in_path + "/**/metadata.txt", recursive = True)
# meta_data_csv = glob(udm_para_in_path + "/**/metadata.csv", recursive = True)
# attractors = glob(udm_para_in_path + "/**/attractors.csv", recursive = True)
# constraints = glob(udm_para_in_path + "/**/constraints.csv", recursive = True)

# if len(meta_data_txt)==1:
#     src = meta_data_txt[0]
#     dst = os.path.join(udm_para_out_path,'metadata.txt')
#     shutil.copy(src,dst)

# if len(meta_data_csv)==1:
#     src = meta_data_csv[0]
#     dst = os.path.join(udm_para_out_path,'metadata.csv')
#     shutil.copy(src,dst)

# if len(attractors)==1:
#     src = attractors[0]
#     dst = os.path.join(udm_para_out_path,'attractors.csv')
#     shutil.copy(src,dst)

# if len(constraints)==1:
#     src = constraints[0]
#     dst = os.path.join(udm_para_out_path,'constraints.csv')
#     shutil.copy(src,dst)

# #seems to be code assocaited with UDM model. comment it out for the moment
# #geojson = json.dumps({
# #    'type': 'Feature',
# #    'properties': {},
# #    'geometry': gpd.GeoSeries(box(*bounds), crs='EPSG:27700').to_crs(epsg=4326).iloc[0].__geo_interface__})
# print(title)

# print('Stage 10')

# # Print all of the input parameters to an excel sheet to be read in later
# with open(os.path.join(outputs_parameters_data,'citycat-parameters.csv'), 'w') as f:
#     f.write('PARAMETER,VALUE\n')
#     f.write('RAINFALL_MODE,%s\n' %rainfall_mode)
#     f.write('OPEN_BOUNDARIES,%s\n' %open_boundaries)
#     f.write('ROOF_STORAGE,%s\n' %roof_storage)
#     f.write('POST_EVENT_DURATION,%s\n' %post_event_duration)
#     f.write('OUTPUT_INTERVAL,%s\n' %output_interval)
#     if size != None:
#         f.write('SIZE,%s\n' %size)
#     if x != None:
#         f.write('X,%s\n' %x)
#     if y != None:
#         f.write('Y,%s\n' %y)
#     if time_horizon != None:
#         f.write('TIME_HORIZON,%s\n' %time_horizon)
#     if return_period != None:
#         f.write('RETURN_PERIOD,%s\n' %return_period)
#     if discharge_parameter != None:
#         f.write('DISCHARGE,%s\n' %discharge_parameter)

# # Move the amended parameter file to the outputs folder
# if len(parameter_file) != 1 :
#     for i in range (0, len(parameter_file)):
#         file_path = os.path.splitext(parameter_file[i])
#         #print('Filepath:',file_path)
#         #filename=file_path[0].split("/")
#         if os.name=='nt':
#             filename=file_path[0].split("\\")
#         else:
#             filename=file_path[0].split("/")
#         #print('Filename:',filename[-1])
    
#         src = parameter_file[i]
#         #print('src:',src)
#         dst = os.path.join(outputs_parameters_data,filename[-1] + '.csv')
#         #print('dst,dst')
#         shutil.copy(src,dst)

# # Moving essential files across:
# boundary_input_path = os.path.join(inputs_path,'boundary')
# boundary_file = glob(boundary_input_path + "/*.gpkg", recursive = True)
# print('boundary_file:',boundary_file)
# boundary_output_path = os.path.join(outputs_path,'boundary')
# if not os.path.exists(boundary_output_path):
#     os.mkdir(boundary_output_path)

# fi_input_path = os.path.join(inputs_path,'flood_impact')
# fi_file = glob(fi_input_path + "/*.gpkg", recursive = True)
# print('fi_file:',fi_file)
# fi_output_path = os.path.join(outputs_path,'flood_impact')
# if not os.path.exists(fi_output_path):
#     os.mkdir(fi_output_path)

# # Move the boundary file to the outputs folder
# if len(boundary_file) != 0 :
#     for i in range (0, len(boundary_file)):
#         file_path = os.path.splitext(boundary_file[i])
#         #filename=file_path[0].split("/")
#         if os.name=='nt':
#             filename=file_path[0].split("\\")
#         else:
#             filename=file_path[0].split("/")
    
#         src = boundary_file[i]
#         dst = os.path.join(boundary_output_path,filename[-1] + '.gpkg')
#         shutil.copy(src,dst)

# # Move the impact files to the outputs folder
# if len(fi_file) != 0 :
#     for i in range (0, len(fi_file)):
#         file_path = os.path.splitext(fi_file[i])
#         #filename=file_path[0].split("/")
#         if os.name=='nt':
#             filename=file_path[0].split("\\")
#         else:
#             filename=file_path[0].split("/")
    
#         src = fi_file[i]
#         dst = os.path.join(fi_output_path,filename[-1] + '.gpkg')
#         shutil.copy(src,dst)

# # Create metadata file
# logger.info('Building metadata file for DAFNI')
# metadata = f"""{{
#   "@context": ["metadata-v1"],
#   "@type": "dcat:Dataset",
#   "dct:language": "en",
#   "dct:title": "{title}",
#   "dct:description": "{description}",
#   "dcat:keyword": [
#     "citycat"
#   ],
#   "dct:subject": "Environment",
#   "dct:license": {{
#     "@type": "LicenseDocument",
#     "@id": "https://creativecommons.org/licences/by/4.0/",
#     "rdfs:label": null
#   }},
#   "dct:creator": [{{"@type": "foaf:Organization"}}],
#   "dcat:contactPoint": {{
#     "@type": "vcard:Organization",
#     "vcard:fn": "DAFNI",
#     "vcard:hasEmail": "support@dafni.ac.uk"
#   }},
#   "dct:created": "{datetime.now().isoformat()}Z",
#   "dct:PeriodOfTime": {{
#     "type": "dct:PeriodOfTime",
#     "time:hasBeginning": null,
#     "time:hasEnd": null
#   }},
#   "dafni_version_note": "created",
#   "dct:spatial": {{
#     "@type": "dct:Location",
#     "rdfs:label": null
#   }},
# }}
# """
# with open(os.path.join(run_path, 'metadata.json'), 'w') as f:
#     f.write(metadata)
