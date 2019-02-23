
import Model
from random import randint


class AI:
    pick_heros = [Model.HeroName.BLASTER,
                Model.HeroName.BLASTER,
                Model.HeroName.BLASTER,
                Model.HeroName.BLASTER]
    final_posisions = []
    nearest_obj = []
    hero_list = []
    def preprocess(self, world):
        print("preprocess")
        print (world.map.my_respawn_zone)
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
        # print("row_min")
        # print(row_min)
        # print("column_min")
        # print(column_min)
        # print("row_max")
        # print(row_max)
        # print("column_max")
        # print(column_max)
        no = 0
        for cell in world.map.my_respawn_zone:
            dist = 1000
            for target in world.map.objective_zone:
                if len(world.get_path_move_directions(start_cell = cell, end_cell = target)) < dist:
                    dist = len(world.get_path_move_directions(start_cell = cell, end_cell = target))
                    if len(self.nearest_obj)>no:
                        self.nearest_obj[no] = target
                    else:
                        self.nearest_obj.append(target)
            no = no + 1

        self.final_posisions.append(world.map.get_cell(row_min,column_min))
        self.final_posisions.append(world.map.get_cell(row_min,column_max))
        self.final_posisions.append(world.map.get_cell(row_max,column_min))
        self.final_posisions.append (world.map.get_cell(row_max,column_max))
        valid_flag = 0

        while valid_flag == 0:
            valid_flag = 1
            for i in range(4):
                if self.final_posisions[i].is_wall:
                    valid_flag = 0
                    row_change = 0
                    column_change = 0
                    if self.final_posisions[i].row < 15:
                        row_change = 1
                    else:
                        row_change = -1
                    if self.final_posisions[i].column < 15:
                        column_change = 1
                    else:
                        column_change = -1
                    self.final_posisions[i] = world.map.get_cell(self.final_posisions[i].row+row_change,self.final_posisions[i].column+column_change)




    def pick(self, world):
        print("pick")
        # hero_names = [hero_name for hero_name in Model.HeroName]  
        world.pick_hero(self.pick_heros.pop(0))

    def move(self, world):
        print (world.map.my_respawn_zone)
        #print("move")
        if len (self.hero_list) < 4:
            for cell in world.map.my_respawn_zone:
                for hero in world.my_heroes:
                    if hero.current_cell == cell:
                       self.hero_list.append(hero.id) 
        no = 0
        for heroid in self.hero_list:
            hero = world.get_hero(heroid)
            if not hero.current_cell.is_in_objective_zone:
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.nearest_obj[no])
            no = no + 1

        no = 0
        for heroid in self.hero_list:    
            hero = world.get_hero(heroid)
            if hero.current_cell != self.final_posisions[no]:
                other_cells = []
                for i in range(4):
                    if i != no:
                        other_cells.append(self.final_posisions[i])
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.final_posisions[no], not_pass=other_cells)
                if path_to_mid:
                    world.move_hero(hero=hero, direction=path_to_mid[0])
            no = no + 1

    def action(self, world):
        for heroid in self.hero_list:
            hero = world.get_hero(heroid)
            for enemy in world.opp_heroes:
                if world.manhattan_distance(hero.current_cell, enemy.current_cell) < 8:
                    world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_BOMB), cell=enemy.current_cell)
                if world.manhattan_distance(hero.current_cell, enemy.current_cell) < 6:
                    world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_ATTACK), cell=enemy.current_cell)
        # for hero in world.my_heroes:
        # no = 0
        # for hero in world.my_heroes:
        #     world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_BOMB), cell=self.attack_targets[no])
        #     world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_ATTACK), cell=self.attack_targets[no])
        #     no = no + 1