from PIL import Image
from gooey import Gooey, GooeyParser
from os import listdir

def OpenImage(path):
	"""
	Opens an image using Image.open()
	"""
	return Image.open(path)

def SaveImage(path, image):
	"""
	Saves an image as PNG using image.save()
	"""
	image.save(path, "PNG")

def OverlayImage(image, overlay):
	"""
	Overlays the overlay on an image
	"""

	if(image.size[1] > overlay.size[1]):
		image = Resize(image, overlay.size, option="height")

	elif(image.size[1] < overlay.size[1]):
		overlay = Resize(overlay, image.size, option="height")

	image.paste(overlay, (image.size[0]-overlay.size[0], image.size[1]-overlay.size[1]), overlay)

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

def ListFiles(dir_path, extension):
	"""
	Returns all files from a directory with a certain extension
	"""
	files = []

	print(f"Listing files in {dir_path}")

	for filename in listdir(dir_path):
		if filename.endswith(extension):
			files.append(dir_path + "\\" + filename)

	print(f"Files found in {dir_path}")

	for f in files:
		print(f)

	return files

@Gooey
def main():
	parser = GooeyParser()

	parser.add_argument(
		"Images", 
		type=str, 
		help="A pasta com as imagens onde por o overlay",
		widget="DirChooser")

	parser.add_argument(
		"Overlay", 
		type=str, 
		help="O ficheiro para colocar como overlay", 
		widget="FileChooser")

	args = parser.parse_args()

	images = ListFiles(args.Images, ".jpg")

	overlay = OpenImage(args.Overlay)
	
	print('Processing Images')

	for image in images:
		SaveImage(image + "edited.PNG", OverlayImage(OpenImage(image), overlay))

if __name__ == "__main__":
	main()
