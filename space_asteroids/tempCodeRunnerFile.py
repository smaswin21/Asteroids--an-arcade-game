import pygame

class Start_Screen:
    WHITE = (255, 255, 255)
    TRANSPARENT = (0, 0, 0, 0)
    screen_width, screen_height = 800, 600
    pygame.init()  # Initialize all imported pygame modules
    screen = pygame.display.set_mode((800, 600))  # Use your game's resolution
    pygame.display.set_caption('Space Game')

    # Load and scale the background image
    background_image = pygame.image.load("space_asteroids/assets/sprites/background.png")
    background_image = pygame.transform.scale(background_image, (800, 600))

    # Title properties using the custom font
    font_path = "space_asteroids/assets/sprites/font.ttf"  # Path to your futuristic font file
    font_size = 100  # Adjust the size to fit your design
    font = pygame.font.Font(font_path, font_size)
    text_surface = font.render('Space Game', True, WHITE).convert_alpha()
    text_rect = text_surface.get_rect(center=(screen_width // 2, 150))

    # Create a mask from the text surface
    warning_font = pygame.font.Font(None, 30)
    mask = pygame.mask.from_surface(text_surface)
    mask_surface = mask.to_surface(setcolor=WHITE, unsetcolor=TRANSPARENT).convert_alpha()

    # Copy the background image to the text shape
    title_surface = pygame.Surface(text_rect.size, pygame.SRCALPHA)
    title_surface.blit(background_image, (0, 0), area=text_rect)
    title_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Draw a squircle shape behind the title text
    squircle_rect = text_rect.inflate(20, 20)  # Inflate the rect to make the squircle larger than the text

    # Button properties
    button_color = (0, 204, 153)  # A teal color; adjust as needed
    button_rect = pygame.Rect(0, 0, 200, 50)  # Adjust width and height as needed
    button_rect.center = (screen_width // 2, 450)  # Position of the button

    # Text properties for the button
    button_font = pygame.font.Font(None, 36)  # Use a font and size that fits the button
    button_text = button_font.render('START', True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    # Text entry box properties
    text_box_color = (0, 0, 0)  # Black color for the text box
    text_color = (255, 255, 255)  # White color for the text
    text_box_rect = pygame.Rect(0, 0, 200, 50)  # Adjust width and height as needed
    text_box_rect.center = (screen_width // 2, 350)  # Position of the text box
    active = False
    user_name = ''  # Variable to store user input
    display_warning = False  # Variable to control the display of the warning message
    text_box_font = pygame.font.Font(None, 36)  # Use a font and size that fits the text box
    running = True

    while running:
        # Draw the background
        screen.blit(background_image, (0, 0))

        # Draw the squircle and title
        pygame.draw.rect(screen, WHITE, squircle_rect, border_radius=25)  # Squircle behind the title
        screen.blit(title_surface, text_rect.topleft)  # Title text with background fill

        # Draw the button and text
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, button_text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()  # Exit the game completely

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the text box or start button is clicked
                if text_box_rect.collidepoint(event.pos):
                    active = True
                    display_warning = False  # Reset the warning when the text box is clicked
                elif button_rect.collidepoint(event.pos):
                    if len(user_name) >= 3:
                        running = False  # Proceed to the game
                    else:
                        display_warning = True  # Display warning if the name is too short
                else:
                    active = False  # Deactivate text box if clicked outside

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    print(user_name)
                    user_name = ''  # Clear text box after pressing Enter
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]  # Delete the last character
                else:
                    user_name += event.unicode  # Add the typed character to the text

        # Render the current text in the text box
        text_surface = text_box_font.render(user_name, True, text_color)
        # Resize the box if the text is too long.
        width = max(200, text_surface.get_width() + 10)
        text_box_rect.w = width
        # Draw the text box
        screen.fill((30, 30, 30), text_box_rect)
        screen.blit(text_surface, (text_box_rect.x + 5, text_box_rect.y + 5))
        pygame.draw.rect(screen, text_box_color, text_box_rect, 2)

        # Draw the warning message if needed
        if display_warning:
            if len(user_name) == 0:
                warning_message = "Please enter a name to begin!"
            else:
                warning_message = "Your name must include at least 3 characters!"
            warning_surface = warning_font.render(warning_message, True, (255, 0, 0))
            warning_rect = pygame.Rect(0, 0, 600, 30)  # Adjust width and height to fit the smaller text
            warning_rect.center = (screen_width // 2, 500)  # Position of the warning box
            screen.fill((255, 255, 255), warning_rect)
            screen.blit(warning_surface, (warning_rect.x + 5, warning_rect.y + 5))

        # Update the display
        pygame.display.flip()