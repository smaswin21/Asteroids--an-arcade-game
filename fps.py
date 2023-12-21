import pygame

# Initialization
pygame.init()  # Initializes Pygame, a standard procedure in Pygame applications
pygame.display.set_caption("FPS")  # Sets the window title to FPS

# Window setup
width, height = 900, 600  # Setting up the dimensions for the window
screen = pygame.display.set_mode((width, height))  # Creates a window with specified dimensions

# Animation and Control Variables
position = 0  # Initial position for the moving object (circle)
direction = 1  # Initial direction of movement (1 for right, -1 for left)
speed = 3  # Speed of the object's movement
fps = 120  # Frame rate (frames per second)
clock = pygame.time.Clock()  # Clock object to control frame rate

# Main Game Loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()  # Exits the game if the window is closed

        # Keyboard Event Handling
        if event.type == pygame.KEYDOWN:
            # Adjusting speed and FPS with arrow keys
            if event.key == pygame.K_RIGHT:
                speed += 1  # Increase speed
            if event.key == pygame.K_LEFT and speed > 0:
                speed -= 1  # Decrease speed
            if event.key == pygame.K_UP:
                fps += 1  # Increase FPS
            if event.key == pygame.K_DOWN and fps > 1:
                fps -= 1  # Decrease FPS

            print(f"Speed: {speed} @ FPS: {fps}")

    # Updating Object Position
    position += direction * speed  # Update position based on speed and direction
    # Boundary checks to change direction
    if position <= 0:
        position = 0
        direction = 1
    elif position > width:
        position = width
        direction = -1

    # Drawing
    screen.fill((0, 0, 0))  # Clear screen
    pygame.draw.circle(screen, (255, 0, 0), (position, 300), 5)  # Draw moving object

    # Update Display
    pygame.display.flip()  # Refresh the screen with updated contents

    # Frame Rate Control
    clock.tick(fps)  # Maintain the game at the specified FPS
