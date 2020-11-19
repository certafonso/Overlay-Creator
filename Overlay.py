from PIL import Image
from gooey import Gooey, GooeyParser
from os import listdir

SUPPORTED_EXTENSIONS = ["png", "jpg", "jpeg"]
OUTPUT_EXTENSION = "PNG"

def GenerateOutname(path):
	"""
	Generates the filename for the exit file
	"""

	# change the extension
	path = path.split(".")
	path[-1] = OUTPUT_EXTENSION
	path = ".".join(path)

	# separate filename
	path = path.split("\\")[-1]

	return path

def OpenImage(path):
	"""
	Opens an image using Image.open()
	"""
	return Image.open(path)

def SaveImage(path, image):
	"""
	Saves an image as PNG using image.save()
	"""
	image.save(path, OUTPUT_EXTENSION)

def OverlayImage(image, overlay, alignment):
	"""
	Overlays the overlay on an image
	"""

	if(image.size[1] > overlay.size[1]):
		image = Resize(image, overlay.size, option="height")

	elif(image.size[1] < overlay.size[1]):
		overlay = Resize(overlay, image.size, option="height")


	image.paste(overlay, (image.size[0]-overlay.size[0] if alignment[0] else 0, image.size[1]-overlay.size[1] if alignment[1] else 0), overlay)

	return image

def Resize(image, size, option=""):
	"""
	Resizes an image to a certain size. 
	option="height" will maintain the aspect ratio and match the heights
	option="width" will maintain the aspect ratio and match the width
	"""

	if option == "height":
		size = (int(size[1]/image.size[1]*image.size[0]), size[1])

	elif option == "width":
		size = (size[0], int(size[0]/image.size[0]*image.size[1]))

	return image.resize(size)

def GetExtension(filename):
	"""
	Returns the extension (in lowercase) of a file
	"""
	return filename.split(".")[-1].lower()

def ListFiles(dir_path):
	"""
	Returns all files from a directory with the supported extensions
	"""
	files = []

	for filename in listdir(dir_path):
		if GetExtension(filename) in SUPPORTED_EXTENSIONS:
			files.append(dir_path + "\\" + filename)

	print(f"{len(files)} files found in {dir_path}")

	return files

@Gooey(
	progress_regex=r"^Processing image (?P<current>\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100"
	)
def main():
	parser = GooeyParser()

	parser.add_argument(
		"Images", 
		type=str, 
		help="A pasta com as imagens onde por o overlay",
		widget="DirChooser")

	parser.add_argument(
		"Output", 
		type=str, 
		help="A pasta para os ficheiros de output", 
		widget="DirChooser")

	parser.add_argument(
		"Overlay", 
		type=str, 
		help="O ficheiro para colocar como overlay", 
		widget="FileChooser")

	options = parser.add_argument_group(
		"Opções"
	)

	options.add_argument(
		'Alinhamento', 
		choices=["Canto Superior Direito", "Canto Superior Esquerdo", "Canto Inferior Direito", "Canto Inferior Esquerdo"], 
		default="Canto Inferior Direito",
		help="Alinhamento do overlay")

	args = parser.parse_args()

	align_arg = args.Alinhamento.split(" ")

	alignment = (align_arg[2] == "Direito", align_arg[1] == "Inferior")

	print(alignment)

	images = ListFiles(args.Images)

	overlay = OpenImage(args.Overlay)

	for image in images:
		print(f"Processing image {images.index(image)+1}/{len(images)}")
		SaveImage(args.Output + "\\" + GenerateOutname(image), OverlayImage(OpenImage(image), overlay, alignment))

	print(f"{len(images)} images processed successefully :)")

if __name__ == "__main__":
	main()
