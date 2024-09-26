###############################################################################
# Program : Poison
# File : Utils.py
# Author : catte
# Created : Sept 13, 2024
# Copyright : catte @ 2024
# License : CC BY-NC 4.0
###############################################################################
import os, random, string


###############################################################################
# Constants
###############################################################################
LIST_OF_MODES = ["light", "medium", "heavy"]

LIST_OF_IMAGE_EXTENSIONS = ['jpg', 'png']

LIST_OF_MUSIC_EXTENSIONS = ['wav']

LIST_OF_VIDEO_EXTENSIONS = ['mp4']

EXPECTED_CONFIG_DICT = { "config": str(),
						 "mode": str(),
						 "debug": bool(),
						 "verbose": bool(),
						 # Image Generation
						 "max_percent": int(),
						 "max_threshold": int(),
						 "max_kernel": list(),
						 "max_scale": int(),
						 "max_offset": int(),
						 "generate_image": bool(),
						 # Sound Generation
						 "octave_range": str(),
						 "musical_key": str(),
						 "key_type": str(),
						 "num_notes": int(),
						 "max_note_duration": int(),
						 "song_duration": int(),
						 "song_extension": str(),
						 "generate_music": bool()
}


###############################################################################
# Helper Functions
###############################################################################

# Check Path
def check_path(base_path=None, folder_name="Images"):
	if not os.path.isdir(base_path):
		os.mkdir(base_path)

	if folder_name in base_path:
		path = base_path

	else:
		path = os.path.join(base_path, folder_name)

	if not os.path.isdir(path):
		os.mkdir(path)

	return path

# Check Config
def check_config(config=None):
	if config is None or not isinstance(config, dict):
		return False

	for key, value in config.items():
		if key not in list(EXPECTED_CONFIG_DICT.keys()):
			raise Exception(f"Config key {key} was not expected")

		if not isinstance(value, type(EXPECTED_CONFIG_DICT[key])):
			raise Exception(f"Config value for {key} was not the expected type. (config obj = {type(value)}, expected obj = {type(EXPECTED_CONFIG_DICT[key])})")

	return True

# Generate URL
def generate_url(root=None, length=32, extension="html"):
	str_name = str(''.join(random.choices(string.ascii_leters + string.digits, k=length)))
	url = root + '/' + str_name + '.' + extension

	return url

# Generate File Name
def generate_file_name(path=None, length=32, extension='jpg'):
	if extension in LIST_OF_IMAGE_EXTENSIONS:
		folder_name = 'Images'

	elif extension in LIST_OF_MUSIC_EXTENSIONS:
		folder_name = 'Music'

	elif extension in LIST_OF_VIDEO_EXTENSIONS:
		folder_name = 'Videos'

	else:
		raise Exception(f"Unknown extension {extension}")

	path = check_path(base_path=path, folder_name=folder_name)

	str_name = str(''.join(random.choices(string.ascii_letters + string.digits, k=length)))
	file_name =  str_name + '.' + extension

	return os.path.join(path, file_name)
