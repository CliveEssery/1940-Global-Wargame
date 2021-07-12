"""
Contains the models of a MVC type project

Part of the WW2 rules project as written by Clive Essery copyright 2003
updated many times until 2020 and software written 2020 from a previous
Delphi version written in 2004

Contains routines to 
- move all ships in a battle
- get range to target and bearings
- engage in combat
  - future projects:
- design classes of ships
- build ships from those classes that are required
- put ships into formations
- build a fleet from formations
- build battle from two antagonistic fleets - may be Neutrals
- start to build ships on slips, completions docks
- repair damaged ships in completion docks or dry docks
- move equipment around world
- move fleets around world
- perform sighting of one fleet to another
"""
from .constants import *
import math as math
from .constants import FieldTypes as FT
import json
import os
from tkinter import messagebox
from tkinter import filedialog
from . import utilities as util


class battle_model:
#"""                                                                                             DONE """ 
#""" a	select primary fleet for battle, determines the directory where battle info is stored        """
#""" b	select secondary fleet(s)                                                                    """
#""" c	record move number=0, fleet names in battle record                                           """
#""" d	import formations from all fleets and ships and add to record                                """
#""" e	save battle situation - see k below                                                          """
#""" f	import formation moves and damage from torpedoes/aircraft                                    """
#""" g	make moves,                                                                             YES  """     
#"""     apply damage from torpedoes/aircraft                                                         """
#""" h	import targets                                                                               """
#""" i	calculate ranges to targets, angle of bearing and crossing T angles                     YES  """
#""" j	perform battle as below, apply damage to ship record                                         """
#""" k	save battle situation                                                                        """
#""" l	at end of battle save fleets back to original location                                       """
#""" note fleets that are out of range at start of battle will also be moved and can join the         """
#""" action at any point

#    note at the start of the battle all formations must be in one of the following
#       layouts - Line Ahead, Line Abreast, En Echelon, either to port or starboard
#    if the player wishes at least one ship to be out of position, eg an AA ship 45 degrees
#       off the bow of the flagship to provide defense against aircraft than that ship
#       must be in a separate formation

#""" Formations data definition """
    forms_fields = {
        "curr_speed": {'req': True, 'type': FT.integer,'width': 10},
        "b4turn": {'req': True, 'type': FT.integer,'width': 10},
        "straight": {'req': True, 'type': FT.integer,'width': 10},
        "move":  {'req': True, 'type': FT.string,'width': 10},
        "ships": {'req': True, 'type': FT.string_list,'width': 10}
    }

#""" Ships data definition """
    ships_fields = {
        "locn": {'req': True, 'type': FT.int_list},
        "turn_points": {'req': True, 'type': FT.int_list},
        "main": {
            "targ": {'req': True, 'type': FT.string},
            "calibre": {'req': True, 'type': FT.string},
            "fore": {'req': True, 'type': FT.integer},
            "mid": {'req': True, 'type': FT.integer},
            "aft": {'req': True, 'type': FT.integer},
            "range": {'req': True, 'type': FT.integer},
            "rangeband": {'req': True, 'type': FT.string},
            "arc": {'req': True, 'type': FT.integer},
            "xingt": {'req': True, 'type': FT.integer},
        }
    }

    def __init__(self, extension='bat.json', path='./Data/SlowABC/', move=0, log=False):
#        super().__init__(*args, **kwargs)
        super().__init__()

        print('entered model init ')
        self.log = log
        if self.log:
#            print("log value",self.log)
            self.logging_fh = open ("./Data/logging.txt",mode="w",buffering=-1)
        
# temporary load of data to test logic, remove once a battle file can be read
        self.move_num = move
        self.fleets = FLEETS
        self.formations = FORMATIONS
        self.ships = SHIPS
        self.sunk_ships = SUNK_SHIPS
        self.path = path
        self.extension = extension
        # determine the file paths - not needed at the moment
        self.battle_filepath = path + 'LgIsle-' + str(move) + 'BAT' +extension
        print("battle file",self.battle_filepath)
            
        # indicate that the battle data has been loaded
        self.battle_loaded = False

        self.moves = []

        # isdirty indicates something has been written to the database
        self.isdirty = False
        
    def logging(self,msg_to_log="no message"):
        if self.log:
            print(msg_to_log)
#            self.logging_fh(msg_to_log)

    def print_ships(self,message="no message"):
        if self.log:
            print(message)
            for this_ship, ship_data in list(self.ships.items()):
                if this_ship == 'GB10':
                    line = this_ship + " : "
#                print(ship_data)
                    line += str(ship_data['locn'][0]) + ","
                    line += format(ship_data['locn'][1],'.2f') + ","
                    line += format(ship_data['locn'][2],'.2f') + ","
                    line += ship_data['main']['targ'] + ","
                    line += ship_data['main']['calibre'] + ","
                    line += format(ship_data['main']['range'],'.2f') + ","
                    line += ship_data['main']['rangeband'] + ","
                    line += format(ship_data['main']['arc'],'.2f') + ","
                    line += format(ship_data['main']['xingt'],'.2f')
                    print(line)

    def get_nation_directory(self):
        print('enter mod:get_nation_directory')
        directories = os.listdir(r'./data/')
        print(directories)
        return(directories)
        
    def get_unassigned_ships(self, directory, red, port, name):
        print('enter mod:get_unassigned_ships')
        self.nation = directory
        self.port = port
        self.formation_name = name
        
        filepath = './Data/' + directory + '/ships.json'
        # if the file doesn't exist, return
        if not os.path.exists(filepath):
            print("mod:get_unassigned_ships no ships file")
            return('fail',[])
        print('mod:get_unassigned_ships file exists ', filepath)

