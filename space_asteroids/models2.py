# models.py
# Import necessary Pygame modules and utility functions
from pygame.math import Vector2
from pygame.transform import rotozoom
import random
from utils import load_sprite, load_sound, wrap_position, print_text

# Constants for movement direction
DIRECTION_UP = Vector2(0, -1)

# Base class for all game objects.
class GameObject:
    def __init__(self, position, sprite, velocity, wraps=True):

        # Initialize common attributes for game objects.
        self.position = Vector2(position)  # Position as a 2D vector for easy manipulation.
        self.sprite = sprite  # Image representation of the object.
        self.radius = sprite.get_width() / 2  # Collision detection radius.
        self.velocity = Vector2(velocity)  # Velocity as a 2D vector.
        self.wraps = wraps  # Flag to determine if object wraps around screen edges.

    def draw(self, surface):
        # Draw the object on the given surface (screen).
        position = self.position - Vector2(self.radius)  # Adjust position for drawing.
        surface.blit(self.sprite, position)  # Blit the sprite on the surface.

    def move(self, surface):
        # Update the object's position based on its velocity.
        move_to = self.position + self.velocity  # Calculate new position.
        self.position = wrap_position(move_to, surface) if self.wraps else move_to  # Wrap position if required.

    def collides_with(self, other):
        # Check for collision with another object using radii and distance.
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius

# Spaceship class extending GameObject.
class Spaceship(GameObject):
    # Class constants defining spaceship behavior.
    ROTATION_SPEED = 4
    ACCELERATION = 0.20
    BULLET_SPEED = 3

    def __init__(self, position, asteroids_instance):
        # Initialize the spaceship with specific attributes.
        self.direction = Vector2(DIRECTION_UP)  # Initial direction facing up.
        self.pew_pew = load_sound("laser")  # Load shooting sound effect.
        super().__init__(position, load_sprite("spaceship"), Vector2(0))  # Initialize base class.
        self.asteroids_instance = asteroids_instance  # Reference to the game instance.

    def rotate(self, clockwise=True):
    # Adjusts the rotation of the spaceship.
        sign = 1 if clockwise else -1  # Determine rotation direction based on the 'clockwise' flag.
        angle = self.ROTATION_SPEED * sign  # Calculate rotation angle per frame.
        self.direction.rotate_ip(angle)  # Rotate the direction vector in place.

    def accelerate(self):
        # Increases the spaceship's velocity in its current direction.
        self.velocity += self.direction * self.ACCELERATION  # Add acceleration to the velocity vector.

    def decelerate(self):
        # Decreases the spaceship's velocity.
        self.velocity -= self.direction * self.ACCELERATION  # Subtract acceleration from the velocity vector.
        # Ensure the velocity does not become negative, which would reverse the spaceship.
        if self.velocity.length() < 0:
            self.velocity = Vector2(0, 0)  # Reset velocity to zero if it becomes negative.


    def shoot(self):
    # Handles shooting mechanics for the spaceship.
    # The bullet's velocity is a combination of the spaceship's current direction and its velocity.
        velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, velocity)  # Create a new bullet instance.
        self.asteroids_instance.bullets.append(bullet)  # Add the bullet to the game's bullet list.
        self.pew_pew.play()  # Play shooting sound effect.

    def draw(self, surface):
        # Renders the rotated spaceship on the given surface.
        # Calculate the angle for rotation based on the current direction relative to up.
        angle = self.direction.angle_to(DIRECTION_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)  # Rotate the sprite image.
        # Calculate the correct position to blit the rotated sprite.
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)  # Draw the rotated sprite on the surface.

class Rock(GameObject):
    # Constants defining rock behavior.
    MIN_START_GAP = 250  # Minimum distance from the spaceship for rock to appear.
    MIN_SPEED = 1  # Minimum speed of a rock.
    MAX_SPEED = 3  # Maximum speed of a rock.

    @classmethod
    def create_random(cls, surface, ship_position):
        # Generates a rock at a random position, ensuring it doesn't appear too close to the spaceship.
        while True:
            position = Vector2(
                random.randrange(surface.get_width()),
                random.randrange(surface.get_height()),
            )
            # Ensure sufficient distance from the spaceship.
            if position.distance_to(ship_position) > cls.MIN_START_GAP:
                break
        return Rock(position)  # Create a new rock instance with this position.

    def __init__(self, position, size=3):
        # Initialize the rock with a specific size.
        # Adjust the sprite scale based on the size of the rock.
        scale = 1.0 if size == 3 else 0.5 if size == 2 else 0.25
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        # Randomize the velocity of the rock.
        speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        angle = random.randint(0, 360)
        velocity = Vector2(speed, 0).rotate(angle)
        super().__init__(position, sprite, velocity)

    def split(self):
        # Split the rock into smaller pieces upon collision.
        if self.size > 1:
            from game2 import rocks  # Import rocks list from game2 module.
            # Create two smaller rocks and add them to the rocks list.
            rocks.append(Rock(self.position, self.size - 1))
            rocks.append(Rock(self.position, self.size - 1))

class Bullet(GameObject):
    def __init__(self, position, velocity):
        # Initialize the bullet object.
        super().__init__(position, load_sprite("bullet"), velocity, False)  # Bullets don't wrap around the screen.
