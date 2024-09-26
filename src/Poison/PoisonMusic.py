###############################################################################
# Program : Poison
# File : PoisonImage.py
# Author : catte
# Created : Sept 19, 2024
# Copyright : catte @ 2024
# License : CC BY-NC 4.0
###############################################################################

###############################################################################
# Imports
###############################################################################
import random, os, wave

# Signals
from gensound import Sine, Triangle, Square, Sawtooth

# Transforms
from gensound import Shift, Extend, Reverse, Fade, FadeIn, FadeOut, CrossFade
from gensound import Gain, SineAM, Limiter, Mono, Pan, Repan, Convolution, ADSR

# Poison
# from . import Utils
import Utils


###############################################################################
# Constants
###############################################################################
LIST_OF_SIGNALS = ["sine", "triangle", "square", "sawtooth"]

LIST_OF_CURVES = ["constant", "line", "logistic", "sinecurve", "log"]

LIST_OF_TRANSFORMS = ["shift", "extend", "reverse", "fadein", "fadeout",
					  "sineam", "limiter", "mono",
					  "pan", "convolution", "adsr"]

LIST_OF_PITCHES = ["a", "b", "c", "d", "e", "f", "g", "r"]

LIST_OF_ACCIDENTALS = ["#", "b", None]

LIST_OF_OCTAVES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

NOT_IMPLEMENTED_TRANSFORMS = ["crossfade", "limiter", "mono", "pan", "convolution", "adsr"]

LIST_OF_TRANSFORMS = [x for x in LIST_OF_TRANSFORMS if x not in NOT_IMPLEMENTED_TRANSFORMS ]

DICT_OF_MAJOR_KEYS = {
	"A": ["a", "b", "c#", "d", "e", "f#", "g#", "r"],
	"Ab": ["ab", "bb", "c", "db", "eb", "f", "g", "r"],
	"B": ["b", "c#", "d#", "e", "f#", "g#", "a#", "r"],
	"Bb": ["bb", "c", "d", "eb", "f", "g", "a", "r"],
	"C": ["c", "d", "e", "f", "g", "a", "b", "r"],
	"Cb": ["cb", "db", "eb", "fb", "gb", "ab", "bb", "r"],
	"D": ["d", "e", "f#", "g", "a", "b", "c#", "r"],
	"Db": ["db", "eb", "f", "gb", "ab", "bb", "c", "r"],
	"E": ["e", "f#", "g#", "a", "b", "c#", "d#", "r"],
	"Eb": ["eb", "f", "g", "ab", "bb", "c", "d", "r"],
	"F": ["f", "g", "a", "bb", "c", "d", "e", "r"],
	"F#": ["f#", "g#", "a#", "b", "c#", "d#", "e#", "r"],
	"G": ["g", "a", "b", "c", "d", "e", "f#", "r"],
	"Gb": ["gb", "ab", "bb", "cb", "db", "eb", "f", "r"]
}

DICT_OF_MINOR_KEYS = {
	"A": ["a", "b", "c", "d", "e", "f", "g", "r"],
	"A#": ["a#", "b#", "c#", "d#", "e#", "f#", "g#", "r"],
	"Ab": ["ab", "bb", "cb", "db", "eb", "fb", "gb", "r"],
	"B": ["b", "c#", "d", "e", "f#", "g", "a", "r"],
	"Bb": ["bb", "c", "db", "eb", "f", "gb", "ab", "r"],
	"C": ["c", "d", "eb", "f", "g", "ab", "bb", "r"],
	"C#": ["c#", "d#", "e", "f#", "g#", "a", "b", "r"],
	"D": ["d", "e", "f", "g", "a", "bb", "c", "r"],
	"D#": ["d#", "e#", "f#", "g#", "a#", "b", "c#", "r"],
	"E": ["e", "f#", "g", "a", "b", "c", "d", "r"],
	"Eb": ["eb", "f", "gb", "ab", "bb", "cb", "db", "r"],
	"F": ["f", "g", "ab", "bb", "c", "db", "eb", "r"],
	"F#": ["f#", "g#", "a", "b", "c#", "d", "e", "r"],
	"G": ["g", "a", "bb", "c", "d", "eb", "f", "r"],
	"G#": ["g#", "a#", "b", "c#", "d#", "e", "f#", "r"]
}


