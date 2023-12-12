"""
Contains the Application Process of a MVC project

Part of the WW2 rules project as written and Copyright Clive Essery 2003
with updates to 2020 and the software written from 2020
see header in MODELS for a list of facilities successfully coded.

note, a previous version written in Delphi in 2004 exists
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

from .constants import *
from . import models as mod
from . import views as vie

class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Clives WW2 Rules")
        self.resizable(width=True, height=True)
        self.frame = tk.Frame(height = 20,width = 640)
# ,bg = fm   .pack()
        # new code for chapter6
        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "WW2_Rules_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)
        # self.settings_model = mod.SettingsModel()
        # self.load_settings()

# delete this line if the settings are loaded
        self.settings = {}
        
        self.callbacks = {
            'fleet->select_world':self.on_select_world,
            'fleet->select_nation':self.on_select_nation,
            'fleet->save_nation':self.on_save_nation,
            'fleet->new_fleet':self.on_new_fleet,
            'fleet->complete_new_fleet':self.on_complete_new_fleet,
            'fleet->rename_fleet':self.on_rename_fleet,
            'fleet->complete_rename_fleet':self.on_complete_rename_fleet,
            'fleet->delete_fleet':self.on_delete_fleet,
            'fleet->complete_delete_fleet':self.on_complete_delete_fleet,
#			 can perform join_fleets by swapping formations from the second fleet into the first
#            can perform split_fleets by creating a NEW one and swaping formations into the new fleet
            'fleet->swap_formations':self.on_swap_formations,
            'fleet->complete_swap_formations':self.on_complete_swap_formations,
#            'fleet->execute_movement':self.on_execute_movement,
#            'fleet->engage_enemy':self.on_engage_enemy,
            'formation->new_formation':self.on_new_formation,
            'formation->complete_new_formation':self.on_complete_new_formation,
            'formation->rename_formation':self.on_rename_formation,
            'formation->complete_rename_formation':self.on_complete_rename_formation,
            'formation->delete_formation':self.on_delete_formation,
            'formation->complete_delete_formation':self.on_complete_delete_formation,
#			 can perform join_formations by swapping ships from the second formation into the first
#			 can perform split_formation by creating a new formation, and swapping ships into it
            'formation->swap_ships':self.on_swap_ships,
            'formation->complete_swap_ships':self.on_complete_swap_ships,
            'battle->load_battle': self.on_load_battle,
            'battle->get_moves': self.on_get_move,
            'battle->make_move': self.on_make_move,
            'battle->range_bear': self.on_range_bear,
            'battle->perform_firing': self.on_perform_firing,
            'battle->save_battle': self.on_save_battle,
            'battle->get_move_num': self.on_get_move_num,
            'battle->get_targets': self.on_get_targets,
            'battle->completed_1st_targets': self.completed_1st_targets,
            'battle->on_done_firing': self.on_done_firing,
            'battle->on_print_formation': self.on_print_formation,   # send the key,data to model to update db
            'battle->update_move_b4turn_currspd': self.update_move_b4turn_currspd,
            'battle->get_dbs':self.get_dbs,
            'battle->get_ships':self.get_ships_db,
            'battle->get_ship_targ_info':self.get_targ_info,
            'battle->update_firer_target':self.update_firer_target,
            'battle->display_ships':self.display_ships,
            'battle->return_disp_ship_info':self.return_disp_ship_info,
            'battle->finishtarg':self.finishtarg
        }

        # inititalise start date and time for game
        self.date = (1940,"i",1)
        self.time = (0,0)
        # initialise move number for battles
        self.move_num = 0
        # initialise variables so that they can be tested in case user doesn't select world and nation
        self.world = ""
        self.nation = ""

        # set to False to stop logging entry/exit for routines
        self.log = False        # True

        # used to store the initialised model so that routines can be called
        ########
        # will need to change the path somehow
        ############
        self.model = mod.battle_model(extension='.json',path='./Data/SlowABC/',move=self.move_num,
                                      log=self.log)

        # note a quick user could click on a menu item before the model is initialised if order is reversed
        ############################
        # maybe we want to initialise the world/nation before the model ????
        # but then we want the forms_fields from the model b4 initialising the main menu
        ############################
        self.menu = vie.MainMenu(self,
                                 mod.battle_model.forms_fields,
                                 self.settings,
                                 self.callbacks,
                                 )
        self.config(menu=self.menu)

        self.select_nation = vie.SelectNation(self,
                                        mod.battle_model.forms_fields,
                                        self.callbacks)
        self.select_nation.grid(row=0, column = 0, padx=10, sticky='NSEW')
        
        self.objectsform = vie.objects(self,
                                     mod.battle_model.forms_fields,
                                     self.callbacks)
        self.objectsform.grid(row=0, column = 0, padx=10, sticky='NSEW')

#        self.formationsform = vie.objects(self,
#                                      mod.battle_model.forms_fields,
#                                      self.callbacks)
#        self.formationsform.grid(row=0, column = 0, padx=10, sticky='NSEW')

        # used to store the form that appears in views and connect with that form - GetMoveForm
        self.getmoveform = vie.GetMoveForm(self,
                                         mod.battle_model.forms_fields,
                                         self.callbacks,
                                         self.move_num,)
        self.getmoveform.grid(row=0, column = 0, padx=10, sticky='NSEW')

        # used to store the form that appears in views for getting targets
        self.gettargform = vie.GetTargForm(self,
                                         mod.battle_model.forms_fields,
                                         self.callbacks,
                                         self.move_num,) 
        self.gettargform.grid(row=0, column = 0, padx=10, sticky='NSEW')
        
        # used to store the form that appears in views for getting targets
        self.getdamageform = vie.GetDamageForm(self,
                                         mod.battle_model.forms_fields,
                                         self.callbacks,
                                         self.move_num,) 
        self.getdamageform.grid(row=0, column = 0, padx=10, sticky='NSEW')
        
        self.dispshipform = vie.DispShipForm(self,
                                             mod.battle_model.forms_fields,
                                             self.callbacks,
                                             self.move_num)
        self.dispshipform.grid(row=0, column = 0, padx=10, sticky='NSEW')
        
# end of __init__

    ##########################
    # worlds routines
    ##########################

    def on_select_world(self):
        # get the list of possible worlds from the Model (directories in the Data directory)
        # if there is only one world, then save it and call on_select_nation
        # otherwise, send the world list to VIEWS to display to the User
        # the user will select one and click on it to call on_select_nation
        print('enter app:on_select_world')
        success, worlds_info = self.model.get_json_file(directory = "", subdirectory = "", filename = "worlds")
        print(success, worlds_info)
        self.num_worlds = worlds_info["num_worlds"]
        if self.num_worlds == 1:
            self.world = worlds_info["world_list"][0]
            self.nation = self.on_select_nation(self.world)
        else:
            # send list of possible worlds to VIEW,
            # allow user to select desired world                              
            self.select_nation.select_world(worlds_info["world_list"])
            self.select_nation.tkraise()       # raise the select_nation to the highest level
        print('exit app:on_select_world')

    def on_select_nation(self, world):
        # note, the selected world might already be in self.world if there is only 1 world
        # get the list of possible nations from the Model (directories in the Data directory)
        # send these to VIEWS to display to the User
        # the user will select one and click on nation selected to call on_save_nation
        print('enter app:on_select_nation')
        self.world = world
        success, nations_info = self.model.get_json_file(directory = self.world, subdirectory = "", filename = "world")
        print(success, nations_info)
        self.num_nations = nations_info["num_nations"]
        if self.num_nations == 1:
            self.nation = nations_info["nation_list"][0]
        else:
            # send list of possible nations to VIEW,
            # allow user to select desired nation
            self.select_nation.select_nation_info(world=self.world, nations=nations_info["nation_list"])
            self.select_nation.tkraise()       # raise the select_nation to the highest level

        print('exit app:on_select_nation')

    def on_save_nation(self, selected_nation,plyr_neut):
        # save the selected nation and player-neutral indicator
        # in the application - will be sent to model when needed
        print('enter app:on_save_nation')
        self.nation = selected_nation
        self.plyr_neut = plyr_neut
# will need to get the files for that world/nation combo - can ano routine fleets/formations/ships
        print("selected world = ", self.world, "selected nation = ",self.nation)
        print('exit app:on_save_nation')
        
    ##########################
    # fleets routines
    ##########################

    def on_new_fleet(self):
        # the User selects a fleet at the same location as an existing fleet
        # and assigns a unique name to the new fleet
        print('enter app:on_new_fleet')
        success, fleets_file = self.model.get_json_file(directory = self.world, subdirectory = self.nation, filename = "fleets")
        print(success, fleets_file)
        self.objectsform.object_info(title="New Fleet",
                                     world=self.world,
                                     nation=self.nation,
                                     objects_file=fleets_file,
                                     object = "fleet",
                                     subobject = "formation")
        self.objectsform.tkraise()       # raise the form to the highest level
        self.objectsform.new_object_info()
        print('exit app:on_new_fleet')

    def on_complete_new_fleet(self, selected_fleet, new_fleet_name):
        # callback from VIEWS to create a new fleet at the same location as the specified fleet
        print('enter app:on_complete_fleet')
        print("selected fleet ", selected_fleet)
        print("new fleet name ", new_fleet_name)
        self.model.complete_new_fleet(self.world, self.nation, selected_fleet, new_fleet_name)
        print('exit app:on_complete_fleet')
        
    def on_rename_fleet(self):
        # send the world and nation to VIEWS to display to the User
        # they will be shown (in VIEWS) all fleets in the chosen world/nation
        # the User selects one Fleet and enters a new name
        # will need to send the fleets-file to views too
        # MODEL will change the name of the fleet
        print('enter app:on_rename_fleet')
# already selected world and nation but if null raise error
        if self.world == "" or self.nation == "":
            messagebox.showerror(title="Error", message="No World or Nation Selected Yet")
            return()
        print('app:on_rename_fleet ',self.world, self.nation)
        success, fleets_file = self.model.get_json_file(directory = self.world, subdirectory = self.nation, filename = "fleets")
        print(success, fleets_file)
        self.objectsform.object_info(title="Rename Fleet",
                                     world=self.world,
                                     nation=self.nation,
                                     objects_file=fleets_file,
                                     object = "fleet",
                                     subobject = "formation")
        self.objectsform.tkraise()       # raise the formations form to the highest level
        self.objectsform.rename_object_info()
        print('exit app:on_rename_fleet')
    
    def on_complete_rename_fleet(self, fleet, new_fleet_name):
        # send this info to the model to perform the changes
        print("enter app:on_complete_rename_fleet")
        print("parameters ", fleet, new_fleet_name)
        self.model.complete_rename_fleet(self.world, self.nation, fleet, new_fleet_name)
        print("exit app:on_complete_rename_fleet")

    def on_delete_fleet(self):
        # send the world and nation to VIEWS to display to the User
        # they will be shown (in VIEWS) all fleets in the chosen world/nation
        # the User selects one Fleet for deletion
        # MODEL will check the name of the fleet to ensure it is empty
        # and delete it if it is empty
        print('enter app:on_delete_fleet')
# already selected world and nation but if null raise error
        if self.world == "" or self.nation == "":
            messagebox.showerror(title="Error", message="No World or Nation Selected Yet")
            return()
        print('app:on_delete_fleet ',self.world, self.nation)
        success, fleets_file = self.model.get_json_file(directory = self.world, subdirectory = self.nation, filename = "fleets")
        print(success, fleets_file)
        self.objectsform.object_info(title="Delete Formation",
                                     world=self.world,
                                     nation=self.nation,
                                     objects_file=fleets_file,
                                     object = "fleet",
                                     subobject = "formation")
        self.objectsform.tkraise()       # raise the formations form to the highest level
        self.objectsform.delete_object_info()
        print('exit app:on_delete_fleet')
        
    def on_complete_delete_fleet(self, fleet_name):
        # send this info to the model to perform the changes
        print("enter app:on_complete_delete_fleet")
        print("parameters ", fleet_name)
        self.model.complete_delete_fleet(self.world, self.nation, fleet_name)
        print("exit app:on_complete_delete_fleet")

    def on_swap_formations(self):
        # in Frame1, need to add combo for Fleet1 in col 1, combo for Fleet2 in col 5 on row 0
        # then "load Fleet1" button in col 0 and "Load Fleet2" button in Col 3 and Finish Button in Col 5 on row 1
        # then in Frame2, ^ and v buttons above each other in Col 0 a tree in Col 1, < > in col 2/3, tree in col 4 and ^ v in col 5
        # call views to display frame2 to put up the two fleets and the up/down (on left side and right side) and
        # the left/right buttons to swap between the two fleets.
        print("enter app:on_swap_formations")
        success, fleets_file = self.model.get_json_file(directory = self.world, subdirectory = self.nation, filename = "fleets")
        print(success, fleets_file)
        self.objectsform.swap_subobjects_panel1(objects_file=fleets_file,
                                                object = "fleet",
                                                subobject = "formation")
        self.objectsform.tkraise()       # raise the formations form to the highest level
        self.objectsform.swap_subobjects_panel2("Formations in Fleet1")
        
        print("exit app:on_swap_formations")

    def on_complete_swap_formations(self, fleet1, fleet1_formations, fleet2, fleet2_formations):
        print("enter app:on_complete_swap_formations")
        print('fleet1 ', fleet1, fleet1_formations)
        print('fleet2 ', fleet2, fleet2_formations)
        self.model.complete_swap_formations(self.world, self.nation, fleet1, fleet1_formations, fleet2, fleet2_formations)
        print("exit app:on_complete_swap_formations")
        
    ##########################
    # formation routines
    ##########################
    
    def on_new_formation(self):
        # the User selects a fleet and assigns a unique name to the new formation
        # and indicates if they want to include Neutral ships in the new formation
        # note Player and Neutral ships should not be mixed in one formation
        # if the Player captures a Neutral ship, it will be assigned a Player name.
        print('enter app:on_new_formation')
# already selected world and nation but if null raise error
        if self.world == "" or self.nation == "":
            messagebox.showerror(title="Error", message="No World or Nation Selected Yet")
            return()
        success, formations_file = self.model.get_json_file(directory = self.world,
                                                        subdirectory = self.nation,
                                                        filename = "formations")
        print(success, formations_file)
        self.objectsform.object_info(title="New Formation",
                                     world=self.world,
                                     nation=self.nation,
                                     objects_file=formations_file,
                                     object = "formation",
                                     subobject = "ship")
        self.objectsform.tkraise()       # raise the form to the highest level
        self.objectsform.new_object_info()
        print('exit app:on_new_formation')

    def on_complete_new_formation(self, selected_fleet, new_formation_name):
        # callback from VIEWS to assign the selected ships to the specified new formation
        print('enter app:on_complete_new_formation')
        print("selected fleet ", selected_fleet)
        print("new formation name ", new_formation_name)
        self.model.complete_new_formation(self.world, self.nation, selected_fleet, new_formation_name)
        print('exit app:on_complete_formation')


# proly not needed but keep for now
#    def on_get_unassigned_ships(self, nation, port, name):
#        # callback from VIEWS to get the list of ships that are not assigned
        # in the appropriate Port
        # nation tells model what directory to look in
        # port indicates what port to check for unassigned ships
        # name is the name of the new formation
#        print('enter app:on_get_unassigned_ships')
#        success, unassigned_ships = self.model.get_unassigned_ships(nation, port, name)
#        print('app:on_get_unassigned_ships ',success, unassigned_ships)
        # note success should be one of ok, duplicate, empty
#        if success == "ok":
#            self.buildformationform.setup_buildforminfo(
#                "Select Ships to add to this Formation and click Finish")
#            print('app:after setup_buildforminfo')
#            self.buildformationform.populate_buildform(unassigned_ships)
#            print('app:after populate_buildform')

#        print('exit app:on_get_unassigned ships')


# don't need join formations, can do this with swap_ships
# dont need split formation - select new and then swap ships to new

    def on_rename_formation(self):
        # send the world and nation to VIEWS to display to the User
        # they will be shown (in VIEWS) all fleets in the chosen world/nation
        # the User selects one Fleet and formations within it and enters a new name
        # will need to send the fleets-file to views too
        # MODEL will change the name of the formation and the formation name for each ship in it
        print('enter app:on_rename_formation')
# already selected world and nation but if null raise error
        if self.world == "" or self.nation == "":
            messagebox.showerror(title="Error", message="No World or Nation Selected Yet")
            return()
        print('app:on_rename_formation ',self.world, self.nation)
        success, formations_file = self.model.get_json_file(directory = self.world,
                                                            subdirectory = self.nation,
                                                            filename = "formations")
        print(success, formations_file)
        self.objectsform.object_info(title="Rename Formation",
                                     world=self.world,
                                     nation=self.nation,
                                     objects_file=formations_file,
                                     object = "formation",
                                     subobject = "ship")
        self.objectsform.tkraise()       # raise the formations form to the highest level
        self.objectsform.rename_object_info()
        print('exit app:on_rename_formation')
    
    def on_complete_rename_formation(self, old_formation, new_formation_name):
        # send this info to the model to perform the changes
        print("enter app:on_complete_rename_formation")
        print("parameters ", old_formation, new_formation_name)
        self.model.complete_rename_formation(self.world, self.nation, old_formation, new_formation_name)
        print("exit app:on_complete_rename_formation")

    def on_delete_formation(self):
        # send the world and nation to VIEWS to display to the User
        # they will be shown (in VIEWS) all fleets in the chosen world/nation
        # the User selects one Fleet and one formation within it for deletion
        # MODEL will check the name of the formation to ensure it is empty
        # and delete it if it is empty
        print('enter app:on_delete_formation')
# already selected world and nation but if null raise error
        if self.world == "" or self.nation == "":
            messagebox.showerror(title="Error", message="No World or Nation Selected Yet")
            return()
        print('app:on_delete_formation ',self.world, self.nation)
        success, formations_file = self.model.get_json_file(directory = self.world,
                                                            subdirectory = self.nation,
                                                            filename = "formations")
        print(success, formations_file)
        self.objectsform.object_info(title="Delete Formation",
                                     world=self.world,
                                     nation=self.nation,
                                     objects_file=formations_file,
                                     object = "formation",
                                     subobject = "ship")
        self.objectsform.tkraise()       # raise the formations form to the highest level
        self.objectsform.delete_object_info()
        print('exit app:on_delete_formation')
        
    def on_complete_delete_formation(self, formation_name):
        # send this info to the model to perform the changes
        print("enter app:on_complete_delete_formation")
        print("parameters ", formation_name)
        self.model.complete_delete_formation(self.world, self.nation, formation_name)
        print("exit app:on_complete_delete_formation")

    def on_swap_ships(self):
        # in Frame1, need to add combo for Formation1 in col 1, combo for Formation2 in col 5 on row 0
        # then "load Formation1" button in col 0 and "Load Formation2" button in Col 3 and Finish Button in Col 5 on row 1
        # then in Frame2, ^ and v buttons above each other in Col 0 a tree in Col 1, < > in col 2/3, tree in col 4 and ^ v in col 5
        # call views to display frame2 to put up the two formations and the up/down (on left side and right side) and
        # the left/right buttons to swap between the two formations.
        print("enter app:on_swap_ships")
        success, formations_file = self.model.get_json_file(directory = self.world,
                                                            subdirectory = self.nation,
                                                            filename = "formations")
        print(success, formations_file)
        self.objectsform.swap_subobjects_panel1(objects_file=formations_file,
                                                object = "formation",
                                                subobject = "ship")
        self.objectsform.tkraise()       # raise the objects form to the highest level
        self.objectsform.swap_subobjects_panel2("Ships in Formation1")
        
        print("exit app:on_swap_ships")

    def on_complete_swap_ships(self, formation1, formation1_ships, formation2, formation2_ships):
        print("enter app:on_complete_swap_ships")
        print('formation1 ', formation1, formation1_ships)
        print('formation2 ', formation2, formation2_ships)
        self.model.complete_swap_ships(self.world, self.nation, 
                                            formation1, formation1_ships,
                                            formation2, formation2_ships)
        print("exit app:on_complete_swap_ships")
        
    ##########################
    # BATTLE routines
    ##########################
    
    def on_load_battle(self):
        self.model.get_file_to_load()

    def on_get_move_num(self):
#        print('enter app.get_move_num')
        self.move_num = self.model.get_move_num()
        self.getmoveform.setup_move_num(self.move_num)
        self.gettargform.setup_move_num(self.move_num)
        self.getdamageform.setup_move_num(self.move_num)
        self.dispshipform.setup_move_num(self.move_num)
#        print('exit app.get_move_num')

    def get_formations_db(self):
#        print('enter app.get_formations_db')
        try:
            rows = self.model.get_formations()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            return(rows)
#            self.getmoveform.populate_formations(rows,g,r, column_def=display_column)
#        print('exit app.get_formations_db')

    def get_ships_db(self):
        print('enter app.get_ships_db')
        try:
            rows = self.model.get_ships()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.move_num = rows[0]
            ships = rows[1]
#            print(self.move_num)
#            print(ships)
            self.gettargform.send_ships_db(move_num = self.move_num, ships = ships)

        print('exit app.get_ships_db')

    def get_dbs(self):
        print('enter app.get_dbs')
        try:
            move_num, fleets, formations, ships = self.model.get_dbs()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
#            print(move_num)
#            print(ships)
            print('exit app.get_dbs')
            self.gettargform.receive_dbs(move_num = move_num, fleets= fleets, formations = formations, ships = ships)

    def on_get_move(self):
        """ may need to modify this to get the formations data to pass back to views to get the moves """
#        print("entered app.on_get_move")

#        self.move_num, self.fleets, self.formations, self.ships = self.model.get_dbs()
#        self.getmoveform.receive_dbs(self.move_num, self.fleets, self.formations, self.ships)

        # The data record list for the formations panel
        self.form_info = self.model.get_all_form_info(allied=True, enemy=True)
        # getmoveform is defined in the init routine to store info about the object in views
        self.getmoveform.setup_widgets_for_get_move(self.getmoveform)

        self.getmoveform.populate_formations(
            ancestor = self.getmoveform.forminfoa,
            form_info = self.form_info,
            column_def=0)
        self.getmoveform.update_status_bar(
            'Double Click a Formation to replace its Move')
        
        self.records_saved = 0
        self.on_get_move_num()
        
        self.getmoveform.tkraise()       # raise the getmoveform to the highest level
#        print("exiting app.on_get_move")

    def update_move_b4turn_currspd(self, formation, move, b4turn, currspd):
        print('enter app:update_move_b4turn_currspd')
        self.model.update_move_b4turn_currspd(formation, move, b4turn, currspd)
        print('exit app:update_move_b4turn_currspd')
        
    def on_get_targets(self):
        # called when a record is selected in the get targets part of the code in battle
        # to populate the selection values for a formation
        print('enter app.on_get_targets')
        # The data record list for the formations panel
        # gettargform is defined in the init routine to store info about the object in views
        self.move_num, self.fleets, self.formations, self.ships = self.model.get_dbs()
#        self.gettargform.receive_dbs(self.move_num, self.fleets, self.formations, self.ships)

        # The data record list for the formations panel
        self.form_info = self.model.get_all_form_info(allied=True, enemy=False)
        vie.GetTargForm.setup_move_num(self.gettargform,move_num=self.move_num)

        self.gettargform.setup_widgets_for_get_targets()

        self.gettargform.populate_formations(
            ancestor = self.gettargform.forminfoa,
            form_info = self.form_info,
            column_def=0)
        self.form_info = self.model.get_all_form_info(allied=False, enemy=True)
        self.gettargform.populate_formations(
            ancestor = self.gettargform.forminfob,
            form_info = self.form_info,
            column_def=1)

        self.gettargform.update_status_bar(
            'Double Click a Firer Formation to show Ships in it')
        self.gettargform.tkraise()       # raise the gettargform to the highest level
        print('exit app.on_get_targets')

    def get_targ_info(self, formation):
        print('enter app:get_targ_info')
        result = self.model.get_targ_info(formation)
        return(result)
        print('exit app:get_targ_info')
        
    def finishtarg(self, colour):
        # note colour should be Green or Red
        if colour == 'Green':
            result = 'Complete Red'
            # get data for Red firing at Green
            self.form_info = self.model.get_all_form_info(allied=False, enemy=True)
            self.gettargform.populate_formations(
                ancestor = self.gettargform.forminfoa,
                form_info = self.form_info,
                column_def=0)
            self.form_info = self.model.get_all_form_info(allied=True, enemy=False)
            self.gettargform.populate_formations(
                ancestor = self.gettargform.forminfob,
                form_info = self.form_info,
                column_def=1)

            return(result)
        elif colour == 'Red':
            result = 'Complete Green'
            # note, should have already entered targets for Green, do we want to repeat this?
            return(result)
        else:
            print('Incorrect colour passed to finishtarg-',colour)
            return('Complete ?')

    def on_range_bear(self):
        # called when the user requests the range and bearings to be calculated
#        print('enter app.on_range_bear')
        self.model.get_range_all()
        print('exit app.on_range_bear')

    def completed_1st_targets(self):
        print('enter app.completed_1st_targets')
        self.getmoveform.populate_formations(
            ancestor = self.gettargform.forminfoa,
            rows = self.formations,
            g=False,r=True,
            column_def=0)
        self.getmoveform.populate_formations(
            ancestor = self.gettargform.forminfob,
            rows = self.formations,
            g=True, r=False,
            column_def=1)
        self.getmoveform.update_status_bar(
            'Sides Switched - Double Click a Firer Formation to show Ships in it')
        
        self.records_saved = 0

        self.gettargform.tkraise()       # raise the gettargform to the highest level
#        print('exit app.completed_1st_targets')

    def update_firer_target(self,firer,target,targfrmtn):
        # called to pass the firer/target pairing to the model
        self.model.update_firer_target(firer,target,targfrmtn)
        return('success')

    def on_perform_firing(self):
        # called to perform the firing in the model,
        # for now display the data for one firing to the user
        # and input Straddle and Damage
#        print('enter app.on_perform_firing')
        self.getdamageform.tkraise()       # raise the getdamageform to the highest level
        firing_data = self.model.get_1st_firing_data()
        self.getdamageform.setup_firing_info(firing_data)

#        print('exit app.on_perform_firing')

    def on_done_firing(self, firing_data, straddle, damage):
        # the user has entered straddle and damage
        # call the model to put that into the DB and
        # get the next firing data - call view if not empty
        print('enter app.on_done_firing')
        firing_data = self.model.done_firing(firing_data, straddle, damage)
        # if there are no more ships in range, this will return [""] for views to put up messagebox
        self.getdamageform.setup_firing_info(firing_data)            
        print('exit app.on_done_firing')
    
    def on_print_formation(self,key,data):
        # called to show the current value of one formation for debugging purposes
#        print('enter app.on_print_formation')
        self.model.print_formation(key,data)
#        print('exit app.on_print_formation')

    def on_put_formations(self, formations):
#        print('enter app.on_put_formations')
        self.model.put_formations(formations)
#        print('exit app.on_put_formations')

    def on_make_move(self):
#        print('enter app.on_make_move')
        self.model.move_all()
#        print('exit app.on_make_move')

    def on_save_battle(self):
#        print('enter app.on_save_battle')
        self.model.save_battle()
#        print('exit app.on_save_battle')
        
    def on_range(self):
        """Handles get range button clicks"""
#        print('enter app.on_range')
        self.model.get_range_all()
#        print('exit app.on_range')

    def display_ships(self):
        # handles Battle-Display_Ships clicks
        print('enter app.display_ships')
        self.move_num, self.fleets, self.formations, self.ships = self.model.get_dbs()
        self.dispshipform.receive_dbs(self.move_num, self.fleets, self.formations, self.ships)

# not needed because this is setup in receive_dbs - may be needed later tho
#        vie.DispShipForm.setup_move_num(self.dispshipform)

        self.dispshipform.setup_widgets_for_display_ships(self.dispshipform)
        self.dispshipform.tkraise()       # raise the dispshipform to the highest level
        print('exit app.display_ships')

    def return_disp_ship_info(self,user,password,undamaged_state,
                              damaged_state,sunk_state,allied,enemy):
        print('enter app.return_disp_ship_info')
        print(user,password,undamaged_state,damaged_state,sunk_state,allied,enemy)
        self.dispshipform.setup_dispshipinfo(
            ancestor = self.dispshipform,
            tree_text = "Displayed Ships",
            r=2, c=0)
        self.dispshipform.populate_dispship(
            ancestor = self.dispshipform,
            g=True, r=True,
            column_def=0)

#        self.gettargform.update_status_bar(
#            'Double Click a Firer Formation to show Ships in it')
        self.dispshipform.tkraise()       # raise the dispshipform to the highest level
        print('exit app.return_disp_ship_info')
        
