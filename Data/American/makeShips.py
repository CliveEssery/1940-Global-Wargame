"""
Contains the models of a MVC type project

Part of the programme to convert Class.CSV to Class.JSON and add
the resultant ships to Ships.JSON which should already exist
as written by Clive Essery copyright 2023
"""
# from .constants import *
import math as math
#from .constants import FieldTypes as FT
import json
import os
import csv
# from . import utilities as util

class FT:
    # FieldTypes
    string = 1
    string_list = 2
    iso_date_string = 3
    long_string = 4
    decimal = 5
    integer = 6
    boolean = 7
    roman_date_string = 8
    int_list = 9

class makeShips_model:

    def __init__(self, extension='.json', path='.', log=False):
        super().__init__()

        print('entered makeShips_model.init ')
        self.log = log
        if self.log:
            print("log value",self.log)
#            self.logging_fh = open ("./Data/logging.txt",mode="w",buffering=-1)

        self.passwords = {}
        self.read_class("class.csv")
        # indicate that the database is not changed
        self.class_CSV_is_dirty = False
        
        success, self.classes = self.get_class_csv("class.csv")
        # indicate that the data has been loaded
#        self.CSV_loaded = success

#        return(self.classes)
    
    def logging(self,msg_to_log="no message"):
        if self.log:
            print(msg_to_log)
#            self.logging_fh(msg_to_log)

    def print_classes(self,message="no message"):
        if self.log:
            print(message)

        # print the class name, num , value
        for num, class_names, class_values in list(self.classes.items()):

            line = class_names + ","
            line += num + ","
            line += class_values
            print(line)

    def get_class_names(self):
        print("enter mod:get_class_names")
        print(self.class_names)
        class_names = []
        for key in list(self.classes.items()):
            class_names.append(key)
        success = True
        print("exit mod:get_class_names")
        return(success, class_names)
        
    def save_json_file (self, filename):
#       save the json file and clear is_dirty
        print("enter mod:save_json_file")
        json_string = '{"csv_converted":' + json.dumps(self.classes)
        print(json_string)

        with open(filename + '.json', 'w') as fh:
            fh.write(json_string)

        self.csv_is_dirty = False
        print("exit mod:save_json_file")
        
    def get_is_dirty(self):
#       check the is_dirty status of the database and return it
        print("enter mod:get_is_dirty")
        print("exit mod:get_is_dirty")
        return(self.is_dirty)

    def read_passwords(self, load_filename="passwords.json"):
#        """Load the settings from the file
#            need to change this to load_battle and split"""
        print("enter mod:read_passwords", load_filename)

        # if the file doesn't exist, return
        print("file ",os.path.isfile("passwords.json"))
        print("exists ",os.path.exists("passwords.json"))
        print("size ",os.path.getsize("passwords.json"))
        if not os.path.exists('passwords.json'):
            print("no file exists in read_passwords")
            return
        print('file exists ', load_filename)

        # open the file and read in the raw values
        with open(load_filename, 'r') as fh:
            raw_values = json.loads(fh.read())

        self.passwords = raw_values['passwords']
        print(self.passwords)
        # don't implicitly trust the raw values, but only get known keys
#        for key in self.formations:
#            if key in raw_values and 'value' in raw_values[key]:
#                raw_value = raw_values[key]['value']
#                self.formations[key]['value'] = raw_value
        print("exit mod:read_passwords")

'''    def get_dbs(self):
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

    def print_formation(self,key,data):
#        print('print_formation ',self.formations[key])
        pass
'''

