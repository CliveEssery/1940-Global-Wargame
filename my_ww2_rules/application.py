"""
Contains the Application Process of a MVC project

Part of the WW2 rules project as written and Copyright Clive Essery 2003
with updates to 2020 and the software written in 2020

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
            'formation->build_formation':self.on_build_formation,
            'formation->get_unassigned_ships': self.on_get_unassigned_ships,
            'formation->complete_formation':self.on_complete_formation,
            'formation->join_formations':self.on_join_formations,
            'formation->split_formation':self.on_split_formations,
            'formation->rename_formation':self.on_rename_formations,
            'formation->delete_formation':self.on_delete_formations,
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

        self.move_num = 0

        # set to False to stop logging entry/exit for routines
        self.log = False        # True

        self.menu = vie.MainMenu(self,
                                 mod.battle_model.forms_fields,
                                 self.settings,
                                 self.callbacks,
                                 )
        self.config(menu=self.menu)

        # used to store the initialised model so that routines can be called
        self.model = mod.battle_model(extension='.json',path='./Data/SlowABC/',move=self.move_num,
                                      log=self.log)

        self.buildformationform = vie.BuildFormation(self,
                                      mod.battle_model.forms_fields,
                                      self.callbacks)
        self.buildformationform.grid(row=0, column = 0, padx=10, sticky='NSEW')

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
    # formation routines
    ##########################
    
    def on_build_formation(self):
        print('enter app:on_get_nations')
        nations = self.model.get_nation_directory()
        print('app:on_get_nations ',nations)
        self.buildformationform.buildformation_info(nations)
        self.buildformationform.tkraise()       # raise the build_formation to the highest level

        
    def on_get_unassigned_ships(self, nation, red, port, name):
        print('enter app:on_get_unassigned_ships')
        success, unassigned_ships = self.model.get_unassigned_ships(nation, red, port, name)
        print('app:on_get_unassigned_ships ',success, unassigned_ships)
        # note success should be one of ok, duplicate, empty
        if success == "ok":
            self.buildformationform.setup_buildforminfo(
                "Select Ships to add to this Formation and click Finish")
            print('app:after setup_buildforminfo')
            self.buildformationform.populate_buildform(unassigned_ships)
            print('app:after populate_buildform')

        print('exit app:on_get_unassigned ships')

    def on_complete_formation(self, selections):
        print('enter app:on_complete_formation')
        self.model.complete_formation(selections)
        print('exit app:on_complete_formation')
        
    def on_join_formations(self):
        print('enter app:on_join_formations')

    def on_split_formations(self):
        print('enter app:on_split_formation')

    def on_rename_formations(self):
        print('enter app:on_rename_formation')

    def on_delete_formations(self):
        print('enter app:on_delete_formation')

    ##########################
    # battle routines
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
        
