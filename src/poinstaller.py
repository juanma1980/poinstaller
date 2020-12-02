import polib
import os
import shutil
import tempfile


DEST_TEMP = "share/locale/{}/LC_MESSAGES/"

class PoInstaller:
	def __init__(self, po_folder, textdomain, dest_folder, links_lang={} ):
		self.po_folder = po_folder
		self.textdomain = textdomain
		self.dest_folder = dest_folder
		self.langs = []
		self.temp_mo_folder = tempfile.mkdtemp(dir='.',prefix='.mo_')
		self.links_lang = links_lang

	def get_languages(self):
		return [ x[:-3] for x in os.listdir(self.po_folder) if x[-3:] == ".po" ]

	def build(self):
		if os.path.exists(self.temp_mo_folder):
			shutil.rmtree(self.temp_mo_folder)
		os.makedirs(self.temp_mo_folder)
		for language in self.get_languages():
			aux_file = polib.pofile(os.path.join(self.po_folder,language + ".po"))
			aux_path = os.path.join(self.temp_mo_folder, language)
			os.makedirs(aux_path)
			aux_file.save_as_mofile(os.path.join(aux_path, self.textdomain + ".mo"))
			if language in self.links_lang.keys():
				if type(self.links_lang[language]) != list:
					continue
				for aux_language in self.links_lang[language]:
					aux_path = os.path.join(self.temp_mo_folder,aux_language)
					if not os.path.exists(aux_path):
						os.makedirs(aux_path)
					aux_file.save_as_mofile(os.path.join(aux_path,self.textdomain + ".mo"))
		
	def install(self):
		for language in self.get_languages():
			dest = os.path.join(self.dest_folder,DEST_TEMP.format(language))
			file_to_copy = os.path.join(self.temp_mo_folder,language,self.textdomain + ".mo")
			if not os.path.exists(dest):
				os.makedirs(dest)
			shutil.copy2(file_to_copy, os.path.join(dest,self.textdomain + ".mo"))
			if language in self.links_lang.keys():
				if type(self.links_lang[language]) != list:
					continue
				for aux_language in self.links_lang[language]:
					aux_path = os.path.join(self.dest_folder,DEST_TEMP.format(aux_language))
					file_to_copy = os.path.join(self.temp_mo_folder, aux_language, self.textdomain + ".mo")
					if not os.path.exists(aux_path):
						os.makedirs(aux_path)
					shutil.copy2(file_to_copy,os.path.join(aux_path,self.textdomain + ".mo"))

	def setup_install(self):
		polist = []
		for language in self.get_languages():
			dest = os.path.join(self.dest_folder,DEST_TEMP.format(language))
			file_to_install = os.path.join(self.temp_mo_folder, language, self.textdomain + ".mo")
			polist.append( ( dest, [ file_to_install ] ) )
			if language in self.links_lang.keys():
				if type(self.links_lang[language]) != list:
					continue
				for aux_language in self.links_lang[language]:
					dest = os.path.join(self.dest_folder,DEST_TEMP.format(aux_language))
					file_to_install = os.path.join(self.temp_mo_folder, aux_language, self.textdomain + ".mo")
					polist.append( ( dest, [ file_to_install ] ) )

		return polist

	def clean(self):
		shutil.rmtree(self.temp_mo_folder)
