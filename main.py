from settings import *
from pytmx.util_pygame import load_pygame
from sprites import Sprite
from entities import Player
from groups import AllSprites

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Creature Quest')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # groups
        self.all_sprites = AllSprites()
        
        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')
    
    def import_assets(self):
        self.tmx_maps = {'world': load_pygame(join('data', 'maps', 'world.tmx'))}
        
    def setup(self, tmx_map, player_start_pos):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
            
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                Player((obj.x, obj.y), self.all_sprites)
        
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # update
            self.all_sprites.update(dt)
            
            
            # draw
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
            
        pygame.quit()
        
if __name__ == '__main__':
    game = Game()
    game.run()