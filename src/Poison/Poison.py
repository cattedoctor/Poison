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
# 3D Model Generation
# TODO : Add 3D model generation
#
###############################################################################

###############################################################################
# Imports
###############################################################################
import random, os, string, json

import numpy as np

from PIL import Image, ImageDraw, ImageColor, ImageFilter
from PIL.ExifTags import Base as ExifTags

import skimage

# from . import Utils
import Utils


###############################################################################
# Poison class
###############################################################################
class Poison(object):
	# Initialization
	def __init__(self, mode=None, debug=False, verbose=False, config_path=None, generate_image=False, generate_music=False, generate_video=False):
		self.mode = None

		if mode is None:
			pass

		elif mode.lower() in Utils.LIST_OF_MODES:
			self.mode = mode

		else:
			raise Exception(f"Mode {mode} not implemented")

		# Debug Variab;es
		self.debug = debug
		self.verbose = verbose

		# Configuration Variables
		self.config = None
		self.config_path = config_path
		self.generate_image = generate_image
		self.generate_music = generate_music
		self.generate_video = generate_video

		# Image Filter Variables
		self.max_percent = None
		self.max_threshold = None
		self.max_kernel = None
		self.max_scale = None
		self.max_offset = None

		# Image Noise Variables
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
			self.process_config()

		else:
			self.load_defaults()

		if self.generate_image:
			from PoisonImage import PoisonImage

			self.image = PoisonImage(mode=self.mode, debug=self.debug, verbose=self.verbose,
				                     max_percent=self.max_percent, max_threshold=self.max_threshold,
				                     max_kernel=self.max_kernel, max_scale=self.max_scale, max_offset=self.max_offset)

		if self.generate_music:
			from PoisonMusic import PoisonMusic
			self.music = PoisonMusic(mode=self.mode, debug=self.debug, verbose=self.verbose)

		if self.generate_video:
			from PoisonVideo import PoisonVideo
			self.video = PoisonVideo(mode=self.mode, debug=self.debug, verbose=self.verbose, config=self.config)

	# Save Config
	def save_config(self):
		with open(config_path, mode="w", encoding="utf-8") as f:
			f.write(json.dumps(self.config))

	# Process Config
	def process_config(self):
		for key, value in self.config.items():
			if key == "config":
				print(value)
				exit()

			elif key == "mode":
				self.mode = value
			
				if self.mode is None:
					self.load_defaults()
					break

			elif key in ["debug", "verbose", "max_percent", "max_threshold", "max_kernel", "max_scale", "max_offset",
						 "octave_range", "musical_key", "key_type", "num_notes", "max_note_duration", "song_duration", "song_extension"]:
				self.set_value(key, value)

			elif key == "generate_image":
				self.generate_image = value

			elif key == "generate_music":
				self.generate_music = value

			else:
				raise Exception(f"Config key {key} not recognized")

	# Set Value
	def set_value(self, key, value):
		if key in list(Utils.EXPECTED_CONFIG_DICT.keys()):
			setattr(self, key, value)

		else:
 			raise Exception(f"Config key {key} is not recognized")

	# Load Defaults
	def load_defaults(self):
		if self.mode is None:
			self.mode = "light"

		if self.mode.lower() == "light":
			if self.generate_image:
				self.max_percent = 100
				self.max_threshold = 100
				self.max_kernel = (100, 10)
				self.max_scale = 10
				self.max_offset = 10

			if self.generate_music:
				self.octave_range = "middle"
				self.musical_key = "C"
				self.key_type = "major"
				self.num_notes = 100
				self.max_note_duration = 100
				self.song_duration = 600
				self.song_extension = "wav"

		elif self.mode.lower() == "medium":
			if self.generate_image:
				self.max_percent = 500
				self.max_threshold = 500
				self.max_kernel = (500, 50)
				self.max_scale = 50
				self.max_offset = 50

			if self.generate_music:
				self.octave_range = "middle"
				self.musical_key = "C"
				self.key_type = "major"
				self.num_notes = 1000
				self.max_note_duration = 250
				self.song_duration = 6000
				self.song_extension = "wav"

		elif self.mode.lower() == "heavy":
			if self.generate_image:
				self.max_percent = 1000
				self.max_threshold = 1000
				self.max_kernel = (1000, 100)
				self.max_scale = 100
				self.max_offset = 100

			if self.generate_music:
				self.octave_range = "middle"
				self.musical_key = "C"
				self.key_type = "major"
				self.num_notes = 1000
				self.max_note_duration = 500
				self.song_duration = 60000
				self.song_extension = "wav"

		else:
			raise Exception(f"Mode {self.mode.lower()} not implemented")


###############################################################################
# Test
###############################################################################
if __name__ == "__main__":
	from PoisonImage import DICT_OF_COLORS

	generate_image = False
	generate_music = False
	generate_video = True

	num_generated = 10
	config_path = os.path.join(os.getcwd(), 'config.json')

	colors = DICT_OF_COLORS["pansexual"]

	poison = Poison(config_path=config_path)

	if poison.debug:
		import time
		average_time = 0.0

	if generate_image:
		for index in range(1, num_generated + 1):
			if poison.debug:
				start_time = time.thread_time()
				print(f"\nGenerating image #{index}")

			# colors = random.choice(list(DICT_OF_COLORS.values()))

			output_file_name = poison.image.generate_image_simple(image_mode="RGB", extension="jpg", image_name_length=32, image_size=(1920, 1080), colors=colors)

			if poison.debug:
				elapsed_time = time.thread_time() - start_time
				average_time = (average_time * (index - 1) + elapsed_time) / index
				print(f"\telapsed time: {elapsed_time:3.3f} s")

			# poison.image.delete_image(output_file_name)

		if poison.debug:
			print(f"\naverage time: {average_time:3.3f} s")
			print(f"\nProgram complete")

	if generate_music:
		if poison.debug:
			average_time = 0.0

		for index in range(1, num_generated + 1):
			if poison.debug:
				start_time = time.thread_time()
				print(f"\nGenerating music #{index}")

			music_file = poison.music.generate_music_simple(key=poison.musical_key, key_type=poison.key_type, octave_range=poison.octave_range, song_duration=poison.song_duration)

			if poison.debug:
				elapsed_time = time.thread_time() - start_time
				average_time = (average_time * (index - 1) + elapsed_time) / index
				print(f"\telapsed time: {elapsed_time:3.3f} s")

			# poison.music.delete_music(music_file)

		if poison.debug:
			print(f"\naverage time: {average_time:3.3f} s")
			print(f"\nProgram complete")

	if generate_video:
		if poison.debug:
			average_time = 0.0

		for index in range(1, num_generated + 1):
			if poison.debug:
				start_Time = time.thread_time()
				print(f"\nGenerating video #{index}")

			poison.video.generate_video_simple()

			if poison.debug:
				elapsed_time = time.thread_time() - start_time
				average_time = (average_time * (index - 1) + elapsed_time) / index
				print(f"\telapsed time: {elapsed_time:3.3f} s")

		if poison.debug:
			print(f"\naverage time: {average_time:3.3f} s")
			print(f"\nProgram complete")

	# poison.save_config()
