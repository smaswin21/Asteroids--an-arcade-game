import pygame
from game2 import Asteroids
from startPage import Start_Screen
from leaderboard import Leaderboard

# Main execution block that starts when the program is run.
if __name__ == "__main__":
    # Initialize the start screen and capture the username.
    start_screen = Start_Screen()
    username = start_screen.run()  

    # Create an instance of the game using the username.
    space_asteroids = Asteroids(username)  

    # Start the main game loop and retrieve the final score.
    score = space_asteroids.main_loop() # Complexity depends on the game's main loop implementation.

    # Creates a leaderboard instance and updates it with the new score.
    leaderboard = Leaderboard()  
    leaderboard.run_leaderb((username, score))  
    # O(n log n) complexity for sorting and updating the leaderboard.

    # Exit the game and clean up resources.
    pygame.quit()  
