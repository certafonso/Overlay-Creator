import tempfile
import cv2
from glob import glob

def SplitFrames(video):
    """ Splits the frames of a video and puts them on a temporary directory """

    frames = tempfile.TemporaryDirectory(dir = "./")  

    success, frame = video.read()

    i = 0

    while success:
        cv2.imwrite(frames.name + "/frame{:05d}.png".format(i), frame)

        success, frame = video.read()

        i += 1

    print(f"Exported {i} frames from video")

    return frames

def JoinFrames(dir_path, out_path, frame_rate):
    """ Joins all images in a directory to a video """

    frames = []

    for filename in glob(dir_path + "/*.png"):
        img = cv2.imread(filename)
        frames.append(img)

    height, width, layers = frames[0].shape
    size = (width,height)

    print(f"Converting {len(frames)} frames to a video")
    
    out = cv2.VideoWriter(out_path + ".avi",cv2.VideoWriter_fourcc(*'DIVX'), frame_rate, size)
    
    for i in range(len(frames)):
        out.write(frames[i])
    out.release()



# f = SplitFrames(r"C:\Users\certa\Documents\Overlay-Creator\test\bubbles.mp4")

# JoinFrames(f.name, "./teste", 15)

# input("done")

# f.cleanup()
