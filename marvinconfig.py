# -*- coding: utf-8 -*-

#rend la console tres bavarde
DEBUG = False

#les sorties CSV et texte peuvent être active en même temps
CONFIG = {
	'details_CSV' : True,#active ou non les details sous forme de fichier CSV
	'details_text' : True,#active ou non les details sous forme de fichier text
}

IMAGE_NAMING_PATTERN = {
	'separator' : '_',
	'page_number_location' : -2,
}

#tableau des metadonnees a aller chercher et des valeurs attendues
#les operations supporté sont : 'exact', 'get', 'interval', 'exist'
#'exact' : retourne true si la valeur est exactement la valeur donnes dans le champ 'value' et false sinon
#'get' : retourne la valeur du champ
#'interval' : retourne true si la valeur est un nombre compris entre les valeurs 'start' et 'end' (qui doivent être aussi des nombres) et false sinon
#'exist' : retourne true si la valeur existe et n'est pas une chaine vide et false sinon
METADATA_TO_READ = {
	#l'attribut fileName est indispensable, tout les autres sont facultatifs
	'fileName' : {
		'realPath' : '/jpylyzer/fileInfo/fileName',
		'operation' : 'get'
	},
	'isValidJP2' : {
		'realPath' : '/jpylyzer/isValidJP2',
		'splitedPath' : ['isValidJP2'],
		'operation' : 'exact',
		'value' : 'True'
	},
	'imageHeaderBoxc' : {
		'realPath' : '/jpylyzer/properties/jp2HeaderBox/imageHeaderBox/c',
		'operation' : 'exact',
		'value' : 'jpeg2000'
	},
	'colourSpecificationBoxMeth' : {
		'realPath' : '/jpylyzer/properties/jp2HeaderBox/colourSpecificationBox/meth',
		'operation' : 'exact',
		'value' : 'Restricted ICC'
	},
	'iccDescription' : {
		'realPath' : '/jpylyzer/properties/jp2HeaderBox/colourSpecificationBox/icc/description',
		'operation' : 'exact',
		'value' : 'sRGB IEC61966-2.1'
	},
	'vRescInPixelsPerMeter' : {
		'realPath' : '/jpylyzer/properties/jp2HeaderBox/resolutionBox/captureResolutionBox/vRescInPixelsPerMeter',
		'operation' : 'exist',
	},
	'hRescInPixelsPerMeter' : {
		'realPath' : '/jpylyzer/properties/jp2HeaderBox/resolutionBox/captureResolutionBox/hRescInPixelsPerMeter',
		'operation' : 'exist'
	},
	'transformation' : {
		'realPath' : '/jpylyzer/properties/contiguousCodestreamBox/cod/transformation',
		'operation' : 'exact',
		'value' : '9-7 irreversible'
	},
	'compressionRatio' : {
		'realPath' : '/jpylyzer/properties/compressionRatio',
		'operation' : 'interval',
		'start' : '3',
		'end' : '10'
	},
}

#les problemes ignores sont ignore lors de la creation du bordereau mais ils sont ajoute dans le csv de details
IGNORE_PROBLEM = ['fileName','iccDescription']