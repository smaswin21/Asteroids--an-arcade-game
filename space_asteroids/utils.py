# utilities.py
import pygame
from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pathlib import Path


def load_sprite(name, with_alpha=True):
    # Construct the file path relative to the current file
    filename = Path(__file__).resolve().parent / f"assets/sprites/{name}.png"
    sprite = load(str(filename))  # Load the image from the file system

    # Image Processing
    if with_alpha:
        return sprite.convert_alpha()  # Return the image with alpha channel (transparency)
    else:
        return sprite.convert()  # Return the image without alpha channel

def wrap_position(position, surface):
    # Wrapping Position for Continuous Movement
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)  # Use modulo operation to wrap position around the surface

def load_sound(name):
    # Construct the file path for sound
    filename = Path(__file__).resolve().parent / f"assets/sounds/{name}.wav"
    return Sound(str(filename))  # Load the sound file

def print_text(surface, text, font, color=Color("tomato"), top_right=False):
    # Rendering and Displaying Text
    text_surface = font.render(text, True, color)  # Create a surface with the rendered text
    rect = text_surface.get_rect()  # Get the rectangle area of the text surface
    if top_right:
        rect.topright = (surface.get_width() - 10, 10)
    else:
        rect.center = Vector2(surface.get_size()) / 2  # Center the text
    surface.blit(text_surface, rect)  # Draw the text surface onto the main surface

def load_font(name, size):
    # Constructs the file path for the font
    filename = Path(__file__).resolve().parent / f"assets/sprites/{name}.ttf"
    return pygame.font.Font(str(filename), size)  # Loads the font file with the specified size

