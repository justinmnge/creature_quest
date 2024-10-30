from settings import *
from sprites import Sprite, AnimatedSprite
from entities import Player
from groups import AllSprites
from support import *

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
        self.tmx_maps = {
            'world': load_pygame(join('data', 'maps', 'world.tmx')),
            'hospital': load_pygame(join('data', 'maps', 'hospital.tmx'))
            }
        
        self.overworld_frames = {
            'water': import_folder('graphics', 'tilesets', 'water')
        }

        
    def setup(self, tmx_map, player_start_pos):
        # terrain
        for layer in ['Terrain', 'Terrain Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
                    
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        # water
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites)
        
        # entities    
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player((obj.x, obj.y), self.all_sprites)
        
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
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
            
        pygame.quit()
        
if __name__ == '__main__':
    game = Game()
    game.run()