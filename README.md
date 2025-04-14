# optimise-seup
This model takes data provided by other models and converts it to the correct format for the CityCAt optimisation model.

## Description
The CityCAT optimisation model needs DEM, buildings and green-areas data in the right format. This is achived by this model


## Input Files (data slots)
* Buildings
  * Description: gpkg file of the buildings
  * Location: /data/buildings
* Green_areas
  * Description: A .gpkg of the green-areas. 
  * Location: /data/green_areas
* dem
  * Description: An asc dem
  * Location: /data/dem

## Outputs
* Buildings
  * Description: shape file of the buildings
  * Location: /data/buildings
* Green-areas
  * Description: GreenAreas.txt and GreenAreas_0.txt of the green areas
  * Location: /data/green-areas
* dem
  * Description: Baseline_DEM.asc, DEM.asc, Domain_DEM.asc
  * Location: /data/dem
