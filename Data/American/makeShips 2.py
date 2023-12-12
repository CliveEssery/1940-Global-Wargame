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

#        self.read_class("class.csv")
        # indicate that the database is not changed
        self.class_CSV_is_dirty = False
        
#        success, self.classes = self.get_class_csv("AmericanClass.csv")
        # indicate that the data has been loaded

#        return(self.classes)
    
    def logging(self,msg_to_log="no message"):
        if self.log:
            print(msg_to_log)
#            self.logging_fh(msg_to_log)

    def print_classes(self,message="no message"):
        if self.log:
            print(message)

        # print the class name, num , value
        for class_names, num, class_values in list(self.classes.items()):

            line = class_names + ","
            line += num + ","
            line += class_values
            print(line)

    def get_class_names(self):
        print("enter mod:get_class_names")
        class_names = []
        for key in list(self.classes.items()):
            class_names.append(key)
        print(self.class_names)
        success = True
        print("exit mod:get_class_names")
        return(success, class_names)
        
    def save_json_file (self, filename="Class", json_string={}):
#       save the json file and clear is_dirty
        print("enter mod:save_json_file")
#        json_string = '{' + json.dumps(self.classes) + '}'
#        print(json_string)

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
# print(class_list)
print(len(class_list))

# convert to dictionary
json_string = {}
for i in range(len(class_list)):     
#    print(class_list[i])
    class_key = class_list[i]["Class"]
    main = {'Calibre': class_list[i]["MCalibre"],
            'Fore': class_list[i]["MFore"],
            'Mid': class_list[i]["MMid"],
            'Aft': class_list[i]["MAft"]}
    sec = {'Calibre': class_list[i]["SCalibre"],
            'Fore': class_list[i]["SFore"],
            'Mid': class_list[i]["SMid"],
            'Aft': class_list[i]["SAft"]}
    tert = {'Calibre': class_list[i]["TCalibre"],
            'Fore': class_list[i]["TFore"],
            'Mid': class_list[i]["TMid"],
            'Aft': class_list[i]["TAft"]}
    tt = {'Calibre': class_list[i]["TTCalibre"],
            'Fore': class_list[i]["TTFore"],
            'Mid': class_list[i]["TTMid"],
            'Aft': class_list[i]["TTAft"]}
    class_values = {"Num": class_list[i]["Num"],
                    "Prefix": class_list[i]["Prefix"],
                    "Spd": class_list[i]["Spd"],
                    "Belt": class_list[i]["Belt"],
                    "Deck": class_list[i]["Deck"],
                    "Len": class_list[i]["Len"],
                    "Flag": class_list[i]["Flag"],
                    "DC": class_list[i]["DC"],
                    "Xtra Oil": class_list[i]["Xtra oil"],
                    "Xtra Ammo": class_list[i]["Xtra ammo"],
                    "AC": class_list[i]["AC"],
                    "FP": class_list[i]["FP"],
                    "SAC": class_list[i]["SAC"],
                    "LAC": class_list[i]["LAC"],
                    "AS": class_list[i]["AS"],
                    "Build": class_list[i]["Build"],
                    "Weight": class_list[i]["Weight"],
                    "HAC": class_list[i]["HAC"],
                    "main": main,
                    "sec": sec,
                    "tert": tert,
                    "TT": tt,
                    "40": class_list[i]["40"],
                    "20": class_list[i]["20"],
                    "HalfInch": class_list[i]["HalfInch"]}
    json_string[class_key] = class_values
#    print(class_key, class_values)
# save to json file
#print(json_string)
makeShips_mod = makeShips_model(extension='.json', path='', log=False)
strjson_string = str(json_string)
makeShips_mod.save_json_file (filename="Class", json_string=strjson_string)
'''
KISS - MVC
Class and Self
Objects from Class
Each Self is different, objects need to have different names
Python Different from Delphi for example, no list of variables
look at powerpoint done for John Wilson
IDLE

'''
