from game_data import MONSTER_DATA
from random import randint

class Monster:
    def __init__(self, name, level):
        self.name, self.level = name, level
        
        # stats
        self.element = MONSTER_DATA[name]['stats']['element']
        self.base_state = MONSTER_DATA[name]['stats']
        
        # experience
        self.xp = randint(0, 1000)
        self.level_up = self.level * 150