###############################################################################
# Helper Functions
###############################################################################

# Is Rest?
def is_rest(pitch):
	""" Is Rest?
		:description:
		:param pitch:	str
		:return rest:	bool
	"""
	return pitch.lower() == 'r'

# Select Signal
def select_signal(signal, song_duration):
	""" Select Signal
		:description:
		:param signal:			str
		:param song_duration:	int
		:return cmd:			str
	"""
	if signal.lower() == "sine":
		cmd = f"Sine(song_layer, duration={song_duration})"

	elif signal.lower() == "triangle":
		cmd = f"Triangle(song_layer, duration={song_duration})"

	elif signal.lower() == "square":
		cmd = f"Square(song_layer, duration={song_duration})"

	elif signal.lower() == "sawtooth":
		cmd = f"Sawtooth(song_layer, duration={song_duration})"

	else:
		raise Exception(f"Signal {signal} not recognized")

	return cmd

# Get Transform Attributes
def get_transform_attributes(transform, duration, curve, degree, frequency, size, phase):
	""" Get Transform Attributes
		:description:
		:param transform:
		:param duration:
		:param curve:
		:param degree:
		:param frequency:
		:param size:
		:param phase:
		:return attributes:
	"""
	attributes = {}
	if transform.lower() == "shift":
		attributes.update({'duration': duration})

	elif transform.lower() == "extend":
		attributes.update({'duration': duration})

	elif transform.lower() == "reverse":
		pass  # Reverse has no attributes

	elif transform.lower() == "fadein":
		attributes.update({'duration': duration})
		attributes.update({'curve': curve})
		attributes.update({'degree': degree})

	elif transform.lower() == "fadeout":
		attributes.update({'duration': duration})
		attributes.update({'curve': curve})
		attributes.update({'degree': degree})

	elif transform.lower() == "sineam":
		attributes.update({'frequency': frequency})
		attributes.update({'size': size})
		attributes.update({'phase': phase})

	elif transform.lower() == "limiter":
		pass  # Not implemented

	elif transform.lower() == "mono":
		pass  # Not implemented

	elif transform.lower() == "pan":
		pass  # Not implemented

	elif transform.lower() == "convolution":
		pass  # Not implemented

	elif transform.lower() == "adsr":
		pass  # Not implemented

	else:
		raise Exception(f"Transform {transform} not recognized")

	return attributes

# Select Transform
def select_transform(transform, transform_attributes):
	""" Select Transform
		:description:
		:param transform:				str
		:param transform_attributes:	dict
	"""
	if transform.lower() == "shift":
		cmd = f"Shift(duration={transform_attributes['duration']})"

	elif transform.lower() == "extend":
		cmd = f"Extend(duration={transform_attributes['duration']})"

	elif transform.lower() == "reverse":
		cmd = f"Reverse()"  # Reverse has no arguments

	elif transform.lower() == "fadein":
		cmd = f"FadeIn(duration={transform_attributes['duration']}, curve=\'{transform_attributes['curve']}\', degree={transform_attributes['degree']})"

	elif transform.lower() == "fadeout":
		cmd = f"FadeOut(duration={transform_attributes['duration']}, curve=\'{transform_attributes['curve']}\', degree={transform_attributes['degree']})"

	elif transform.lower() == "sineam":
		cmd = f"SineAM(frequency={transform_attributes['frequency']}, size={transform_attributes['size']}, phase={transform_attributes['phase']})"

	elif transform.lower() == "limiter":
		cmd = f"Limiter()"  # Not implemented

	elif transform.lower() == "mono":
		cmd = f"Mono()"  # Not implemented

	elif transform.lower() == "pan":
		cmd = f"Pan"  # Not implemented

	elif transform.lower() == "convolution":
		cmd = f"Convolution()"  # Not implemented

	elif transform.lower() == "adsr":
		cmd = f"ADSR()"  # Not implemented

	else:
		raise Exception(f"Transform {transform} not recognized")

	return cmd


