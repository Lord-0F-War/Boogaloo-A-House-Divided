import pygame


class Pygame:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH:int   = SCREEN_WIDTH
        self.SCREEN_HEIGHT:int  = SCREEN_HEIGHT
    
    def start_pygame(self):
        pygame.init()
        pygame.font.init()
    
    def config_pygame(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.USEREVENT, pygame.MOUSEWHEEL, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        
        self.CLOCK = pygame.time.Clock()

        pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))  

    def get_time_variables(self):
        return self.CLOCK
    
    def get_event_variables(self):
        return pygame.QUIT