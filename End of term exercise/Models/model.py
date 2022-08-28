"""
Model exported as python.
Name : model
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids', 'centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Totsla1500', 'totsla1500', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Slavetrade', 'Slavetrade', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Borderstribes', 'borderstribes', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ExplorerRoutes', 'Explorer routes', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Fix geometries - explorer routes
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/TRABAJO FINAL/pre_colonial_africa_explorer_routes/Explorer_Routes_Final.shp',
            'OUTPUT': parameters['ExplorerRoutes']
        }
        outputs['FixGeometriesExplorerRoutes'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ExplorerRoutes'] = outputs['FixGeometriesExplorerRoutes']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Fix geometries - borders_tribes
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/TRABAJO FINAL/murdock_shapefile/borders_tribes.shp',
            'OUTPUT': parameters['Borderstribes']
        }
        outputs['FixGeometriesBorders_tribes'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Borderstribes'] = outputs['FixGeometriesBorders_tribes']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Fix geometries - slave trade
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/TRABAJO FINAL/BaseNunnModificada.shp',
            'OUTPUT': parameters['Slavetrade']
        }
        outputs['FixGeometriesSlaveTrade'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Slavetrade'] = outputs['FixGeometriesSlaveTrade']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Field calculator - total slave exports
        # We replicated at hand this path to form the 1600, 1700 and 1800.
        alg_params = {
            'FIELD_LENGTH': 100000000,
            'FIELD_NAME': 'totsla1500',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': 'atlantic_n + indian_num',
            'INPUT': outputs['FixGeometriesSlaveTrade']['OUTPUT'],
            'OUTPUT': parameters['Totsla1500']
        }
        outputs['FieldCalculatorTotalSlaveExports'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Totsla1500'] = outputs['FieldCalculatorTotalSlaveExports']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Centroids
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['FixGeometriesSlaveTrade']['OUTPUT'],
            'OUTPUT': parameters['Centroids']
        }
        outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids'] = outputs['Centroids']['OUTPUT']
        return results

    def name(self):
        return 'model'

    def displayName(self):
        return 'model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model()
