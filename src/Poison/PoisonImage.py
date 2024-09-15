###############################################################################
# Program : Poison
# File : PoisonImage.py
# Author : catte
# Created : Sept 13, 2024
# Copyright : catte @ 2024
# License : CC BY-NC 4.0
###############################################################################
import os, random

from PIL import Image, ImageDraw, ImageColor, ImageFilter
from PIL.ExifTags import Base as ExifTags

import skimage
import numpy as np

from . import Utils


class PoisonImage(object):
	def __init__(self, mode, debug, verbose, max_percent, max_threshold, max_kernel, max_scale, max_offset):
		self.mode = mode
		self.debug = debug
		self.verbose = verbose
		self.max_percent = max_percent
		self.max_threshold = max_threshold
		self.max_kernel = max_kernel
		self.max_scale = max_scale
		self.max_offset = max_offset

	# Generate Image Simple
	def generate_image_simple(self, path=None, image_mode='RGB', extension='jpg', image_name_length=32, image_size=(1920, 1080), colors=None, shapes=None, filters=None):
		if self.mode.lower() == "light":
			shapes_k = 10
			filters_k = 3
			num_shapes = 100
			num_filters = 1
			noise_types = ["guassian", "salt_pepper"]

		elif self.mode.lower() == "medium":
			shapes_k = 50
			filters_k = 10
			num_shapes = 250
			num_filters = 5
			noise_types = ["guassian", "salt_pepper", "poisson"]

		elif self.mode.lower() == "heavy":
			shapes_k = 50
			filters_k = 15
			num_shapes = 250
			num_filters = 5
			noise_types = ["guassian", "salt_pepper", "poisson", "speckle"]

		if path is None:
			path = os.getcwd()

		if not os.path.isdir(path):
			os.mkdir(path)

		base_path = os.path.join(path, 'Images')

		if not os.path.isdir(base_path):
			os.mkdir(base_path)

		if not os.path.isdir(os.path.join(base_path, self.mode.lower())):
			os.mkdir(os.path.join(base_path, self.mode.lower()))

		dir_path = os.path.join(base_path, self.mode.lower(), str(image_size[0]) + '_' + str(image_size[1]))

		if not os.path.isdir(dir_path):
			os.mkdir(dir_path)

		density = random.randint(1, 300)

		if shapes is None:
			shapes = random.choices(Utils.LIST_OF_SHAPES, k=shapes_k)

		if filters is None:
			filters = random.choices(Utils.LIST_OF_FILTERS, k=filters_k)

		if self.mode.lower() == "light":
			filters = [filt for filt in filters if filt not in Utils.LIGHT_MODE_EXCLUDED_FILTERS]

		elif self.mode.lower() == "medium":
			filters = [filt for filt in filters if filt not in Utils.MEDIUM_MODE_EXCLUDED_FILTERS]

		return self.generate_image(path=dir_path, image_mode=image_mode, extension=extension, image_name_length=32,
					  			   height=image_size[0], width=image_size[1], density=density, colors=colors,
					  			   num_shapes=num_shapes, shapes=shapes,
					  			   num_filters=num_filters, filters=filters,
					  			   noise_level="light", noise_types=noise_types)

	# Generate Image
	def generate_image(self, path=None, image_mode='RGB', extension='jpg', image_name_length=32,
					   height=120, width=120, background_color=None, colors=None, density=2,
					   num_shapes=0, shapes=list(),
					   num_filters=0, filters=list(),
					   noise_level=None, noise_types=list()):

		output_file_name = Utils.generate_file_name(path=path, extension=extension, length=image_name_length)

		if colors is None:
			colors = list(ImageColor.colormap.keys())

		if background_color is not None:
			image = Image.new(mode=image_mode, size=(height, width), color=background_color)
		
		else:
			image = Image.new(mode=image_mode, size=(height, width), color=random.choice(colors))

		draw = ImageDraw.Draw(image)

		if noise_level is not None:
			if noise_level.lower() == "light":
				self.mean = random.uniform(75, 150)
				self.var = random.uniform(0.001, 10)
				self.local_vars = np.random.uniform(low=0.01, high=0.1, size=image.size)
				self.amount = random.uniform(0.01, 0.1)
				self.salt_vs_pepper = 0.5

			elif noise_level.lower() == "medium":
				self.mean = random.uniform(10, 100)
				self.var = random.uniform(10, 100)
				self.local_vars = np.random.uniform(low=10, high=100, size=image.size)
				self.amount = random.uniform(0.1, 0.5)
				self.salt_vs_pepper = random.uniform(0.25, 0.75)

			elif noise_level.lower() == "heavy":
				self.mean = random.uniform(0, 256)
				self.var = random.uniform(0, 256)
				self.local_vars = np.random.uniform(low=100, high=1000, size=image.size)
				self.amount = random.uniform(0.5, 1.0)
				self.salt_vs_pepper = random.uniform(0.01, 0.99)

			else:
				raise Exception(f"Noise level {noise_level} not implemented")

		list_of_shapes = []
		for shape in shapes:
			for _ in range(num_shapes):
				list_of_shapes.append(shape)

		random.shuffle(list_of_shapes)

		list_of_filters = []
		for filt in filters:
			for _ in range(num_filters):
				list_of_filters.append(filt)

		random.shuffle(list_of_filters)

		for shape in list_of_shapes:
			points = random.randint(3, 10)
			cmd = Utils.select_shape(shape, points)

			attributes = Utils.get_shape_attributes(height, width, shape, points, density)

			if self.debug and self.verbose:
				print("\t\t" + cmd)
				print("\t\t" + str(attributes))

			eval(cmd)

		for filt in list_of_filters:
			radius = random.uniform(1, min(height, width))
			size = [random.randint(10, max(height // 4, 11)), random.randint(1, max(width // density, 2))]
			rank = random.randint(0, min(height, width) // 4)
			percent = random.randint(0, self.max_percent)
			threshold = random.randint(0, self.max_threshold)
			kernel = list(random.uniform(0, self.max_kernel[0]) for _ in range(self.max_kernel[1]))
			scale = random.uniform(1, self.max_scale)
			offset = random.uniform(0, self.max_offset)

			cmd = Utils.select_filter(filt, radius, size, percent, threshold, kernel, scale, offset, rank)

			if self.debug and self.verbose:
				print("\t\t" + cmd)

			eval(cmd)

		exif = image.getexif()

		exif[ExifTags.ImageDescription.value] = f"mode: {self.mode.lower()}"

		image.save(output_file_name, exif=exif)

		if self.debug:
			print(f"\nFile saved @ {output_file_name}")

		del(image)

		for noise_type in noise_types:
			image = skimage.io.imread(output_file_name)

			if noise_type.lower() == "guassian":
				noise_mode = "gaussian"

			elif noise_type.lower() == "localvar":
				noise_mode = "localvar"

			elif noise_type.lower() == "poisson":
				noise_mode = "poisson"

			elif noise_type.lower() == "salt":
				noise_mode = "salt"

			elif noise_type.lower() == "pepper":
				noise_mode = "pepper"

			elif noise_type.lower() == "salt_pepper":
				noise_mode = "s&p"

			elif noise_type.lower() == "speckle":
				noise_mode = "speckle"

			else:
				raise Exception(f"Noise type {noise_type} not implemented")

			if noise_mode in ["guassian", "speckle"]:
				image = skimage.util.random_noise(image, mode=noise_mode, mean=self.mean, var=self.var)

			elif noise_mode == "localvar":
				image = skimage.util.random_noise(image, mode=noise_mode, local_vars=self.local_vars)

			elif noise_mode in ["salt", "pepper"]:
				image = skimage.util.random_noise(image, mode=noise_mode, amount=self.amount)

			elif noise_mode == "s&p":
				image = skimage.util.random_noise(image, mode=noise_mode, amount=self.amount, salt_vs_pepper=self.salt_vs_pepper)

			noise_img = np.array(255 * image, dtype='uint8')

			del(image)

			image = Image.fromarray(np.array(noise_img))
			image.save(output_file_name)

		return output_file_name
