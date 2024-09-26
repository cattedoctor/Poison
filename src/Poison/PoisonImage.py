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
import os, random, signal
from collections import OrderedDict
from itertools import zip_longest

from PIL import Image, ImageDraw, ImageColor, ImageFilter
from PIL.ExifTags import Base as ExifTags

import skimage
import numpy as np

from Poison import Utils


###############################################################################
# Constants
###############################################################################
LIST_OF_COMMON_IMAGE_SIZES = [(2650, 1400), (1920, 1080), (1280, 720), (1200, 400), (1200, 800), (400, 100), (100, 100), (300, 300), (1080, 1080)]

LIST_OF_SHAPES = ["circle", "line", "curve", "arc", "chord", "ellipse", "pieslice",
				  "point", "polygon", "regular_polygon", "rectangle", "rounded_rectangle"]

LIST_OF_FILTERS = ["blur", "contour", "detail", "edge_enhance", "edge_enhance_more",
				   "emboss", "find_edges", "sharpen", "smooth", "smooth_more",
				   "box_blur", "gaussian_blur", "unsharp_mask", "kernel", "rank_filter",
				   "median_filter", "min_filter", "max_filter", "mode_filter"]

LIST_OF_NOISE_TYPES = ["guassian", "localvar", "poisson", "salt", "pepper", "salt_pepper", "speckle"]

NOT_IMPLEMENTED_SHAPES = []

NOT_IMPLEMENTED_FILTERS = ["kernel", "rank_filter", "median_filter", "min_filter", "max_filter"]

LIGHT_MODE_EXCLUDED_FILTERS = ["rank_filter", "median_filter", "min_filter", "max_filter", "mode_filter"]

MEDIUM_MODE_EXCLUDED_FILTERS = ["rank_filter", "median_filter", "min_filter", "max_filter", "mode_filter"]

LIST_OF_SHAPES = [x for x in LIST_OF_SHAPES if x not in NOT_IMPLEMENTED_SHAPES]

LIST_OF_FILTERS = [x for x in LIST_OF_FILTERS if x not in NOT_IMPLEMENTED_FILTERS]

DICT_OF_COLORS = {"pride": [(288, 3, 3), (255, 140, 0), (255, 237, 0), (0, 128, 38), (0, 76, 255), (115, 41, 130)],
				  "gay": [(7, 141, 112), (38, 206, 170), (152, 232, 193), (255, 255, 255), (123, 173, 226), (80, 73, 204), (61, 26, 120)],
				  "lesbian": [(213, 45, 0), (239, 118, 39), (255, 154, 86), (255, 255, 255), (209, 98, 164), (181, 86, 144), (163, 2, 98)],
				  "bisexual": [(214, 2, 112), (155, 79, 150), (0, 56, 168)],
				  "pansexual": [(255, 33, 140), (255, 216, 0), (33, 177, 255)],
				  "transgender": [(91, 206, 250), (245, 169, 184), (255, 255, 255)],
				  "agender": [(0, 0, 0), (188, 196, 199), (255, 255, 255), (183, 246, 132)],
				  "bigender": [(196, 121, 162), (237, 165, 205), (214, 199, 232), (255, 255, 255), (154, 199, 232), (109, 130, 209)],
				  "nonbinary": [(252, 244, 52), (255, 255, 255), (156, 89, 209), (44, 44, 44)]
}

TIME_OUT = 1


###############################################################################
# Helper Functions
###############################################################################

def timeout_handler(signum, frame):
	raise TimeoutError("Rendering function timed out.")


