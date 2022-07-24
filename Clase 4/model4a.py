"""
Model exported as python.
Name : model4a
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# se establecen los parametros iniciales para la creacion del modelo 4a
class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Calcula las estadísticas de un campo en función de una clase principal
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'], # los campos combinados definen las categorías
            'INPUT': 'Intersection_9368dc74_2d3a_4a25_a0e5_5a11925ea511',
            'OUTPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/output/laguages_by_country.csv',
            'VALUES_FIELD_NAME': '', # si está vacío solo se calcula el recuento
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT # tabla para las estadísticas generadas
        }
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Arregla geometrias. Crea una representación válida de una geometría no válidaa de los paises
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', # capa de vector de entrada
            'OUTPUT': parameters['Fixgeo_countries'] # especifica la capa vectorial saliente
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Arregla geometrias. Crea una representación válida de una geometría no válidaa de wlds
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/clean.shp', # capa de vector de entrada
            'OUTPUT': parameters['Fixgeo_wlds'] # especifica la capa vectorial saliente
        }
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # extrae las partes de entidades de la capa de entrada que se superponen a entidades en la capa de superposición
        alg_params = {
            'INPUT': outputs['FixGeometriesWlds']['OUTPUT'], # capa de la que extraer entidades
            'INPUT_FIELDS': ['GID'], # campos de la capa de entrada para mantener en la salida. Si no se elige ningún campo, se toman todos los campos
            'OVERLAY': outputs['FixGeometriesCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'], # campos de la capa de superposición para mantener en la salida. Si no se elige ningún campo, se toman todos los campos
            'OVERLAY_FIELDS_PREFIX': '', # prefijo para agregar a los nombres de campo de los campos de la capa de intersección para evitar colisiones de nombres con campos en la capa de entrada
            'OUTPUT': parameters['Intersection'] # especifique la capa para contener las partes de las entidades de la capa de entrada que se superponen a una o más entidades de la capa superpuesta.
        }
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Intersection']['OUTPUT']
        return results
 
 # define elementos
 
    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()
