mkdir shapefiles/WRAL
mkdir shapefiles/WTVD
mkdir shapefiles/WNCN
mkdir shapefiles/Spectrum
mkdir "shapefiles/NWS Final"
ogr2ogr -f "ESRI Shapefile" "shapefiles/Spectrum/Spectrum.shp" "KML/Spectrum.kml" -dim 2 
ogr2ogr -f "ESRI Shapefile" "shapefiles/WNCN/WNCN.shp" "KML/WNCN.kml" -dim 2 
ogr2ogr -f "ESRI Shapefile" "shapefiles/WRAL/WRAL.shp" "KML/WRAL.kml" -dim 2 
ogr2ogr -f "ESRI Shapefile" "shapefiles/WTVD/WTVD.shp" "KML/WTVD.kml" -dim 2 
ogr2ogr -f "ESRI Shapefile" "shapefiles/NWS Final/NWS Final.shp" "KML/NWS Final.kml" -dim 2 
