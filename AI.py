
import Model
from random import randint

# get_path_move_directions(self, start_cell=None, start_row=None, start_column=None, end_cell=None, end_row=None,
                                 # end_column=None, not_pass=None)
class AI:
    pick_heros = [Model.HeroName.GUARDIAN,
                Model.HeroName.GUARDIAN,
                Model.HeroName.HEALER,
                Model.HeroName.HEALER]
    def preprocess(self, world):
        print("preprocess")

    def pick(self, world):
        print("pick")
        # hero_names = [hero_name for hero_name in Model.HeroName]  
        world.pick_hero(self.pick_heros.pop(0))

    def move(self, world):
        print("move")
        dirs = [direction for direction in Model.Direction]
        no = 0
        for hero in world.my_heroes:
            no = no + 1
            if not hero.current_cell.is_in_objective_zone:
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = world.map.objective_zone[randint(0, len(world.map.objective_zone) - 1)])
                if path_to_mid:
                    world.move_hero(hero=hero, direction=path_to_mid[0])

    def action(self, world):
        healers = [hero for hero in world.my_heroes if hero.name == Model.HeroName.HEALER]
        guardians = [hero for hero in world.my_heroes if hero.name == Model.HeroName.GUARDIAN]

        world.cast_ability(hero=healers[0], ability=healers[0].get_ability(Model.AbilityName.HEALER_HEAL), cell=guardians[0].current_cell)
        world.cast_ability(hero=healers[1], ability=healers[1].get_ability(Model.AbilityName.HEALER_HEAL), cell=guardians[1].current_cell)