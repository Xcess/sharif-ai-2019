
import Model
from random import randint


class AI:
    pick_heros = [Model.HeroName.BLASTER,
                Model.HeroName.BLASTER,
                Model.HeroName.BLASTER,
                Model.HeroName.BLASTER]
    final_posisions = [[],[],[]]
    nearest_obj = []
    hero_list = []
    reached_final_pos = [0,0,0,0]
    def get_dodge_cell(self, world, hero):
        target_cell = hero.current_cell
        for cell in world.get_cells_in_aoe(hero.current_cell,3):
            if len(world.get_path_move_directions(start_cell = cell, end_cell = self.final_posisions[0][self.hero_list.index(hero.id)])) < len(world.get_path_move_directions(start_cell = target_cell, end_cell = self.final_posisions[0][self.hero_list.index(hero.id)])) and not cell.is_wall:
                target_cell = cell
        return target_cell

    def get_nearest_enemy_cell(self,world,hero):
        nearest_enemy_cell = world.map.get_cell(-1,-1)
        for enemy in world.opp_heroes:
            if world.manhattan_distance(hero.current_cell, enemy.current_cell) < world.manhattan_distance(hero.current_cell, nearest_enemy_cell):
                nearest_enemy_cell = enemy.current_cell
        return nearest_enemy_cell

    def get_nearest_ally_cell(self,world,hero):
        nearest_ally_cell = world.map.get_cell(-1,-1)
        for allyid in self.hero_list:
            ally = world.get_hero(allyid)
            if ally == hero:
                continue
            if world.manhattan_distance(hero.current_cell, ally.current_cell) < world.manhattan_distance(hero.current_cell, nearest_ally_cell):
                nearest_ally_cell = ally.current_cell
        return nearest_ally_cell

    def preprocess(self, world):
        print("preprocess")
        #print (world.map.my_respawn_zone)
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
        for num, cell in enumerate(world.map.my_respawn_zone):
            dist = 1000
            for target in world.map.objective_zone:
                if len(world.get_path_move_directions(start_cell = cell, end_cell = target)) < dist:
                    dist = len(world.get_path_move_directions(start_cell = cell, end_cell = target))
                    if len(self.nearest_obj)>num:
                        self.nearest_obj[num] = target
                    else:
                        self.nearest_obj.append(target)

        self.final_posisions[0].append(world.map.get_cell(row_min,column_min))
        self.final_posisions[0].append(world.map.get_cell(row_min,column_max))
        self.final_posisions[0].append(world.map.get_cell(row_max,column_min))
        self.final_posisions[0].append (world.map.get_cell(row_max,column_max))

        for j in range(2):
            for i in range(4):
                row_change = 0
                column_change = 0
                if self.final_posisions[j][i].row < 15:
                    row_change = 1
                else:
                    row_change = -1
                if self.final_posisions[j][i].column < 15:
                    column_change = 1
                else:
                    column_change = -1
                self.final_posisions[j+1].append(world.map.get_cell(self.final_posisions[j][i].row+row_change,self.final_posisions[j][i].column+column_change))


        valid_flag = 0
        while valid_flag == 0:
            valid_flag = 1
            j = 0
            for i in range(4):
                if self.final_posisions[j][i].is_wall:
                    valid_flag = 0
                    self.final_posisions[j][i] = self.final_posisions[j+1][i]




    def pick(self, world):
        world.pick_hero(self.pick_heros.pop(0))

    def move(self, world):

        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            if hero.current_hp <= 0:
                self.reached_final_pos[num] = 0
        #list heroes
        hero_move_flag = [0,0,0,0]
        if len (self.hero_list) < 4:
            for cell in world.map.my_respawn_zone:
                for hero in world.my_heroes:
                    if hero.current_cell == cell:
                       self.hero_list.append(hero.id) 

        #go to nearest_obj
        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            if not hero.current_cell.is_in_objective_zone:
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.nearest_obj[num])
                if path_to_mid:
                    world.move_hero(hero=hero, direction=path_to_mid[0])


        #check for proper position to attack
        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            nearest_enemy_cell = self.get_nearest_enemy_cell(world,hero)

            if self.reached_final_pos[num] == 1 and 5 < world.manhattan_distance(hero.current_cell, nearest_enemy_cell) and nearest_enemy_cell.is_in_objective_zone and world.manhattan_distance(hero.current_cell,self.get_nearest_ally_cell(world,hero)) > 3:
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = nearest_enemy_cell)
                if path_to_mid:
                    world.move_hero(hero=hero, direction=path_to_mid[0])
                hero_move_flag[num] = 1



        #go to final posision
        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            if hero_move_flag[num] == 1: 
                continue 
            if hero.current_cell != self.final_posisions[0][num]:
                other_cells = []
                for num2, heroid2 in enumerate(self.hero_list):
                    hero2 = world.get_hero(heroid2)
                    if num != num2:
                        other_cells.append(self.final_posisions[0][num2])
                        if self.reached_final_pos[num2]:
                            other_cells.append(hero2.current_cell)
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.final_posisions[0][num], not_pass=other_cells)
                nearest_enemy_cell = self.get_nearest_enemy_cell(world,hero)
                if (path_to_mid and self.reached_final_pos[num] == 0) or (path_to_mid and (world.manhattan_distance(world._get_next_cell(hero.current_cell,path_to_mid[0]), nearest_enemy_cell) <= world.manhattan_distance(hero.current_cell, nearest_enemy_cell) or not hero.current_cell.is_in_objective_zone )):
                    world.move_hero(hero=hero, direction=path_to_mid[0])
            else:
                self.reached_final_pos[num] = 1
    def action(self, world):
        for heroid in self.hero_list:
            hero = world.get_hero(heroid)
            for enemy in world.opp_heroes:
                if world.manhattan_distance(hero.current_cell, enemy.current_cell) < 8:
                    target_cell = self.get_dodge_cell(world,hero)
                    # print("dodge from ({},{}) to ({},{})".format(hero.current_cell.row, hero.current_cell.column,target_cell.row,target_cell.column))
                    world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_BOMB), cell=enemy.current_cell)
                    action_flag = 1
                if world.manhattan_distance(hero.current_cell, enemy.current_cell) < 6:
                    world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_ATTACK), cell=enemy.current_cell)
                    action_flag = 1
        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            # if hero.current_cell != self.final_posisions[0][num]:
            if not hero.current_cell.is_in_objective_zone:
                target_cell = self.get_dodge_cell(world,hero)
                world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_DODGE), cell=target_cell)