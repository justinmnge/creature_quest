from settings import *
from game_data import *
from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, Collidableprite, TransitionSprite
from entities import Player, Character
from groups import AllSprites
from support import *
from dialog import *
from monster import Monster
from monster_index import MonsterIndex
from battle import Battle

class Game:
    # general
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Creature Quest')
        self.clock = pygame.time.Clock()
        self.running = True
        
        # player monsters
        self.player_monsters = {
            0: Monster('Charmadillo', 30),
            1: Monster('Friolera', 29),
            2: Monster('Sparchu', 31),
            3: Monster('Finsta', 28),
            4: Monster('Ivieron', 31),
            5: Monster('Pouch', 25),
            6: Monster('Atrox', 4),
            7: Monster('Gulfin', 19)
        }
        
        self.dummy_monsters = {
            0: Monster('Finsta', 18),
            1: Monster('Ivieron', 22),
            2: Monster('Pouch', 21),
            3: Monster('Atrox', 17),
            4: Monster('Gulfin', 19)
        }
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()
        
        # transition / tint
        self.transition_target = None
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600
        
        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')
        
        # overlays
        self.dialog_tree = None
        self.monster_index = MonsterIndex(self.player_monsters, self.fonts, self.monster_frames)
        self.index_open = False
        self.battle = None
                
    def import_assets(self):
        self.tmx_maps = tmx_importer('data', 'maps')
        
        self.overworld_frames = {
            'water': import_folder('graphics', 'tilesets', 'water'),
            'coast': coast_importer(24, 12, 'graphics', 'tilesets', 'coast'),
            'characters': all_character_import('graphics', 'characters')
        }
        
        self.monster_frames = {
            'icons': import_folder_dict('graphics', 'icons'),
            'monsters': monster_importer(4, 2, 'graphics', 'monsters'),
            'ui': import_folder_dict('graphics', 'ui'),
            'attacks': attack_importer('graphics', 'attacks')
        }
        self.monster_frames['outlines'] = outline_creator(self.monster_frames['monsters'], 4)
        
        self.fonts = {
            'dialog': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 30),
            'regular': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 18),
            'small': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 14),
            'bold': pygame.font.Font(join('graphics', 'fonts', 'dogicapixelbold.otf'), 20)
        }
        self.bg_frames = import_folder_dict('graphics', 'backgrounds')
                
    def setup(self, tmx_map, player_start_pos):
        # clear the map
        for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
            group.empty()
        
        # terrain
        for layer in ['Terrain', 'Terrain Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

        # water
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])
                    
        # coast
        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites, WORLD_LAYERS['bg'])
                    
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'top':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
            else:
                Collidableprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        # transition objects
        for obj in tmx_map.get_layer_by_name('Transition'):
            TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)
                
        # collision objects
        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
            
        # grass patches
        for obj in tmx_map.get_layer_by_name('Monsters'):
            MonsterPatchSprite((obj.x, obj.y), obj.image, self.all_sprites, obj.properties['biome'])
        
        # entities    
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                if obj.properties['pos'] == player_start_pos:
                    self.player = Player(
                        pos = (obj.x, obj.y), 
                        frames = self.overworld_frames['characters']['player'], 
                        groups = self.all_sprites,
                        facing_direction = obj.properties['direction'],
                        collision_sprites = self.collision_sprites)
            else:
                Character(
                        pos = (obj.x, obj.y), 
                        frames = self.overworld_frames['characters'][obj.properties['graphic']], 
                        groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
                        facing_direction = obj.properties['direction'],
                        character_data = TRAINER_DATA[obj.properties['character_id']],
                        player = self.player,
                        create_dialog = self.create_dialog,
                        collision_sprites = self.collision_sprites,
                        radius = obj.properties['radius'],
                        nurse = obj.properties['character_id'] == 'Nurse')
                
    # dialog system
    def input(self):
        if not self.dialog_tree and not self.battle:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_SPACE]:
                for character in self.character_sprites:
                    if check_connections(100, self.player, character):
                        self.player.block()
                        character.change_facing_direction(self.player.rect.center)
                        self.create_dialog(character)
                        character.can_rotate = False
            
            if keys[pygame.K_RETURN]:
                self.index_open = not self.index_open
                self.player.blocked = not self.player.blocked
    
    def create_dialog(self, character):
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)
    
    def end_dialog(self, character):
        self.dialog_tree = None
        if character.nurse:
            for monster in self.player_monsters.values():
                monster.health = monster.get_stat('max_health')
                monster.energy = monster.get_stat('max_energy')                
        
            self.player.unblock()
        elif not character.character_data['defeated']:
            self.battle = Battle(
                player_monsters = self.player_monsters, 
                opponent_monsters = character.monsters, 
                monster_frames = self.monster_frames, 
                bg_surf = self.bg_frames[character.character_data['biome']],
                fonts = self.fonts)
    
    # transition system
    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.player.block()
            self.transition_target = sprites[0].target
            self.tint_mode = 'tint'
            
    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        
        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
                self.tint_mode = 'untint'
                self.transition_target = None
                                
        self.tint_progress = max(0, min(self.tint_progress, 255))    
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0, 0))
        
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            self.display_surface.fill('black')
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # update
            self.input()
            self.transition_check()
            self.all_sprites.update(dt)
            
            # draw
            self.all_sprites.draw(self.player)
            
            # overlays
            if self.dialog_tree:    self.dialog_tree.update()
            if self.index_open:     self.monster_index.update(dt)
            if self.battle:         self.battle.update(dt)
            
            self.tint_screen(dt)
            pygame.display.update()
            
        pygame.quit()
        
if __name__ == '__main__':
    game = Game()
    game.run()