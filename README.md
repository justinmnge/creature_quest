## Game

A Pokemon-inspired RPG. Explore an overworld full of characters, trainers and wild monsters. Complex battle system, you are able to: choose a range of attacks with monsters and catch wild ones. Contains a lot of animations and visual details. Monsters can level up and evolve, while also learning new attacks on some levels. Visualizing all that information, there will be a monster index (similar to a Pokedex) that shows: stats, attacks and abilities of all of them.

## Controls

- Player overworld movement WASD or Arrow keys
- Player overworld interaction SPACE
- Player overworld Monster Index ENTER/RETURN
    - Monster Index selection Arrow Keys
    - Monster Index interaction SPACE * 2 (To rotate order of monsters, you press SPACE on monster, then move to another monster position and press SPACE again to switch both monster positions)
    - Monster Index exit ENTER/RETURN
- Battle system selection Arrow Keys
- Battle system interaction SPACE

### Lessons Observed

- I learned how to organize complex projects, manage databases and how to build UIs from scratch.
- I learned to how implement the water system via tmx
- I learned how to implement an overworld system where the character can enter a building from a large map and once they go to the door, it transitions the player to inside the building.
- I learned how to implement a dialog system
- I learned how to make a monster index with relevant stats and abilities
- I learned to create a battle system with a player side and opponent side of 3 monsters each
    - This battle system allows the player to either 'attack', 'defend', 'switch' monsters or 'catch' an opponent's monster during the their respective turn
    - Turn rotation is also based on the 'initiative' of each monster, that is tied to their current level
    - Monsters (active on your side) will also recieve experience points to level up once they have defeated an opponent monster
- I learned to connect the overworld with the battle system so that their is a smooth transition between the two to have a seemless experience
    - By connecting the overworld and battle system, I have learned to pull the opponent data to show what they have for monsters in the battle system
        - Created variety in battles with random opponents
- I have learned how to create an 'evolving' system where monsters evolve to a stronger version and new version of themself once they reach a specific level
- I have learned how to implement a 'nurse' to heal all of the player monsters after a battle in the overworld
- I have learned to add of the necessary sounds in the game
- I learned to create a monster encounter timer when the player walks through the tall grass in-game, it will trigger a battle with a random monster


