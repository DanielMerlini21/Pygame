import os
from MazeGenerator import *

def load_images():
    files = os.listdir()
    directory = os.getcwd()
    images = {}

    for file in files:
        if (os.path.splitext(file))[1] == ".png":
            file_path = os.path.join(directory, file)
            image = pygame.image.load(file_path)
            images[os.path.splitext(os.path.basename(file_path))[0]] = image
    return images

print(load_images())