###############################################################################
# Classes
###############################################################################

# Note Class
class Note(object):
	# Initialize
	def __init__(self, pitch="A", accidental=None, octave=5, cents=0, duration=1):
		""" Initialize the Note class instantiation
			:description:
			:param pitch:		str
			:param accidental:	str | None
			:param octave:		int
			:param cents:		int
			:param duration:	int
			:return None:
		"""
		if len(pitch) > 1 and pitch.endswith('b'):
			pitch = pitch[:-1]

		if pitch.replace('#', '').lower() not in LIST_OF_PITCHES:
			raise Exception(f"Unknown pitch {pitch}. Try {LIST_OF_PITCHES}")

		rest = is_rest(pitch)

		self.pitch = pitch

		self.accidental = ''
		if not rest and accidental is not None:
			if accidental in ["#", 'b', '']:
				self.accidental = accidental

			else:
				raise Exception(f"Unknown accidental {accidental}. Try {LIST_OF_ACCIDENTALS}")

		else:
			self.accidental = ''

		if not (0 <= octave <= 9):
			raise Exception(f"Unknown octave {octave}. Use a number between 0 and 9, inclusive")

		self.octave = octave if not rest else ''

		if cents is not None and not (-255 <= cents <= 255):
			raise Exception(f"Unknown cents {cents}. Use a number between -255 and 255, inclusive")

		self.cents = abs(cents) if not rest and cents is not None else ''

		if self.cents != '' and not rest:
			self.sign = '+' if cents >= 0 else '-'

		else:
			self.sign = ''

		if duration <= 0:
			raise Exception(f"Invalid duration {duration}. Use a positive, non-zero integer value")

		self.duration = duration

	def __str__(self):
		return f"{self.pitch.upper()}{self.accidental}{self.octave}{self.sign}{self.cents}={self.duration}"

