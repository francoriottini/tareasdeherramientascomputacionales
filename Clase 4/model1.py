"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFeatureSink)
import processing

# se establecen los parametros iniciales para la creacion del modelo 1

class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use una retroalimentación de varios pasos progreso del algoritmo secundario se ajustan para el progreso general a través del modelo.
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        # Filtra entidades de la capa de entrada y las redirige a una o varias salidas
        # Arreglar la geometrias para procesar el shapefile
        
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/langa/langa/langa.shp',  # capa entrante
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11'] # las capas salientes con filtros
        }
        outputs['FiltroDeEntidad'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FiltroDeEntidad']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos
        # Creo una columna con el largo de la columna "NAME_PROP" solo para
        # poder seleccionar segun el numero de caracteres
        alg_params = {
            'FIELD_LENGTH': 2, # longitud del campo
            'FIELD_NAME': 'length',  # nombre del campo para los resultados
            'FIELD_PRECISION': 0, # precisión del campo
            'FIELD_TYPE': 1,  #  tipo de campo en este caso entero
            'FORMULA': 'length(NAME_PROP)', # fórmula para calcular el resultado
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'OUTPUT': parameters['Length'] # especificación de la capa saliente
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos en forma de clone modificado
        alg_params = {
            'FIELD_LENGTH': 10, # longitud del campo
            'FIELD_NAME': 'lnm', # nombre del campo para los resultados
            'FIELD_PRECISION': 0, # precisión del campo
            'FIELD_TYPE': 2,  # #  tipo de campo en este caso cadena
            'FORMULA': '"NAME_PROP"', # fórmula para calcular el resultado
            'INPUT': outputs['FeatureFilter']['OUTPUT_menor_a_11'],
            'OUTPUT': parameters['Field_calc'] # especificación de la capa saliente
        }
        outputs['CalculadoraDeCamposClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['CalculadoraDeCamposClone']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # # Quita las columnas nombradas de la forma '....' de la tabla
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': outputs['FieldCalculatorClone']['OUTPUT'],
            'OUTPUT': parameters['Wldsout']
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # crea una representación válida de una geometría no válidaa
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/langa/langa/langa.shp', # capa de vector de entrada
            'OUTPUT': parameters['Fix_geo'] # especifica la capa vectorial saliente
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Agregar campo autoincremental mediante una nueva capa
        alg_params = {
            'FIELD_NAME': 'GID', # nombre del campo con valores autoincremental
            'GROUP_FIELDS': [''], #elige los campos 
            'INPUT': outputs['CorregirGeometras']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True, # controla el orden en el que se asignan valores  
            'SORT_EXPRESSION': '', # ordena las entidades de la capa de forma global
            'SORT_NULLS_FIRST': False, # establece que los valores nulos se cuentan al final
            'START': 1,
            'OUTPUT': parameters['Autoinc_id'] # capa vectorial con campo autoincremental
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']
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