# need to check that formation doesn't already exist and return duplicate if it does

        # open the file and read in the raw values
        with open(filepath, 'r') as fh:
            ship_string = fh.read()
            print("*",ship_string,"*")
            raw_values = json.loads(ship_string)

        self.ships = raw_values   #['ships']
        print(self.ships)
        
        unassigned_ships = {}
        for ship in self.ships:
            values = self.ships[ship]
            if values['formation'] == "":
                if red and ship[0].lower() == 'r':
                    unassigned_ships[ship] = values["notes"]
                elif not(red) and ship[0].lower() != 'r':
                    unassigned_ships[ship] = values["notes"]
                
        print(unassigned_ships)
        return('ok', unassigned_ships)

    def complete_formation(self, selections):
        ########################################################
        # open the formations file in self.nation directory
        # add the new formation with the selections as the ships
        # save the formations file back again
        # close the file (not necessary)?
##### question do we need to allow split/join formations within the battle?
##### proly ask for port or fleet before split/join and only allow formations
##### at that location
        print('enter mod:complete_formation')
        self.selections = selections
        print('selections ',self.selections)

        filepath = './Data/' + self.nation + '/ships.json'
        # open the file and read in the raw values
        with open(filepath, 'r') as fh:
            allships = json.loads(fh.read())

        # add formation name to selected ships
        for ship in self.selections:
            allships[ship]["formation"] = self.formation_name

        json_string = json.dumps(allships)
        print('ships ', json_string)
        # open the file in write mode and write the changed values back
        with open(filepath, 'w') as fh:
            fh.write(json_string)

        filepath = './Data/' + self.nation + '/formations.json'
        # open the file and read in the raw values
        with open(filepath, 'r') as fh:
            allformations = json.loads(fh.read())

        newformation = self.build_formation(self.selections, allships)
        allformations[self.formation_name] = newformation

        json_string = json.dumps(allformations)
        print('formations ', json_string)
        # open the file in write mode and re-write the values
        with open(filepath, 'w') as fh:
            fh.write(json_string)
            
        filepath = './Data/' + self.nation + '/ports.json'
        # open the file and read in the raw values
        with open(filepath, 'r') as fh:
            allports = json.loads(fh.read())

        formations = allports[self.port]["formations"]
        print(self.port,' formations is ',formations)
        formations.append(self.formation_name)
        allports[self.port]["formations"] = formations
        print(self.port,' formations is ',allports[self.port]["formations"])

        json_string = json.dumps(allports)
        print('ports ', json_string)
        # open the file in write mode and re-write the values
        with open(filepath, 'w') as fh:
            fh.write(json_string)
         
        print("exit mod:complete_formation")

    def build_formation(self, selections, ships):
        ######################################################
        # build a formation with info from the selected ships
        # 
        empty_formation = {"currspd":0,"spdstep":0,"bestspd":0,"b4turn": 0,"straight":0,"move":"","facing":0,"ships":[]}

        object_sizes = {"LZ":{"b4turn":2,"spdstep":6},"MZ":{"b4turn":4,"spdstep":6},
                        "SZ":{"b4turn":6,"spdstep":6},"HZ":{"b4turn":8,"spdstep":6},
                        "XZ":{"b4turn":10,"spdstep":3},"CZ":{"b4turn":13,"spdstep":3},
                        "GZ":{"b4turn":16,"spdstep":3}}
        # vessel sizes are GZ = HMS Habbakuk and Battlewagons > 1200' long
        #                  CZ = Battlewagons at least 1000' long and VG or VC
        #                  XZ = smaller Battlewagons and carriers
        #                  HZ = Cruisers or Merchantmen of at least 5000 tons
        #                  SZ = smaller Cruisers or Merchantmen
        #                  MZ = Destroyer Leaders and smaller
        #                  LZ = MTBs, Landing Craft and Aircraft

        print('enter build_formation ')

        bestspd = 60     # the highest speed of any ship = MTB
        b4turn = 2       # the smallest step before a ship can turn
        spdstep = 6      # the largest speed step          
        
        empty_formation["ships"]= selections
        for ship in selections:
            object_size = object_sizes[ships[ship]["shipsize"]]
            if ships[ship]["dsgnspd"] < bestspd:
                bestspd = ships[ship]["dsgnspd"]
            if object_size["b4turn"] > b4turn:
                b4turn = object_size["b4turn"]
            if object_size["spdstep"] < spdstep:
                spdstep = object_size["spdstep"]

        empty_formation["spdstep"] = spdstep
        empty_formation["bestspd"] = bestspd
        empty_formation["b4turn"] = b4turn

        print('exit build_formation ', empty_formation)
        return(empty_formation)
        
    def get_move_num(self):
        print("enter mod:get_move_num")
        print(self.move_num)
        print("exit mod:get_move_num")
        return(self.move_num)
        
    def get_form_info(self, formation_list=[], return_var={}):
        # formation_list is a list of formations to strip the data out of
        # return_var is a dictionary consisting of a formation name as the key
        #    and a list of values to return to the Application
        print('enter mod:get_form_info')
        for key in formation_list:

            value = self.formations[key]
            values = {'bestspd': value['bestspd']}
            values['b4turn'] = value['b4turn']
            values['straight'] = value['straight']
            values['move'] = value['move']
            values['currspd'] = value['currspd']
            values['spdstep'] = value['spdstep']
            values['facing'] = value['facing']

            return_var[key]=values

        print('exit mod:get_form_info')
        return(return_var)

    def get_all_form_info(self, allied=False, enemy=False):
        print('enter mod:get_all_form_info')
        return_var = {}
        if allied:
            for fleet in self.fleets['Allied']:
                return_var = self.get_form_info(fleet['formations'], return_var)
        if enemy:
            for fleet in self.fleets['Enemy']:
                return_var = self.get_form_info(fleet['formations'], return_var)

        print('exit mod:get_all_form_info')
        print(return_var)
        return(return_var)

    def update_move_b4turn_currspd(self, formation, move, b4turn, currspd):
        print('enter mod:update_move_b4turn_currspd')
        self.formations[formation]['move'] = move
        self.formations[formation]['b4turn'] = b4turn
        self.formations[formation]['currspd'] = currspd
        print(self.formations[formation])

        self.isdirty = True           # database has changed
        print('exit mod:update_move_b4turn_currspd')
        
    def get_formations(self):
