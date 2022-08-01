/************************************************************************************
Tarea 2 de la clase 5 de herramientas computacionales para la investigación científica.

RECORDATORIO: en las primeras lineas cambiar el repositorio desde donde se están tomando la base de datos.

*/
global DATA = "C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 5/videos 2 y 3 2022/videos 2 y 3/data" 
cd "$DATA"

********************************************************************************************
/* 					  INSTALACIÓN DE LOS PAQUETES NECESARIOS    						  */
********************************************************************************************

ssc install spmap
ssc install shp2dta
*net install sg162, from(http://www.stata.com/stb/stb60)
*net install st0292, from(http://www.stata-journal.com/software/sj13-2)
net install spwmatrix, from(http://fmwww.bc.edu/RePEc/bocode/s)
*net install splagvar, from(http://fmwww.bc.edu/RePEc/bocode/s)
*ssc install xsmle.pkg
*ssc install xtcsd
*net install st0446.pkg

*Cargamos la base de datos

use london_crime_shp.dta, clear

*Para las etiquetas
keep x_c y_c name
save "labels.dta", replace

*Cargamos nuevamente la base

use london_crime_shp.dta, clear

*Armamos el mapa

spmap crimecount using coord_ls, id(id) clmethod(q) cln(5) label(data("labels.dta") x(x_c) y(y_c) label(name) size(tiny)) legend(size(vsmall) position(5) xoffset(1.55)) legtitle("Amount of thefts") fcolor(Blues2) plotregion(margin(b+15)) ndfcolor(gray) name(graf3,replace)

*Guardamos (recordar cambiar path)

graph export "C:\Users\Franco\Desktop\UDESA\Herramientas computacionales\Clase 5\graf3.png", as(png) name("graf3
> ") replace



