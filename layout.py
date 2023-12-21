# layout.py

import pygame
import random

# Initializes and sets up using pygame
pygame.init() # Initializes Pygame modules
pygame.display.set_caption("Test Try") 

"""
# Creates a window of size 900x600 pixels 
# This is essentially setting up a 2D array (or matrix) 
# where each element represents a pixel on the screen.
"""
screen = pygame.display.set_mode((900, 600)) 

# Main Game Loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()  # Exits the game if the QUIT event is triggered

    # Drawing on Screen
    screen.fill((135, 206, 235)) # Fills the screen with a light blue color
    x = random.randint(10, 790)  #  x-coordinate
    y = random.randint(10, 590)  #  y-coordinate
    r = random.randint(2, 10)    #  radius for the circle

    # The randomness in x, y, and r adds an element of unpredictability
    pygame.draw.circle(screen, (0, 0, 150), (x, y), r) # Draws a circle at the random location

    # Display Update
    pygame.display.flip()  # Updates the entire screen to reflect the new drawings