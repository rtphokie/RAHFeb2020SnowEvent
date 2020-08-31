rm -Rf shapefiles/20200220NCSnowForecasts shapefiles/20200220NCSnowResults
mkdir shapefiles/20200220NCSnowForecasts
mkdir shapefiles/20200220NCSnowResults
ogr2ogr -f "ESRI Shapefile" "shapefiles/20200220NCSnowForecasts" "KML/20200220NCSnowForecasts.kml" -dim 2
ogr2ogr -f "ESRI Shapefile" "shapefiles/20200220NCSnowResults" "KML/20200220NCSnowResults.kml" -dim 2
