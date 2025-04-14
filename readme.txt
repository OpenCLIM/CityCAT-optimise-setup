cmd in folder C:\Users\steve\Documents\CityCAT-dafni\CityCAT-optimise-setup
start docker desktop
docker build -t optimise-setup .
Run container in Docker Desktop. In Images find optimise-setup. Click on the play button. Then "optional settings" and call "Container name" something like "global-flood-impact-optimise-setup"
or docker run --name global-flood-impact-optimise-setup optimise-setup 

docker cp global-flood-impact-optimise-setup:/data/outputs/dem/Domain_DEM.asc ./Domain_DEM.asc

docker save -o optimise-setup.tar optimise-setup
compress optimise-setup.tar to optimise-setup.tar.gz using 7Zip add to archive




change to produce buildings.txt not buildings shape files
docker cp global-flood-impact-optimise-setup:/data/outputs/buildings/Buildings.txt ./Buildings.txt




superceded stuff
****************

Anaconda3 prompt
conda activate myenv2
cd C:\Users\steve\Documents\CityCAT-dafni\global-flood-impacts-frictioncoeffs-0.0.1
setenv.bat
spyder

in two places:
if os.name=='nt':
    filename=file_path[0].split("\\")
else:
    filename=file_path[0].split("/")


conda create -n myenv rasterio geopandasconda activate myenv
pip install citycatio
pip install pyogrio
pip install spyder


myenv citycatio files are in C:\Users\steve\anaconda3\envs\myenv\Lib\site-packages\citycatio>

Changes to:
1) run.py. a) different folder structure for parameter.csv and green_areas in DOCKER and NON DOCKER versions and b) xarrays ufunc changed to numpy c) rio.set.crs changed to rio.write.crs d) friction added to model call e) comment out figure creation near end f) read spatial rainfall if rainfall polygons exist. g) add rainfall_polygons to Model call h) read infiltration parameters if file exists and check if "value" exists in greenareas shape file if infiltration parameters exists i) add infiltration parameters to model call j) read reservoir data if it exists k) add reservoir to model call
2) utils.py modify for correct application of friction coeffs and sptial infiltration
3) friction.py allows friction coeffs (updated)
4) rainfall.py linetermination issues with different versions of the same package
5) rainfall_polygons.py change geoseries to GeoDataFrame
6) model.py a) add infiltration_parameters to init and configuration call b) a) add reservoir to init and write definitions
7) green_areas.py choice of green areas or spatial green areas
8) configuration.py a) allow infiltration parameters in init and write b) allow init_surface_water_elv in init and write
9) in inputs/_init_.py add reservoir.py
10) create reserovir.py

python run.py




cmd in folder C:\Users\steve\Documents\CityCAT-dafni\global-flood-impacts-frictioncoeffs-0.0.1
docker build -t friction-coeffs .


docker build -t Global Urban_Flooding:Friction-coeffs .
Run container in Docker Desktop. In Images find friction-coeffs. Click on the play button. Then "optional settings" and call "Container name" something like "friction-coeffs"
A new Container called "fraction-coeffs" is produced.
*** not needed as default **** Enivonment Variables DATA_PATH /data

The Dockerfile spefies that this reads script.py into the src folder and the data into the /data folder in the container. then python script.py is run.

The output is in the Docker container. to view output copy it to a local path
docker cp friction-coeffs:/data/outputs/FrictionCoeffs.txt ./FrictionCoeffs.txt


https://docs.docker.com/guides/walkthroughs/run-a-container/
https://docs.docker.com/reference/cli/docker/container/cp/


docker save -o friction-coeffs.tar friction-coeffs
compress friction-coeffs.tar to friction-coeffs.tar/gz using 7Zip add to achive



set DATA_PATH=C:\Users\steve\Documents\citycat\CityCAT-FrictionCoeffs-Docker\data
set DATA_PATH=C:\Users\steve\Documents\citycat\CityCAT-SecondModel-Docker\data
set NUMBER_TEST=5 or  Enivonment Variables NUMBER_TEST 5 
docker system prune -a