#        """return the formations data to the application"""
        print("enter mod:get_formations")
        if self.battle_loaded:
            return(self.formations)
        else:
            print("exit mod:Get_formations")
            return(none)

    def get_ships(self):
#        """return the ships data to the application"""
        print("enter mod:get_ships")
        if self.battle_loaded:
            return(self.move_num, self.ships)
        else:
            print("exit mod:get_ships")
            return(none)

    def get_dbs(self):
        print("enter mod:get_dbs")
        print(self.move_num)
        if self.battle_loaded:
            print("exit mod:get_dbs")
            return(self.move_num, self.fleets, self.formations, self.ships)
        else:
            print("exit mod:get_dbs-failure")
            return(none)

#---------------------------------------------------------------------#
#    Get Range                                                        #
#    Save the X and Y values for both vessels                         #
#    Compute the Range as the sum of the squares of the differences   #
#    Compute the Range Band from the Range and the Wpn Type           #
#    Compute the Bearing, handling the special cases first where      #
#    the ships are exactly on the same axis, either horizontally      #
#    or vertically                                                    #
#    Note bearing is the angle that Targ2 is from Targ1, ie Targ1     #
#    is the firer. Bearing is calculated with 0 being vertically      #
#    upwards                                                          #
#                                                                     #
#---------------------------------------------------------------------#

    def get_range(self,point1 = [0,0,0], point2 = [0,0,0], wpn = "LM"):
#        if self.log:
#            print("enter mod:get_range",point1,' points ',point2,wpn)
    # note contents of the points are angle [0-7],X,Y both in cms from bottom left
        x1 = point1[1]
        y1 = point1[2]
        x2 = point2[1]
        y2 = point2[2]

        diffx = x1 - x2
        diffy = y1 - y2

        # by exponentiating by 1/2 you get a square root
        range = round((diffx * diffx + diffy * diffy)**0.5, 2)

        irangeband = 0
        while (range > RANGE_BANDS[wpn][irangeband]) and (irangeband < 5):
            irangeband += 1
    # Note, if irangeband is 5, band_names[5] is correctly Bynd=Beyond #
        rangeband = BAND_NAMES[irangeband]
#        if self.log:
#            print("exit mod:get_range", range, rangeband)
        return(range,rangeband)
    # end of get range

    def get_bearing(self,point1 = [0,0,0], point2 = [0,0,0]):
#        if self.log:
#            print("enter mod:get_bearing",point1,' points ',point2)
    # note contents of the points are angle [0-7],X,Y both in cms from bottom left
        x1 = point1[1]
        y1 = point1[2]
        x2 = point2[1]
        y2 = point2[2]
        if abs(x1-x2) < 0.01:   # defensive coding in case of rounding errors #
            if abs(y1-y2) < 0.01:
            # objects at same point
                bearing = 0.0   # in radians
            elif y2 > y1:
                bearing = 0.0
            else:
                bearing = math.pi

        elif abs(y1-y2) < 0.01:  # defensive coding in case of rounding errors #
            bearing = math.pi / 2.0 if x2 > x1 else 3.0 * math.pi / 2.0
    # else option x2 < x1 - case for equal positions already catered for #
        elif (x2 > x1) and (y2 > y1): #top right quadrant#
            bearing = math.atan((x2-x1)/(y2-y1))
        elif (x2 > x1) and (y2 < y1): #bottom right quadrant#
            bearing = math.pi - math.atan((x2-x1)/(y1-y2))
        elif (x2 < x1) and (y2 > y1): #top left quadrant#
            bearing = 2.0 * math.pi - math.atan((x1-x2)/(y2-y1))
        elif (x2 < x1) and (y2 < y1): #bottom left quadrant#
            bearing = math.pi + math.atan((x1-x2)/(y1-y2))
        else:
            #Application.MessageBox
            print('Cannot find Bearing ')

#        if self.log:
#            print("exit mod:get_bearing", bearing)
        return (bearing) # in radians
    # end of get bearing

    def move_ship(self,move_dist,this_ship):
#        if self.log:
#        print("enter mod.move_ship")
# check range to turn point if greater than move distance move at
# current angle else move to turn point, change facing, delete first
# turn point - the move formation routine will call this one again
# note, uses the key from the ships dictionary to ensure the data is 
# written back to the database
        xMult = [0.0,0.707,1.0,0.707,0.0,-0.707,-1,-0.707]
        yMult = [1.0,0.707,0.0,-0.707,-1.0,-0.707,0.0,0.707]
        ship = self.ships[this_ship]
        move_data = [ship,self.ships[this_ship]['locn'],self.ships[this_ship]["turn_points"],
                     self.ships[this_ship]['currspd'],move_dist]
#        print(this_ship, ship)
# turn_point is a list containing new direction of travel at the
# turn_point, the x and y position of the turnpoint - note there may
# be several lists in the turn points list. locn has the same format
        print('start move_ship:',this_ship,ship['locn'],ship['turn_points'])
        tndamage, maxspd = util.dmg_effect(ship['currblock'],ship['blockfill'],ship['dsgnspd'])
        if ship['turn_points'] == []:
# to check code is working without printing all data and wasting reams of paper #
#            if this_ship == "GB10":         
#                print('GB10a-move dist',move_dist,'locn',self.ships[this_ship]['locn'])
            self.ships[this_ship]['locn'][1] += int(move_dist * xMult[ship['locn'][0]])
            self.ships[this_ship]['locn'][2] += int(move_dist * yMult[ship['locn'][0]])
