"""
Contains the models of a MVC type project

Part of the WW2 rules project as written by Clive Essery
Contains routines to 
- move all ships in a battle
- engage in combat - future projects:
- design classes of ships
- build ships from those classes that are required
- put ships into formations
- build a fleet from formations
- build battle from fleets
- start to build ships on slips, completions docks
- repair damaged ships in completion docks or dry docks
- move equipment around world
- move fleets around world
- perform sighting of one fleet to another
"""
from constants import *


class Model():

    def __init__(self, filename='.json', path='.', move=0):
        self.formations = FORMATIONS
        self.ships = SHIPS
        # determine the file paths
        self.formation_filepath = os.path.join(os.path.expanduser(path), 'formations-',str(move), filename)
        self.ships_filepath = os.path.join(os.path.expanduser(path), 'ships-',str(move), filename)
        print("formations file",self.formation_filepath)
        print("ships file",self.ships_filepath)
        self.move = move

        # load in saved values
# comment out for now - we want the version from constants.py
#        self.load_formations('formations')
#        self.load_ships('ships')

# need to save both formations and ships as json files
# need to be able to read them back in again to formations & ships
# need to write get_range_n_bearings - check pascal version

        save_ships (self.move)
        move_all()
        self.move += 1
        save_ships (self.move)

    def move_all(self):
# for all formatations in FORMATIONS move that formation
        for key, value in self.formations:
            move_formation(key)

    def move_formation(self,this_formation):
# for all ships in this_formation move that ship
        for key,value in self.formations[this_formation].ships:
            dist_to_move = self.formations[this_formation].speed/3 
# generate from the speed prob speed/3 maybe more or less
            while dist_to_move > 0:
                dist_to_move = move_ship(dist_to_move,key)

    def move_ship(self,move_dist,this_ship):
# check range to turn point if greater than move distance move at
# current angle else move to turn point, change facing, delete first
# turn point - the move formation routine will call this one again
# note, uses the key from the ships dictionary to ensure the data is 
# written back to the database
        xMult = (0.0,0.707,1.0,0.707,0.0,-0.707,-1,-0.707)
        yMult = (1.0,0.707,0.0,-0.707,-1.0,-0.707,0.0,0.707)
        ship = self.ships["this_ship"]
# turn_point is a tuple containing new direction of travel at the
# turn_point, the x and y position of the turnpoint - note there may
# be several tuples in the list. locn has the same format
        turn_point = ship.turn_point[0]
        rng_to_turn, arc, bearing = get_range_n_bearings(ship.locn(1),ship.locn(2),turn_point(1),turn_point(2))
        if (rng_to_turn > move_dist):
            self.ships[this_ship].locn[1] += move_dist * xMult(ship.locn[0])
            self.ships[this_ship].locn[2] += move_dist * yMult(ship.locn[0])
            return(0)
        else:
            move_dist -= rng_to_turn # may ofc be zero
# turn the ship to the new angle at the turn point and move to turn point
            self.ships[this_ship].locn = turn_point
            self.ships[this_ship].turn_points[0].delete
            return(move_dist)

    def set(self, key, value):
        """Set may need to have one for formations and ships
           variable value"""
        if (
            key in self.variables and
            type(value).__name__ == self.variables[key]['type']
        ):
            self.variables[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

    def save_formations(self, formations=None):
        """Save the current formations data to the file"""
        json_string = json.dumps(self.formations)
        with open(self.formation_filepath, 'w') as fh:
            fh.write(json_string)

    def save_ships(self, ships=None):
        """Save the current ships data to the file"""
        json_string = json.dumps(self.ships)
        with open(self.ships_filepath, 'w') as fh:
            fh.write(json_string)

    def load_formations(self):
        """Load the settings from the file"""

        # if the file doesn't exist, return
        if not os.path.exists(self.formation_filepath):
            return

        # open the file and read in the raw values
        with open(self.formation_filepath, 'r') as fh:
            raw_values = json.loads(fh.read())

        # don't implicitly trust the raw values, but only get known keys
        for key in self.formations:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.formations[key]['value'] = raw_value

    def load_ships(self):
        """Load the settings from the file"""

        # if the file doesn't exist, return
        if not os.path.exists(self.ships_filepath):
            return

        # open the file and read in the raw values
        with open(self.ships_filepath, 'r') as fh:
            raw_values = json.loads(fh.read())

        # don't implicitly trust the raw values, but only get known keys
        for key in self.ships:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.ships[key]['value'] = raw_value
