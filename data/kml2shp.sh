mkdir shapefiles/20200220NCSnowForecasts
mkdir shapefiles/20200220NCSnowResults
ogr2ogr -f "ESRI Shapefile" "shapefiles/20200220NCSnowForecasts/20200220NCSnowForecasts.shp" "KML/20200220NCSnowForecasts.kml" -dim 2
ogr2ogr -f "ESRI Shapefile" "shapefiles/20200220NCSnowResults/20200220NCSnowResults.shp" "KML/20200220NCSnowResults.kml" -dim 2