# PoisonSound Class
class PoisonMusic(object):
	# Initialize
	def __init__(self, mode="", debug=False, verbose=False):
		""" Initialize
			:description:	Initializes the PoisonSound class instantiation
			:param mode:	str
			:param debug:	bool
			:param verbose:	bool
		"""
		self.mode = mode
		self.debug = debug
		self.verbose = verbose

	def delete_music(self, music_file_name):
		os.remove(music_file_name)

	def get_duration(self, file_path):
		with wave.open(file_path, 'r') as audio_file:
			frame_rate = audio_file.getframerate()
			n_frames = audio_file.getnframes()

		duration = n_frames / float(frame_rate)

		return duration

	# Generate Music Simple
	def generate_music_simple(self, octave_range="low", base_path=None, key=None, key_type="major", num_notes=100, max_note_duration=100, song_duration=600, extension='wav'):
		""" Generate Music Simple
			:description:	Generate music with a simple interface
			:param octave_range: 		str
			:param base_path:			str | None
			:param key:					str
			:param key_type:			str
			:param num_notes:			int
			:param max_note_duration:	int
			:param song_duration:		int
			:param extension:			str
			:return file_name:			str
		"""
		pitches = []
		accidentals = []
		cents = []

		if self.mode.lower() == "light":
			num_song_layers = 5

		elif self.mode.lower() == "medium":
			num_song_layers = 50

		elif self.mode.lower() == "heavy":
			num_song_layers = 100

		else:
			raise Exception(f"Mode {self.mode} is not known")

		if key_type == "major" and key in list(DICT_OF_MAJOR_KEYS.keys()):
			pitches = DICT_OF_MAJOR_KEYS[key]
			accidentals = ['']
			cents = [None]

		elif key_type == "minor" and key in list(DICT_OF_MINOR_KEYS.keys()):
			pitches = DICT_OF_MINOR_KEYS[key]
			accidentals = ['']
			cents = [None]

		elif key_type == "all":
			pitches = LIST_OF_PITCHES
			accidentals = LIST_OF_ACCIDENTALS
			cents = [random.randint(-255, 255) for _ in range(num_notes)]

		else:
			raise Exception(f"Key {key} type {key_type} is not known")

		if octave_range == "low":
			octaves = range(5)

		elif octave_range == "middle":
			octaves = range(3, 7)

		elif octave_range == "high":
			octaves = range(5, 10)

		elif octave_range == "all":
			octaves = LIST_OF_OCTAVES

		else:
			raise Exception(f"Octave range {octave_range} is not known")

		signals = LIST_OF_SIGNALS
		transforms = LIST_OF_TRANSFORMS

		num_transforms = 10

		return self.generate_music(base_path=base_path, extension=extension, pitches=pitches, accidentals=accidentals, octaves=octaves, cents=cents,
								   max_note_duration=max_note_duration, num_notes=num_notes, num_song_layers=num_song_layers, song_duration=song_duration,
								   signals=signals, transforms=transforms, num_transforms=num_transforms)

	# Generate Music
	def generate_music(self, base_path=None, extension='wav', pitches=[], accidentals=[], octaves=[], cents=[],
					   max_note_duration=100, num_notes=100, num_song_layers=100, song_duration=600,
					   signals=[], transforms=[], num_transforms=10):
		""" Generate Music
			:description:	Generate music in the desired location with the desired extension
			:param base_path:		str | None 	
			:param extension:		str
			:param pitches:			list
			:param accidentals:		list
			:param octaves:			list
			:param cents:			list
			:param signals:			list
			:param transforms:		list
			:param num_transforms:	int
			:return file_name:		str
		"""
		if self.debug and self.verbose:
			print(f"Pitches: {pitches}")
			print(f"Accidentals: {accidentals}")
			print(f"Octaves: {octaves}")
			print(f"Cents: {cents}")
			print(f"Song duration: {song_duration}")
			print(f"Num notes: {num_notes}")
			print(f"Num song layers: {num_song_layers}")

		save_succeeded = False

		if base_path is None:
			base_path = os.getcwd()

		file_name = Utils.generate_file_name(path=base_path, length=32, extension='wav')

		while not save_succeeded:
			notes = self.generate_notes(pitches=pitches, accidentals=accidentals, octaves=octaves, cents=cents, max_note_duration=max_note_duration, num_song_layers=num_song_layers)

			song_layers = self.generate_song_layers(notes=notes, num_song_layers=num_song_layers)

			waveforms = self.generate_waveforms(song_duration=song_duration, song_layers=song_layers, signals=signals, transforms=transforms, num_transforms=num_transforms)
			
			combined_waveform = sum(waveforms)

			try:
				combined_waveform.export(file_name)
			except ValueError as ex:
				if self.debug and self.verbose:
					print(f"Error in generating file: {ex}")
			else:
				save_succeeded = True

		return file_name

	# Generate Notes
	def generate_notes(self, pitches=[], accidentals=[], octaves=[], cents=[], max_note_duration=10, num_notes=100, num_song_layers=10):
		""" Generate Notes
			:description:	Generates the notes in a song
			:param pitches: 			list 	A list of pitches to be used to generate a song
			:param accidentals:			list 	A list of accidentals to be used to generate a song
			:param octaves:				list 	A list of octaves to be used to generate a song
			:param cents:				list 	A list of cents to be used to generate a song
			:param max_note_duration:	int 	The maximum length of time for a note to last
			:param num_notes:			int 	The number of notes to be used in generating a song
			:param num_song_layers:		int 	The number of song layers to be used in generating a song
			:return notes:				list 	A list of notes generated
		"""
		notes = [[Note(random.choice(pitches), random.choice(accidentals), random.choice(octaves), random.choice(cents), random.randint(1, max_note_duration)) for _ in range(num_notes)] for __ in range(num_song_layers)]

		return notes

	# Generate Song Layers
	def generate_song_layers(self, notes=[], num_song_layers=10):
		""" Generate Song Layers
			:description: 	Generates the song layers needed to generate a song from a list of notes
			:param notes: 			list 	A list of notes to be processed into song layers
			:param num_song_layers:	int 	The number of song layers to be generated
			:return song_layers: 	list 	A list of song layers that were generated
		"""
		song_layers = [' '.join([str(note) for note in notes[index]]) for index in range(num_song_layers)]

		return song_layers

	# Generate Waveforms
	def generate_waveforms(self, song_duration=600, song_layers=[], signals=["sine"], transforms=[], num_transforms=10):
		""" Generate Waveforms
			:description:	Generates a number of waveforms equal to len(song_layers) to be combined later into a single song track
			:param song_duration:	int 	Duration of the song
			:param song_layers:		list 	A list of song layers
			:param signals:			list 	A list of signals to be used
			:param transforms:		list    A list of transforms to be used
			:param num_transforms:  int 	Number of transforms to apply
			:return waveforms:		list 	A list of waveforms generated from the signals and transforms
		"""
		list_of_signals = [select_signal(random.choice(signals), song_duration) for _ in range(len(song_layers))]

		if self.debug and self.verbose:
			print(list_of_signals)

		list_of_transforms = []
		for _ in range(num_transforms * len(transforms)):
			transform = random.choice(transforms)
			curve = random.choice(["linear", "polynomial"])
			duration = random.choice(list(range(song_duration)))
			degree = random.choice(list(range(0, 360)))
			frequency = random.randint(300, 3000)
			size = random.randint(300, 3000)
			phase = random.randint(0, 361)

			transform_attributes = get_transform_attributes(transform, duration, curve, degree, frequency, size, phase)
			list_of_transforms.append(select_transform(transform, transform_attributes))

		waveforms = []
		for song_layer, signal in zip(song_layers, list_of_signals):
			transform = random.choice(list_of_transforms)

			if self.debug and self.verbose:
				print(f"Transform: {transform}")

			waveforms.append(eval(signal) * eval(transform))

		return waveforms


