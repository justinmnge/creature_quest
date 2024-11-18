from settings import *


class MonsterIndex:
    def __init__(self, monsters, fonts):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.monsters = monsters
        
        # tint surf
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)
        
        # dimension
        self.main_rect =pygame.FRect(0, 0, WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * 0.8).move_to(center = (WINDOW_WIDTH/ 2, WINDOW_HEIGHT / 2))
        
        # list
        self.visibile_items = 6
        self.list_width = self.main_rect.width * 0.3
        self.item_height = self.main_rect.height / self.visibile_items
        
    def update(self, dt):
        # input
        self.display_surface.blit(self.tint_surf, (0,0))
        pygame.draw.rect(self.display_surface, 'black', self.main_rect)
        
        # tint the main game
        
        # display the list
        
        # display the main section
        