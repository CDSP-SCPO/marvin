# -*- coding: utf-8 -*-
'''
Copyright 2015 

	Centre de données socio-politiques (CDSP)
	Fondation nationale des sciences politiques (FNSP)
	Centre national de la recherche scientifique (CNRS)

License

	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>

'''

from jpylyzer.jpylyzer import checkOneFile
from marvinconfig import METADATA_TO_READ, CONFIG, DEBUG, IGNORE_PROBLEM, IMAGE_NAMING_PATTERN
import sys, csv
from os import listdir
from os.path import isfile, join, basename
from datetime import datetime
import collections

#programme
def check_file (path, metadata, functions):
	'''Fonction effectuant tout les tests demandé par la documentation pour un fichier
		arguments :
			path : le chemin de l'image a analyser
			functions : le tableau des fonctions associe au mots clefs
		return : 
			un dictionnaire disant pour chaque propriete si le test est passé ou pas
	'''
	if DEBUG:
		print('checking ' + path )
	root = checkOneFile(path)
	result = collections.OrderedDict()

	for key in metadata :
		operation = functions[metadata[key]['operation']]
		candidate = find_value_for_path(root, metadata[key]['splitedPath'])
		result[key] = operation(candidate, metadata[key])
	
	return result

def find_value_for_path(obj, route):
	'''retourne la valeur d'un champ pour une route donnée (la route doir être définie dans la constante globale PATH)
		arguments :
			obj : l'arbre dans lequel on doit chercher
			path_name : le nom de la route dans la 
	'''
	node = obj
	for node_name in route:
		node = search_node(node, node_name)
	if node == None:
		print('node ' + str(route) + ' not found')
		return None
	return node.text

def search_node(root, node_name):
	''' trouve le bon node d'apres son nom de tag (attention ne gere pas le cas ou plusieurs tags ont le même nom dans un même tag)
	'''
	if root != None :
		for node in root._children:
			if node.tag == node_name :
				return node

def get_file_list(path):
	'''algorithe recursif recuperant la liste des fichier dont le nom finit par .jp2 sous forme d'un dictionnaire
	'''
	file_list = []
	for o in listdir(path):
		if not isfile(join(path,o)):
			file_list.extend(get_file_list(join(path,o)))
		elif o[-3:].lower() == 'jp2':
			file_list.append( {
				'complete_path' :join(path,o), 
				'folder_path' : path, 
				'file_name': o
				} )
	return file_list

def extract_folder_name(folder_full_path):
	return basename(folder_full_path)

def generate_short_comment_for_file(file_data):
	'''Retourne le numero di fichier dans la liasse si il n'est pas parfait (et un string vide sinon)
	'''
	for index in file_data:
		if index not in IGNORE_PROBLEM and file_data[index] == False:
			return  get_short_file_name(file_data['fileName']) + ', '
	return ''

def generate_long_comment_for_file(file_data):
	'''Retourne la liste des erreur pour chaque fichiers contenant au moins une erreur
	'''
	output = get_short_file_name(file_data['fileName']) + ' : '
	for index in file_data:
		if index not in ['fileName'] and file_data[index] == False:
			output += index + ', '
	if output != file_data['fileName'] + ' : ' :
		return output + '\n'
	else:
		return ''

def generate_csv_details_for_file(file_data):
	'''Retourne une ligne CSV donnant pour chaque metadonnée si elle est correcte ou pas.
	'''
	output = [str(file_data['fileName'])]
	for index in file_data:
		if index not in ['fileName']:
			output.append(str(file_data[index]))
	return output

def is_file_perfect(file_data):
	'''Retourne true si le fichier est parfait (pas de metadonnée en erreur ou les metadonnées en erreur sont dans la liste a ignorer)
	'''
	for index in file_data:
		if index not in IGNORE_PROBLEM and file_data[index] == False:
			return False
	return True