in run.py

    #filename=file_path[0].split("\")
    filename=file_path[0].split("\\")




additional environment variables. The others come from the command line in:
https://github.com/OpenCLIM/citycat-dafni/tree/master

NAME=test
OUTPUT_INTERVAL=3600

setenv.bat
set PYTHONUNBUFFERED=1
set RAINFALL_MODE=total_depth
set SIZE=0.1
set DURATION=1
set POST_EVENT_DURATION=0
set TOTAL_DEPTH=40
set RETURN_PERIOD=100
set X=258722
set Y=665028
set OPEN_BOUNDARIES=True
set PERMEABLE_AREAS=polygons
set ROOF_STORAGE=0
set TIME_HORIZON=2050
set DATA_PATH=C:\Users\steve\Documents\citycat-dafni-0.20.4\data
set NAME=test
set OUTPUT_INTERVAL=3600


C:\Users\steve\anaconda3\envs\myenv\lib\site-packages\citycatio\inputs\rainfall.py:37: FutureWarning: DataFrame.applymap has been deprecated. Use DataFrame.map instead.
  self.data.applymap(float_to_str).to_csv(f, sep=' ', header=False, line_terminator='\n')


In rainfall.py
            self.data.applymap(float_to_str).to_csv(f, sep=' ', header=False, line_terminator='\n')
            self.data.applymap(float_to_str).to_csv(f, sep=' ', header=False, lineterminator='\n')



velocity = xr.ufuncs.sqrt(a.x_vel**2+a.y_vel**2).astype(np.float64)
Xarray’s ufuncs have been removed, now that they can be replaced by numpy’s ufuncs in all supported versions of numpy. 

#velocity = xr.ufuncs.sqrt(a.x_vel**2+a.y_vel**2).astype(np.float64)
velocity = np.sqrt(a.x_vel**2+a.y_vel**2).astype(np.float64)
max_velocity = max_velocity.where(np.isfinite(max_velocity), other=output.fill_value)
#max_velocity = max_velocity.where(xr.ufuncs.isfinite(max_velocity), other=output.fill_value)
#max_velocity.rio.set_crs('EPSG:27700')
max_velocity.rio.write_crs('EPSG:27700')
max_vd_product = max_vd_product.where(np.isfinite(max_vd_product), other=output.fill_value)
#max_vd_product = max_vd_product.where(xr.ufuncs.isfinite(max_vd_product), other=output.fill_value)
#max_vd_product.rio.set_crs('EPSG:27700')
max_vd_product.rio.write_crs('EPSG:27700')


C:\Users\steve\anaconda3\envs\myenv\lib\site-packages\citycatio\utils.py

add

def geoseries_with_value_to_string(geoseries: gpd.GeoSeries, value, index=False, index_first=True):
    """GeoSeries to CityCAT string representation

    Args:
        geoseries: Polygons to convert
        value: Fraction coefficient value
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
            s += '{} {}'.format(idx, len(geometry.exterior.coords))
        else:
            s += '{} {}'.format(len(geometry.exterior.coords), value[idx])
        x, y = geometry.exterior.coords.xy
        for x_val in x:
            s += ' {}'.format(x_val)
        for y_val in y:
            s += ' {}'.format(y_val)
        s += '\n'

    return s

C:\Users\steve\anaconda3\envs\myenv\lib\site-packages\citycatio\inputs\friction.py

from ..utils import geoseries_with_value_to_string

    def write(self, path):
        with open(os.path.join(path, 'FrictionCoeffs.txt'), 'w') as f:
            f.write(geoseries_with_value_to_string(self.data.geometry,self.data.Value,index=True, index_first=False))


plus add frction stuff to run.py


myenv
C:\Users\steve\anaconda3\envs\myenv\Lib\site-packages\citycatio>

# If a parameter.csv is available: read the variables from the document
if len(parameter_file) == 1 :
    file_path = os.path.splitext(parameter_file[0])
    print('Filepath:',file_path)
    #filename=file_path[0].split("\")
    filename=file_path[0].split("\\")
    print('Filename:',filename[-1])



