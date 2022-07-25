"""
Calculamos centroides y distancia mìnima a la costa
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# se establecen los parametros iniciales para la creacion del modelo 4b
class Model4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coastline', 'fixgeo_coastline', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_distance_joined', 'centroids_nearest_coast_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_w_coord', 'centroids_w_coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use una retroalimentación de varios pasos progreso del algoritmo secundario se ajustan para el progreso general a través del modelo.
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}

        # # Arregla geometrias. Crea una representación válida de una geometría no válidaa de los paises
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', # capa de vector de entrada
            'OUTPUT': parameters['Fixgeo_countries'] # especifica la capa vectorial saliente
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla de centroids_coast_joint
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Joined_layer_52b79c0f_a990_4729_a223_ec167639eb97',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['DropFieldsFromCentroids_coas_joint'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['DropFieldsFromCentroids_coas_joint']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Agregar atributos de geometría. Calcula las propiedades geométricas de los objetos de una capa vectorial y las incluye en la capa resultado
        alg_params = {
            'CALC_METHOD': 0,  # Cálculo de los parámetros a usar para las propiedades geométricas. 0 es SRC de la Capa
            'INPUT': 'Remaining_fields_77183d4e_408d_4e93_9406_14e51d89eaaf',
            'OUTPUT': parameters['Add_geo_coast'] # Especificar la capa de salida
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AddGeometryAttributes']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos. Abre la calculadora de campos
        alg_params = {
            'FIELD_LENGTH': 4, # longitud del campo
            'FIELD_NAME': 'cat', # nombre del campo para los resultados
            'FIELD_PRECISION': 3, # precisión del campo resultante
            'FIELD_TYPE': 1,  # tipo de campo: Integer
            'FORMULA': "attribute($currentfeature, 'cat')-1", # fórmula a emplear para calcular el resultado
            'INPUT': outputs['Vdistance']['from_output'],
            'OUTPUT': parameters['Nearest_cat_adjust'] # especificación de la capa saliente
        }
        outputs['FieldCalculatorCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorCatAdjust']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Agregar atributos de geometría. Calcula las propiedades geométricas de los objetos de una capa vectorial y las incluye en la capa resultado.
        alg_params = {
            'CALC_METHOD': 0,  # Cálculo de los parámetros a usar para las propiedades geométricas. 0 SRC de la Capa
            'INPUT': outputs['Centroids']['OUTPUT'],
            'OUTPUT': parameters['Centroids_w_coord'] # Especificar la capa de salida
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AddGeometryAttributes']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extraer por atributo. Crea dos capas vectoriales a partir de una capa de entrada: una contendrá solo entidades coincidentes mientras que la segunda contendrá todas las entidades no coincidentes.
        alg_params = {
            'FIELD': 'distance', # campo de filtrado de la capa
            'INPUT': 'Vertices_1966fc2f_a721_4371_967d_fa6a4a4de95d',
            'OPERATOR': 2,  # es >
            'VALUE': '0', # valor a evaluar
            'OUTPUT': parameters['Extract_by_attribute'] # especifica la capa vectorial saliente para la conincidencia de entidades
        }
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos - coast_lat
        alg_params = {
            'FIELD_LENGTH': 10, # longitud del campo resultante
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10, # precisión del campo resultante
            'FIELD_TYPE': 0,  # tipo de campo: float
            'FORMULA': "attribute($currentfeature, 'ycoord')", # fórmula a emplear para calcular el resultado
            'INPUT': 'Added_geom_info_d84ade8a_3eba_4f89_ab7a_9023cf8e9951', # capa en la que calcular
            'OUTPUT': parameters['Added_field_coast_lat'] # especificación de la capa saliente
        }
        outputs['FieldCalculatorCoast_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['FieldCalculatorCoast_lat']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Unir atributos por valor de campo. Toma una capa de vector de entrada y crea una nueva capa de vector que es una versión extendida de la de entrada, con atributos adicionales en su tabla de atributos
        alg_params = {
            'DISCARD_NONMATCHING': False,  # Compruebe si no desea conservar los objetos que no se pudieron unir
            'FIELD': 'cat',  #Campo de la capa fuente a usar para la unión
            'FIELDS_TO_COPY': [''],  # Seleccione los campos específicos que desea agregar. De forma predeterminada, se agregan todos los campos.
            'FIELD_2': 'cat',  #Campo de la segunda capa (unión) que se utilizará para la combinación
            'INPUT': 'output_87ba0daa_6155_4484_ad84_d4606bb3a0e8',  # Capa de vector de entrada
            'INPUT_2': 'Remaining_fields_fe4bd62f_de5b_4307_83d4_507e2d9f957f',  # Capa con la tabla de atributos a unir
            'METHOD': 1,  # El tipo de capa unida final. 1 : Tomar atributos de la primera entidad coincidente únicamente (uno a uno)
            'PREFIX': '',  # Agregue un prefijo a los campos unidos para identificarlos fácilmente y evitar la colisión de nombres de campo
            'OUTPUT': parameters['Centroids_nearest_coast_distance_joined']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_joined'] = outputs['JoinAttributesByFieldValue']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo - cent_lon
        alg_params = {
            'FIELD_LENGTH': 10, # longitud del campo resultante
            'FIELD_NAME': 'cent_lon', # nombre del campo para los resultados
            'FIELD_PRECISION': 10,  # precisión del campo resultante 
            'FIELD_TYPE': 0,  # El tipo de campo: float 
            'FORMULA': "attribute($currentfeature, 'xcoord')",
            'INPUT': 'Calculated_5e74f333_fd0d_4a3e_a69c_230adb9a73a4',
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['FieldCalculatorCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['FieldCalculatorCent_lon']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo - coast_lon
        alg_params = {
            'FIELD_LENGTH': 10, # longitud del campo resultante
            'FIELD_NAME': 'coast_lon', # nombre del campo para los resultados
            'FIELD_PRECISION': 10, # precisión del campo resultante 
            'FIELD_TYPE': 0,  # tipo de campo: float 
            'FORMULA': "attribute($currentfeature, 'xcoord')",
            'INPUT': 'Calculated_8bfa95cb_8620_4b47_9b3d_721dbd91c1f0',
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['FieldCalculatorCoast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['FieldCalculatorCoast_lon']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla cent_lat_lon
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': 'Calculated_a3d7236e_5101_4f9e_b2c6_fdd1b2645f80',
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['DropFieldsFromCent_lat_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['DropFieldsFromCent_lat_lon']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla centroid_w_coord
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': 'Added_geom_info_c32036b7_cda3_4cb3_a11b_3714a82b9b00',
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['DropFieldsFromCentroid_w_coord'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['DropFieldsFromCentroid_w_coord']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Unir atributos por valor de campo. Toma una capa de vector de entrada y crea una nueva capa de vector que es una versión extendida de la de entrada, con atributos adicionales en su tabla de atributos. - centroids y coast
        alg_params = {
            'DISCARD_NONMATCHING': False,  #Compruebe si no desea conservar los objetos que no se pudieron unir
            'FIELD': 'ISO_A3',  #Campo de la capa fuente a usar para la unión
            'FIELDS_TO_COPY': [''],  #Seleccione los campos específicos que desea agregar. De forma predeterminada, se agregan todos los campos.
            'FIELD_2': 'ISO_A3',  #Campo de la segunda capa (unión) que se utilizará para la combinación El tipo de campo debe ser igual (o compatible) con el tipo de campo de la tabla de entrada.
            'INPUT': 'Remaining_fields_8331b36f_9867_40fd_8505_52df796da935',  #Capa de vector de entrada
            'INPUT_2': 'Remaining_fields_b30e4b15_f3e6_4939_ac58_56d84622efde',  #Capa con la tabla de atributos a unir
            'METHOD': 1,  # El tipo de capa unida final: 1 — Tomar atributos de la primera entidad coincidente únicamente (uno a uno)
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined'] #  Especifica la capa vectorial saliente para la unión
        }
        outputs['JoinAttributesByFieldValueCentroidsYCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['JoinAttributesByFieldValueCentroidsYCoast']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Arregla geometria. Crea una representación válida de una geometría no válida - coastline
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/ne_10m_coastline/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coastline']
        }
        outputs['FixGeometriesCoastline'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coastline'] = outputs['FixGeometriesCoastline']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Centroides. Crea una nueva capa de puntos, con puntos representado los centroides de las geometrías de la capa de entrada.
        alg_params = {
            'ALL_PARTS': False, # Si es verdadero (marcado), un centroide puede ser creado para cada parte de la geometría
            'INPUT': outputs['FixGeometriesCountries']['OUTPUT'], # Capa de vector de entrada
            'OUTPUT': parameters['Country_centroids'] # Especifica la capa de salida (centroide)
        }
        outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['Centroids']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla coast_lon
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_ea5aa226_0b17_4cfa_b2e7_1a89b8a851ad',
            'OUTPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/output/csvout.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFieldsFromCoast_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Extraer vértices. Toma una capa vectorial y genera una capa de puntos con puntos representando los vértices en las geometrías de entrada.
        alg_params = {
            'INPUT': 'Joined_layer_9795745b_6353_4bdf_addf_9e2c5a4aec10',  # Capa de vector de entrada
            'OUTPUT': parameters['Extract_vertices']  # Especifica la capa vectorial saliente
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        #  Quita las columnas nombradas de la forma '....' de la tabla nearest_cat_adjust
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': 'Calculated_c9dd1acd_cc82_4587_a498_b810cfb65a3d',
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['DropFieldsFromNearest_cat_adjust'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsFromNearest_cat_adjust']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo
        alg_params = {
            'FIELD_LENGTH': 10,  # longitud del campo 
            'FIELD_NAME': 'cent_lat', # nombre del campo para los resultados
            'FIELD_PRECISION': 10, # precisión del campo resultante
            'FIELD_TYPE': 0,  # tipo de campo: float
            'FORMULA': "attribute($currentfeature, 'ycoord')",
            'INPUT': 'Extracted__attribute__3f6526dc_a44f_42eb_8490_c0e2b60738e1',
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['FieldCalculatorCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCent_lat']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla fixgeo_coastline
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': 'Fixed_geometries_19aef157_f33b_4792_8a27_efb167921eaa',
            'OUTPUT': parameters['Coastout']
        }
        outputs['DropFieldsFromFixgeo_coastline'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['DropFieldsFromFixgeo_coastline']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # v.distance. encuentra el elemento más cercano en el mapa vectorial 'hasta' para los elementos en el mapa vectorial 'desde'
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': outputs['DropFieldsFromCentroid_w_coord']['OUTPUT'],
            'from_type': [0,1,3],  # point,line,area
            'to': outputs['DropFieldsFromFixgeo_coastline']['OUTPUT'],
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']
        return results

#define elementos
    def name(self):
        return 'model4b'

    def displayName(self):
        return 'model4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()