#            if this_ship == "GB10":
#                print('GB10b-ship',this_ship,ship,'addition',move_dist*xMult[ship['locn'][0]],self.ships[this_ship]['locn'])
            print('mod.moveship1:',ship['currspd'],' max ',maxspd,' dist ', move_dist)
            self.ships[this_ship]['currspd'] = min(maxspd, ship['currspd'] + move_dist)
            print('mod.moveship1a:',this_ship,ship['currspd'])
            move_dist = 0  # used up all the move in the current direction
        else:
            rng_to_turn, rangeband = self.get_range(ship['locn'],ship['turn_points'][0],'XM')
            if (rng_to_turn > move_dist):
                self.ships[this_ship]['locn'][1] += int(move_dist * xMult[ship['locn'][0]])
                self.ships[this_ship]['locn'][2] += int(move_dist * yMult[ship['locn'][0]])
                print('mod.moveship2:', this_ship, ship['currspd'],maxspd,move_dist)
                self.ships[this_ship]['currspd'] = min(maxspd, ship['currspd'] + move_dist)
                move_dist = 0
        
            else:
                move_dist -= rng_to_turn # may ofc be zero
# turn the ship to the new angle at the turn point and move to next turn point
                new_locn = []
                for i in range(3):
                    # note turn_points[0] is the first turn point in the list and i runs through all the three
                    new_locn.append(self.ships[this_ship]['turn_points'][0][i])
                self.ships[this_ship]['locn'] = new_locn  
                self.ships[this_ship]['turn_points'].pop(0)
                print('mod.moveship3:', this_ship, ship['currspd'],maxspd,move_dist)
                self.ships[this_ship]['currspd'] = min(maxspd, ship['currspd'] + move_dist)

            # end of if (rng_to_turn > move_dist)
        # end of if self.ships[this_ship]['turn_points'] == []
        move_data.append(self.ships[this_ship]['locn'])
        move_data.append(self.ships[this_ship]["turn_points"])
        self.moves.append(move_data)
        print('end move_ship:',this_ship,ship['locn'],ship['turn_points'])
#        print("exit mod.move_ship")
        return(move_dist)

    def move_ships_one_element(self,this_formation, dist_to_move, move):
#        if self.log:
#        print("enter move_ships one element")
#        self.formations[this_formation]['currspd'] = dist_to_move
#        self.formations[this_formation]['move'] = move
        for this_ship in self.formations[this_formation]['ships']:
# note dist_to_move gets changed every time round the loop
# some ships in the formation may not be able to keep up with the formation
#            print('mod.move ships 1 elem1:',this_ship,dist_to_move)
            ship = self.ships[this_ship]
            tndamage, maxspd = util.dmg_effect(ship['currblock'],ship['blockfill'],ship['dsgnspd'])
            move_dist = min(dist_to_move, maxspd)
#            print('mod.move ships 1 elem2:',this_ship,dist_to_move,maxspd)
# generate from the speed prob speed/3 maybe more or less
            while move_dist > 0:
                move_dist = self.move_ship(move_dist,this_ship)

#        if self.log:
#        print("exit move_ships one element")
        return()

    def move_formation(self,this_formation):
#        self.logging("enter move_formation")
#        if self.log:
#            self.print_ships("enter move_formation")
        print("enter mod:move_formation",this_formation)

# for all ships in this_formation move that ship
        formation = self.formations[this_formation]
        dist_to_move = 0
        if len(formation['ships']) == 0:
            # do nothing there is no ships in the formation to move, defo applies to sunk
            # at the beginning and later on other formations when all ships in it become sunk
            print('No ships in this formation, eg "sunk" at the start of the game')
            self.formations[this_formation]['facing'] = 0
        else:
            ships = formation['ships']
#           for a_ship in ships:
#               print(a_ship,self.ships[a_ship])
            move = formation['move'].upper()
            # store the old move for this formation to set as proposed for next move
            old_move = move
            count = 0
            total_dist = 0            
            while len(move) > 0 and count < 10:
# defensive coding - need to add check on count to avoid infinite loop
                count += 1
#               print(move,'count ',count)
# an element is either just a distance or a turn and a distance
# must move this distance before adding a second turn because you don't know
# where that will be
                if len(move) > 2:
                    first1 = move[0]
                    first2 = move[0:2]  # slicing doesn't include the last index
                else:
                    first1 = move[0]
                    first2 = ""
#               print('first #',first1,'#',first2,'#',sep='')

                self.straight_after_turn = 0
                new_angle = self.ships[ships[0]]['locn'][0]
                if first2 == "TS":  # all ships turn to starboard together at the same time
                    self.straight_after_turn = 0
                    new_angle = (new_angle + 1) % 8
#                   print("TS new angle ",new_angle,current_locn)
                    for i in range(len(ships)):
                        print(ships[i], self.ships[ships[i]])
#                       need to reset the current locn for each ship otherwise the locations of all will be added to it
                        current_locn = [new_angle]
                        current_locn.append(self.ships[ships[i]]['locn'][1])
                        current_locn.append(self.ships[ships[i]]['locn'][2])
                        self.ships[ships[i]]['turn_points'].append(current_locn)
                        print(ships[i],self.ships[ships[i]])
                    move = move[2:]
#                   print('#',move,'#',sep='')
                elif first2 == "TP":  # all ships turn to port together at the same time
                    self.straight_after_turn = 0
                    new_angle = (new_angle - 1) % 8
#                   print("TP new angle",new_angle,current_locn)
                    for i in range(len(ships)):