def get_short_file_name(file_name):
	'''Retourne le numero du fichier dans la liasse
	'''
	separator = IMAGE_NAMING_PATTERN['separator']
	page_number_location = IMAGE_NAMING_PATTERN['page_number_location']
	page_number_location_bis = IMAGE_NAMING_PATTERN['page_number_location_bis']
	short_file_name = file_name.split(separator)[page_number_location].split('.')[0]
	try :
		int(short_file_name)
	except :
		short_file_name = file_name.split(separator)[page_number_location_bis].split('.')[0]
		try :
			int(short_file_name)
		except :
			short_file_name = '0'
			print 'this should never happen'
	return short_file_name


##################gestion du fichier de fonf dynamique

def interval(value, meta_object):
	''' Verifie si la valeur value est entre les bornes start et end
	'''
	if value is None:
		return False
	float_start = float(meta_object['start'])
	float_end = float(meta_object['end'])
	float_value = float(value)
	if float_value < float_end and float_value > float_start:
		return True
	else:
		return False

def exact(value, meta_object):
	'''Verifie que la valeur demande soit exactement celle trouve
	'''
	return (value == meta_object['value'])

def exist(value, meta_object):
	'''verifie l'existance de la valeur et sa non nullité
	'''
	if value != None and value != '':
		return True
	else:
		return False

def get_value(value, meta_object):
	'''Fonction innutile pour l'instant mais presente si il y a besoin de traitement sur le get dans le futur
	'''
	return value

def generate_Function_dict():
	return {
		'interval' : interval,
		'exact' : exact,
		'exist' : exist,
		'get': get_value,
	}

def generate_csv_detail_headers(metadata_dict):
	'''genere les headers pour le csv detail dans le bon ordre (non constent)
	'''
	headers = ['Nom du fichier']
	for key in metadata_dict:
		if key != 'fileName':
			headers.append(str(key))
	return headers

def populate_metadata_dict(meta):
	'''genere pour chaque metadata un chemin exploitable par l'application
	'''
	for key in meta:
		meta[key]['splitedPath'] = _split_path(meta[key]['realPath'])
	return meta

def _split_path(path):
	'''Retourne le chemin splite sous forme d'un tableau en retirant la premier case vide et la premiere occurance de jpylyzer
	'''
	splited = path.split('/')
	if splited[0] == '':
		splited = splited[1:]
	if splited[0] == 'jpylyzer':
		splited = splited[1:]
	return splited

