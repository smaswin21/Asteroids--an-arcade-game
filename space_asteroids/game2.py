import pygame
from models2 import Rock, Spaceship, Bullet
from utils import load_sprite, print_text
from startPage import Start_Screen
import time


# Global lists to hold bullets and rocks
rocks = [] # List to store instances of 'Rock' objects.
bullets = [] # List to store instances of 'Bullet' objects.

# Dictionary to define the points for each size of the rock. 
# This allows for O(1) score updates since 
# we can directly look up the points based on rock size.
rock_points = {3: 100, 2: 50, 1: 25}

# Initialize the score variable to keep track of the player's score.
score = 0

# Function to update the score, this should be called whenever a rock is destroyed
def update_score(rock_size):
    global score
    score += rock_points[rock_size]

# Class representing the main game.
class Asteroids:
    
    # Constructor to initialize the game state.
    def __init__(self, username):
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.username = username
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.ship = Spaceship((400, 300), self)
        self.bullets = bullets  # Using the global bullets list
        # Instantiate global rocks list with randomly placed rocks at the start of the game.
        global rocks
        rocks = [Rock.create_random(self.screen, self.ship.position) for _ in range(6)]

    def main_loop(self):
        while True:
            self.handles_input()  # Handles player's input
            self.game_logic()  # Runs the game logic (movement, collision detection, etc.)
            self.draw()  # Renders the game objects to the screen
            
            # Check if the game has been won or lost and print the outcome with the score.
            if self.message == "You won!" or self.message == "You lost!":
                print(f"Username: {self.username}, Score: {score}")
                time.sleep(1)
                break  # Exit the main game loop if a game-ending condition is met.
            
        return score
    # Return the player's score after the loop ends.
            
    def handles_input(self):

        # Handles input from the player each frame.

        for event in pygame.event.get():
            # Allow the player to quit the game.
            if event.type == pygame.QUIT:
                quit()
            # Respond to key presses.
            if event.type == pygame.KEYDOWN:
                # Shooting mechanics, listening for SPACE or B key to shoot.
                if event.key == pygame.K_SPACE or event.key == pygame.K_b:  # Listen for SPACE or B key
                    self.ship.shoot()
        
        # Check for continuous key presses.
        is_key_pressed = pygame.key.get_pressed()

        # Allow the player to quit using ESC or Q key.
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()
        
        # If the ship has been destroyed, no need to process further input.
        if self.ship is None:
            return
        
        # Ship rotation and acceleration based on arrow key input.
        if is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate() 
        elif is_key_pressed[pygame.K_DOWN]:
            self.ship.decelerate()  

    @property
    def game_objects(self):
        # Property gets a combined list of all game objects.
        # This design simplifies the process of 
        # iterating over all objects for drawing and updating their state.
        global bullets, rocks
        stuff = [*bullets, *rocks]
        if self.ship:
            stuff.append(self.ship)
        return stuff

    def game_logic(self):
        # Core game logic processing each frame.
        global bullets, rocks

        # Move all game objects.
        for obj in self.game_objects:
            obj.move(self.screen)

        # Remove bullets that have left the screen.
        rect = self.screen.get_rect()  # Get the screen's rectangle.
        for bullet in bullets[:]:      # Iterate over a copy of the bullets list.
            if not rect.collidepoint(bullet.position):  # Check if bullet is out of screen.
                bullets.remove(bullet)

        # Check for bullet and rock collisions.
        for bullet in bullets[:]:
            for rock in rocks[:]:
                if rock.collides_with(bullet):  # If a collision is detected.
                    update_score(rock.size)  # Update score based on rock size.
                    rocks.remove(rock)  # Remove the rock from the list.
                    rock.split()  # Split the rock into smaller rocks.
                    bullets.remove(bullet)  # Remove the bullet.
                    break  # Exits the inner loop after a collision.

        # Check if the ship collides with any rock.
        if self.ship:
            for rock in rocks[:]:
                if rock.collides_with(self.ship):
                    self.ship = None  # Ship is destroyed.
                    self.message = "You lost!"  # Set the losing message.
                    break

        # Check if all rocks are destroyed.
        if not rocks and self.ship:
            self.message = "You won!"  # Set the winning message.

    def draw(self):
        # Draw all game objects and UI elements.
        self.screen.blit(self.background, (0, 0))  # Draw the background.

        # Draw all game objects.
        for obj in self.game_objects:
            obj.draw(self.screen)

        # Display the current score.
        print_text(self.screen, f"Score: {score}", self.font, (255, 255, 255), top_right=True)

        # Display a message if the game is over.
        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()  # Update the full display Surface to the screen.
        self.clock.tick(30)    # Limit the frame rate to 30 frames per second.