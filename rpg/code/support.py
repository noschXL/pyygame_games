from os import walk
import pygame
import os

def import_folder(path):
    surface_list = []

    img_files = os.listdir(path)
    img_files = sorted(img_files, key=lambda x: int(x.split('.')[0]))
    
    for image in img_files:
        full_path = os.path.join(path, image)
        print(f"Loading image: {full_path}")
        image_surf = pygame.image.load(full_path).convert_alpha()
        surface_list.append(image_surf)

    return surface_list