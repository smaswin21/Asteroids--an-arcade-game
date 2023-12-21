import pygame

# Leaderboard class manages the display and sorting of game scores alphabetically and by score. 

class Leaderboard:

    # Initialization sets up the game window and loads necessary resources.

    def __init__(self):
        pygame.init()
        self.scores = []  # List to hold scores. Utilizes a dynamic array, ideal for variable-length data.
        self.font = pygame.font.Font(None, 36)  # Loads the font for score text rendering.
        self.title_font = 'space_asteroids/assets/sprites/font.ttf' # Custom font for titles.
        self.screen = pygame.display.set_mode((800, 600)) # Game window dimensions.
        self.background = pygame.image.load('space_asteroids/assets/sprites/Leaderboard.png') # Background image for leaderboard.
        self.new_score = ("", 0)
    
    # This function adds a new score to the list and sorts it. 
    # Efficient for managing a leaderboard.
    def add_score(self, name, score):
        # Appending is O(1)
        self.scores.append((name, score)) # Tuple format for scores.
        self.sort_by_score()   # Will sort scores after adding a new entry.
    
    # Merge Sort Algorithm 
    def merge_sort(self, array):
        # Recursive sorting with O(n log n) complexity, good for performance.
        # (Include detailed steps of merge sort here).

        if len(array) > 1:
            mid = len(array) // 2  # Finding the mid of the array
            L = array[:mid]  # Dividing the array elements into 2 halves
            R = array[mid:]

            self.merge_sort(L)  # Sorting the first half
            self.merge_sort(R)  # Sorting the second half

            i = j = k = 0

            # Copies the data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if L[i][1] < R[j][1]:
                    array[k] = L[i]
                    i += 1
                else:
                    array[k] = R[j]
                    j += 1
                k += 1

            # Checks if any element was left
            while i < len(L):
                array[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                array[k] = R[j]
                j += 1
                k += 1
    
    # Sorts scores using merge_sort and prepares the list for display.
    def sort_by_score(self):

        # Sorts scores in ascending and then reverses for descending order.

        self.merge_sort(self.scores)  # In-place sorting with merge_sort.
        self.scores.reverse()         # Reversing the list is O(n).
        self.scores = self.scores[:10]# Truncating to top 10 is O(1).
    
    # Sorts the scores alphabetically by player name.
    def sort_alphabetically(self):
        # Python's built-in sort is O(n log n), efficient for this use case.
        self.scores.sort(key=lambda x: x[0])  # Lambda provides a sorting key.
    
    # Displays the leaderboard on the screen.
    def display(self, x, y):

        # Background
        self.screen.blit(self.background, (0, 0))

        # Loads a custom TTF font for the title
        custom_title_font = pygame.font.Font(self.title_font, 48)

        # Display the title (centered at the top)
        title_surface = custom_title_font.render("Leader Board", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 50))  # Adjust y to place the title accordingly
        self.screen.blit(title_surface, title_rect)

        # Calculate the starting y position of the list so it's centered vertically
        list_start_y = (self.screen.get_height() - len(self.scores) * 40) // 2  # Adjust 40 to match the line height

        # Display the top 10 scores (centered)
        for index, (name, score) in enumerate(self.scores):
            score_text = self.font.render(f"{index + 1}. {name} - {score}", True, (255, 255, 255))
            text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, list_start_y + index * 40))  # 40 is line height

            # Draw a rectangle around the name
            pygame.draw.rect(self.screen, (255, 255, 255), text_rect.inflate(20, 10), 2)

            # Blit the score text (centered on the screen)
            self.screen.blit(score_text, text_rect)

    # Draws an interactive button on the screen.
    def draw_button(self, text, x, y, width, height):
        """Draw a button and return its rect for click detection."""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (50, 50, 50), button_rect)  # Blue button
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return button_rect

    # Handles the click event for buttons.
    def handle_button_click(self, button_rect, mouse_pos):
        """Check if a button is clicked and return True or False."""
        if button_rect.collidepoint(mouse_pos):
            return True
        return False
    
    # Reads scores from a file, demonstrating file I/O operations.
    def read_scores_from_file(self, filename):
        scores = []
        with open(filename, 'r') as file:
            for line in file:
                name, score = line.strip().split(',')
                scores.append((name, int(score)))
        return scores
    
    # Writes scores to a file, useful for persistent storage of score data.
    def write_scores_to_file(self, filename, scores):
        with open(filename, 'w') as file:
            for name, score in scores:
                file.write(f"{name},{score}\n")
    
     # Main method for leaderboard logic, integrates all components.
    def run_leaderb(self, new_score):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Leaderboard")
        
        # Creates a Leaderboard instance
        leaderboard = Leaderboard()

        # Example scores
        scores = leaderboard.read_scores_from_file("Score_storing.txt")
        print(scores)
        scores.append(new_score)
        scores.sort(key=lambda x: x[1], reverse=True)  # Assuming the score is the second element of the tuple

        # We only keep only the top 10 scores
        scores = scores[:10]
        for name, score in scores:
            leaderboard.add_score(name, score)

        # Defines the button dimensions and positions
        button_width, button_height = 150, 50
        alpha_button_rect = pygame.Rect(100, 550, button_width, button_height)
        score_button_rect = pygame.Rect(550, 550, button_width, button_height)

        # Game Loop
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if either button is clicked
                    if leaderboard.handle_button_click(alpha_button_rect, event.pos):
                        leaderboard.sort_alphabetically()
                    elif leaderboard.handle_button_click(score_button_rect, event.pos):
                        leaderboard.sort_by_score()

            # Clears the screen
            screen.fill((0, 0, 0))

            # Displays the leaderboard
            leaderboard.display(100, 50)

            # Draw Buttons
            button_width, button_height = 150, 50
            alpha_button_rect = leaderboard.draw_button("Alphabet", 100, 550, button_width, button_height)
            score_button_rect = leaderboard.draw_button("Score", 550, 550, button_width, button_height)

            # Update Display
            pygame.display.flip()
            updated_scores = scores[:10]
            self.write_scores_to_file("Score_storing.txt", updated_scores)
          
