from PIL import Image
from gooey import Gooey, GooeyParser
from os import listdir
import VideoProcessing
import tempfile
import cv2

IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "jfif"]
VIDEO_EXTENSIONS = ["mp4", "mov"]
OUTPUT_IMAGE = "PNG"
OUTPUT_VIDEO = "avi"

def GenerateOutname(path, extension):
	"""
	Generates the filename for the exit file
	"""

	# change the extension
	path = path.split(".")
	path[-1] = extension
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
	image.save(path, OUTPUT_IMAGE)

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

def ListFiles(dir_path, extensions):
	"""
	Returns all files from a directory with the given extensions
	"""
	files = []

	for filename in listdir(dir_path):
		if GetExtension(filename) in extensions:
			files.append(dir_path + "\\" + filename)

	print(f"{len(files)} files found in {dir_path}")

	return files

def ProcessFolder(paths, overlay, alignment, output_dir):
	""" Puts the overlay in all images of a list """

	for image in paths:
		print(f"Processing image {paths.index(image)+1}/{len(paths)}")
		SaveImage(output_dir + "\\" + GenerateOutname(image, OUTPUT_IMAGE), OverlayImage(OpenImage(image), overlay, alignment))

	print(f"{len(paths)} images processed successefully :)")

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

	overlay = OpenImage(args.Overlay)

	alignment = (align_arg[2] == "Direito", align_arg[1] == "Inferior")

	# process images
	images = ListFiles(args.Images, IMAGE_EXTENSIONS)

	ProcessFolder(images, overlay, alignment, args.Output)

	# process videos
	videos = ListFiles(args.Images, VIDEO_EXTENSIONS)

	for video in videos:
		print(f"Processing video {videos.index(video)+1}/{len(videos)}")

		# open video and split into frames
		print("Openning video...")
		capture = cv2.VideoCapture(video)
		frames_dir = VideoProcessing.SplitFrames(capture)
		frames = ListFiles(frames_dir.name, ["png"])

		# put overlay in frames
		overlayed_frames = tempfile.TemporaryDirectory(dir = "./")  
		ProcessFolder(frames, overlay, alignment, overlayed_frames.name)

		# join frames
		VideoProcessing.JoinFrames(overlayed_frames.name, args.Output + "\\" + GenerateOutname(video, ""), capture.get(cv2.CAP_PROP_FPS))
	
	print(f"{len(videos)} videos processed successefully :)")

if __name__ == "__main__":
	main()