#                       need to reset the current locn for each ship otherwise the locations of all will be added to it
                        current_locn = [new_angle]
                        current_locn.append(self.ships[ships[i]]['locn'][1])
                        current_locn.append(self.ships[ships[i]]['locn'][2])
                        print(ships[i], self.ships[ships[i]])
                        self.ships[ships[i]]['turn_points'].append(current_locn)
                        print(ships[i], self.ships[ships[i]])
                    move = move[2:]
                elif first1 == 'S':    # all ships turn at the point where the lead ship currently is
                    self.straight_after_turn = 0
                    new_angle = (new_angle + 1) % 8
#                   build the locn for the first ship in the formation, that will be the turn point
                    current_locn = [new_angle]
                    current_locn.append(self.ships[ships[0]]['locn'][1])
                    current_locn.append(self.ships[ships[0]]['locn'][2])
#                   print("S new angle ",new_angle,'curr locn',current_locn)
                    for i in range(len(ships)):
                        self.ships[ships[i]]['turn_points'].append(current_locn)
                    move = move[1:]
#                   print('move @',move,'@ ships ',ships,sep='')
                elif first1 == "P":  # all ships turn to port at the point where the lead ship currently is
                    self.straight_after_turn = 0
                    new_angle = (new_angle - 1) % 8
                    current_locn = [new_angle]
                    current_locn.append(self.ships[ships[0]]['locn'][1])
                    current_locn.append(self.ships[ships[0]]['locn'][2])
#                   print("P new angle ",new_angle,'curr locn',current_locn)
                    for i in range(len(ships)):
                        self.ships[ships[i]]['turn_points'].append(current_locn)
                    move = move[1:]
#                   print('move @',move,'@ ships ',ships,sep='')
# changed a distance to be preceeded by A in case user does two straight moves in a row
# 18 followed by 3 would appear to be 183, A18A3 makes this obvious
# probably not necessary as the code should correctly read this as 18 + 3 but 912 would be read as 91 + 2
                elif move[0] == "A":
                    move = move[1:]
# reached the number that is a straight distance to move
                elif move[0] in ['0','1','2','3','4','5','6','7','8','9']:
# leading 0 is allowed for the case when the turn takes place at the end of the move
#                   print('this formation ',this_formation,'move ',move,'len ',len(move))
                    if len(move) > 1:
                        if move[1] in ['0','1','2','3','4','5','6','7','8','9']:  
# note need to perform the first element of movement before assigning any
# further elements so that 2nd turn point is in correct location
                            dist_to_move = int(move[0:2])   # slicing doesnt include last index
                            # don't allow the ship to move more than its current speed
                            move = move[2:]
                            total_dist += dist_to_move
# still got issue here - can turn multiple times if formation travelling faster than ships maxspd
                            self.straight_after_turn += dist_to_move
                            print('dist to move1:',dist_to_move,'move:'+move+':')
                            self.move_ships_one_element(this_formation, dist_to_move, move)
                        else:
                            dist_to_move = int(move[0])
                            move = move[1:]
                            total_dist += dist_to_move
                            self.straight_after_turn += dist_to_move
                            print('dist to move2:',dist_to_move,'move:'+move+':')
                            self.move_ships_one_element(this_formation, dist_to_move, move)
                    else:
                        dist_to_move = int(move[0])
                        move = move[1:]
                        total_dist += dist_to_move
                        self.straight_after_turn += dist_to_move
                        print('dist to move3:',dist_to_move,'move:'+move+':')
                        self.move_ships_one_element(this_formation, dist_to_move, move)

            #end of while len(move) > 0 and count < 10:

            # restore old move as proposal for next move
#           if this_formation == 'RBatDiv1':
#               print('mod.move_formation currspd ',self.formations[this_formation]['currspd'],' tot dist ',total_dist)
#           print('mod.move_formation1:',total_dist,self.formations[this_formation]['currspd'])
            self.formations[this_formation]['currspd'] = total_dist
            self.formations[this_formation]['b4turn'] = max(0, self.formations[this_formation]['straight'] - self.straight_after_turn)
            self.formations[this_formation]['move'] = old_move
            first_ship = self.formations[this_formation]['ships'][0]
            print('move form:',first_ship)
            self.formations[this_formation]['facing'] = self.ships[first_ship]['locn'][0]            
#        end of len("ships" > 0

#        if self.log:
#            self.print_ships("exit move_formation")
#            print("exit mod:move_formation")
            
    def move_all(self):
        # for all formatations in FORMATIONS move that formation
#        logging
        print("enter move_all")

        # increment the move number
        self.move_num += 1
        print("MOVE NUM **** ",self.move_num)
        for this_ship, value in list(self.ships.items()):
            # clear the currspd for each ship, it will be rebuilt in move ship
            self.ships[this_ship]['currspd'] = 0
        for key, value in list(self.formations.items()):
            if key == 'sunk':
                print('not moving sunk formation')
            else:
                self.move_formation(key)

        self.isdirty = True           # database has changed

#        logging
        self.move_filepath = self.path + 'LgIsle-' + str(self.move_num) + 'move' + self.extension
        
# note need to convert lists to strings b4 we can use json encoding
#        with open(self.move_filepath, 'w') as fh:
#            fh.write(self.moves)
#        self.print_ships("exit move_all")
        
