global INPUT "C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 3/Data"

use "$INPUT/Crimen/MD_crime_2015_wide.dta"

egen objectid = concat(ID month), punct(-)
