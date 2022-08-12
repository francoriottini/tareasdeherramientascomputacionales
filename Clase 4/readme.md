Python files replicating Michalopoulus (2012, AER).
--------------------
Files information:
-------------------
* model1.py: It's an example model to learn how to create models in QGIS that can be extrapolated to Python.
* model1_agri.py: Preparing the shapefile World Language Mappin System using the langa.shp file downloaded from: worldgeodatasets.com/language.
* model2.py: Preparing the agricultural suitability raster. Original raster from: https://sage.nelson.wisc.edu/?incdataset=Suitability%20for%20Agriculture is used
* model3.py: Code to generate a raster file by country that includes the mean popd of 1800, 1900 and 2000. The shp from: http://www.naturalearthdata.com/downloads/%2010m-cultural-vectors/10m-admin-0-countries/ is used for countries. Raster from: https://dataportaal.pbl.nl/downloads/HYDE/HYDE3.0/
in this last link the files of 1800, 1900 and 2000 are used.
* model4a.py: Code to generate the number of languages by country, distance and areas, using the WLMS of model1 and intersecting with the countries shp. The langa.shp file downloaded from: worldgeodatasets.com/language is used.
and the shp from: http://www.naturalearthdata.com/downloads/%2010m-cultural-vectors/10m-admin-0-countries/ is also used.
* model4b.py: We calculate centroids and minimum distance to the coast.
* model4c.py: We calculate the area of the countries. The countries shp used is: http://www.naturalearthdata.com/downloads/%2010m-cultural-vectors/10m-admin-0-countries/
