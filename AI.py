
import Model
from random import randint


class AI:
    pick_heros = [Model.HeroName.BLASTER,
                Model.HeroName.BLASTER,
                Model.HeroName.BLASTER,
                Model.HeroName.BLASTER]
    final_posisions = []
    attack_targets = []
    def preprocess(self, world):
        print("preprocess")
        row_min = 100
        column_min = 100
        row_max = 0
        column_max = 0
        for cell in world.map.objective_zone:
            if cell.row < row_min:
                row_min = cell.row
            if cell.row > row_max:
                row_max = cell.row 
            if cell.column > column_max:
                column_max = cell.column
            if cell.column < column_min:
                column_min = cell.column 

        self.final_posisions.append(world.map.get_cell(row_min,column_min))
        self.final_posisions.append(world.map.get_cell(row_min,column_max))
        self.final_posisions.append(world.map.get_cell(row_max,column_min))
        self.final_posisions.append (world.map.get_cell(row_max,column_max))

        self.attack_targets.append(world.map.get_cell(row_min+2,column_min+2))
        self.attack_targets.append(world.map.get_cell(row_min+2,column_max-2))
        self.attack_targets.append(world.map.get_cell(row_max-2,column_min+2))
        self.attack_targets.append (world.map.get_cell(row_max-2,column_max-2))
    def pick(self, world):
        print("pick")
        # hero_names = [hero_name for hero_name in Model.HeroName]  
        world.pick_hero(self.pick_heros.pop(0))

    def move(self, world):
        #print("move")
        dirs = [direction for direction in Model.Direction]
        no = 0
        for hero in world.my_heroes:    
            
            if not hero.current_cell.is_in_objective_zone:
                other_cells = []
                for i in range(4):
                    if i != no:
                        other_cells.append(self.final_posisions[i])
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.final_posisions[no], not_pass=other_cells)
                if path_to_mid:
                    world.move_hero(hero=hero, direction=path_to_mid[0])
            no = no + 1

    def action(self, world):
        pass
        # print("action")
        no = 0
        for hero in world.my_heroes:
            world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_BOMB), cell=self.attack_targets[no])
            world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_ATTACK), cell=self.attack_targets[no])
            no = no + 1