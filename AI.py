
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
    used_dodge_cells = []
    attacking = []
    reached_final_pos = [0,0,0,0]
    not_pass_objective_zone = []

    def get_direction_cell(self, world, current_cell, path, length):
        cell = current_cell
        if len(path) < length:
            return current_cell
        for i in range(length):
            cell = world._get_next_cell(cell,path[i])
        return cell           

    def get_dodge_cell(self, world, hero):
        target_cell = hero.current_cell
        for cell in world.get_cells_in_aoe(hero.current_cell,4):
            if world.manhattan_distance(cell, self.nearest_obj[self.hero_list.index(hero.id)]) < world.manhattan_distance( target_cell, self.nearest_obj[self.hero_list.index(hero.id)]) and not cell.is_wall and cell not in self.used_dodge_cells:
                target_cell = cell
        return target_cell

    def get_nearest_enemy_cell(self,world,hero):
        nearest_enemy_cell = world.map.get_cell(-1,-1)
        for enemy in world.opp_heroes:
            if enemy.current_cell == world.map.get_cell(-1,-1):
                continue
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

    def get_lowest_in_range_cell(self,world,hero,range):
        lowest_in_range_cell = world.map.get_cell(-1,-1)
        lowest_hp = 1000
        for enemy in world.opp_heroes:
            if world.manhattan_distance(hero.current_cell, enemy.current_cell) < range and enemy.current_hp < lowest_hp and enemy.current_cell not in self.attacking:
                lowest_hp = enemy.current_hp
                lowest_in_range_cell = enemy.current_cell
        return lowest_in_range_cell



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

        for i in range(row_min, row_max + 1):
            for j in range(column_min, column_max + 1):
                cell = world.map.get_cell(i, j)
                if not cell.is_in_objective_zone:
                    self.not_pass_objective_zone.append(cell)

        for c in self.not_pass_objective_zone:
            print("({},{})".format(c.row, c.column))
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
                if self.final_posisions[j][i].row < (row_min+row_max)/2:
                    row_change = 1
                else:
                    row_change = -1
                if self.final_posisions[j][i].column < (column_min+column_max)/2:
                    column_change = 1
                else:
                    column_change = -1
                self.final_posisions[j+1].append(world.map.get_cell(self.final_posisions[j][i].row+row_change,self.final_posisions[j][i].column+column_change))

        count = 0
        valid_flag = 0
        while valid_flag == 0:
            count = count + 1 
            valid_flag = 1
            for i in range(4):
                if self.final_posisions[0][i].is_wall or not self.final_posisions[0][i].is_in_objective_zone:
                    valid_flag = 0
                    row_change = 0
                    column_change = 0
                    if self.final_posisions[0][i].row < 16:
                        row_change = 1
                    else:
                        row_change = -1
                    if self.final_posisions[0][i].column < 16:
                        column_change = 1
                    else:
                        column_change = -1
                    self.final_posisions[0][i] = world.map.get_cell(self.final_posisions[0][i].row+row_change,self.final_posisions[0][i].column+column_change)
                    
                    if count > 30:
                        self.final_posisions[0][i] =world.map.objective_zone[randint(0, len(world.map.objective_zone) - 1)]

            
        
            
        # while valid_flag == 0:
        #     valid_flag = 1
        #     j = 0
        #     for i in range(4):
        #         if self.final_posisions[j][i].is_wall or not self.final_posisions[i][j].is_in_objective_zone:
        #             valid_flag = 0
        #             self.final_posisions[j][i] = self.final_posisions[j+1][i]
        #     j = j + 1   



    def pick(self, world):
        world.pick_hero(self.pick_heros.pop(0))

    def move(self, world):

        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            if hero.current_hp <= 0:
                self.reached_final_pos[num] = 0
        #list heroes
        hero_move_flag = [0,0,0,0]
        hero_dodge_flag = [0,0,0,0]
        if len (self.hero_list) < 4:
            for cell in world.map.my_respawn_zone:
                for hero in world.my_heroes:
                    if hero.current_cell == cell:
                       self.hero_list.append(hero.id) 

        #do nothing if dodge is more effective

        #go to nearest_obj
        fix_cells = []
        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            if not hero.current_cell.is_in_objective_zone and world._get_my_hero(cell=self.nearest_obj[num]) == None:
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.nearest_obj[num])
                if path_to_mid:
                    dodge_cell = self.get_dodge_cell(world,hero)
                    move_cell = self.get_direction_cell(world, hero.current_cell,path_to_mid,6)
                    if (not hero.get_ability(Model.AbilityName.BLASTER_DODGE).is_ready()) or len(world.get_path_move_directions(start_cell = move_cell, end_cell = self.nearest_obj[num])) <= len(world.get_path_move_directions(start_cell = dodge_cell, end_cell = self.nearest_obj[num])):
                        pass
                        #world.move_hero(hero=hero, direction=path_to_mid[0])
                    else:
                        hero_dodge_flag[num] = 1
                        fix_cells.append(hero.current_cell)


        # copy

        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            if not hero.current_cell.is_in_objective_zone and world._get_my_hero(cell=self.nearest_obj[num]) == None:
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.nearest_obj[num], not_pass = fix_cells)
                if path_to_mid and hero_dodge_flag[num] == 0:
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
                other_cells = other_cells + self.not_pass_objective_zone
                path_to_mid = world.get_path_move_directions(start_cell = hero.current_cell, end_cell = self.final_posisions[0][num], not_pass=other_cells)
                nearest_enemy_cell = self.get_nearest_enemy_cell(world,hero)
                if (path_to_mid and self.reached_final_pos[num] == 0 and hero_dodge_flag[num] == 0) or (hero_dodge_flag[num] == 0 and path_to_mid and (world.manhattan_distance(world._get_next_cell(hero.current_cell,path_to_mid[0]), nearest_enemy_cell) <= world.manhattan_distance(hero.current_cell, nearest_enemy_cell) or not hero.current_cell.is_in_objective_zone )):
                    world.move_hero(hero=hero, direction=path_to_mid[0])
            else:
                self.reached_final_pos[num] = 1
    def action(self, world):
        self.attacking = []
        self.used_dodge_cells = []
        for heroid in self.hero_list:
            hero = world.get_hero(heroid)
            target_cell = self.get_lowest_in_range_cell(world,hero,8)
            if target_cell and target_cell != world.map.get_cell(-1,-1):
                world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_BOMB), cell=target_cell)
            target_cell = self.get_lowest_in_range_cell(world,hero,6)
            if world._get_opp_hero(target_cell) and world._get_opp_hero(target_cell).current_hp < 40 and hero.get_ability(Model.AbilityName.BLASTER_BOMB).is_ready(): 
                    self.attacking.append(target_cell)
                    continue
            if target_cell and target_cell != world.map.get_cell(-1,-1):
                world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_ATTACK), cell=target_cell)
                if world._get_opp_hero(target_cell) and world._get_opp_hero(target_cell).current_hp < 20: 
                    self.attacking.append(target_cell)

        for num, heroid in enumerate(self.hero_list):
            hero = world.get_hero(heroid)
            # if hero.current_cell != self.final_posisions[0][num]:
            if not hero.current_cell.is_in_objective_zone:
                target_cell = self.get_dodge_cell(world,hero)
                if target_cell and target_cell != world.map.get_cell(-1,-1):
                    self.used_dodge_cells.append(target_cell)
                    world.cast_ability(hero=hero, ability=hero.get_ability(Model.AbilityName.BLASTER_DODGE), cell=target_cell)
