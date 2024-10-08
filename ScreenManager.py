
from PygameManager import pygame
from pygame.locals import *

class Screen:
    def __init__(self, Main_Menu, ESC_Menu, Options_Menu, SCREEN_WIDTH, SCREEN_HEIGHT):

        self.SCREEN_WIDTH:int               = SCREEN_WIDTH
        self.SCREEN_HEIGHT:int              = SCREEN_HEIGHT	
        self.REFERENCE_SCREEN_SIZE_X:int    = 1920
        self.REFERENCE_SCREEN_SIZE_y:int    = 1080
        self.FACTOR_X:int                   = self.SCREEN_WIDTH / self.REFERENCE_SCREEN_SIZE_X
        self.FACTOR_Y:int                   = self.SCREEN_HEIGHT / self.REFERENCE_SCREEN_SIZE_y		
        
        self.SCREEN_RECT                    = pygame.Rect([0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT])	

        self.DISPLAY                        = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), FULLSCREEN)
        self.SCREEN                         = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.SURFACE_ALFA                   = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)        	

        self.ESC_Menu                       = ESC_Menu
        self.Options_Menu                   = Options_Menu
        self.Main_Menu                      = Main_Menu

        self.BRIGHTNESS_SURFACE             = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)


    def render_main_menu(self, brightness_value, is_options_menu_open, is_in_esc_menu):
        self.SCREEN.fill((0, 0, 0))
        self.SURFACE_ALFA.fill((0, 0, 0, 0))
        self.BRIGHTNESS_SURFACE.fill((0, 0, 0, 0))


        self.Main_Menu.draw(self.SCREEN)


        if is_in_esc_menu == True:
            self.ESC_Menu.draw(self.SURFACE_ALFA)
        elif is_options_menu_open == True:
            self.Options_Menu.draw(self.SURFACE_ALFA)            		
        self.SCREEN.blit(self.SURFACE_ALFA, (0, 0))	


        pygame.draw.rect(self.BRIGHTNESS_SURFACE, (255, 255, 255, brightness_value), ((0, 0), (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)))		
        self.SCREEN.blit(self.BRIGHTNESS_SURFACE, (0, 0))


        self.DISPLAY.blit(self.SCREEN, (0, 0))
        pygame.display.update(self.SCREEN_RECT)