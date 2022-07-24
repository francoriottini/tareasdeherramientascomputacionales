"""
Model exported as python.
Name : model2
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing

# se establecen los parametros iniciales para la creacion del modelo 2
class Model2(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use una retroalimentación de varios pasos progreso del algoritmo secundario se ajustan para el progreso general a través del modelo.
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
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
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout'] # especifica la capa vectorial saliente
        }
        outputs['CombarReproyectar'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['CombarReproyectar']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Extrae la proyección
        alg_params = {
            'INPUT': outputs['CombarReproyectar']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        outputs['ExtraerProyeccin'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results
# define elementos
    def name(self):
        return 'model2'

    def displayName(self):
        return 'model2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model2()