###############################################################################
# Test
###############################################################################
if __name__ == "__main__":
	debug = True
	verbose = True

	mode = "heavy"

	num_notes = 100
	num_song_layers = 10
	num_of_songs = 10

	min_duration = 60
	max_duration = 600

	if debug:
		import time
		average_time = 0.0

	music = PoisonMusic(mode=mode, debug=debug, verbose=verbose)

	for index in range(1, num_of_songs + 1):
		duration = random.randint(min_duration, max_duration + 1)
		octave_range = random.choice(["low", "middle", "high", "all"])
		key_type = random.choice(["major", "minor", "all"])

		if key_type == "major":
			key = random.choice(list(DICT_OF_MAJOR_KEYS.keys()))

		elif key_type == "minor":
			key = random.choice(list(DICT_OF_MINOR_KEYS.keys()))

		else:
			key = random.choice(list(DICT_OF_MAJOR_KEYS.keys()) + list(DICT_OF_MINOR_KEYS.keys()))

		if debug:
			start_time = time.thread_time()
			print(f"\nGenerating music #{index - 1}")

		music.generate_music_simple(key=key, key_type=key_type, octave_range=octave_range, song_duration=duration)

		if debug:
			elapsed_time = time.thread_time() - start_time
			average_time = (average_time * (index - 1) + elapsed_time) / index
			print(f"\telapsed time: {elapsed_time:3.3f} s")

	if debug:
		print(f"\naverage time: {average_time:3.3f} s")
		print(f"\nProgram complete")
