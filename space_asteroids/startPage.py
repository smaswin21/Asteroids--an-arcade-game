import pygame

class Start_Screen:
    def __init__(self):
        # Initialize pygame and set up the screen
        pygame.init()
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Space Game')

        # Load and scale the background image
        self.background_image = pygame.image.load("space_asteroids/assets/sprites/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (800, 600))

        # Setup title, button, and text box properties
        self.setup_properties()

    def setup_properties(self):
        # Initialize colors and font properties
        self.WHITE = (255, 255, 255)
        self.TRANSPARENT = (0, 0, 0, 0)
        self.font_path = "space_asteroids/assets/sprites/font.ttf"
        self.font_size = 100
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.warning_font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render('Space Game', True, self.WHITE).convert_alpha()
        self.text_rect = self.text_surface.get_rect(center=(self.screen_width // 2, 150))
        self.setup_title_surface()
        self.setup_button()
        self.setup_text_box()

    def setup_title_surface(self):
        # Create a mask from the text surface and prepare the title
        mask = pygame.mask.from_surface(self.text_surface)
        mask_surface = mask.to_surface(setcolor=self.WHITE, unsetcolor=self.TRANSPARENT).convert_alpha()
        self.title_surface = pygame.Surface(self.text_rect.size, pygame.SRCALPHA)
        self.title_surface.blit(self.background_image, (0, 0), area=self.text_rect)
        self.title_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.squircle_rect = self.text_rect.inflate(20, 20)

    def setup_button(self):
        # Button properties
        self.button_color = (0, 204, 153)
        self.button_rect = pygame.Rect(0, 0, 200, 50)
        self.button_rect.center = (self.screen_width // 2, 450)
        self.button_font = pygame.font.Font(None, 36)
        self.button_text = self.button_font.render('START', True, self.WHITE)
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)

    def setup_text_box(self):
        # Text box properties
        self.text_box_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.text_box_rect = pygame.Rect(0, 0, 200, 50)
        self.text_box_rect.center = (self.screen_width // 2, 350)
        self.active = False
        self.user_name = ''
        self.display_warning = False
        self.text_box_font = pygame.font.Font(None, 36)

    def run(self):
        running = True
        while running:
            # Draw the background and UI elements
            self.screen.blit(self.background_image, (0, 0))
            pygame.draw.rect(self.screen, self.WHITE, self.squircle_rect, border_radius=25)
            self.screen.blit(self.title_surface, self.text_rect.topleft)
            pygame.draw.rect(self.screen, self.button_color, self.button_rect)
            self.screen.blit(self.button_text, self.button_text_rect)
            self.draw_text_box()
            self.draw_warning_message()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.text_box_rect.collidepoint(event.pos):
                        self.active = True
                        self.display_warning = False
                    elif self.button_rect.collidepoint(event.pos):
                        if len(self.user_name) >= 3:
                            return self.user_name  # Return the username and exit the loop
                        else:
                            self.display_warning = True
                    else:
                        self.active = False
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        if len(self.user_name) >= 3:
                            return self.user_name  # Return the username and exit the loop
                        else:
                            self.display_warning = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    else:
                        self.user_name += event.unicode

            pygame.display.flip()

    def draw_text_box(self):
        text_surface = self.text_box_font.render(self.user_name, True, self.text_color)
        width = max(200, text_surface.get_width() + 10)
        self.text_box_rect.w = width
        self.screen.fill((30, 30, 30), self.text_box_rect)
        self.screen.blit(text_surface, (self.text_box_rect.x + 5, self.text_box_rect.y + 5))
        pygame.draw.rect(self.screen, self.text_box_color, self.text_box_rect, 2)

    def draw_warning_message(self):
        if self.display_warning:
            warning_message = "Your name must include at least 3 characters!" if len(self.user_name) > 0 else "Please enter a name to begin!"
            warning_surface = self.warning_font.render(warning_message, True, (255, 0, 0))
            warning_rect = pygame.Rect(0, 0, 600, 30)
            warning_rect.center = (self.screen_width // 2, 500)
            self.screen.fill((255, 255, 255), warning_rect)
            self.screen.blit(warning_surface, (warning_rect.x + 5, warning_rect.y + 5))

    def handle_mouse_click(self, event):
        if self.text_box_rect.collidepoint(event.pos):
            self.active = True
            self.display_warning = False
        elif self.button_rect.collidepoint(event.pos):
            if len(self.user_name) >= 3:
                return self.user_name  # Proceed to the game
            else:
                self.display_warning = True
        else:
            self.active = False

    def handle_keypress(self, event):
        if event.key == pygame.K_RETURN:
            if len(self.user_name) >= 3:
                return self.user_name  # Proceed to the game
            else:
                self.display_warning = True
        elif event.key == pygame.K_BACKSPACE:
            self.user_name = self.user_name[:-1]
        else:
            self.user_name += event.unicode

