###############################################################################
# Program : Poison
# File : Utils.py
# Author : catte
# Created : Sept 13, 2024
# Copyright : catte @ 2024
# License : CC BY-NC 4.0
###############################################################################
import os, random, string
from collections import OrderedDict

###############################################################################
# Constants
###############################################################################
LIST_OF_MODES = ["light", "medium", "heavy"]

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

[LIST_OF_SHAPES.remove(shape) for shape in NOT_IMPLEMENTED_SHAPES]

[LIST_OF_FILTERS.remove(filt) for filt in NOT_IMPLEMENTED_FILTERS]

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

EXPECTED_CONFIG_DICT = { "config": str(),
						 "mode": str(),
						 "debug": bool(),
						 "verbose": bool(),
						 "max_percent": int(),
						 "max_threshold": int(),
						 "max_kernel": list(),
						 "max_scale": int(),
						 "max_offset": int(),
						 "generate_image": bool()
}


###############################################################################
# Helper Functions
###############################################################################

# Check Path
def check_path(path=None):
	if path is None:
		path = os.path.join(os.getcwd(), 'Images')

		if not os.path.isdir(path):
			os.mkdir(path)

	if not os.path.isdir(path):
		raise Exception(f"The path {path} is not a directory")

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
		cmd = f"raise Exception('{filt} not implemented')"

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
		cmd = f"raise Exception('{shape} not implemented')"

	return cmd

# Generate URL
def generate_url(root=None, length=32, extension="html"):
	str_name = str(''.join(random.choices(string.ascii_leters + string.digits, k=length)))
	url = root + '/' + str_name + '.' + extension

	return url

# Generate File Name
def generate_file_name(path=None, length=32, extension='jpg'):
	path = check_path(path=path)

	str_name = str(''.join(random.choices(string.ascii_letters + string.digits, k=length)))
	file_name =  str_name + '.' + extension

	return os.path.join(path, file_name)
