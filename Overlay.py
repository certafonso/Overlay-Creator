from PIL import Image
from gooey import Gooey, GooeyParser

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
	
	print(image.size[1], overlay.size[1])

	if(image.size[1] > overlay.size[1]):
		image = Resize(image, overlay.size, option="height")

	elif(image.size[1] < overlay.size[1]):
		overlay = Resize(overlay, image.size, option="height")

	image.paste(overlay, (image.size[0]-overlay.size[0], image.size[1]-overlay.size[1]), overlay)

	SaveImage("teste.PNG", image)

def Resize(image, size, option=""):
	"""
	Resizes an image to a certain size. 
	option="height" will maintain the aspect ratio a match the heights
	option="width" will maintain the aspect ratio a match the width
	"""

	if option == "height":
		size = (int(size[1]/image.size[1]*image.size[0]), size[1])

	elif option == "width":
		size = (size[0], int(size[0]/image.size[0]*image.size[1]))

	return image.resize(size)

@Gooey
def main():
	parser = GooeyParser()

	parser.add_argument(
		"Image", 
		type=str, 
		help="A imagem onde por o overlay",
		widget="FileChooser")

	parser.add_argument(
		"Overlay", 
		type=str, 
		help="Tests directory", 
		widget="FileChooser")

	args = parser.parse_args()
	
	print('Processing Images')

	OpenImage(args.Image)
		
	OverlayImage(OpenImage(args.Image), OpenImage(args.Overlay))

if __name__ == "__main__":
	main()
