import sys

import pygame
from pygame.constants import QUIT

from ui.gui import GUI
from ui.ui_component import UIComponent


class PyGameUI(GUI):

    FPS = 60
    BACKGROUND = (0, 0, 0)

    def __init__(self) -> None:
        self.window = None

    def new_gui(self) -> None:
        pygame.init()
        pygame.font.init()
        # Colours

        # Game Setup
        self.fpsClock = pygame.time.Clock()
        WINDOW_WIDTH = 1920/2
        WINDOW_HEIGHT = 1080
        
        self.window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('WCRG Video Feedback System')
        self.window.fill(self.BACKGROUND)


    def add_component(self, component: UIComponent) -> None:
        pass
        # component.draw(self.window)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Processing
            # This section will be built out later
        
            # Render elements of the game
            #pygame.draw.rect(self.window, (255,0,0), [100,100,400,100], 0)
        pygame.display.update()
        self.fpsClock.tick(self.FPS)

    def clear(self):
        self.window.fill(self.BACKGROUND)

