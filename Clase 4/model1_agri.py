"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing

# se establecen los parametros iniciales para la creacion del modelo 1
class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Agrisuit', 'agrisuit', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Counties', 'counties', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal', 'Zonal', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Reproyecta una capa vectorial en un SRC diferente
        alg_params = {
            'DATA_TYPE': 0,  # Usar el tipo de datos de la capa de entrada
            'EXTRA': '',
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/SUIT/suit/hdr.adf', # elige la capa vectorial entrante a reproyectar
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # vecino más próximo
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'), # sistema de coordenadas de referencia de destino
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Agrisuit'] # especifica la capa vectorial saliente
        }
        outputs['CombarReproyectar'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Agrisuit'] = outputs['CombarReproyectar']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla
        alg_params = {
            'COLUMN': ['GID_0','NAME_0','GID_1','GID_2','HASC_2','CC_2','TYPE_2','NL_NAME 2','VARNAME_2','NL_NAME_1','NL_NAME_2',' ENGTYPE_2'],
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/gadm41_USA/gadm41_USA_2.shp', # Guarda el archivo como .shp file
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Agregar campo autoincremental mediante una nueva capa 
        alg_params = {
            'FIELD_NAME': 'cid', # nombre del campo con valores autoincremental
            'GROUP_FIELDS': [''],  #elige los campos 
            'INPUT': outputs['QuitarCampos']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,  # controla el orden en el que se asignan valores  
            'SORT_EXPRESSION': '', # ordena las entidades de la capa de forma global
            'SORT_NULLS_FIRST': False, # establece que los valores nulos se cuentan al final
            'START': 1,
            'OUTPUT': parameters['Counties'] # capa vectorial con campo autoincremental
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Counties'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Estadísticas de zona
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': outputs['AgregarCampoQueAutoincrementa']['OUTPUT'],
            'INPUT_RASTER': outputs['CombarReproyectar']['OUTPUT'], # capa ráster de entrada
            'RASTER_BAND': 1, # elije una banda
            'STATISTICS': [2],  # calcula la media
            'OUTPUT': parameters['Zonal'] # capa de polígono de vector de salida
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonal'] = outputs['EstadsticasDeZona']['OUTPUT']
        return results

    
 # define elementos
    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
