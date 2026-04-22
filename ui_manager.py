import pygame
import os
import sys
import app


"""COLOUR CONSTANTS"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

"""SCREEN SETUP"""
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Shooter Game Menu")  # Window title

"""FONT SETUP"""
font = pygame.font.Font(None, 74)       # Large font for title
small_font = pygame.font.Font(None, 36) # Smaller font for buttons

"""MUSIC SETUP"""
music_path = os.path.join("assets", "sounds", "background_music.mp3")
pygame.mixer.music.load(music_path)      # Load music file
pygame.mixer.music.set_volume(0.5)       # Set volume to 50%
pygame.mixer.music.play(-1)              # Play in infinite loop


def draw_text(text, font, color, x, y):
    ##Helper function to draw centered text on screen
    text_obj = font.render(text, True, color)          # Create text surface
    text_rect = text_obj.get_rect(center=(x, y))       # Center the text
    screen.blit(text_obj, text_rect)                   # Draw to screen

"""MENU CLASS"""
class Menu:
    ##Main menu class handling menu display and interactions
    def __init__(self):
        self.game_state = "menu"  # Tracks game state (menu/playing/etc)
        
        # Load and scale background image to full screen
        self.background_image = pygame.image.load(os.path.join("assets", "download.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (app.WIDTH, app.HEIGHT))
    
    def run(self):
        ##Main menu loop
        while self.game_state == "menu":
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Window close button
                    pygame.quit()
                    sys.exit()
            
            # Draw background image
            screen.blit(self.background_image, (0, 0))
            
            # Draw game title
            draw_text("Shooter Game", font, BLACK, app.WIDTH // 2, 250)

            # Create Start button rectangle and draw it
            start_button = pygame.Rect(app.WIDTH // 2 - 100, 350, 200, 60)
            pygame.draw.rect(screen, GRAY, start_button)
            draw_text("Start", small_font, BLACK, start_button.centerx, start_button.centery)

            # Create Quit button rectangle and draw it
            quit_button = pygame.Rect(app.WIDTH // 2 - 100, 450, 200, 60)
            pygame.draw.rect(screen, GRAY, quit_button)
            draw_text("Quit", small_font, BLACK, quit_button.centerx, quit_button.centery)

            # Get mouse position and click status
            mouse_x, mouse_y = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()  # Returns tuple of mouse button states
            
            # Check for Start button click
            if start_button.collidepoint(mouse_x, mouse_y) and click[0]:
                self.game_state = "playing"  # Change game state
                return "playing"             # Return new state
            
            # Check for Quit button click
            if quit_button.collidepoint(mouse_x, mouse_y) and click[0]:
                pygame.quit()  # Clean up pygame
                sys.exit()     # Exit program
            
            # Update display
            pygame.display.update()


"""OVERLAY CLASS"""
class Overlay:

    def __init__(self, screen, font_small, font_large):
        self.screen = screen
        self.font_small = font_small
        self.font_large = font_large

    def draw_game_over_screen(self):
        overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_surf = self.font_large.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)

        prompt_surf = self.font_small.render("Press R to play again or ESC to Quit", True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 + 20))
        self.screen.blit(prompt_surf, prompt_rect)

    def draw_pause_screen(self):
        overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        pause_surf = self.font_large.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 - 50))
        self.screen.blit(pause_surf, pause_rect)

        prompt_surf = self.font_small.render("Press ESC to resume", True, (200, 200, 200))
        prompt_rect = prompt_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 + 20))
        self.screen.blit(prompt_surf, prompt_rect)
