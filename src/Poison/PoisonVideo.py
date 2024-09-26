###############################################################################
# Program : Poison
# File : PoisonImage.py
# Author : catte
# Created : Sept 20, 2024
# Copyright : catte @ 2024
# License : CC BY-NC 4.0
###############################################################################

###############################################################################
# Imports
###############################################################################
import os, random, subprocess

from PoisonImage import PoisonImage
from PoisonMusic import PoisonMusic

import Utils


###############################################################################
# Constants
###############################################################################


###############################################################################
# Helper Functions
###############################################################################


###############################################################################
# Classes
###############################################################################

# PoisonVideo Class
class PoisonVideo(object):
	def __init__(self, debug=False, verbose=False, mode=None, config=None):
		self.debug = debug
		self.verbose = verbose
		self.config = config
		self.mode = mode if mode is not None else self.config["mode"]

		# self.image = PoisonImage.PoisonImage(mode=self.mode, debug=self.debug, verbose=self.verbose,
		# 	                     max_percent=self.config['max_percent'], max_threshold=self.config['max_threshold'],
		# 	                     max_kernel=self.config['max_kernel'], max_scale=self.config['max_scale'],
		# 	                     max_offset=self.config['max_offset'])

		# self.music = PoisonSound.PoisonSound(mode=self.mode, debug=self.debug, verbose=self.verbose)

		self.image = PoisonImage(mode=self.mode, debug=self.debug, verbose=self.verbose,
			                     max_percent=self.config['max_percent'], max_threshold=self.config['max_threshold'],
			                     max_kernel=self.config['max_kernel'], max_scale=self.config['max_scale'],
			                     max_offset=self.config['max_offset'])

		self.music = PoisonMusic(mode=self.mode, debug=self.debug, verbose=self.verbose)

	def cleanup(self, image_file_names, music_file_name):
		self.cleanup_images(image_file_names)

		self.cleanup_music(music_file_name)

	def cleanup_images(self, image_file_names):
		for image_file_name in image_file_names:
			self.image.delete_image(image_file_name)

	def cleanup_music(self, music_file_name):
		self.music.delete_music(music_file_name)

	def generate_video_simple(self, base_path=None, extension='mp4', video_duration=600, colors=[]):
		return self.generate_video(image_base_path=base_path, image_directory='Images', image_file_extension='png',
								   music_base_path=base_path, music_directory='Music', music_extension='wav',
								   video_base_path=base_path, video_directory='Videos', video_extension='mp4',
								   video_duration=video_duration, colors=colors)

	def generate_video(self, image_base_path=None, image_directory=None, image_file_extension='png',
					   music_base_path=None, music_directory=None, music_extension='wav',
					   video_base_path=None, video_directory=None, video_extension='mp4',
					   video_duration=600, colors=[]):
		image_base_path = Utils.check_path(base_path=image_base_path, folder_name=image_directory if image_directory is not None else 'Images')

		music_base_path = Utils.check_path(base_path=music_base_path, folder_name=music_directory if music_directory is not None else 'Music')

		video_base_path = Utils.check_path(base_path=video_base_path, folder_name=video_directory if video_directory is not None else 'Videos')

		if self.debug:
			print(f"\nImage base path: {image_base_path}")
			print(f"Music base path: {music_base_path}")
			print(f"Video base path: {video_base_path}")

		music_file_name = self.music.generate_music_simple(base_path=music_base_path, key=self.config['musical_key'], key_type=self.config['key_type'], octave_range=self.config['octave_range'], song_duration=self.config['song_duration'])

		num_images = int(self.music.get_duration(music_file_name))

		if self.debug:
			print(f"Creating {num_images} images")

		image_file_names = []
		for index in range(num_images):
			if self.debug:
				print(f"Generating image #{index}")

			image_file_names.append(self.image.generate_image_simple(path=image_base_path, image_mode="RGB", extension=image_file_extension, image_name_length=32, image_size=(1920, 1080), colors=colors))

		video_file_name = Utils.generate_file_name(path=video_base_path, length=32, extension=video_extension)

		if self.debug and self.verbose:
			print(f"\nImage file names: {image_file_names}")
			print(f"Music file name: {music_file_name}\n")

		cmd = f"/usr/bin/ffmpeg -framerate 1 -pattern_type glob -i '{image_base_path}/*.{image_file_extension}' -i {music_file_name} -c:v libx264 -pix_fmt yuv420p {video_file_name}"

		if self.debug:
			print(cmd)

		subprocess.run(cmd, shell=True)

		self.cleanup(image_file_names, music_file_name)

		return video_file_name


###############################################################################
# Test
###############################################################################
if __name__ == "__main__":
	debug = False
	verbose = False

	mode = "heavy"

	num_videos = 1

	config = {	"mode": mode,
				"max_percent": 100,
				"max_threshold": 100,
				"max_kernel": [100, 10],
				"max_scale": 10,
				"max_offset": 10,
				"octave_range": "middle",
				"musical_key": "C",
				"key_type": "major",
				"num_notes": 100,
				"max_note_duration": 100,
				"song_duration": 600,
				"song_extension": "wav"
	}

	from PoisonImage import DICT_OF_COLORS

	colors = DICT_OF_COLORS["transgender"]

	video = PoisonVideo(debug=debug, verbose=verbose, mode=mode, config=config)

	if debug:
		import time
		average_time = 0.0

	for index in range(1, num_videos + 1):
		if debug:
			start_time = time.thread_time()
			print(f"Generating video #{index}")

		video_file = video.generate_video_simple(base_path=os.getcwd(), extension='mp4', video_duration=600, colors=colors)

		if debug:
			elapsed_time = time.thread_time() - start_time
			average_time = (average_time * (index - 1) + elapsed_time) / index
			print(f"\telapsed time: {elapsed_time:3.3f} s")

	if debug:
		print(f"\naverage time: {average_time:3.3f} s")
		print(f"\nProgram complete")
