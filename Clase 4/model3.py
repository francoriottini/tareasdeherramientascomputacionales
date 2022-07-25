"""
Model exported as python.
Name : model3
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# se establecen los parametros iniciales para la creacion del modelo 3
class Model3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo_3', 'fix_geo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use una retroalimentación de varios pasos progreso del algoritmo secundario se ajustan para el progreso general a través del modelo.
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}

        # Estadísticas de zona
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Campos_restantes_5fa3a83a_7c84_4a0c_804c_805023db7c09',
            'INPUT_RASTER': 'landquality_19a06321_f915_45c1_8741_e156742b9baa', # capa ráster de entrada
            'RASTER_BAND': 1, # elije una banda
            'STATISTICS': [2],   # calcula la media
            'OUTPUT': parameters['Landq'] # capa de polígono de vector de salida
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Estadísticas de zona
        alg_params = {
            'COLUMN_PREFIX': 'pop1900',
            'INPUT': 'Estadistica_zonal_51b7ae4c_895a_465b_a163_18fbf6cb5cba',
            'INPUT_RASTER': 'popd_1900AD_909d2ce0_1ec7_45e6_96bf_ee499df268ea', # capa ráster de entrada
            'RASTER_BAND': 1, # elije una banda
            'STATISTICS': [2],  # calcula la media
            'OUTPUT': parameters['Pop1900'] # capa de polígono de vector de salida
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Estadísticas de zona
        alg_params = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': 'Estadistica_zonal_4bf51785_ffb5_43ee_bf9d_7f44ba8372de',
            'INPUT_RASTER': 'popd_1800AD_2dfdecf5_d20f_4f85_ad5e_a81c48c744a5', # capa ráster de entrada
            'RASTER_BAND': 1, # elije una banda
            'STATISTICS': [2],  # calcula la media
            'OUTPUT': parameters['Pop1800'] # capa de polígono de vector de salida
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Guardar objetos vectoriales en archivo
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Estadistica_zonal_34814cdd_3371_42d8_95a4_761e0953a3a2', # capa vectorial de polígonos entrante
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/output/raster_stats.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT # salida de puntos aleatorios
        }
        outputs['GuardarObjetosVectorialesEnArchivo'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Quita las columnas nombradas de la forma '....' de la tabla
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Geometr_as_corregidas_dfc9dba5_429c_4d07_b74c_4008844e25b2',
            'OUTPUT': parameters['Drop_fields_3']
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Estadísticas de zona
        alg_params = {
            'COLUMN_PREFIX': 'pop2000',
            'INPUT': 'Estadistica_zonal_b93e141b_bbc8_425b_b3db_1d363b89285a',
            'INPUT_RASTER': 'popd_2000AD_09e35551_147e_4753_bbff_dbd6ff5df28a', # capa ráster de entrada
            'RASTER_BAND': 1, # elije una banda
            'STATISTICS': [2],  # calcula la media
            'OUTPUT': parameters['Pop2000'] # capa de polígono de vector de salida
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

         # crea una representación válida de una geometría no válida
        alg_params = {
            'INPUT': 'C:/Users/Franco/Desktop/UDESA/Herramientas computacionales/Clase 4/input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', # capa de vector de entrada
            'OUTPUT': parameters['Fix_geo_3'] # especifica la capa vectorial saliente
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo_3'] = outputs['CorregirGeometras']['OUTPUT']
        return results
# define elementos

    def name(self):
        return 'model3'

    def displayName(self):
        return 'model3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model3()