#        print("exit move_all")

    def set(self, key, value):
        logging("enter set")
        """Set may need to have one for formations and ships
           variable value"""
        if (
            key in self.variables and
            type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")
        logging("exit set")

    def get_range_bear(self, ship1="", ship2=""):
#        """ gets the range and updates the ships database
#            gets the bearing of ship1 to 2, the reverse
#            is the bearing of ship2 to 1 again
#            the ships database is updated """
#        if self.log:
 #           print("enter get range bear ", ship1, ship2)
        ranges, rangeband = self.get_range(self.ships[ship1]['locn'],
                                          self.ships[ship2]['locn'],
                                          self.ships[ship1]['main']['calibre'])
        self.ships[ship1]['main']['range'] = ranges
        self.ships[ship1]['main']['rangeband'] = rangeband
        bearing_rad = self.get_bearing(self.ships[ship1]['locn'],
                                       self.ships[ship2]['locn'])
        bearing_deg = bearing_rad * 180/math.pi
        bearing_deg_rev = (bearing_deg + 180) % 360
#        print('bearging deg',bearing_deg,bearing_deg_rev)
        # the bearing from the point of view of the second ship is 180 degrees on
        bearing_deg -= self.ships[ship1]['locn'][0] * 45
        # the first element of the locn list is the angle number which can be
        # multiplied by 45 degrees or pi/4
        bearing_deg = bearing_deg % 360
        if bearing_deg > 180:
            bearing_deg = 360 - bearing_deg  # value set to range -179 to 180
        self.ships[ship1]['main']['arc'] = round(bearing_deg, 2)
        xing_t = bearing_deg_rev - self.ships[ship2]['locn'][0] * 45
        if xing_t > 180:
            xing_t = 360 - xing_t
        self.ships[ship1]['main']['xingt'] = round(xing_t, 2)
        if ship1[0] == "G":                # and rangeband != 'Bynd'
            tndamage1, maxspd1 = util.dmg_effect(self.ships[ship1]['currblock'],self.ships[ship1]['blockfill'],
                                                 self.ships[ship1]['dsgnspd'])
            tndamage2, maxspd2 = util.dmg_effect(self.ships[ship2]['currblock'],self.ships[ship2]['blockfill'],
                                                 self.ships[ship2]['dsgnspd'])
            print(ship1,ship2,int(ranges),rangeband,
                  self.ships[ship1]['locn'],self.ships[ship1]['currspd'],maxspd1,
                  self.ships[ship2]['locn'],self.ships[ship2]['currspd'],maxspd2)

        self.isdirty = True           # database has changed

#        if self.log:
#            print("exit get range bear")
        return()

    def get_range_all(self):
#        """ goes through ship database & if the ship has a target then compute the
#            distance and bearngs to the target """
        print("enter get range all")
        ships_in_range = {}
        for this_ship, ship_data in list(self.ships.items()):
#            print('current line of ship', this_ship, ship_data)
            if ship_data['main']['targ'] != "":
                ships_in_range = self.get_range_bear(this_ship, ship_data['main']['targ'])
                if ship_data['main']['rangeband'] != 'Bynd':
                    print('in range ', this_ship, self.ships[this_ship]['main'])
# put this back in                    ships_in_range = dict((this_ship, self.ships[this_ship]['main']))
#                   print('current ship', this_ship, ship_data['main']['targ'],
#                          format(ship_data['main']['range'], '.2f'),
#                          ship_data['main']['rangeband'],
#                          format(ship_data['main']['arc'], '.2f'),
#                          format(ship_data['main']['xingt'], '.2f'))

        print('ships in range: ', ships_in_range)

#        if self.log:
#            print("exit get range all")
        self.print_ships("exit get range all")
        return(ships_in_range)

    def get_targ_info(self, formation):
        print('enter mod:get_targ_info')
        ships = self.formations[formation]['ships']
        result = {}
        for ship in ships:
            values = {}
            print(self.ships[ship]['main'])
            values['targ'] = self.ships[ship]['main']['targ']
            values['arc'] = self.ships[ship]['main']['arc']
            values['rangeband'] = self.ships[ship]['main']['rangeband']
            print(values)
            result[ship] = values
            print('get targ info', result)
        print('exit mod:get_targ_info')
        print(result)
        return(result)

    def get_1st_firing_data(self):
        DAMAGE_SHELL = {"IM":[27,15,9,27,7],"GM":[24,13,8,24,6],"CM":[21,11,7,21,5],
                        "XM":[18,9,6,18,4],"HM":[15,7,5,15,3],"SM":[12,6,4,12,2],
                        "MM":[11,5,3,11,2],"LM":[10,4,3,10,2],"GS":[9,4,3,9,2],
                        "CS":[8,3,2,8,1],"XS":[6,2,2,6,1],"HS":[0,0,12,12,0],
                        "SS":[0,0,9,9,0],"MS":[0,0,6,6,0],"LS":[0,0,4,4,0]}
        # Range at which belts can be penetrated from 6" to 15" in 0.5" steps for different guns
        PEN_BELT = {"HM":[240,240,239,238,238,237,236,235,235,234,232,231,229,226,223,219,215,211,207],
                    "SM":[230,229,227,226,225,223,222,220,219,217,214,211,207,202,197,191,185,179,173],
                    "MM":[207,199,191,183,175,167,159,151,143,137,130,125,120,114,112,108,104,100,96],
                    "LM":[190,184,178,172,166,160,154,148,142,136,129,123,117,112,107,101,96,91,86]}
        # Range at which decks can be penetrated from 2" to 4" in 0.25" steps for different guns
        PEN_DECK = {"HM":[77,85,93,94,95,96,97,98,99],
                    "SM":[82,89,96,98,100,101,102,103,104],
                    "MM":[92,99,106,108,110,111,112,113,114],
                    "LM":[114,122,130,133,136,138,140,142,144]}

        print('enter mod.get_1st_firing_data')
        self.all_firing_data = []
        self.max_firer = 0
        for this_ship, ship_data in list(self.ships.items()):
            if ship_data['main']['targ'] != "" and ship_data['main']['rangeband'] != 'Bynd':
                self.max_firer += 1     # found a pair of ships in range, add their data
                target = ship_data['main']['targ']
                targspd = self.ships[target]['currspd']
                rangeband = ship_data['main']['rangeband']
                onethirdtargspd = int(targspd/3)
                tnrangespd = TNRANGESPD[rangeband][onethirdtargspd]
                arc = ship_data['main']['arc']
                print('arc ',arc)
                if arc > 180.01:
                    arc = 360 - arc              #convert to +- 0 to 180
                if abs(arc) < 45.0:
                    numguns = ship_data['main']['fore']
                elif abs(arc) < 135.01:
                    numguns = ship_data['main']['mid']
                else:
                    numguns = ship_data['main']['aft']
                tntime = TNTIME[ship_data['main']['time']]
                tnfiredat = ship_data['firedat']
                xingt = ship_data['main']['xingt']
                if xingt > 180.01:
                    xingt = 360 - xingt
                if abs(xingt) < 15.01:
                    tnxingt = -5
                else:
                    tnxingt = 0

                tnstraddle = ship_data['main']['straddle']
                tndamage, maxspd = util.dmg_effect(ship_data['currblock'],ship_data['blockfill'],ship_data['dsgnspd'])
                tntotal = tnrangespd + tntime + tnfiredat + tnxingt
                tntotal += tnstraddle + tndamage

                tn = 'rngspd ' + str(tnrangespd) + ' time ' + str(tntime)
                tn += ' fired at ' + str(tnfiredat) + ' xingt ' + str(tnxingt)
                tn += ' strad ' + str(tnstraddle) 
                tn += ' tndmg ' + str(tndamage)
                tn += ' = ' + str(tntotal)

                print('1st fire:',target,int(self.ships[target]['belt']*2)-12,' max 16')
                penb = PEN_BELT[ship_data['main']['calibre']][int(self.ships[target]['belt']*2)-12]
                pend = PEN_DECK[ship_data['main']['calibre']][int(self.ships[target]['deck']*4)-8]
                dmgshell = str(DAMAGE_SHELL[ship_data['main']['calibre']][0]) + ' noPen ' + str(DAMAGE_SHELL[ship_data['main']['calibre']][4])
                                                                            
                firing_data = [this_ship, target, targspd, rangeband,
                               ship_data['main']['range'],
                               ship_data['main']['calibre'],
                               numguns,
                               round(xingt, 2),
                               tn,
                               self.ships[target]['belt'],
                               self.ships[target]['deck'],
                               penb,
                               pend,
                               dmgshell]
                self.all_firing_data.append(firing_data)

        # end of for this_ship, ship_data
        self.firer = 0
        print('exit mod.get_firing_data')
        if self.max_firer == 0:
            return([""])
        else:
            return(self.all_firing_data[self.firer])

    def done_firing(self, firing_data, straddle, damage):
        # routine to deal with the damage received on one ship
        print('enter mod.done_firing')
    
        # set the firer's straddle result from the entered data
        firer = firing_data[0]
        self.ships[firer]['main']['straddle'] = straddle
        # if not at the higest level for tntime, increment that value in firer
#        print('b4 update of time:', self.ships[firer]['main']['time'])
        if self.ships[firer]['main']['time'] < 8:
            self.ships[firer]['main']['time'] += 1
#            print('time ',firer,self.ships[firer]['main']['time'])
        
#        print('after update of time:', self.ships[firer]['main']['time'])
        # the target has been fired at so doesn't get the not fired at bonus
        target = firing_data[1]
        self.ships[target]['firedat'] = 0
        # apply the damage
#        print('b4 update of totdamage',self.ships[target]['blockfill'],' dmg:',damage)
        totdamage = self.ships[target]['blockfill'] + damage
#        print('b4 while, totdamage:',totdamage)
        while totdamage > 0:
#            print('in while, totdamage:',totdamage)
            if totdamage >= self.ships[target]['blocksize']:
                totdamage = totdamage - self.ships[target]['blocksize']
#                print('in if, totdamage:',totdamage)
                self.ships[target]['blockfill'] = 0
#                if self.ships[target]['currblock'] < 6:   # 7 = listing(DIW), 8 = sunk
                self.ships[target]['currblock'] += 1
#                print('end of if, currblock:',self.ships[target]['currblock'])
# keep these next 4 lines together, either commented out or in use
#               tndamage, maxspd = util.dmg_effect(self.ships[target]['currblock'],
#                                                  self.ships[target]['blockfill'],
#                                                  self.ships[target]['dsgnspd'])
#               print('max spd ',target, maxspd)
#               print('curr spd ',target, self.ships[target]['currspd'])
            else:                     # totdamage is < blocksize
                self.ships[target]['blockfill'] = totdamage
                totdamage = 0
#                print('in else, blockfill:',self.ships[target]['blockfill'],'dmg:',damage)
        # end of while damage > 0
        if self.ships[target]['blockfill'] >= 1:
            # at least some damage has been done into this block
#            self.ships[target]['maxspd'] -= 3
#           tndamage, maxspd = util.dmg_effect(self.ships[target]['currblock],self.ships[target]['blockfill'],
#                                            self.ships[target]['dsgnspd'])
#            if self.ships[target]['currspd'] > maxspd:
#                self.ships[target]['currspd'] = maxspd
#           print('curr spd ',target, self.ships[target]['currspd'])
#           print('max spd ',target, maxspd)
#            self.ships[target]['tndamage'] += 2
#           elif self.ships[target]['currblock'] == 6:
            if self.ships[target]['currblock'] == 7:
                print('currblock = 7')
                self.ships[target]['dsgnspd'] = 0    # ship is Dead in Water
#                self.ships[target]['tndamage'] = 14
            elif self.ships[target]['currblock'] >= 8:    # ship has sunk or exploded
                print('currblock = 8')
                # move ship to sunk formation
                # find which formation the ship is in and delete it
                for formation, values in self.formations.items():
                    print('in for formation:')
                    found_target = -1
                    ship_num = 0
                    print('formation:',formation)
                    print('formations:',self.formations[formation]['ships'])
                    for ship in self.formations[formation]['ships']:
                        print('ship:',ship,' formation:',formation)
                        if ship == target:
                            found_target = ship_num
                        else:
                            ship_num += 1
                    print('mod:done_firing:ship_num:',ship_num, found_target)
                    if found_target > -1:
                        print(self.formations[formation]['ships'][found_target])
                        self.ships[target]['currblock'] = 8
                        self.ships[target]['blockfill'] = 1   # enough to set the ship to SUNK
                        self.formations[formation]['ships'].pop(found_target)
# do we even need sunk formation if we are putting ship into separate directory?
#                        self.formations['sunk']['ships'].append(target)
                        self.ships.pop(target)
                        self.sunk_ships.append(target)
                        print('sunk ship:',self.sunk_ships)
        
        # select the next ship that is in range and return the firing data
        self.firer += 1
#        print('Firer: ',firer,' straddle ',self.ships[firer]['main']['straddle'])
#       tndamage, maxspd = util.dmg_effect(self.ships[target]['currblock'],self.ships[target]['blockfill'],
#                                          self.ships[target]['dsgnspd'])
#        print('Target: ',target,' block data ',self.ships[target]['currblock'],
#              self.ships[target]['blockfill'],
#              ' maxspd ',maxspd,' currspd ', self.ships[target]['currspd'],
#              ' tndmg ',tndamage)
        print('exit mod.done_firing')
        print('firer ',self.firer,' max firer ',self.max_firer)

        self.isdirty = True           # database has changed

        if self.firer >= self.max_firer:
            return([""])           # return an empty list to show there is no more in range
        else:
            return(self.all_firing_data[self.firer])
                
    def save_battle(self):
#        """Save the current formations data to the file
#           note, need to combine this to one file save_battle with move number """
#           and fleet names so we can return the fleet to the correct file
#           question, how do we know which formation is in which fleet?
#           and which fleets are allied?
#        print("enter save_battle")

        # determine the file path
        self.battle_filepath = self.path + 'LgIsle-' + str(self.move_num) + 'BAT' + self.extension
        print("battle file",self.battle_filepath)
            
        json_string = '{"move":' + json.dumps(self.move_num)
        print(json_string)
        json_string += ',"fleets":' + json.dumps(self.fleets)
        print(json_string)
        json_string += ',"formations":' + json.dumps(self.formations)
        json_string += ',"ships":' + json.dumps(self.ships)
        json_string += ',"sunk_ships":' + json.dumps(self.sunk_ships)
        json_string += "}"
        print(json_string)
        print(self.battle_filepath)

        with open(self.battle_filepath, 'w') as fh:
            fh.write(json_string)
#        print("exit save battle")

    def get_file_to_load(self):
        # get the filename to load and tell the application what the name is
        print("enter mod:get_file_to_load")
        if self.isdirty:
            reply = messagebox.askyesno(
                title = "Data has changed",
                message = """Do you really want to delete it?""")
            if not(reply):
                return()
        load_filename = filedialog.askopenfilename(
            title= "Select the filename to Load",
            initialdir = ".Data",
            defaultextension = ".json",
            filetypes = [("Battle Json", '*bat.json *BAT.json')])
        self.load_battle(load_filename)
        print("exit mod:get_file_to_load")

    def load_battle(self, load_filename):
#        """Load the settings from the file
#            need to change this to load_battle and split"""
        print("enter mod:load battle", load_filename)

        # if the file doesn't exist, return - note, should never happen
        if not os.path.exists(load_filename):
            print("in load_battle, file doesn't exist")
            return
        print('file exists ', load_filename)

        # open the file and read in the raw values
        with open(load_filename, 'r') as fh:
            raw_values = json.loads(fh.read())

        self.move_num = raw_values['move']
        print(self.move_num)
        self.fleets = raw_values['fleets']
        print(self.fleets)
        self.formations = raw_values['formations']
        print(self.formations)
        self.ships = raw_values['ships']
        print(self.ships)
        # don't implicitly trust the raw values, but only get known keys
#        for key in self.formations:
#            if key in raw_values and 'value' in raw_values[key]:
#                raw_value = raw_values[key]['value']
#                self.formations[key]['value'] = raw_value

        self.isdirty = False           # database has been loaded

        print("exit mod:load battle")

    def update_firer_target(self,firer,target,targfrmtn):
        # receives the firer/target pairing from View and updates the ship DB
        print("enter mod:update_firer_target")
        if target == "":     # firer no longer has a target
            self.ships[firer]['main']['targ'] = ""
            print('exit mod:update_firer_target', 'firen no longer has a target')
            return('firer has no target')
        
        old_target = self.ships[firer]['main']['targ']
        old_target_num = -1
        count = 0
        for ship in self.formations[targfrmtn]['ships']:
            if ship == old_target:
                old_target_num = count
            else:
                count += 1
        target_num = -1
        count = 0
        for ship in self.formations[targfrmtn]['ships']:
            if ship == target:
                target_num = count
            else:
                count += 1
        print('frmtn, old targ, new targ:',self.formations[targfrmtn]['ships'],old_target,target)
        print('time before adjust:',self.ships[firer]['main']['time'])
        if old_target_num == -1:
            # if the new target is not in the same formation then reset the time
            # could also be the case that gun had no previous target
            self.ships[firer]['main']['time'] = 0
        else:
            # both the old target and the new target are in the same formation, correct the time
            tn_adjust = abs(target_num - old_target_num)
            self.ships[firer]['main']['time'] = max(0,self.ships[firer]['main']['time'] - tn_adjust)
        print('time after adjust:',self.ships[firer]['main']['time'])
            
        self.ships[firer]['main']['targ'] = target
        print('mod:update_firer_target:',self.ships[firer])

        self.isdirty = True           # database has changed

        print("exit mod:update_firer_target")
        return('target updated to ' + target)

    def print_formation(self,key,data):
#        print('print_formation ',self.formations[key])
        pass