def do_work(argv):
	'''fonction effectuant le travail principal du programme
	'''
	#initialisation
	start = datetime.now()
	path_root = argv[1]
	output_file = argv[2]
	function_dict = generate_Function_dict()
	metadata_dict = populate_metadata_dict(METADATA_TO_READ)

	print('exploring folder ' + path_root)
	#construction de la lite des fichiers a examiner
	file_list = get_file_list(path_root)

	csv_data = collections.OrderedDict()
	total_number_of_pages = 0
	file_light_fault = 0
	for f in file_list:
		#traitement pour chaque fichier
		print('generating metadata, file : ' + str(total_number_of_pages) + '/' + str(len(file_list)) )
		#on extrait et on verifie les metadonnes
		file_data = check_file(f['complete_path'], metadata_dict, function_dict)
		#si il n'e'xiste pas ligne dans le bordereau pour cette liassen, on la cree
		if not csv_data.has_key(extract_folder_name(f['folder_path'])):
			csv_data[extract_folder_name(f['folder_path'])] = {'number_of_files' : 0, 'shortComments' : '', 'longComments' : extract_folder_name(f['folder_path']) + ' : \n', 'csv_details' : [], 'last_file_number' : 0 }
		#on ajoute un fichier dans le compteur de la liasse
		csv_data[extract_folder_name(f['folder_path'])]['number_of_files'] += 1
		#on ajoute le numero du fichier dans la lisasse si il n'est pas parfait
		csv_data[extract_folder_name(f['folder_path'])]['shortComments'] += generate_short_comment_for_file(file_data)
		if CONFIG['details_text']:
			#si les details dans un fichier texte ont étés demandés, on genere la ligne concernant le fichier
			csv_data[extract_folder_name(f['folder_path'])]['longComments'] += generate_long_comment_for_file(file_data)
		if CONFIG['details_CSV']:
			#si les details dans un fichier csv ont étés demandés, on genere la ligne concernant le fichier
			csv_data[extract_folder_name(f['folder_path'])]['csv_details'].append(generate_csv_details_for_file(file_data))
		total_number_of_pages += 1
		#on essaye de savoir si le dossier est complet
		if csv_data[extract_folder_name(f['folder_path'])]['last_file_number'] < int(get_short_file_name(file_data['fileName'])):
			csv_data[extract_folder_name(f['folder_path'])]['last_file_number'] = int(get_short_file_name(file_data['fileName']))
		if not is_file_perfect(file_data):
			file_light_fault += 1
	print('creating csv')
	

	#partie écriture des CSV
	csv_file_pointer  = open(output_file + '.csv', 'wb+')
	details_file_pointer = None
	details_file_pointer_csv = None
	if CONFIG['details_CSV']:
		#creation du fichier CSV si il a été demande des details CSV
		details_file_pointer_csv = open(output_file + 'details.csv', 'wb+')
		details_writer = csv.writer(details_file_pointer_csv, dialect='excel')
	if CONFIG['details_text']:
		#creation du fichier de details textes si demandé
		details_file_pointer = open(output_file + 'details.log', 'wb+')
	writer = csv.writer(csv_file_pointer, dialect='excel')
	#preparation des headers du tableau
	writer.writerow(['Bibliotheque de SCIENCES PO (Paris)','Total des erreurs majeures images','Total des erreurs mineures images','Validation du controle images'])
	writer.writerow(['Prestataire : ', file_light_fault, '0', ''])
	writer.writerow(['Nbre de volumes : ' + str(len(file_list))])
	writer.writerow(['Nbre de pages : ' + str(total_number_of_pages)])
	writer.writerow(['Nombre de fichiers a controler pour l\'echantillon : '])
	writer.writerow(['Date d\'enlevement : '])
	writer.writerow(['Date de retour : '])
	writer.writerow(['COTE','Nombre de fichiers a controler','Page manquante a la numerisation','Fichier illisible','Lisibilite du contenu','Troncature d\'information','Non respect de la resolution','Non respect du seuil','Presence de corps etrangers sur l\'image','Halo sur l\'image, Ombre portee, Distorsions geometriques inclinaison/orientation, Derive de la chromie, Cadrage inadapte','Initiales\ncontroleur','Precisions'])
	#preparation des headers du fichier de details csv
	details_writer.writerow(generate_csv_detail_headers(metadata_dict))
	#ecriture des donnes a proprement parler
	for index in csv_data:
		writer.writerow([unicode(index), unicode(csv_data[index]['number_of_files']), unicode(csv_data[index]['last_file_number'] - csv_data[index]['number_of_files']), '', '', '', '', '', '', '', 'Marvin', csv_data[index]['shortComments']])
		if CONFIG['details_text'] :
			details_file_pointer.write(csv_data[index]['longComments'])
		if CONFIG['details_CSV']:
			for details in csv_data[index]['csv_details'] :
				details_writer.writerow(details)

	csv_file_pointer.close()
	if CONFIG['details_text']:
		details_file_pointer.close()
	if CONFIG['details_CSV']:
		details_file_pointer_csv.close()
	print('Done in '  + str((datetime.now() - start)) )


def main():
	'''point d'entre du programme
	'''
	if len(sys.argv) != 3:
		print('args error')
		print('correct usage : ' + sys.argv[0] + ' "path to images folder" "path to outputfile"')
	else:
		do_work(sys.argv)

main()

