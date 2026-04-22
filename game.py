import pygame
import random
import os
from player import Player
from overlay import Overlay
import app


pygame.init()
pygame.mixer.init()

shooting_sound = os.path.join("assets", "sounds", "background_music.mp3")
pygame.mixer.music.load(shooting_sound)
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

"""GAME CLASS"""
class Game:
    def __init__(self):
        # initialise pygame & window
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # load clock & asset
        self.clock = pygame.time.Clock()
        self.assets = app.load_assets()

        # laod and set fonts
        font_path = os.path.join("assets", "PressStart2P.ttf")
        self.font_small = pygame.font.Font(font_path, 18)
        self.font_large = pygame.font.Font(font_path, 32)

        # initalise player
        self.player = Player(100, 100, self.assets)

        self.background = self.create_random_background(
            app.WIDTH, app.HEIGHT, self.assets["floor_tiles"]  # Use floor tiles to create a background
        )

        self.running = True  # set the game state to running
        self.game_over = False  # set the game state of not over
        self.paused = False

        self.overlay = Overlay(self.screen, self.font_small, self.font_large)

        pygame.display.set_caption("Shooter Game")  # Setting the title of window to shooter game

    def reset_game(self):
        self.player = Player(app.WIDTH // 2, app.HEIGHT // 2, self.assets)
        self.game_over = False

    def create_random_background(self, width, height, floor_tiles):
        bg = pygame.Surface((width, height))  # Setting bg object as a surface
        tile_w = floor_tiles[0].get_width()  # Set start position of tile (width)
        tile_h = floor_tiles[0].get_height()  # Set start position of tile (length)

        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                bg.blit(tile, (x, y))  # Use blit to place object on screen

        return bg

    def run(self):
        while self.running:
            self.clock.tick(60)  # Set FPS to 60

            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused


    def update(self):
        if self.paused:
            return
        self.player.handle_input()
        self.player.update()

        #if self.player.health <= 0:
            #self.game_over = True
            #return

    def draw(self):
        self.screen.blit(self.background, (0, 0))  # update the screen to position 0,0

        if not self.game_over:
            self.player.draw(self.screen)

        if self.game_over:
            self.overlay.draw_game_over_screen()

        if self.paused:
            self.overlay.draw_pause_screen()

        pygame.display.flip()