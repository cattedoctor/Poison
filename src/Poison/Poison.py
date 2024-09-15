###############################################################################
# Program : Poison
# File : Poison.py
# Author : catte
# Created : Sept 13, 2024
# Copyright : catte @ 2024
# License : CC BY-NC 4.0
#
# This project poisons AI databases by generating
# bogus material automatically to be scraped by
# AI crawler programs.
#
# Image Generation
# TODO : Add option for watermarking
# TODO : Add option for placing text on images
# TODO : Add customization of Exif data
# TODO : Verify and expand image extensions
# TODO : Add generation of GIFs
#
# Text Generation
# TODO : Add text generation of search terms, authors, and paragraphs of text
#
# Video Generation
# TODO : Add generation of videos
#
# Sound Generation
# TODO : Add generation of sound, to be used in videos
#
###############################################################################

import random, os, string, time, json

import numpy as np

from PIL import Image, ImageDraw, ImageColor, ImageFilter
from PIL.ExifTags import Base as ExifTags

import skimage

from . import Utils


###############################################################################
# Poison class
###############################################################################
class Poison(object):
	# Initialization
	def __init__(self, mode=None, debug=False, verbose=False, config_path=None):
		self.mode = None

		if mode is None:
			pass

		elif mode.lower() in Utils.LIST_OF_MODES:
			self.mode = mode

		else:
			raise Exception(f"Mode {mode} not implemented")

		self.debug = debug
		self.verbose = verbose
		self.config_path = config_path

		# Configuration Variables
		self.config = None
		self.generate_image = None

		# Filter Variables
		self.max_percent = None
		self.max_threshold = None
		self.max_kernel = None
		self.max_scale = None
		self.max_offset = None

		# Noise Variables
		self.mean = None
		self.var = None
		self.local_vars = None
		self.amount = None
		self.salt_vs_pepper = None

		if self.config_path is not None:
			is_json = config_path.split('.')[1].lower() == "json"

			if os.path.isfile(config_path) and is_json:
				with open(config_path, mode="r", encoding='utf-8') as f:
					self.config = json.load(f)

			elif not is_json:
				raise Exception(f"Config file should be json")

			else:
				raise Exception(f"Config path {config_path} is not a file")

		if Utils.check_config(self.config):
			generate_image = self.process_config()

		else:
			generate_image = self.load_defaults()

		if generate_image:
			from . import PoisonImage as PoisonImage
			self.image = PoisonImage.PoisonImage(mode=self.mode, debug=self.debug, verbose=self.verbose,
							                     max_percent=self.max_percent, max_threshold=self.max_threshold,
							                     max_kernel=self.max_kernel, max_scale=self.max_scale, max_offset=self.max_offset)

	# Save Config
	def save_config(self):
		with open(config_path, mode="w", encoding="utf-8") as f:
			f.write(json.dumps(self.config))

	# Process Config
	def process_config(self):
		generate_image = False

		for key, value in self.config.items():
			if key == "config":
				print(value)
				exit()

			elif key == "mode":
				self.mode = value
			
				if self.mode is None:
					self.load_defaults()
					break

			elif key in ["debug", "verbose", "max_percent", "max_threshold", "max_kernel", "max_scale", "max_offset", "mean", "var", "local_vars"]:
				self.set_value(key, value)

			elif key == "generate_image":
				generate_image = value

			else:
				raise Exception(f"Config key {key} not recognized")

		return generate_image

	# Set Value
	def set_value(self, key, value):
		if key in list(Utils.EXPECTED_CONFIG_DICT.keys()):
			setattr(self, key, value)

		else:
 			raise Exception(f"Config key {key} is not recognized")

	# Load Defaults
	def load_defaults(self):
		generate_image = False

		if self.mode is None:
			self.mode = "light"

		if self.mode.lower() == "light":
			self.max_percent = 100
			self.max_threshold = 100
			self.max_kernel = (100, 10)
			self.max_scale = 10
			self.max_offset = 10
			generate_image = True

		elif self.mode.lower() == "medium":
			self.max_percent = 500
			self.max_threshold = 500
			self.max_kernel = (500, 50)
			self.max_scale = 50
			self.max_offset = 50
			generate_image = True

		elif self.mode.lower() == "heavy":
			self.max_percent = 1000
			self.max_threshold = 1000
			self.max_kernel = (1000, 100)
			self.max_scale = 100
			self.max_offset = 100
			generate_image = True

		else:
			raise Exception(f"Mode {self.mode.lower()} not implemented")

		return generate_image

###############################################################################
# Test
###############################################################################
if __name__ == "__main__":
	num_generated = 10
	config_path = os.path.join(os.getcwd(), 'config.json')

	colors = Utils.DICT_OF_COLORS["pansexual"]

	poison = Poison(config_path=config_path)

	if poison.debug:
		average_time = 0.0

	for index in range(1, num_generated):
		if poison.debug:
			start_time = time.thread_time()
			print(f"\nGenerating image #{index}")

		# colors = random.choice(list(DICT_OF_COLORS.values()))

		output_file_name = poison.image.generate_image_simple(image_mode="RGB", extension="jpg", image_name_length=32, image_size=(1920, 1080), colors=colors)

		if poison.debug:
			elapsed_time = time.thread_time() - start_time
			average_time = (average_time * (index - 1) + elapsed_time) / index
			print(f"\telapsed time: {elapsed_time:3.3f} s")

	if poison.debug:
		print(f"\naverage time: {average_time:3.3f} s")
		print(f"\nProgram complete")

	# poison.save_config()