class CSVModel:
    """CSV file storage"""



    def __init__(self, filename="Class.CSV", filepath=None, fields={}):

        if filepath:
            if not os.path.exists(filepath):
                os.mkdir(filepath)
            self.filename = os.path.join(filepath, filename)
        else:
            self.filename = filename

        self.fields = fields

    def get_all_records(self):
        """Read in all records from the CSV and return a list"""
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, 'r', encoding='utf-8') as fh:
            # turning fh into a list is necessary for our unit tests
            csvreader = csv.DictReader(list(fh.readlines()))
            missing_fields = set(self.fields.keys()) - set(csvreader.fieldnames)
            if len(missing_fields) > 0:
                raise Exception(
                    "File is missing fields: {}"
                    .format(', '.join(missing_fields))
                )
            else:
                records = list(csvreader)

        # Correct issue with boolean fields
        trues = ('true', 'yes', '1')
        bool_fields = [
            key for key, meta
            in self.fields.items()
            if meta['type'] == FT.boolean
        ]
        for record in records:
            for key in bool_fields:
                record[key] = record[key].lower() in trues
        return records

    def get_record(self, rownum):
        """Get a single record by row number

        Callling code should catch IndexError
          in case of a bad rownum.
        """

        return self.get_all_records()[rownum]

    def save_record(self, data, rownum=None):
        """Save a dict of data to the CSV file"""

        if rownum is not None:
            # This is an update
            records = self.get_all_records()
            records[rownum] = data
            with open(self.filename, 'w', encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                csvwriter.writeheader()
                csvwriter.writerows(records)
        else:
            # This is a new record
            newfile = not os.path.exists(self.filename)

            with open(self.filename, 'a', encoding='utf-8') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                if newfile:
                    csvwriter.writeheader()
                csvwriter.writerow(data)

class_csv_fields = {
        "Class": {'req': True, 'type': FT.string},
        "Num": {'req': True, 'type': FT.integer},
        "Prefix": {'req': True, 'type':  FT.string},
        "Spd": {'req': True, 'type': FT.integer},
        "Belt": {'req': True, 'type': FT.decimal},
        "Deck":  {'req': True, 'type': FT.decimal},
        "Len": {'req': True, 'type': FT.decimal,
                     'min': 100, 'max': 1200, 'inc': 1},
        "Flag": {'req': True, 'type': FT.boolean},
        "DC": {'req': True, 'type': FT.integer,
                    'min': 0, 'max': 200, 'inc': 1},
        "Xtra oil": {'req': False, 'type': FT.integer},
        "Xtra ammo": {'req': True, 'type': FT.integer,
                   'min': 0, 'max': 20},
        "AC": {'req': True, 'type': FT.integer,
                   'min': 0, 'max': 200},
        "FP": {'req': True, 'type': FT.integer,
                  'min': 0, 'max': 50},
        "SAC": {'req': True, 'type': FT.integer,
                    'min': 0, 'max': 200, 'inc': 1},
        "LAC": {'req': True, 'type': FT.integer,
                    'min': 0, 'max': 100, 'inc': 1},
        "AS": {'req': True, 'type': FT.decimal,
                    'min': 0, 'max': 100, 'inc': 1},
        "Build": {'req': False, 'type': FT.string,
                  'values': ["Hvy","Stnd","Med","Lgt"]},
        "Weight": {'req': False, 'type': FT.integer},
        "HAC": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 4, 'inc': 1},
        "MCalibre": {'req': False, 'type': FT.string},
        "MFore": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 15, 'inc': 1},
        "MMid": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 15, 'inc': 1},
        "MAft": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 15, 'inc': 1},
        "SCalibre": {'req': False, 'type': FT.string},
        "SFore": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "SMid": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "SAft": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "TCalibre": {'req': False, 'type': FT.string},
        "TFore": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "TMid": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "TAft": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "TTCalibre": {'req': False, 'type': FT.string},
        "TTFore": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "TTMid": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "TTAft": {'req': False, 'type': FT.integer,
                    'min': 0, 'max': 20, 'inc': 1},
        "40": {'req': False, 'type': FT.integer},
        "20": {'req': False, 'type': FT.integer},
        "HalfInch": {'req': False, 'type': FT.integer}
}
    
# call CSVmodel init with file name and csv_ft list
class_csv_mod = CSVModel(filename="AmericanClass.CSV",filepath="",
                         fields=class_csv_fields)

# read the contents and print to the shell
class_list = class_csv_mod.get_all_records()
print(class_list)
# convert to dictionary
# print to json file