# Get Shape Attributes
def get_shape_attributes(height, width, shape, points, density=2):
	shape_attributes = OrderedDict()

	if shape == "line":
		w = max(min(height, width) // density, 2)
		shape_attributes.update({'x0': random.randint(0, height)})
		shape_attributes.update({'y0': random.randint(0, width)})
		shape_attributes.update({'x1': random.randint(0, height)})
		shape_attributes.update({'y1': random.randint(0, width)})
		shape_attributes.update({'w': random.randint(1, w)})
	
	elif shape == "curve":
		x = list(random.randint(0, height) for _ in range(points))
		y = list(random.randint(0, width) for _ in range(points))
		w = max(min(height, width) // density, 2)

		for index, coordinate in enumerate(zip(x, y)):
			shape_attributes.update({f'x{index}': coordinate[0]})
			shape_attributes.update({f'y{index}': coordinate[1]})

		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "circle":
		r = max(min(height, width) // density, 2)
		w = max(min(height, width) // density, 2)
		shape_attributes.update({'x0': random.randint(0, height)})
		shape_attributes.update({'y0': random.randint(0, width)})
		shape_attributes.update({'r': random.randint(1, r)})
		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "arc":
		x = sorted([random.randint(0, height) for _ in range(2)])
		y = sorted([random.randint(0, width) for _ in range(2)])

		shape_attributes.update({'x0': x[0]})
		shape_attributes.update({'y0': y[0]})
		shape_attributes.update({'x1': x[1]})
		shape_attributes.update({'y1': y[1]})
		shape_attributes.update({'start': random.uniform(0, 360)})
		shape_attributes.update({'end': random.uniform(0, 360)})
		shape_attributes.update({'w': random.randint(0, min(height, width) // density)})

	elif shape == "chord":
		x = sorted([random.randint(0, height) for _ in range(2)])
		y = sorted([random.randint(0, width) for _ in range(2)])
		w = max(min(height, width) // density, 2)

		shape_attributes.update({'x0': x[0]})
		shape_attributes.update({'y0': y[0]})
		shape_attributes.update({'x1': x[1]})
		shape_attributes.update({'y1': y[1]})
		shape_attributes.update({'start': random.uniform(0, 360)})
		shape_attributes.update({'end': random.uniform(0, 360)})
		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "ellipse":
		x = sorted([random.randint(0, height) for _ in range(2)])
		y = sorted([random.randint(0, width) for _ in range(2)])
		w = max(min(height, width) // density, 2)

		shape_attributes.update({'x0': x[0]})
		shape_attributes.update({'y0': y[0]})
		shape_attributes.update({'x1': x[1]})
		shape_attributes.update({'y1': y[1]})
		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "pieslice":
		x = sorted([random.randint(0, height) for _ in range(2)])
		y = sorted([random.randint(0, width) for _ in range(2)])
		w = max(min(height, width) // density, 2)

		shape_attributes.update({'x0': x[0]})
		shape_attributes.update({'y0': y[0]})
		shape_attributes.update({'x1': x[1]})
		shape_attributes.update({'y1': y[1]})
		shape_attributes.update({'start': random.uniform(0, 360)})
		shape_attributes.update({'end': random.uniform(0, 360)})
		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "point":
		shape_attributes.update({'x0': random.randint(0, height)})
		shape_attributes.update({'y0': random.randint(0, width)})

	elif shape == "polygon":
		x = list(random.randint(0, height) for _ in range(points))
		y = list(random.randint(0, width) for _ in range(points))
		w = max(min(height, width) // density, 2)

		for index, coordinate in enumerate(zip(x, y)):
			shape_attributes.update({f'x{index}': coordinate[0]})
			shape_attributes.update({f'y{index}': coordinate[1]})

		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "regular_polygon":
		w = max(min(height, width) // density, 2)
		shape_attributes.update({'bounding_circle': (random.randint(0, height), random.randint(0, width), random.randint(1, min(height, width)))})
		shape_attributes.update({'n_sides': random.randint(3, max(density, 4))})
		shape_attributes.update({'rotation': random.uniform(0, 360)})
		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "rectangle":
		x = sorted([random.randint(0, height) for _ in range(2)])
		y = sorted([random.randint(0, width) for _ in range(2)])
		w = max(min(height, width) // density, 2)
		shape_attributes.update({'x0': x[0]})
		shape_attributes.update({'y0': y[0]})
		shape_attributes.update({'x1': x[1]})
		shape_attributes.update({'y1': y[1]})
		shape_attributes.update({'w': random.randint(1, w)})

	elif shape == "rounded_rectangle":
		r = random.randint(1, max(min(height, width) // density, 2))
		w = max(min(height, width) // density, 2)
		x = [0, 0]
		y = [0, 0]
		while not (x[0] + r + 1 <= x[1] - r - 1):
			x = sorted([random.randint(0, height) for _ in range(2)])
		while not (y[0] + r + 1 <= y[1] - r - 1):
			y = sorted([random.randint(0, width) for _ in range(2)])

		shape_attributes.update({'x0': x[0]})
		shape_attributes.update({'y0': y[0]})
		shape_attributes.update({'x1': x[1]})
		shape_attributes.update({'y1': y[1]})
		shape_attributes.update({'w': random.randint(1, w)})
		shape_attributes.update({'r': r})
		shape_attributes.update({'corners': (random.randint(0,1), random.randint(0,1), random.randint(0,1), random.randint(0,1))})

	return shape_attributes

# Select Filter
def select_filter(filt, radius, size, percent, threshold, kernel, scale, offset, rank):
	if filt == "blur":
		cmd = "image.filter(ImageFilter.BLUR)"

	elif filt == "contour":
		cmd = "image.filter(ImageFilter.CONTOUR)"

	elif filt == "detail":
		cmd = "image.filter(ImageFilter.DETAIL)"

	elif filt == "edge_enhance":
		cmd = "image.filter(ImageFilter.EDGE_ENHANCE)"

	elif filt == "edge_enhance_more":
		cmd = "image.filter(ImageFilter.EDGE_ENHANCE_MORE)"

	elif filt == "emboss":
		cmd = "image.filter(ImageFilter.EMBOSS)"

	elif filt == "find_edges":
		cmd = "image.filter(ImageFilter.FIND_EDGES)"

	elif filt == "sharpen":
		cmd = "image.filter(ImageFilter.SHARPEN)"

	elif filt == "smooth":
		cmd = "image.filter(ImageFilter.SMOOTH)"

	elif filt == "smooth_more":
		cmd = "image.filter(ImageFilter.SMOOTH_MORE)"

	elif filt == "box_blur":
		cmd = f"image.filter(ImageFilter.BoxBlur(radius={radius}))"

	elif filt == "gaussian_blur":
		cmd = f"image.filter(ImageFilter.GaussianBlur(radius={radius}))"

	elif filt == "unsharp_mask":
		cmd = f"image.filter(ImageFilter.UnsharpMask(radius={radius}, percent={percent}, threshold={threshold}))"

	elif filt == "kernel":
		cmd = f"image.filter(ImageFilter.Kernel(size={size}, kernel={kernel}, scale={scale}, offset={offset}))"

	elif filt == "rank_filter":
		cmd = f"image.filter(ImageFilter.RankFilter(size=random.randint(1, ({size[0]} // 2)), rank={rank}))"

	elif filt == "median_filter":
		cmd = f"image.filter(ImageFilter.MedianFilter(size={size[0]}))"

	elif filt == "min_filter":
		cmd = f"image.filter(ImageFilter.MinFilter(size=random.randint(1, ({size[0]} // 2))))"

	elif filt == "max_filter":
		cmd = f"image.filter(ImageFilter.MaxFilter(size=random.randint(1, ({size[0]} // 2))))"

	elif filt == "mode_filter":
		cmd = f"image.filter(ImageFilter.ModeFilter(size=random.randint(1, ({size[0]} // 2))))"

	else:
		raise Exception(f'{filt} not implemented')

	return cmd

# Select Shape
def select_shape(shape, points):
	if shape == "line":
		cmd = "draw.line((attributes['x0'], attributes['y0']) + (attributes['x1'], attributes['y1']), width=attributes['w'], fill=random.choice(colors))"

	elif shape == "curve":
		string = ""

		for index, digit in enumerate(range(points)):
			if index == 0:
				string += '['

			string += f"(attributes['x{digit}'], attributes['y{digit}'])"

			if index < len(range(points)) - 1:
				string += ', '

			if index == len(range(points)) - 1:
				string += ']'

		cmd = f"draw.line({string}, width=attributes['w'], fill=random.choice(colors), joint='curve')"

	elif shape == "circle":
		cmd = "draw.circle((attributes['x0'], attributes['y0']), radius=attributes['r'], outline=random.choice(colors), fill=random.choice(colors), width=attributes['w'])"

	elif shape == "arc":
		cmd = "draw.arc([(attributes['x0'], attributes['y0']), (attributes['x1'], attributes['y1'])], start=attributes['start'], end=attributes['end'], fill=random.choice(colors), width=attributes['w'])"
	
	elif shape == "chord":
		cmd = "draw.chord([(attributes['x0'], attributes['y0']), (attributes['x1'], attributes['y1'])], start=attributes['start'], end=attributes['end'], outline=random.choice(colors), fill=random.choice(colors), width=attributes['w'])"
	
	elif shape == "ellipse":
		cmd = "draw.ellipse([(attributes['x0'], attributes['y0']), (attributes['x1'], attributes['y1'])], outline=random.choice(colors), fill=random.choice(colors), width=attributes['w'])"
	
	elif shape == "pieslice":
		cmd = "draw.pieslice([(attributes['x0'], attributes['y0']), (attributes['x1'], attributes['y1'])], start=attributes['start'], end=attributes['end'], outline=random.choice(colors), fill=random.choice(colors), width=attributes['w'])"

	elif shape == "point":
		cmd = "draw.point((attributes['x0'], attributes['y0']), fill=random.choice(colors))"

	elif shape == "polygon":
		string = ""

		for index, digit in enumerate(range(points)):
			if index == 0:
				string += '['

			string += f"(attributes['x{digit}'], attributes['y{digit}'])"

			if index < len(range(points)) - 1:
				string += ', '

			if index == len(range(points)) - 1:
				string += ']'

		cmd = f"draw.polygon({string}, width=attributes['w'], fill=random.choice(colors))"

	elif shape == "regular_polygon":
		cmd = f"draw.regular_polygon(bounding_circle=attributes['bounding_circle'], n_sides=attributes['n_sides'], rotation=attributes['rotation'], fill=random.choice(colors), outline=random.choice(colors), width=attributes['w'])"

	elif shape == "rectangle":
		cmd = f"draw.rectangle([(attributes['x0'], attributes['y0']), (attributes['x1'], attributes['y1'])], fill=random.choice(colors), outline=random.choice(colors), width=attributes['w'])"

	elif shape == "rounded_rectangle":
		cmd = f"draw.rounded_rectangle([(attributes['x0'], attributes['y0']), (attributes['x1'], attributes['y1'])], radius=attributes['r'], fill=random.choice(colors), outline=random.choice(colors), corners=attributes['corners'])"

	else:
		raise Exception(f'{shape} not implemented')

	return cmd


###############################################################################
# Classes
###############################################################################
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

		signal.signal(signal.SIGALRM, timeout_handler)

	# Delect Image
	def delete_image(self, file_path):
		os.remove(file_path)

	# Generate Image Simple
	def generate_image_simple(self, path=None, image_mode='RGB', extension='jpg', image_name_length=32, image_size=(1920, 1080), colors=None, shapes=None, filters=None):
		if self.mode.lower() == "light":
			shapes_k = 50
			filters_k = 5
			num_shapes = 100
			num_filters = 1
			noise_types = ["guassian", "salt_pepper"]
			noise_level = "light"

		elif self.mode.lower() == "medium":
			shapes_k = 50
			filters_k = 5
			num_shapes = 250
			num_filters = 5
			noise_types = ["guassian", "salt_pepper", "poisson"]
			noise_level = "light"

		elif self.mode.lower() == "heavy":
			shapes_k = 50
			filters_k = 5
			num_shapes = 250
			num_filters = 5
			noise_types = ["guassian", "salt_pepper", "poisson", "speckle"]
			noise_level = "medium"

		dir_path = Utils.check_path(base_path=path if path is not None else os.getcwd(), folder_name='Images')

		density = random.randint(1, 300)

		if shapes is None:
			shapes = random.choices(LIST_OF_SHAPES, k=shapes_k)

		else:
			shapes = random.choices(shapes, k=shapes_k)

		if filters is None:
			filters = random.choices(LIST_OF_FILTERS, k=filters_k)

		else:
			filters = random.choices(filters, k=filters_k)

		if self.mode.lower() == "light":
			filters = [filt for filt in filters if filt not in LIGHT_MODE_EXCLUDED_FILTERS]

		elif self.mode.lower() == "medium":
			filters = [filt for filt in filters if filt not in MEDIUM_MODE_EXCLUDED_FILTERS]

		return self.generate_image(path=dir_path, image_mode=image_mode, extension=extension, image_name_length=32,
					  			   height=image_size[0], width=image_size[1], density=density, colors=colors,
					  			   num_shapes=num_shapes, shapes=shapes,
					  			   num_filters=num_filters, filters=filters,
					  			   noise_level=noise_level, noise_types=noise_types)

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
				self.mean = random.uniform(10, 100)
				self.var = random.uniform(10, 100)
				self.local_vars = np.random.uniform(low=10, high=100, size=image.size)
				self.amount = random.uniform(0.1, 0.5)
				self.salt_vs_pepper = 0.5

			elif noise_level.lower() == "medium":
				self.mean = random.uniform(10, 100)
				self.var = random.uniform(10, 100)
				self.local_vars = np.random.uniform(low=10, high=100, size=image.size)
				self.amount = random.uniform(0.1, 0.5)
				self.salt_vs_pepper = 0.5

			elif noise_level.lower() == "heavy":
				self.mean = random.uniform(10, 100)
				self.var = random.uniform(10, 100)
				self.local_vars = np.random.uniform(low=10, high=100, size=image.size)
				self.amount = random.uniform(0.5, 1.0)
				self.salt_vs_pepper = 0.5

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

		for shape, filt in zip_longest(list_of_shapes[:num_shapes], list_of_filters[:num_filters], fillvalue=None):
			if shape:
				points = random.randint(3, 10)
				cmd = select_shape(shape, points)

				attributes = get_shape_attributes(height, width, shape, points, density)

				if self.debug and self.verbose:
					print("\t\t" + cmd)
					print("\t\t" + str(attributes))

				signal.alarm(TIME_OUT)

				try:
					eval(cmd)
				except Exception as ex:
					if self.debug:
						print(f"Bailing on creating shape due to: {ex}")

				signal.alarm(0)

			if filt:
				radius = random.uniform(1, min(height, width))
				size = [random.randint(10, max(height // 4, 11)), random.randint(1, max(width // density, 2))]
				rank = random.randint(0, min(height, width) // 4)
				percent = random.randint(0, self.max_percent)
				threshold = random.randint(0, self.max_threshold)
				kernel = list(random.uniform(0, self.max_kernel[0]) for _ in range(self.max_kernel[1]))
				scale = random.uniform(1, self.max_scale)
				offset = random.uniform(0, self.max_offset)

				cmd = select_filter(filt, radius, size, percent, threshold, kernel, scale, offset, rank)

				if self.debug and self.verbose:
					print("\t\t" + cmd)

				signal.alarm(TIME_OUT)

				try:
					eval(cmd)
				except Exception as ex:
					if self.debug:
						print(f"Bailing on creating filter due to: {ex}")
				
				signal.alarm(0)

		exif = image.getexif()

		exif[ExifTags.ImageDescription.value] = f"mode: {self.mode.lower()}"

		image.save(output_file_name, exif=exif)

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

		if self.debug:
			print(f"\nFile saved @ {output_file_name}")

		return output_file_name


if __name__ == "__main__":
	mode = "medium"
	debug = True
	verbose = False

	num_generated = 10

	max_percent = 100
	max_threshold = 100
	max_kernel = (100, 10)
	max_scale = 10
	max_offset = 10

	image = PoisonImage(mode, debug, verbose, max_percent, max_threshold, max_kernel, max_scale, max_offset)

	shapes = ["line"]
	filters = None

	if debug:
		import time
		average_time = 0.0

	for color_key, colors in DICT_OF_COLORS.items():
		for index in range(1, num_generated + 1):
			if debug:
				start_time = time.thread_time()
				print(f"\nGenerating image #{index} in color scheme {color_key}")

			output_file_name = image.generate_image_simple(path=None, image_mode='RGB', extension='png', image_name_length=32, image_size=(1920, 1080), colors=colors, shapes=shapes, filters=filters)

			if debug:
				elapsed_time = time.thread_time() - start_time
				average_time = (average_time * (index - 1) + elapsed_time) / index
				print(f"\telapsed time: {elapsed_time:3.3f} s")

	if debug:
		print(f"\naverage time: {average_time:3.3f} s")
		print(f"\nProgram complete")