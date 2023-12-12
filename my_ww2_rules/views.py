"""
Code illustration: 4.01

@ Tkinter GUI Application Development Blueprints
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from .constants import *
from datetime import datetime
from tkinter import filedialog
from . import widgets as wid
from . import utilities as util

###########################################################
#   Start of utility routines called by all the classes   #
###########################################################

class MainMenu(tk.Menu):
    """The Application's main menu"""

    board_color_1 = BOARD_COLOR_1
    board_color_2 = BOARD_COLOR_2

    def __init__(self, parent, fields, settings, callbacks, **kwargs):
        """Constructor for MainMenu

        arguments:
          parent - The parent widget
          fields - field structure for formations db def in model
          settings - a dict containing Tkinter variables
          callbacks - a dict containing Python callables
        """
        super().__init__(parent, **kwargs)

        print('entered views init ')
        self.parent = parent
        self.fields = fields
        self.settings = settings
        self.callbacks = callbacks

        self.isdirty = False
        
        self.create_WW2_Rules_base()

    def create_WW2_Rules_base(self):
        print('entered create ww2 rules base')
        self.create_top_menu()

    def create_top_menu(self):
        print('entered create top menu ')
#        self.menu_bar = tk.Menu(self.parent)
# do we need to pack this?
        self.create_file_menu()
        self.create_edit_menu()
        self.create_worlds_menu()
        self.create_nations_menu()
        self.create_fleets_menu()
        self.create_formations_menu()
        self.create_slips_menu()
        self.create_battle_menu()
        self.create_about_menu()

    def create_file_menu(self):
        print("entered create file menu")
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(label="Open Builds", command=self.on_open_builds_menu_clicked)
        self.file_menu.add_command(label="Open Classes", command=self.on_open_classes_menu_clicked)
        self.file_menu.add_command(label="Save Builds", command=self.on_save_builds_menu_clicked)
        self.file_menu.add_command(label="Save Fleets", command=self.on_save_fleets_menu_clicked)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_exit_menu_clicked)
        self.add_cascade(label="File", menu=self.file_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_edit_menu(self):
        self.edit_menu = tk.Menu(self, tearoff=False)
        self.edit_menu.add_command(
            label="Preferences", command=self.on_preference_menu_clicked)
        self.add_cascade(label="Edit", menu=self.edit_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_worlds_menu(self):
        self.worlds_menu = tk.Menu(self, tearoff=False)
        self.worlds_menu.add_command(label="Select Nation", command=self.callbacks['fleet->select_world'])
#        self.worlds_menu.add_command(label="New World", command=self.on_new_world_menu_clicked)
        self.add_cascade(label="Worlds", menu=self.worlds_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_nations_menu(self):
        self.nations_menu = tk.Menu(self, tearoff=False)
        self.nations_menu.add_command(label="Select Nation", command=self.callbacks['fleet->select_nation'])
#        self.fleets_menu.add_command(label="New Nation", command=self.on_new_nation_menu_clicked)
#        self.fleets_menu.add_command(label="Remove Nation", command=self.on_remove_nation_menu_clicked)
        self.add_cascade(label="Nations", menu=self.nations_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_fleets_menu(self):
        self.fleets_menu = tk.Menu(self, tearoff=False)
        self.fleets_menu.add_command(label="New Fleet", command=self.callbacks['fleet->new_fleet'])
        self.fleets_menu.add_command(label="Rename Fleet", command=self.callbacks['fleet->rename_fleet'])
        self.fleets_menu.add_command(label="Delete Fleet", command=self.callbacks['fleet->delete_fleet'])
        self.fleets_menu.add_command(label="Swap Formations", command=self.callbacks['fleet->swap_formations'])
#        self.fleets_menu.add_command(label="Execute Movement", command=self.callbacks['fleet->execute_movement'])
#        self.fleets_menu.add_command(label="Engage Enemy", command=self.callbacks['fleet->engage_enemy'])
        self.add_cascade(label="Fleets", menu=self.fleets_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_formations_menu(self):
        self.formations_menu = tk.Menu(self, tearoff=False)
        self.formations_menu.add_command(label="New Formation", command=self.callbacks['formation->new_formation'])
#       to join two formations, run the swap_ships option and move all the ships from one formation to the other
#        self.formations_menu.add_command(label="Join Formations", command=self.callbacks['formation->join_formations'])
#		to split a formation, create a new formation and swap ships between them
#        self.formations_menu.add_command(label="Split Formation", command=self.callbacks['formation->split_formation'])
        self.formations_menu.add_command(label="Rename Formation", command=self.callbacks['formation->rename_formation'])
        self.formations_menu.add_command(label="Delete Formation", command=self.callbacks['formation->delete_formation'])
        self.formations_menu.add_command(label="Swap Ships", command=self.callbacks['formation->swap_ships'])
        self.add_cascade(label="Formations", menu=self.formations_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_slips_menu(self):
        self.slips_menu = tk.Menu(self, tearoff=False)
        self.slips_menu.add_command(label="Build Ship", command=self.on_build_ship_menu_clicked)
        self.slips_menu.add_command(label="Convert_Ship", command=self.on_convert_ship_menu_clicked)
        self.slips_menu.add_command(label="Repair Ship", command=self.on_repair_ship_menu_clicked)
        self.slips_menu.add_command(label="Scrap Ship", command=self.on_scrap_ship_menu_clicked)
        self.slips_menu.add_command(label="Build Slip", command=self.on_build_slip_menu_clicked)
        self.slips_menu.add_command(label="Enlarge Slip", command=self.on_enlarge_slip_menu_clicked)
        self.add_cascade(label="Slips", menu=self.slips_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_battle_menu(self):
        self.battle_menu = tk.Menu(self, tearoff=False)
#        print(self.callbacks)
        self.battle_menu.add_command(label="Load Battle", command=self.callbacks['battle->load_battle'])
        self.battle_menu.add_command(label="Get Moves", command=self.callbacks['battle->get_moves'])
        self.battle_menu.add_command(label="Apply Moves", command=self.callbacks['battle->make_move'])
        self.battle_menu.add_command(label="Get Targets", command=self.callbacks['battle->get_targets'])
        self.battle_menu.add_command(label="Range and Bearings", command=self.callbacks['battle->range_bear'])
        self.battle_menu.add_command(label="Perform Firing", command=self.callbacks['battle->perform_firing'])
        self.battle_menu.add_command(label="Save Battle", command=self.callbacks['battle->save_battle'])
        self.battle_menu.add_command(label="Display Ships", command=self.callbacks['battle->display_ships'])
        self.add_cascade(label="Battle", menu=self.battle_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_about_menu(self):
        self.about_menu = tk.Menu(self, tearoff=False)
        self.about_menu.add_command(
            label="About", command=self.on_about_menu_clicked)
        self.add_cascade(label="About", menu=self.about_menu)
#        self.parent.config(menu=self.menu_bar)

# not really needed - used to test that menus are working properly
    def pair2_set(self, label, value, index):
        self.label2["text"] = label
        self.combo2["value"] = value
        self.combo2["state"] = "readonly"
        self.combo2.current(newindex=index)
        
    def pair3_set(self, label, value, index):
        self.label3["text"] = label
        self.combo3["value"] = value
        self.combo3["state"] = "readonly"
        self.combo3.current(newindex=index)

    def on_about_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """Programme to aid playing the game
                               Only the Battle Part is partially working at the moment,
                               though you can build a new formation if needed,
                               other parts will be added as I get the opportunity""")

# Files click commands
    def on_open_builds_menu_clicked(self):
        print(" get ",self.nation_combo.get())        
        self.nation_label["text"] = self.nation_combo.get()
        self.label2["text"] = self.combo2.get()
        self.label3["text"] = self.combo3.get()
        
    def on_open_classes_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_save_builds_menu_clicked(self):
        self.nation_combo.set('Albion')
        self.combo2.set('BatGrp')
        self.combo3.set('BatRon2')
       
    def on_save_fleets_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_exit_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

# Slips menu clicked commands
    def on_build_ship_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_convert_ship_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_repair_ship_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_scrap_ship_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_build_slip_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def on_enlarge_slip_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

# Battle menu clicked commands

    def get_file_to_save(self):
        # get the filename to load and tell the application what the name is
        save_filename = asksaveasfilename(
            title= "Select the filename to Save",
            initialdir = ".Data",
            defaultextension = ".json",
            filetypes = [("Battle Json", '*bat.json *BAT.json')])
        self.callbacks['battle->save_battle'](save_filename)
        
# edit menu clicked commands
    def on_preference_menu_clicked(self):
        messagebox.showinfo("Clive Essery's 1940 Global Campaign",
                            """This Option is not currently working""")
        pass

    def create_canvas(self):
        canvas_width = NUMBER_OF_COLUMNS * DIMENSION_OF_EACH_SQUARE
        canvas_height = NUMBER_OF_ROWS * DIMENSION_OF_EACH_SQUARE
        self.canvas = tk.Canvas(
            self.parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)

    def draw_board(self):
        current_color = BOARD_COLOR_2
        for row in range(NUMBER_OF_ROWS):
            current_color = self.get_alternate_color(current_color)
            for col in range(NUMBER_OF_COLUMNS):
                x1, y1 = self.get_x_y_coordinate(row, col)
                x2, y2 = x1 + DIMENSION_OF_EACH_SQUARE, y1 + DIMENSION_OF_EACH_SQUARE
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,  fill=current_color)
                current_color = self.get_alternate_color(current_color)

    def get_alternate_color(self, current_color):
        if current_color == self.board_color_2:
            next_color = self.board_color_1
        else:
            next_color = self.board_color_2
        return next_color

    def on_square_clicked(self, event):
        clicked_row, clicked_column = self.get_clicked_row_column(event)
        print("Hey you clicked on", clicked_row, clicked_column)

    def get_clicked_row_column(self, event):
        col_size = row_size = DIMENSION_OF_EACH_SQUARE
        clicked_column = event.x // col_size
        clicked_row = 7 - (event.y // row_size)
        return (clicked_row, clicked_column)

    def get_x_y_coordinate(self, row, col):
        x = (col * DIMENSION_OF_EACH_SQUARE)
        y = ((7 - row) * DIMENSION_OF_EACH_SQUARE)
        return (x, y)

# routines to be called from Application:
##################
# WORLD'S routines
##################
class SelectWorld(ttk.Frame):
    # display a combobox to select the world from the available ones
    
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:SelectWorld.init')
        self.callbacks = callbacks
        self.fields = fields

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel - for the input info
        self.panel1 = tk.LabelFrame(
            self,
            text="Select World",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User to Select World')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=2, column = 0, sticky="we", padx=10)

        print('exit vie:SelectWorld.init')
        
    def select_world_info(self, worlds=[]):
        ########################################################################
        # setup the combo box for possible Worlds
        ########################################################################
        print('enter vie:select_world_info')
        self.worlds = worlds
        print('worlds = ', self.worlds)

        # this should be a combo box with the options for the Worlds
        self.world = tk.StringVar(value=self.worlds[0])
        self.inputs['Worlds'] = wid.LabelInput(
            self.panel1, "Worlds",
            input_class = wid.ValidatedCombobox,
            input_var = self.world,
            input_args = {'values':self.worlds, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Worlds'].grid(row=0, column=1)

        # The finish button
        self.world_selected_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.select_world_on_finish)
        self.world_selected_button.grid(sticky="e", row=0, column=3, padx=10)

    def select_world_on_finish(self):
        print("enter vie:select_world_on_finish")
        print('selection ',self.inputs['Worlds'].get())
        self.selected_world = self.inputs['Worlds'].get()

        print('Selected World is:', self.selected_world)
        
        print("exit vie:select_world_on_finish")
        self.callbacks['fleet->save_world'](self.selected_world)

##################
# NATION'S routines
##################
class SelectNation(ttk.Frame):
    # display a combobox to select the Nation and an indicator of whether the Player or the Neutral forces are involved
    
    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:SelectNation.init')
        self.callbacks = callbacks
        self.fields = fields

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel - for the input info
        self.panel1 = tk.LabelFrame(
            self,
            text="Select Nation, and whether Player or Neutral Forces are involved",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User to Select Nation')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=2, column = 0, sticky="we", padx=10)

        print('exit vie:Select_Nation.init')
        
    def select_nation_info(self, world = "", nations=[]):
        ########################################################################
        # setup the combo boxes for Nation and the checkbox for Neutral
        ########################################################################
        print('enter vie:select_nation_info')
        self.nations = nations
        print('nations = ', self.nations)

        # this should be a label with the world entered
        self.world = world

        self.worldinfo = ttk.Label(
            self.panel1,
            text='World Selected = ' + str(self.world),
            width = len(self.world) + 22)
        self.worldinfo.grid(row=0, column=0, sticky='NW')
        
        # this should be a combo box with the options for the Nations
        self.nation = tk.StringVar(value=self.nations[0])
        self.inputs['Nations'] = wid.LabelInput(
            self.panel1, "Nations",
            input_class = wid.ValidatedCombobox,
            input_var = self.nation,
            input_args = {'values':self.nations, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Nations'].grid(row=0, column=1)

        # this should be a checkbutton to indicate that the formation is a neutral one
        self.plyr_neut = tk.BooleanVar(value=False)
        self.inputs['plyr_neut'] = wid.LabelInput(
            self.panel1,
            "Player (Neutral)",
            input_class=ttk.Checkbutton,
            input_var=self.plyr_neut)
        self.inputs['plyr_neut'].grid(row=0,column=2, sticky="w")
        print('vie:select_nation_info.plyr_neut')
        
        # The finish button
        self.nation_selected_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.select_nation_on_finish)
        self.nation_selected_button.grid(sticky="e", row=0, column=3, padx=10)

    def select_nation_on_finish(self):
        print("enter vie:select_nation_on_finish")
        print('selection ',self.inputs['Nations'].get())
        self.selected_nation = self.inputs['Nations'].get()

        print('Selected Nation is:', self.selected_nation)
        
        self.status.config(text="Selected World = " + self.world +"  Selected Nation = " + self.selected_nation)

        print("exit vie:select_nation_on_finish")
        self.callbacks['fleet->save_nation'](self.selected_nation, self.plyr_neut)

###################
# OBJECT'S routines
###################

class objects(ttk.Frame):
    """ Objects routines for the Nation that has already been selected
        could be used for Fleets, Formations or Armies - note, ships and
        brigades need special routines that are separate from this """

    swap_subobjects_column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W, 'width': 35, 'stretch': False},
        'Data': {'label': "replace", 'width': 80, 'stretch': False},
#        'Notes': {'label': 'Notes', 'width': 150, 'stretch': False},
#        'Locn': {'label': 'Locn', 'width': 75, 'stretch': False},
#        'BestSpd': {'label': 'BestSpd', 'width': 50, 'stretch': False},        
#        'currblock': {'label': 'CurrBlk', 'width': 55, 'stretch': False},
#        'blockfill': {'label': 'BlkFill', 'width': 55, 'stretch': False},
#        'blocksize': {'label': 'BlkSize', 'width': 55, 'stretch': False},
#        'tndamage': {'label': 'TNDmg', 'width': 55, 'stretch': False}
    }
    default_width = 12
    default_minwidth = 12
    default_anchor = tk.W

    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:objects.init')
        self.callbacks = callbacks
        self.fields = fields

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel - for the input info
        self.panel1 = tk.LabelFrame(
            self,
            text="",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # setup the second panel for the Tree Display
        self.panel2 = tk.LabelFrame(
            self,
            text="Swap subobjects between the objects, or rearrange them",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User to select object and any other entries')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=2, column = 0, sticky="we", padx=10)

        print('exit vie:objects.init')

    def object_info(self, title="",world="", nation="", objects_file={}, object = "", subobject = ""):
        ########################################################################
        # setup the combo boxes for the Fleets in the chosen Nation
        # note the Fleet may be the one in Port for commissioned but unassigned
        # ships and the entry box for the fleet name which must be unique 
        # for that Nation
        # WARNING: fleets below is the LIST of fleets not the fleets file
        # WARNING: identical code exists in the Formations routines - EDIT BOTH
        ########################################################################
        print('enter vie:formation_info')
        self.objects_file = objects_file
        self.objects = list(objects_file)
        self.object = object
        self.subobject = subobject
        print(self.objects)
        print("world = ", world, '  nation = ', nation, "  objects = ", self.objects)

        # this should be comments to show selected world
        self.worldinfo = ttk.Label(
            self.panel1,
            text='World Selected = ' + str(world),
            width = len(world) + 22)
        self.worldinfo.grid(row=0, column=0, sticky='NW')
        
        # this should be comments to show selected nation
        self.nationinfo = ttk.Label(
            self.panel1,
            text='Nation Selected = ' + str(nation),
            width = len(nation) + 22)
        self.nationinfo.grid(row=0, column=1, sticky='NW')
        
        # this should be a combo box with the list of the existing objects
        self.object_var = tk.StringVar(value=self.objects[0])
        self.inputs[self.object + 's'] = wid.LabelInput(
            self.panel1, self.object + "s",
            input_class = wid.ValidatedCombobox,
            input_var = self.object_var,
            input_args = {'values':self.objects, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs[self.object + 's'].grid(row=1, column=0)

    def new_object_info(self):
        #############################################
        # the extra widgets specific to the new_object
        # version of this window
        #############################################
        print('enter vie:new_' + self.object + '_info')
        self.panel1.text = "Select " + self.object + " to build New " + self.object + " close to, and the Unique New " 
        self.panel1.text += str(object) + " Name"
        # this should be an entry for the New object Name
        self.object_name = tk.StringVar(value="")
        self.inputs[self.object + 'Name'] = wid.LabelInput(
            self.panel1, self.object + " Name",
            field_spec = {'req': True, 'type': wid.FT.string},
            input_var = self.object_name,
            input_args={'width': 20},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs[self.object + 'Name'].grid(row=1, column=1)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_new_object)
        self.finish_button.grid(sticky="e", row=2, column=1, padx=10)

        text_value = "Select the " + self.object + " the New one is with and  "
        text_value += "Enter New Unique " + self.object + " Name "
        text_value += "then click 'Finish' button"
        self.status.config(text= text_value)
        print(self.object, self.object_name, self.objects)
        print('exit vie:new_' + self.object + '_info')
        return()

    def finish_new_object(self):
        ##########################################################
        # the object has been selected and new object name entered
        # pass the information back to the application for storage
        # WARNING: identical code exists in the Formations routines - EDIT BOTH
        ##########################################################
        print('enter vie:finish_new_' + self.object)
        self.selected_object = self.inputs[self.object + 's'].get()

        print('Selected ' + self.object + 'is:', self.selected_object)
        self.new_object_name = str(self.inputs[self.object + "Name"].get())
        self.status.config(text="Selected " + self.object + " = " + self.selected_object + "  New " + self.object + " = " +
                           self.new_object_name)

        print(self.selected_object, self.new_object_name, self.objects_file)
        
        self.clean_up_after_finishing(self.panel1)		# tidy up the display after finishing the command
        print('exit vie:finish_new_' + self.object)

        if self.object == "fleet":
            self.callbacks['fleet->complete_new_fleet'](self.selected_object, self.new_object_name)
        elif self.object == "formation":
            self.callbacks['formation->complete_new_formation'](self.selected_object, self.new_object_name)
#        elif self.object == "army":
#            self.callbacks['army->complete_new_army'](self.selected_object, self.new_object_name)
            

    def rename_object_info(self):
        #################################################
        # the extra widgets specific to the rename_fleet
        # version of this window
        # WARNING: identical code exists in the Formations routines - EDIT BOTH
        #################################################
        print('enter vie:rename_' + self.object + '_info')

        self.panel1.text = "Select old " + self.object + " that is to be Renamed, and Unique " + self.object + " Name"
        # this should be an entry for the New Object Name
        self.object_name = tk.StringVar(value="")
        self.inputs[self.object + 'Name'] = wid.LabelInput(
            self.panel1, self.object + " Name",
            field_spec = {'req': True, 'type': wid.FT.string},
            input_var = self.object_name,
            input_args={'width': 20},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs[self.object + 'Name'].grid(row=1, column=1)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_rename_object)
        self.finish_button.grid(sticky="e", row=2, column=1, padx=10)

        text_val = "Select Fleet to be renamed. "
        text_val += "Enter New Unique Fleet Name "
        text_val += "then click 'Finish' button"
        self.status.config(text= text_val)
        print('exit vie:rename_' + self.object + '_info')
        print('exit vie:rename_' + 'object' + '_info')
        return()

    def finish_rename_object(self):
        ####################################################
        # the object has been selected and new object name entered
        # pass the information back to the application for storage
        ####################################################
        print('enter vie:finish_rename_' + self.object)
        self.selected_object = self.inputs[self.object + 's'].get()

        print('Selected ' + self.object + 'is:', self.selected_object)
        self.new_object_name = str(self.inputs[self.object + "Name"].get())
        self.status.config(text="Selected " + self.object + " = " + self.selected_object +
                           " New " + self.object + " = " + self.new_object_name)

        print(self.selected_object, self.new_object_name, self.objects_file)    

        self.clean_up_after_finishing(self.panel1)		# tidy up the display after finishing the command
        print('exit vie:finish_rename_' + self.object)

        if self.object == 'fleet':
            self.callbacks['fleet->complete_rename_fleet'](self.selected_object, self.new_object_name)
        elif self.object == 'formation':
            self.callbacks['formation->complete_rename_formation'](self.selected_object, self.new_object_name)
#        elif self.object == 'army':
#            self.callbacks['army->complete_rename_army'](self.selected_object, self.new_object_name)
        else:
            print('Error in finish_rename_object - object is incorrect', self.object)

    def delete_object_info(self):
        #################################################
        # the extra widgets specific to the delete_object
        # version of this window
        # WARNING: identical code exists in the Formations routines - EDIT BOTH
        #################################################
        print('enter vie:delete_' + self.object + '_info')

        self.panel1.text = "Select " + self.object + " to be Deleted, and click Finish button"

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_delete_object)
        self.finish_button.grid(sticky="e", row=2, column=1, padx=10)

        text_val = "Select the Fleet "
        text_val += "Name that is to be deleted "
        text_val += "then click 'Finish' button"
        self.status.config(text= text_val)
        print('exit vie:delete_' + self.object + '_info')
        return()

    def load_delete_fleet(self):
#		get the selected fleet, setup the fleets combobox from the selected fleet
        print('enter vie:load_delete_' + self.object)
        selected_object = self.inputs[self.object + 's'].get()
        print('Selected ' + self.object + ' is:', selected_object)
        print(self.object + 's', self.objects_file[selected_object])

        print('exit vie:load_delete_' + self.object + 's')
        return()
        
    def finish_delete_object(self):
        ####################################################
        # the object to be deleted has been selected 
        # pass the information back to the application for storage
        ####################################################
        print('enter vie:finish_delete_' + self.object)

        self.object_name_to_delete = str(self.inputs[self.object + "s"].get())
        print(self.object + ' Name to delete ', self.object_name_to_delete)
        self.status.config(text=self.object + " name to delete = " + self.object_name_to_delete)

        print(self.object_name_to_delete, self.objects_file)

        self.clean_up_after_finishing(self.panel1)		# tidy up the display after finishing the command
        print('exit vie:finish_delete_' + self.object)

        if self.object == 'fleet':
            self.callbacks['fleet->complete_delete_fleet'](self.object_name_to_delete)
        elif self.object == 'formation':
            self.callbacks['formation->complete_delete_formation'](self.object_name_to_delete)
#        elif self.object == 'army':
#            self.callbacks['army->complete_delete_army'](self.object_name_to_delete)
        else:
            print('Error in finish_delete_object - object is incorrect', self.object)
            

    def swap_subobjects_panel1(self, objects_file, object = "", subobject = ""):
        ###################################################################
        # in Frame1, need to add combo for object1 in col 1, combo for object2 in col 5 on row 0
        # then "load object1" button in col 0 and "Load object2" button in Col 3 and Finish Button in Col 5 on row 1
        # WARNING: identical code exists in the Formations routines - EDIT BOTH
        ###################################################################
        
        # this should be an entry for the first object Name
        self.objects_file = objects_file
        self.objects = list(objects_file)
        self.object = object
        self.subobject = subobject
        print("enter vie:swap_" + self.subobject + "s_panel1")
        self.panel1.text = "Select the " + self.object + "s to swap " + self.subobject + "s between"
        print(self.objects)
        self.object_name1 = tk.StringVar(value=self.objects[0])
        self.inputs[self.object + '1'] = wid.LabelInput(
            self.panel1, self.object + "1",
            input_class = wid.ValidatedCombobox,
            input_var = self.object_name1,
            input_args = {'values':self.objects, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs[self.object + '1'].grid(row=0, column=1)

        # this should be an entry for the second object Name
        self.object_name2 = tk.StringVar(value=self.objects[1])
        self.inputs[self.object + '2'] = wid.LabelInput(
            self.panel1, self.object + "2",
            input_class = wid.ValidatedCombobox,
            input_var = self.object_name2,
            input_args = {'values':self.objects, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs[self.object + '2'].grid(row=0, column=5)
            
        # The Load object1 button
        self.load_object1_button = ttk.Button(
            self.panel1,
            text = "Load " + self.object + "1",
            command = self.load_object1)
        self.load_object1_button.grid(sticky="e", row=1, column=0, padx=10)

        # The Load object2 button
        self.load_object2_button = ttk.Button(
            self.panel1,
            text = "Load " + self.object + "2",
            command = self.load_object2)
        self.load_object2_button.grid(sticky="e", row=1, column=3, padx=10)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_swap_subobjects)
        self.finish_button.grid(sticky="e", row=1, column=5, padx=10)

        self.status.config(text="Select " + self.object + "1, click the 'Load " + self.object + "1'" +
                                " button, " +
                                "If desired select " + self.object + "2 and click the Load " + self.object + "2 button " +
                                "then click 'Finish' button when all changes complete")
        print("exit vie:swap_" + self.subobject + "s_panel1")
        return()

    def load_object1(self):
        print('enter vie:load_' + self.object + '1')
        self.object1 = self.inputs[self.object + '1'].get()
        print(self.object + '1 ', self.object1, type(self.object1))
        print(self.object + 's file ',self.objects_file, type(self.objects_file))
        print(self.subobject, self.subobject + 's')
        print(self.objects_file[self.object1])
        print(self.subobject + 's', self.objects_file[self.object1][self.subobject + 's'])
        self.object1_subobjects = self.objects_file[self.object1][self.subobject + 's']
        print(self.object + '1 ' + self.subobject + 's ',self.object1_subobjects)
        # load the treeview in Frame2 (2_1)
        self.populate_swap_subobjects_panel2_1(self.object1_subobjects)
        print('exit vie:load_' + self.object + '1')
        
    def load_object2(self):
        print('enter vie:load_' + self.object + '2')
        self.object2 = self.inputs[self.object + '2'].get()
        print(self.object + '2 ', self.object2, type(self.object2))
        self.object2_subobjects = self.objects_file[self.object2][self.subobject + 's']
        print(self.object + '2 ' + self.subobject + 's ',self.object2_subobjects)
        # load the treeview in Frame2 (2_3)
        self.populate_swap_subobjects_panel2_3(self.object2_subobjects)
        
        print('exit vie:load_' + self.object + '2')
        
    def finish_swap_subobjects(self):
        print('enter vie:finish_swap_' + self.subobject + 's')
        
        self.clean_up_after_finishing(self.panel1)		# tidy up the display after finishing the command
        self.clean_up_after_finishing(self.panel2)		# tidy up the display after finishing the command
    
        print('exit vie:finish_swap_' + self.subobject + 's')
        if self.object == 'fleet':
            self.callbacks['fleet->complete_swap_formations'](self.object1, self.swap_subobjects_panel2_1.subobject_list,
                                                              self.object2, self.swap_subobjects_panel2_3.subobject_list)
        elif self.object == 'formation':
            self.callbacks['formation->complete_swap_ships'](self.object1, self.swap_subobjects_panel2_1.subobject_list,
                                                             self.object2, self.swap_subobjects_panel2_3.subobject_list)
#        elif self.object == 'army':
#            self.callbacks['army->complete_swap_brigades'](self.object1, self.swap_subobjects_panel2_1.subobject_list,
#                                                           self.object2, self.swap_subobjects_panel2_3.subobject_list)
        else:
            print('Error - invalid object-' + self.object + ' supplied to swap subobjects')
        

    def swap_subobjects_panel2(self, tree_text):
        # display frame2 to put up the two objects and the up/down (on left side and right side) and
        # the left/right buttons to swap between the two objects.
        # buildforminfo section - sets up the display for the tree info for the subobjects
        # ancestor is the label/labelframe in which this section will be displayed
        # not sure a command is needed in this case, a button terminates the selection process
        # BIG NOTE - to setup the correct command for the binding on the list, you need to set a variable:
        # self.object_command to be the self... function that handles the command before calling this routine
        # eg self.dispship_command = self.dispship_on_open_record

        print('enter vie:swap_' + self.subobject + 's_panel2')

        self.frame2_0 = tk.LabelFrame(
            self.panel2,
            text="",
            width=20,
            padx=0,
            pady=0)
        # note we are going to put the "^" button on Row 1 and the "v" button on row 2
        # these weights force them to be in the middle of the frame vertically
        self.frame2_0.rowconfigure(0, weight=49)
        self.frame2_0.rowconfigure(1, weight=1)
        self.frame2_0.rowconfigure(2, weight=1)
        self.frame2_0.rowconfigure(3, weight=49)
        self.frame2_0.grid(sticky="nsew", row=0, column=0)
        
        # The Left Up button
        self.left_up_button = ttk.Button(
            self.frame2_0,
            text = "^",
            width = 2,
            command = self.left_up_clicked)
        self.left_up_button.grid(sticky="nsew", row=1, column=0)

        # The Left Down button
        self.left_down_button = ttk.Button(
            self.frame2_0,
            text = "v",
            width = 2,
            command = self.left_down_clicked)
        self.left_down_button.grid(sticky="nsew", row=2, column=0)
       
        self.frame2_1 = tk.LabelFrame(
            self.panel2,
            text=tree_text,
            width=155,
            padx=10,
            pady=10)
        self.swap_subobjects_panel2_1 = ttk.Treeview(
            self.frame2_1,
            columns=list(self.swap_subobjects_column_defs.keys())[1:],
            selectmode='extended'                        # user can select multiple items
        )

        # configure scrollbar for the treeview
        self.scrollbar1 = ttk.Scrollbar(
            self.frame2_1,
            orient=tk.VERTICAL,
            command=self.swap_subobjects_panel2_1.yview
        )
        self.swap_subobjects_panel2_1.configure(yscrollcommand=self.scrollbar1.set)
        self.swap_subobjects_panel2_1.grid(row=0, column=1, sticky='W')
        self.scrollbar1.grid(row=0, column=2, sticky='NSW')
        self.frame2_1.grid(row=0, column=1, stick='W')

        # Configure treeview columns
        for name, definition in self.swap_subobjects_column_defs.items():
            label = self.subobject + 's'    # definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            print("name ", name)
            self.swap_subobjects_panel2_1.heading(name, text=label, anchor=anchor)
            self.swap_subobjects_panel2_1.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        self.swap_subobjects_panel2_1.selected_subobjects = []              # used in record_selection1 to store selected formations
        self.swap_subobjects_panel2_1.bind('<<TreeviewSelect>>', self.record_selection1)

        self.frame2_2 = tk.LabelFrame(
            self.panel2,
            text="",
            width=60,
            padx=0,
            pady=0)
        # these weights allow the Left/Right buttons to be placed in the middle vertically
        self.frame2_2.rowconfigure(0, weight=50)
        self.frame2_2.rowconfigure(1, weight=1)
        self.frame2_2.rowconfigure(2, weight=50)
        self.frame2_2.grid(sticky="nsew", row=0, column=2)
        
        # The Left button
        self.left_button = ttk.Button(
            self.frame2_2,
            text = "<",
            width = 2,
            command = self.left_clicked)
        self.left_button.grid(sticky="nsew", row=1, column=0)

        # The right button
        self.right_button = ttk.Button(
            self.frame2_2,
            text = ">",
            width = 2,
            command = self.right_clicked)
        self.right_button.grid(sticky="nsew", row=1, column=1)

        self.frame2_3 = tk.LabelFrame(
            self.panel2,
            text = self.subobject + "s for " + self.object + " 2",
            width=155,
            padx=10,
            pady=10)
        self.swap_subobjects_panel2_3 = ttk.Treeview(
            self.frame2_3,
            columns=list(self.swap_subobjects_column_defs.keys())[1:],
            selectmode='extended'                        # user can select multiple items
        )

        # configure scrollbar for the treeview
        self.scrollbar2 = ttk.Scrollbar(
            self.frame2_3,
            orient=tk.VERTICAL,
            command=self.swap_subobjects_panel2_3.yview
        )
        self.swap_subobjects_panel2_3.configure(yscrollcommand=self.scrollbar2.set)
        self.swap_subobjects_panel2_3.grid(row=0, column=1, sticky='W')
        self.scrollbar2.grid(row=0, column=2, sticky='NSW')
        self.frame2_3.grid(row=0, column=3, stick='W')

        # Configure treeview columns
        for name, definition in self.swap_subobjects_column_defs.items():
            label = self.subobject + 's'    # definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.swap_subobjects_panel2_3.heading(name, text=label, anchor=anchor)
            self.swap_subobjects_panel2_3.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        self.swap_subobjects_panel2_3.selected_subobjects = []      # used in record_selection2 to store selected subobjects
        self.swap_subobjects_panel2_3.bind('<<TreeviewSelect>>', self.record_selection2)

        self.frame2_4 = tk.LabelFrame(
            self.panel2,
            text="",
            width=20,
            padx=0,
            pady=0)
        # note we are going to put the "^" button on Row 1 and the "v" button on row 2
        # these weights force them to be in the middle of the frame vertically
        self.frame2_4.rowconfigure(0, weight=49)
        self.frame2_4.rowconfigure(1, weight=1)
        self.frame2_4.rowconfigure(2, weight=1)
        self.frame2_4.rowconfigure(3, weight=49)
        self.frame2_4.grid(sticky="nsew", row=0, column=4)
        
        # The right Up button
        self.right_up_button = ttk.Button(
            self.frame2_4,
            text = "^",
            width = 2,
            command = self.right_up_clicked)
        self.right_up_button.grid(sticky="nsew", row=1, column=0)

        # The right Down button
        self.right_down_button = ttk.Button(
            self.frame2_4,
            text = "v",
            width = 2,
            command = self.right_down_clicked)
        self.right_down_button.grid(sticky="nsew", row=2, column=0)
       
        print('exit vie:swap_' + self.subobject + 's_panel2')
        
    def setup_selections(self, panel):
        # setup the selections list for the relevant panel
        print('enter vie:setup selections')
        selections = list(panel.selection())
        print('selections ', selections, ' type selections ', type(selections))
        # ensure that the selected_subobjects list is empty before reloading it
        panel.selected_subobjects.clear()
        while len(selections) > 0:
            selected_id = int(selections[0])
            next_selection = list(panel.subobject_list)[selected_id]
            panel.selected_subobjects.append(next_selection)
            del selections[0]
        print('selected_' + self.subobject + 's at end ',panel.selected_subobjects)
        print('exit vie:setup selections')

    def left_up_clicked(self):
        # for each subobject in object1 selected list
        # move it up one spot
        # re-populate object1
        print('enter vie:left_up_clicked')
        self.setup_selections(self.swap_subobjects_panel2_1)
        print(self.subobject + 's list ', self.swap_subobjects_panel2_1.subobject_list)
        self.up_clicked(self.swap_subobjects_panel2_1)
        # repopulate list from the new order
        self.populate_swap_subobjects_panel2_1(self.swap_subobjects_panel2_1.subobject_list)
        print(self.subobject + 's list at end ', self.swap_subobjects_panel2_1.subobject_list)
        print('exit vie:left_up_clicked')
        
    def up_clicked(self, panel):
        for subobject in panel.selected_subobjects:
            index = panel.subobject_list.index(subobject)
            # note, can't move the first item up one level
            if index > 0:
                item = panel.subobject_list.pop(index)        # remove item from list but store it
                panel.subobject_list.insert(index - 1, item)  # replace item into list one level higher
        
    def left_down_clicked(self):
        # for each subobject in object1 selected list
        # move it down one spot
        # re-populate object1
        print('enter vie:left_down_clicked')
        self.setup_selections(self.swap_subobjects_panel2_1)
        print(self.subobject + 's list ', self.swap_subobjects_panel2_1.subobject_list)
        self.down_clicked(self.swap_subobjects_panel2_1)
        # repopulate list from the new order
        self.populate_swap_subobjects_panel2_1(self.swap_subobjects_panel2_1.subobject_list)
        print(self.subobject + 's list at end ', self.swap_subobjects_panel2_1.subobject_list)
        print('exit vie:left_down_clicked')
        
    def down_clicked(self, panel):
        # for each subobject in object1 selected list
        # move it down one spot
        print('enter vie:left_down_clicked')
        self.setup_selections(panel)
        print(self.subobject + 's list ', panel.subobject_list)
        for subobject in panel.selected_subobjects:
            index = panel.subobject_list.index(subobject)
            # note, can't move the last item down one level
            if index < len(panel.subobject_list):
                item = panel.subobject_list.pop(index)			# remove item from list
                panel.subobject_list.insert(index + 1, item)	# and add it back in one level lower
        print(self.subobject + 's list at end ', panel.subobject_list)
        print('exit vie:left_down_clicked')
        
    def record_selection1(self, *args):
        # save the list of selectors that have been clicked
        print('enter vie:record_selection1')
        print('selections ',self.swap_subobjects_panel2_1.selection())
        print('vie:record_selector ',self.swap_subobjects_panel2_1.selected_subobjects)
        print('exit vie:record_selection1')

    def populate_swap_subobjects_panel2_1(self,subobject_list1):
        # load the subobject data into the first treelist in panel2_1
        print('enter vie:populate_swap_subobjects_panel2_1')

        self.swap_subobjects_panel2_1.subobject_list = subobject_list1

        for row in self.swap_subobjects_panel2_1.get_children():
            self.swap_subobjects_panel2_1.delete(row)

        rownum = 0
        print(self.subobject + 's ',self.swap_subobjects_panel2_1.subobject_list)
        for subobject in self.swap_subobjects_panel2_1.subobject_list:
            self.form_label = subobject
            values = (subobject)
            self.swap_subobjects_panel2_1.insert('', 'end', iid=str(rownum),
                                     text=str(rownum), values=values)
            rownum += 1
        print('swap_subobjects_panel2_1 selected subobjects',self.swap_subobjects_panel2_1.selected_subobjects)

        print('exit vie:populate_swap_subobjects_panel2_1')

    def left_clicked(self):
        # append subobjects selected in object1 treeview to object2
        # for each subobject in object1 selected list delete from object1
        # re-populate object1
        # re-populate object2
        print('enter vie:left_clicked')
        print(self.subobject + ' list at beginning ',self.swap_subobjects_panel2_3.subobject_list)
        self.setup_selections(self.swap_subobjects_panel2_3)
        print('vie:left clicked-selected ' + self.subobject + 's ',self.swap_subobjects_panel2_3.selected_subobjects)
        print(self.subobject + ' list at beginning ',self.swap_subobjects_panel2_1.subobject_list)
        self.swap_subobjects_panel2_1.subobject_list += self.swap_subobjects_panel2_3.selected_subobjects
        for subobject in self.swap_subobjects_panel2_3.selected_subobjects:
            index = self.swap_subobjects_panel2_3.subobject_list.index(subobject)
            del self.swap_subobjects_panel2_3.subobject_list[index]
        self.populate_swap_subobjects_panel2_1(self.swap_subobjects_panel2_1.subobject_list)
        self.populate_swap_subobjects_panel2_3(self.swap_subobjects_panel2_3.subobject_list)
        print(self.subobject + ' list 2_1 at end ',self.swap_subobjects_panel2_1.subobject_list)
        print(self.subobject + ' list 2_3 at end ',self.swap_subobjects_panel2_3.subobject_list)
        print('exit vie:left_clicked')
        
    def right_clicked(self):
        # append subobjects selected in object2 treeview to object1
        # for each subobject in object2 selected list delete from object2
        # re-populate object1
        # re-populate object2
        print('enter vie:right_clicked')
        print(self.subobject + ' list at beginning ',self.swap_subobjects_panel2_3.subobject_list)
        self.setup_selections(self.swap_subobjects_panel2_1)
        print('selected list at beginning ',self.swap_subobjects_panel2_1.selected_subobjects)
        self.swap_subobjects_panel2_3.subobject_list += self.swap_subobjects_panel2_1.selected_subobjects
        for subobject in self.swap_subobjects_panel2_1.selected_subobjects:
            index = self.swap_subobjects_panel2_1.subobject_list.index(subobject)
            del self.swap_subobjects_panel2_1.subobject_list[index]
        self.populate_swap_subobjects_panel2_1(self.swap_subobjects_panel2_1.subobject_list)
        self.populate_swap_subobjects_panel2_3(self.swap_subobjects_panel2_3.subobject_list)
        print(self.subobject + ' list 2_1 at end ',self.swap_subobjects_panel2_1.subobject_list)
        print(self.subobject + ' list 2_3 at end ',self.swap_subobjects_panel2_3.subobject_list)
        print('exit vie:right_clicked')
        
    def record_selection2(self, *args):
        # save the list of selectors that have been clicked
        print('enter vie:record_selection2')
        print('selections ',self.swap_subobjects_panel2_3.selection())
        # seems to be called sometimes when the selection is empty - defensive coding
        print('exit vie:record_selection2')

    def populate_swap_subobjects_panel2_3(self,subobject_list2):
        # load the subobject data into the second treelist in panel2_3
        print('enter vie:populate_swap_' + self.subobject + 's_panel2_3')
        self.swap_subobjects_panel2_3.subobject_list = subobject_list2

        for row in self.swap_subobjects_panel2_3.get_children():
            self.swap_subobjects_panel2_3.delete(row)

        rownum = 0
        print(self.subobject + 's ',self.swap_subobjects_panel2_3.subobject_list)
        for subobject in self.swap_subobjects_panel2_3.subobject_list:
            self.form_label = subobject
            values = (subobject)
            self.swap_subobjects_panel2_3.insert('', 'end', iid=str(rownum),
                                     text=str(rownum), values=values)
            rownum += 1
        print('swap_' + self.subobject + 's_panel2_3 selected ' + self.subobject + 's ',
              self.swap_subobjects_panel2_3.selected_subobjects)

        print('exit vie:populate_swap_' + self.subobject + 's_panel2_3')

    def right_up_clicked(self):
        print('enter vie:right_up_clicked')
        self.setup_selections(self.swap_subobjects_panel2_3)
        print(self.subobject + 's list ', self.swap_subobjects_panel2_3.subobject_list)
        self.up_clicked(self.swap_subobjects_panel2_3)
        self.populate_swap_subobjects_panel2_3(self.swap_subobjects_panel2_3.subobject_list)
        print(self.subobject + 's list at end ', self.swap_subobjects_panel2_3.subobject_list)
        print('exit vie:right_up_clicked')
        
    def right_down_clicked(self):
        print('enter vie:right_down_clicked')
        self.setup_selections(self.swap_subobjects_panel2_3)
        print(self.subobject + 's list ', self.swap_subobjects_panel2_3.subobject_list)
        self.down_clicked(self.swap_subobjects_panel2_3)
        self.populate_swap_subobjects_panel2_3(self.swap_subobjects_panel2_3.subobject_list)
        print(self.subobject + 's list at end ', self.swap_subobjects_panel2_3.subobject_list)
        print('exit vie:right_down_clicked')
        
    def clean_up_after_finishing(self, panel):
        # clear the panel (variable passed, either self.Panel1 or 2),
        # its title and status bar
#        print('widget list b4 ', self.inputs)
        for widget in panel.winfo_children():
            widget.destroy()
        for key, value in list(self.inputs.items()):
            del self.inputs[key]
#        print('widget list after ', self.inputs)
        self.panel1.text = ""
        self.status.config(text="Select the Next Action you wish to Perform" +
                                " from the Menus")

######################
# FORMATION'S routines
######################
'''
class Formations(ttk.Frame):
    """ Build a new Formation for the Nation that has already been selected """

    swap_ships_column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W, 'width': 35, 'stretch': False},
        'Ship': {'label': 'Ship', 'width': 80, 'stretch': False},
        'Notes': {'label': 'Notes', 'width': 150, 'stretch': False},
#        'Locn': {'label': 'Locn', 'width': 75, 'stretch': False},
#        'BestSpd': {'label': 'BestSpd', 'width': 50, 'stretch': False},        
#        'currblock': {'label': 'CurrBlk', 'width': 55, 'stretch': False},
#        'blockfill': {'label': 'BlkFill', 'width': 55, 'stretch': False},
#        'blocksize': {'label': 'BlkSize', 'width': 55, 'stretch': False},
#        'tndamage': {'label': 'TNDmg', 'width': 55, 'stretch': False}
    }
    default_width = 12
    default_minwidth = 12
    default_anchor = tk.W

    def __init__(self, parent, fields, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:Formations.init')
        self.callbacks = callbacks
        self.fields = fields

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel - for the input info
        self.panel1 = tk.LabelFrame(
            self,
            text="",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # setup the second panel for the Tree Display
        self.panel2 = tk.LabelFrame(
            self,
            text="Swap Ships between the Formations, or rearrange them",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User to select Fleet and and any other entries')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=2, column = 0, sticky="we", padx=10)

        print('exit vie:NewFormation.init')

    def formation_info(self, title="",world="", nation="", fleets_file={}):
        ########################################################################
        # setup the combo boxes for the Fleets in the chosen Nation
        # note the Fleet may be the one in Port for commissioned but unassigned
        # ships and the entry box for the new formation name which must be unique 
        # for that Nation
        # WARNING: fleets is the LIST of fleets not the fleets file
        # WARNING: identical code exists in the Fleets routines - EDIT BOTH
        ########################################################################
        print('enter vie:formation_info')
        self.fleets_file = fleets_file
        self.fleets = list(fleets_file)
        print(self.fleets)
        print("world = ", world, '  nation = ', nation, "  fleets = ", self.fleets)

        # this should be comments to show selected world
        self.worldinfo = ttk.Label(
            self.panel1,
            text='World Selected = ' + str(world),
            width = len(world) + 22)
        self.worldinfo.grid(row=0, column=0, sticky='NW')
        
        # this should be comments to show selected nation
        self.nationinfo = ttk.Label(
            self.panel1,
            text='Nation Selected = ' + str(nation),
            width = len(nation) + 22)
        self.nationinfo.grid(row=0, column=1, sticky='NW')
        
        # this should be a combo box with the options for the Fleets
        self.fleet = tk.StringVar(value=self.fleets[0])
        self.inputs['Fleets'] = wid.LabelInput(
            self.panel1, "Fleets",
            input_class = wid.ValidatedCombobox,
            input_var = self.fleet,
            input_args = {'values':self.fleets, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Fleets'].grid(row=1, column=0)

    def new_formation_info(self):
        #################################################
        # the extra widgets specific to the new_formation
        # version of this window
        #################################################
        print('enter vie:new_formation_info')
        self.panel1.text = "Select Fleet New Formation is in, and Unique Formation Name"
        # this should be an entry for the New Formation Name
        self.formation_name = tk.StringVar(value="")
        self.inputs['FrmtnName'] = wid.LabelInput(
            self.panel1, "Formation Name",
            field_spec = {'req': True, 'type': wid.FT.string},
            input_var = self.formation_name,
            input_args={'width': 20},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['FrmtnName'].grid(row=1, column=1)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_new_formation)
        self.finish_button.grid(sticky="e", row=2, column=1, padx=10)

        self.status.config(text="Select Fleet and  " +
                                "Enter New Unique Formation Name " +
                                "then click 'Finish' button")
        print(self.fleet, self.formation_name, self.fleets)
        print('exit vie:new_formation_info')
        return()

    def finish_new_formation(self):
        ####################################################
        # the fleet has been selected and formation name entered
        # pass the information back to the application for storage
        ####################################################
        print('enter vie:finish_new_formation')
        self.selected_fleet = self.inputs['Fleets'].get()

        print('Selected Fleet is:', self.selected_fleet)
        self.new_formation_name = str(self.inputs["FrmtnName"].get())
        self.status.config(text="Selected Fleet = " + self.selected_fleet +"  New Formation = " + str(self.new_formation_name))

        print(self.selected_fleet, str(self.new_formation_name), self.fleets_file)
        
        self.clean_up_after_finishing()		# tidy up the display after finishing the command
        print('exit vie:finish_new_formation')

        self.callbacks['formation->complete_new_formation'](self.selected_fleet, self.new_formation_name)

    def rename_formation_info(self):
        #################################################
        # the extra widgets specific to the rename_formation
        # version of this window
        # WARNING: identical code exists in the Fleets routines - EDIT BOTH
        #################################################
        print('enter vie:rename_formation_info')

        self.panel1.text = "Select Fleet Renamed Formation is in, and Unique Formation Name"
        # this should be an entry for the New Formation Name
        self.formation_name = tk.StringVar(value="")
        self.inputs['FrmtnName'] = wid.LabelInput(
            self.panel1, "Formation Name",
            field_spec = {'req': True, 'type': wid.FT.string},
            input_var = self.formation_name,
            input_args={'width': 20},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['FrmtnName'].grid(row=1, column=2)

        # The Load Formations button
        self.load_formation_button = ttk.Button(
            self.panel1,
            text = "Load Formations",
            command = self.load_rename_formations)
        self.load_formation_button.grid(sticky="e", row=2, column=0, padx=10)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_rename_formation)
        self.finish_button.grid(sticky="e", row=2, column=1, padx=10)

        self.status.config(text="Select Fleet, click the 'Load Formations'" +
                                " button and select the old Formation " +
                                "Enter New Unique Formation Name " +
                                "then click 'Finish' button")
        print('exit vie:rename_formation_info')
        return()

    def load_rename_formations(self):
#		get the selected fleet, setup the formations combobox from the selected fleet
        print('enter vie:load_rename_formations')
        selected_fleet = self.inputs['Fleets'].get()
        print('Selected Fleet is:', selected_fleet)
        print('formations', self.fleets_file[selected_fleet]['formations'])

        # this should be a combo box with the options for the Fleets
        self.formation = tk.StringVar(value="Select Formation")
        self.inputs['Formations'] = wid.LabelInput(
            self.panel1, "Formations",
            input_class = wid.ValidatedCombobox,
            input_var = self.formation,
            input_args = {'values':self.fleets_file[selected_fleet]['formations'], 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Formations'].grid(row=1, column=1)

        print('formations', selected_fleet, self.fleets_file[selected_fleet])   
        print('exit vie:load_rename_formations')
        return()

    def finish_rename_formation(self):
        ####################################################
        # the fleet has been selected and formation name entered
        # pass the information back to the application for storage
        ####################################################
        print('enter vie:finish_rename_formation')
        print('selection ',self.inputs['Fleets'].get())
        self.selected_fleet = self.inputs['Fleets'].get()

        print('Selected Fleet is:', self.selected_fleet)
        self.old_formation_name = self.inputs["Formations"].get()
        print('Old Formation Name ', self.old_formation_name)
        self.new_formation_name = self.inputs["FrmtnName"].get()
        self.status.config(text="Selected Fleet = " + self.selected_fleet +
                           " Old Formation = " + self.old_formation_name +
                           " New Formation = " + str(self.new_formation_name))

        print(self.selected_fleet, self.old_formation_name, str(self.new_formation_name), self.fleets_file)
        print('exit vie:finish_rename_formation')

        self.clean_up_after_finishing()		# tidy up the display after finishing the command

        self.callbacks['formation->complete_rename_formation'](self.selected_fleet, self.old_formation_name, str(self.new_formation_name))

    def delete_formation_info(self):
        #################################################
        # the extra widgets specific to the rename_formation
        # version of this window
        # WARNING: identical code exists in the Fleets routines - EDIT BOTH
        #################################################
        print('enter vie:delete_formation_info')

        self.panel1.text = "Select Fleet Deleted Formation is in, and click Delete button"
        # The Load Formations button
        self.load_formation_button = ttk.Button(
            self.panel1,
            text = "Load Formations",
            command = self.load_delete_formations)
        self.load_formation_button.grid(sticky="e", row=2, column=0, padx=10)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_delete_formation)
        self.finish_button.grid(sticky="e", row=2, column=1, padx=10)

        self.status.config(text="Select Fleet, click the 'Load Formations'" +
                                " button and select the Formation " +
                                "Name that is to be deleted " +
                                "then click 'Finish' button")
        print('exit vie:delete_formation_info')
        return()

    def load_delete_formations(self):
#		get the selected fleet, setup the formations combobox from the selected fleet
        print('enter vie:load_delete_formations')
        selected_fleet = self.inputs['Fleets'].get()
        print('Selected Fleet is:', selected_fleet)
        print('formations', self.fleets_file[selected_fleet]['formations'])

        # this should be a combo box with the options for the Fleets
        self.formation = tk.StringVar(value="Select Formation")
        self.inputs['Formations'] = wid.LabelInput(
            self.panel1, "Formations",
            input_class = wid.ValidatedCombobox,
            input_var = self.formation,
            input_args = {'values':self.fleets_file[selected_fleet]['formations'], 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Formations'].grid(row=1, column=1)

        print('formations', selected_fleet, self.fleets_file[selected_fleet])   
        print('exit vie:load_delete_formations')
        return()
        
    def finish_delete_formation(self):
        ####################################################
        # the fleet has been selected and formation name entered
        # pass the information back to the application for storage
        ####################################################
        print('enter vie:finish_delete_formation')
        self.selected_fleet = self.inputs['Fleets'].get()

        print('Selected Fleet is:', self.selected_fleet)

        self.formation_name_to_delete = self.inputs["Formations"].get()
        print('Formation Name to delete ', self.formation_name_to_delete)
        self.status.config(text="Selected Fleet = " + self.selected_fleet +
                           " Formation name to delete = " + self.formation_name_to_delete)

        print(self.selected_fleet, self.formation_name_to_delete, self.fleets_file)
        print('exit vie:finish_delete_formation')

        self.clean_up_after_finishing()		# tidy up the display after finishing the command

        self.callbacks['formation->complete_delete_formation'](self.selected_fleet, self.formation_name_to_delete)

    def clean_up_after_finishing(self):
        # attempt to clear the panel, its title and status bar
#        print('widget list b4 ', self.inputs)
        for widget in self.panel1.winfo_children():
            widget.destroy()
        for key, value in list(self.inputs.items()):
            del self.inputs[key]
#        print('widget list after ', self.inputs)
        self.panel1.text = ""
        self.status.config(text="Select the Next Action you wish to Perform" +
                                " from the Menus")

    def setup_buildforminfo(self, tree_text):
        # buildforminfo section - sets up the display for the tree info for the ships
        # ancestor is the label/labelframe in which this section will be displayed
        # not sure a command is need in this case, a button terminates the selection process
        # BIG NOTE - to setup the correct command for the binding on the list, you need to set a variable:
        # self.formation_command to be the self... function that handles the command before calling this routine
        # eg self.dispship_command = self.dispship_on_open_record

        print('enter vie:buildformation.setup_buildforminfo')
        self.treelabel = tk.LabelFrame(
            self.panel2,
            text=tree_text,
            width=155,
            padx=10,
            pady=10)
        self.buildforminfo = ttk.Treeview(
            self.treelabel,
            columns=list(self.swap_files_column_defs.keys())[1:],
            selectmode='extended'                        # user can select multiple items
        )
        self.buildforminfo.selectors = list()            # will hold the list of items to display in this tree

        # configure scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self.treelabel,
            orient=tk.VERTICAL,
            command=self.buildforminfo.yview
        )
        self.buildforminfo.configure(yscrollcommand=self.scrollbar.set)
        self.buildforminfo.grid(row=0, column=0, sticky='W')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')
        self.treelabel.grid(row=0, column=0, stick='W')

        # Configure treeview columns
        for name, definition in self.swap_files_column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.buildforminfo.heading(name, text=label, anchor=anchor)
            self.buildforminfo.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        self.buildforminfo.selected_ships = []              # used in record_selection to store selected ships
        self.buildforminfo.bind('<<TreeviewOpen>>', self.record_selection)

        print('exit vie:buildformation.setup_buildforminfo')

    def record_selection(self, *args):
        # save the list of selectors that have been clicked
        print('enter vie:record_selection')
        print('selections ',self.buildforminfo.selection())
        selected_id = int(self.buildforminfo.selection()[-1])
        next_selection = list(self.unassigned_ships)[selected_id]
        self.buildforminfo.selected_ships.append(next_selection)
        print('vie:record_selector ',self.buildforminfo.selected_ships)
        print('exit vie:record_selection')

    def populate_buildform(self,unassigned_ships):
        # load the ship data into the treelist in panel2
        # the list of ships is in ships_to_disp
        print('enter vie:buildformation.populate_buildform')
#        util.populate_formations(self, ancestor, g=g, r=r, column_def=column_def)

        self.unassigned_ships = unassigned_ships

        for row in self.buildforminfo.get_children():
            self.buildforminfo.delete(row)

        rownum = 0
        print('unassigned ships ',unassigned_ships)
        for ship in unassigned_ships:
            notes = unassigned_ships[ship]

# is this correct            
            self.form_label = ship
            values = (ship,notes)
            self.buildforminfo.insert('', 'end', iid=str(rownum),
                                     text=str(rownum), values=values)
#            self.shipinfoa.selectors.append(firer)
            rownum += 1
        print('buildforminfo',self.buildforminfo.selectors)

        print('exit vie:buildformation.populate_buildform')

    def get_moves(self, formations={}):
        print("enter vie:get_moves")
        print(formations)
        print("exit vie:get_moves")

    def joinformation_info(self, nations):
        ########################################################################
        # setup the combo boxes for Nation and the Port/Fleet selection
        ########################################################################
        print('enter vie:joinformation_info')
        self.nations = nations
        print('nations = ', self.nations)

        # this should be a combo box with the options for the Nations
        self.nation = tk.StringVar(value='NeutralShips')
        self.inputs['Nation'] = wid.LabelInput(
            self.panel1, "Nation",
            input_class = wid.ValidatedCombobox,
            input_var = self.nation,
            input_args = {'values':self.nations, 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Nation'].grid(row=0, column=0)

        # this should be a combo box to indicate that the formations are in
        # a Port or a Fleet (I can't work out how to use the Radiobutton in Widgets)
        self.port_fleet = tk.StringVar(value='Port')
        self.inputs['Port_Fleet'] = wid.LabelInput(
            self.panel1,
            "Port, Fleet",
            input_class=wid.ValidatedCombobox,
            input_var=self.port_fleet,
            input_args = {'values':['Port', 'Fleet'], 'width': 20},
            field_spec = {'req': True, 'type': wid.FT.integer},
            label_args = {'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Port_Fleet'].grid(row=0,column=1, sticky="w")
        print('vie:joinformation.Port_Fleet')

        self.get_frmtns_button = ttk.Button(
            self.panel1,
            text = "Get Formations",
            command = self.get_frmtns_4_join)
        self.get_frmtns_button.grid(sticky="e", row=0, column=2, padx=10)

        self.status.config(text="Select Nation, Indicate if a Port or Fleet is to " +
                                "be modified, then click 'Get Formations' button")

        print('exit vie:joinformation_info')

    def get_frmtns_4_join(self):
        # the Nation has been selected,
        # and indication made if the formation is in a Port or a Fleet 
        print('enter vie.get_frmtns_4_join')
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()

        self.nation = data['Nation']
        self.port_fleet = data['Port_Fleet']

        print('nation:',self.nation,' Port or Fleet ',self.port_fleet)
        print('exit vie.get_frmtns_4_join')
        self.callbacks['formation->get_frmtns_4_join'](self.nation,self.port_fleet)

# note this should be in another routine as we won't have the values until MODEL has produced them,
# either as a list of port names or a list of fleet names

    def display_frmtnlst(self, frmtnlst):
        # got the formation list from MODEL, add another combobox for it
        
        print('enter vie.display_frmtnlst')
        # this should be a combo box with the options for the Ports
        self.frmtns = tk.StringVar(value=frmtnlst[0])
        self.inputs['Frmtns'] = wid.LabelInput(
            self.panel1, "Port or Fleet",
            input_class = wid.ValidatedCombobox,
            input_var = self.frmtns,
            input_args = {'values':frmtnlst, 'width': 10},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.selected_frmtns = []
        self.inputs['Frmtns'].bind('<<ComboboxSelected>>', self.frmtnlst_selection),
        self.inputs['Frmtns'].grid(row=0, column=3)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_joinformation)
        self.finish_button.grid(sticky="e", row=0, column=4, padx=10)

        self.status.config(text="Select Prime Formation, then all the other " +
                                " formations to add to it, " +
                                "then click 'Finish' button")

        print('exit vie.display_frmtnlst')

    def frmtnlst_selection(self, *args):
        # save the list of selectors that have been clicked
        print('enter vie:frmtnlist_selection')
        print('selections ',self.inputs['Frmtns'].get())
        next_selection = self.inputs['Frmtns'].get()
        self.selected_frmtns.append(next_selection)
        print('vie:record_selector ',self.selected_frmtns)

        print('exit vie.frmtnlst_selection')
        
    def finish_joinformation(selfl):
        print('enter vie.finish_joinformation')

        print('exit vie:buildformation.setup_buildforminfo')
        self.callbacks['formation->finish_joinformations'](self.selected_frmtns)

'''
            
# routines to display the formation data and get new movement information

class GetMoveForm(ttk.Frame):
    """ Display for Formations data """

    formations_column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W, 'width': 35},
        'Formation': {'label': 'Formation', 'width': 80, 'stretch': False},
        'BestSpd': {'label': 'BestSpd', 'width': 55, 'stretch': False},
        'B4Turn': {'label': 'B4Turn', 'width': 55, 'stretch': False},
        'Straight': {'label': 'Straight', 'width': 55, 'stretch': False},
        'Move': {'label': 'Move', 'width': 70, 'stretch': False}
    }
    default_width = 12
    default_minwidth = 12
    default_anchor = tk.W

    def __init__(self, parent, fields, callbacks, move_num, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:GetMoveForm.init')
        self.callbacks = callbacks
        self.fields = fields
        self.move_num = move_num

#        self.geometry("400x300")
#        self.resizable(width=False, height=False)

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel
        self.panel1 = tk.LabelFrame(
            self,
            text="Move Info",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')
                                 
        # setup the second panel
        self.panel2 = tk.LabelFrame(
            self,
            text="Create Move",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # setup the third panel
        self.panel3 = tk.LabelFrame(
            self,
            text="Formations to Select",
            padx=10,
            pady=10
        )
        self.panel3.grid(row=2,column=0, sticky='NW')

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User Menu Select')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=3, column = 0, sticky="we", padx=10)

        print('exit vie:GetMoveForm.init')

    def receive_dbs(self,move,fleets, formations,ships):
        # called from Application to pass the move_num, fleets, formations and ships to the views
        print('enter vie:GetMoveForm.receive_dbs')
        self.move_num = move
        self.panel1.config(text='Move Info')
        self.moveinfo = ttk.Label(
            self.panel1,
            text='Move Num = ' + str(self.move_num))
        self.moveinfo.grid(row=0, column=0, sticky='NW')
        self.fleets = fleets
        self.formations = formations
        self.ships = ships
        print('exit vie:GetMoveForm.receive_dbs')
        
    def setup_formation_info(self, ancestor):
        # adds the elements that displays the info for the selected formation and gets the next movement
        # by getting each step seperately - uses panel2 to place the elements
        print('enter vie:setup_formation_info')
#        print (self.fields)
        self.panel2.config(text='Formation Info')
        self.formation_label = tk.LabelFrame(self.panel2,text = "Formation")
        self.formation_value = ttk.Label(self.formation_label,
                                         text = "None Selected Yet")
        self.formation_value.grid(row=1,column=0, sticky="w")
        self.formation_label.grid(row=0,column=0)

        self.currspd = '0'
        self.currspd_label = tk.LabelFrame(self.panel2,
            text = "Curr Speed")
        self.currspd_value = ttk.Label(self.currspd_label,
            text = self.currspd)
        self.currspd_value.grid(row=1, column=0, sticky='w')
        self.currspd_label.grid(row=0, column=1)

        self.step = '0'
        self.step_label = tk.LabelFrame(self.panel2,
            text = "Step")
        self.step_value = ttk.Label(self.step_label,
            text = self.step)
        self.step_value.grid(row=1, column=0, sticky='w')
        self.step_label.grid(row=0, column=2)

        self.bestspd = '0'
        self.bestspd_label = tk.LabelFrame(self.panel2,
            text = "Best Speed")
        self.bestspd_value = ttk.Label(self.bestspd_label,
            text = self.bestspd)
        self.bestspd_value.grid(row=1, column=0, sticky='w')
        self.bestspd_label.grid(row=0, column=3)

        self.b4turn = '0'
        self.b4turn_label = tk.LabelFrame(self.panel2,
            text = "B4 Turn")
        self.b4turn_value = ttk.Label(self.b4turn_label,
            text = self.b4turn)
        self.b4turn_value.grid(row=1, column=0, sticky='w')
        self.b4turn_label.grid(row=0, column=4)

        self.minturn = '0'
        self.minturn_label = tk.LabelFrame(self.panel2,
            text = "Min Turn")
        self.minturn_value = ttk.Label(self.minturn_label,
            text = self.minturn)
        self.minturn_value.grid(row=1, column=0, sticky='w')
        self.minturn_label.grid(row=0, column=5)

        self.facing = '0'
        self.facing_label = tk.LabelFrame(self.panel2,
            text = "Facing")
        self.facing_value = ttk.Label(self.facing_label,
            text = self.facing)
        self.facing_value.grid(row=1, column=0, sticky='w')
        self.facing_label.grid(row=0, column=6)

# this should be a combo box with 5 elements, Together Port, Port, Straight on, Stbd, Together Stbd
        self.direction = tk.StringVar(value='Straight On')
        self.inputs['Direction'] = wid.LabelInput(
            self.panel2, "Direction",
            input_class = wid.ValidatedCombobox,
            input_var = self.direction,
            input_args = {'values':["Straight On", "Port Together", "Port in Line",
                                    "Stbd in Line", "Stbd Together", "Complete Move"], 'width': 12},
# there is no definition in fields of "direction" bcos it is not a forms field, maybe this should be an int
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Direction'].grid(row=0, column=7)

# this should be an entry for a number between Min Turn and Curr Spd
        self.inputs['Distance'] = wid.LabelInput(
            self.panel2, "Distance",
# this is not a forms field either
            field_spec = {'req': True, 'type': wid.FT.integer},
            input_args={'increment':3, 'width': 12},
                #'from':0, 'to':60, 'increment':3,
                #        'min_var':int(self.currspd)-6,'max_var':min(int(self.bestspd),int(self.currspd)+6)},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Distance'].grid(row=0, column=8)

        # The next button
        self.nextbutton = ttk.Button(
            self.panel2,
            text = "Select",
            command = self.formation_on_null)
        self.nextbutton.grid(sticky="e", row=0, column=9, padx=10)

        # displays the built move
        self.move = ''   # used to store the move string as its being built
        self.move_label = tk.LabelFrame(self.panel2,
            text = "Move")
        self.move_value = ttk.Label(self.move_label,
            text = self.move)
        self.move_value.grid(row=1, column=0, sticky='w')
        self.move_label.grid(row=0, column=10)

        # The finish button
        self.finishbutton = ttk.Button(
            self.panel2,
            text = "Finish",
            command = self.formation_on_finish)
        self.finishbutton.grid(sticky="e", row=0, column=11, padx=10)
        print('exit vie:setup_formation_info')

    def setup_move_num(self, move_num):
        # move_num section
        print('enter vie:getmoveform.setup_move')
        util.setup_move_num(self, move_num)
        print('exit vie:getmoveform.setup_move')

    def setup_forminfo(self, ancestor, tree_text, r=2, c=0):
        # forminfo section - sets up the display for the tree info for the formations
        # ancestor is the label/labelframe in which this section will be displayed
        # BIG NOTE - to setup the correct command for the binding on the list, you need to set a variable:
        # self.formation_command to be the self... function that handles the command before calling this routine
        # eg self.formation_command = self.formation_on_open_record

#   ancestor.config(text="Formation List")
        self.treelabel = tk.LabelFrame(
            ancestor,
            text=tree_text,
            width=155,
            padx=10,
            pady=10)
        self.treeview = ttk.Treeview(
            self.treelabel,
            columns=list(self.formations_column_defs.keys())[1:],
            selectmode='browse'
        )
        self.treeview.selectors = list()            # will hold the list of items to select from for this tree

        # configure scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self.treelabel,
            orient=tk.VERTICAL,
            command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.grid(row=0, column=0, sticky='W')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')
        self.treelabel.grid(row=r, column=c, stick='W')

        # Configure treeview columns
        for name, definition in self.formations_column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.treeview.heading(name, text=label, anchor=anchor)
            self.treeview.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        self.treeview.bind('<<TreeviewOpen>>', self.formation_command)

        return(self.treeview)

    def setup_widgets_for_get_move(self, ancestor):
        # called from application to load the data into the panels (1-3) when the user has clicked on get move
#        print('enter vie:setup_widgets_for_get_move')
        # setup panel1 with the widgets to display the move number to the user
#        self.setup_move_num()          not yet received from model?

        # setup the widgets for the formation info to allow user to enter the next move for each formation in panel2
        self.setup_formation_info(ancestor)
       
        # setup the widgets for the formation list in panel3
        self.formation_command = self.formation_on_open_record
        self.forminfoa = util.setup_forminfo(self,self.panel3, 'Formations', r=2, c=0)
#        print('exit vie:setup_widgets_for_get_move')
        
    def populate_formations(self, ancestor, form_info, column_def=0):
#       used to have ", rows" as the third parameter 
        # load the formation data into the treelist in panel3
        print('enter vie:getmoveform.populate_formations')

        self.form_info = form_info
        util.populate_formations(self, ancestor, form_info, column_def=column_def)

        print('exit vie:getmoveform.populate_formations')

    def formation_on_open_record(self, *args):
        # called by the application after it gets a callback when the user clicks a formation to place the 
        # move info for that formation into the move info section

#        print('enter vie.formation_on_open_record')
        self.selected_id = int(self.treeview.selection()[0])
        self.formation = list(self.form_info)[self.selected_id]

#        print(self.formation, self.formations[self.formation])
        
        self.formation_value.config(text=self.formation)
        self.currspd = str(self.form_info[self.formation]['currspd'])
        self.currspd_value.config(text = self.currspd)
        self.step = str(self.form_info[self.formation]['step'])
        self.step_value.config(text = self.step)
        self.bestspd = str(self.form_info[self.formation]['bestspd'])
        self.bestspd_value.config(text = self.bestspd)
        self.b4turn = str(self.form_info[self.formation]['b4turn'])
        self.b4turn_value.config(text = self.b4turn)
        self.minturn = str(self.form_info[self.formation]['straight'])
        self.minturn_value.config(text = self.minturn)
        self.facing = str(self.form_info[self.formation]['facing'])
        self.facing_value.config(text = self.facing)
        self.dist_moved = min(int(self.currspd)+ int(self.step),int(self.bestspd))
        self.inputs['Direction'].set('Straight On')
        self.inputs['Distance'].set(self.dist_moved)
        self.move = ''
        self.move_value.config(text = self.move)
        self.nextbutton.config(text='Next', command=self.formation_on_next)

#        print('exit vie.formation_on_open_record')

    def formation_on_null(self):
#       nothing should happen if the user clicks this button in this state
        messagebox.showinfo("Selecting a Formation",
                            """Double-click on a Formation line in the Formations List below:""")
    
    def formation_on_next(self):
        # called when Next button is pressed to form the Move string
        turn_conversion = {'Straight On': 'A', 'Port Together': 'TP', 'Port in Line': 'P',
                        'Stbd Together': 'TS', 'Stbd in Line': 'S'}
#        print('enter vie.formation_on_next')
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        if data['Direction'] == 'Complete Move':
            # complete the move as if the user had clicked the Finish button (currently Next is showing)
            self.formation_on_finish()
            return                  # ensure that the rest of the procedure is not run
        
        if int(self.b4turn) > 0 and data['Direction'] != 'Straight On':
            messagebox.showinfo("ERROR",
                                'You must continue in a straight line for at least {}'.
                                format(int(self.b4turn)))
        else:
            self.move += turn_conversion[data['Direction']] + str(data['Distance'])
#            self.formations[self.formation]['move'] = self.move
            self.move_value.config(text = self.move)
            self.dist_moved = int(self.dist_moved) - int(data['Distance'])
# set b4turn to be (minturn - last distance) and update to database
# set min for Distance to be the same value
# set max for Distance to be the remaining currspd
            if data['Direction'] == 'Straight On':
                self.b4turn = str(max(0,int(self.b4turn) - int(data['Distance'])))
            else:
                self.b4turn = str(max(0,int(self.minturn) - int(data['Distance'])))
#            self.formations[self.formation]['b4turn'] = self.b4turn
            self.b4turn_value.config(text=self.b4turn)
# don't know why but can't set the min/max value this way
#           self.inputs['Distance'].config(input_args ={'min_value':self.b4turn,'max_value':self.currspd})
            if int(self.dist_moved) <= 0:
                self.nextbutton.config(text = 'Finish', command=self.formation_on_finish)
# change the command on the button to point to putting the rows back to the model
#            print('exit vie.formation_on_next')

    def formation_on_finish(self):
#       the formation move has been setup, save the value back to the database in the model directory
#       reset the button to the null state
#        print('enter vie.formation_on_finish', self.currspd, self.step, self.bestspd, self.dist_moved)
        self.currspd = str(min(int(self.currspd)+ int(self.step),int(self.bestspd))
                           + int(self.dist_moved))
#        print('after calculation', self.currspd)
        self.currspd_value.config(text = self.currspd)
        print('vie:formation_on_finish',self.formation,self.move,self.b4turn,self.currspd)
        self.callbacks['battle->update_move_b4turn_currspd'](self.formation,
                                                             self.move, self.b4turn, self.currspd)
#        print('vie:formation_on_finish.forminfoa:',self.forminfoa.item(item=None))
        self.forminfoa.set(self.selected_id, 1, self.bestspd)
        self.forminfoa.set(self.selected_id, 2, self.move)

        self.nextbutton.config(text='Select', command=self.formation_on_null)
#        print('exit vie.formation_on_finish')
        
    def update_status_bar(self,status_text='No Status Text Given'):
        print('enter vie.update_status_bar')
        self.status.config(text=status_text)
        print('exit vie.update_status_bar')

class GetTargForm(ttk.Frame):
    """ Display for Firers and Targets data """

    formations_column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W, 'width': 35},
        'Formation': {'label': 'Formation', 'width': 80, 'stretch': False},
        'BestSpd': {'label': 'BestSpd', 'width': 55},
        'Move': {'label': 'Move', 'width': 70, 'stretch': False}
    }
    ships_column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W, 'width': 35},
        'Firer': {'label': 'Ship', 'width': 80, 'stretch': False},
        'Target': {'label': 'Target', 'width': 80}
    }

    default_width = 35
    default_minwidth = 15
    default_anchor = tk.W

    def __init__(self, parent, fields, callbacks, move_num, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:GetTargForm.init')
        self.callbacks = callbacks
        self.fields = fields
        self.move_num = move_num

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel
        self.panel1 = tk.LabelFrame(
            self,
            text="Move Info",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')
                                 
        # setup the second panel
        self.panel2 = tk.LabelFrame(
            self,
            text="Button Panel",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # setup the third panel
        self.panel3 = tk.LabelFrame(
            self,
            text="Formations Panel",
            padx=10,
            pady=10
        )
        self.panel3.grid(row=2,column=0, sticky='NW')

        self.panel4 = tk.LabelFrame(
            self,
            text="Ships Panel",
            padx=10,
            pady=10
        )
        self.panel4.grid(row = 3, column = 0, sticky='W')

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User Menu Select')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=4, column = 0, sticky="we", padx=10)

    def receive_dbs(self, move_num, fleets, formations, ships):
        # called when Application has been asked to provide the move num, fleets, formations and ships to this file
        print('enter vie.gettargform.receive_dbs')
        self.move_num = move_num
        print('move_num:',self.move_num)
        self.fleets = fleets
        self.formations = formations
#        print('formations:',self.formations)
#        print('ships:',ships)
        self.ships = ships
        print('exit vie.gettargform.receive_dbs')
        
    def setup_move_num(self, move_num):
        # move_num section
        print('enter vie:gettargform.setup_move')
        util.setup_move_num(self, move_num)
        print('exit vie:gettargform.setup_move')

    def update_status_bar(self,status_text='No Status Text Given'):
        print('enter vie:get_targform.update_status_bar')
        self.status.config(text=status_text)
        print('exit vie:get_targform.update_status_bar')

    def setup_widgets_for_get_targets(self):
        # called from application to load the data into the panels (1-3) when the user has clicked on get targets
        print('enter vie:gettargform.setup_widgets_for_get_target')

        # Setup the button for "No Target" in Panel 2
        self.notargetbutton = ttk.Button(
            self.panel2,
            text = "No Target",
            command = self.notarget)
        self.notargetbutton.grid(sticky="e", row=0, column=0, padx=10)

        # setup the button for "Complete Green" in Panel 2
        self.finishtargbutton = ttk.Button(
            self.panel2,
            text = "Complete Green",
            command = self.finishtarg)
        self.finishtargbutton.grid(sticky="e", row=0, column=1, padx=10)

        # setup the widgets for the formation list in panel3        
        self.formation_command = self.display_firing_ships
        self.forminfoa = util.setup_forminfo(
            self,self.panel3, 'Firers', r=2, c=0)
        self.formation_command = self.display_target_ships
        self.forminfob = util.setup_forminfo(
            self,self.panel3, 'Targets', r=2, c=1)

        # setup the widgets for the ship lists in panel4 for the get targets
        self.ship_command = self.store_firer_selected
        self.shipinfoa = self.setup_shiplist(self.panel4, ship_text = 'Firers', r=3, c=0)
        self.ship_command = self.store_target_selected
        self.shipinfob = self.setup_shiplist(self.panel4, ship_text = 'Targets', r=3, c=1)

        print('exit vie:gettargform.setup_widgets_for_get_target')

    def populate_formations(self, ancestor, form_info, column_def=0):
        # load the formation data into the specified treelist in panel3
        print('enter vie:gettargform.populate_formations')
        self.form_info = form_info
        util.populate_formations(self, ancestor, form_info, column_def=column_def)
        print('exit vie:gettargform.populate_formations')

    def setup_shiplist(self,ancestor, ship_text='List of Ships for one side', r=0, c=0):
        # shiplist section - sets up the display for the tree info for the ships
        # ship_text is the text to display in the label
        # ancestor is the label/labelframe in which this section will be displayed
        # r and c are the row and column in which to grid the display
        print('enter vie:gettargform.setup_shiplist')
        ancestor.config(text='Shiplists')

        self.shiplabel = tk.LabelFrame(
            ancestor,
            text=ship_text,
            width=155,
            padx=10,
            pady=10)
        self.shiplist = ttk.Treeview(
            self.shiplabel,
            columns=list(self.ships_column_defs.keys())[1:],
            selectmode='browse'
        )
        self.shiplist.selectors = list()            # will hold the list of items to select from for this tree

        # configure scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self.shiplabel,
            orient=tk.VERTICAL,
            command=self.shiplist.yview
        )
        self.shiplist.configure(yscrollcommand=self.scrollbar.set)
        self.shiplist.grid(row=0, column=0, sticky='W')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')
        self.shiplabel.grid(row=r, column=c, stick='W')

        # Configure treeview columns
        for name, definition in self.ships_column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.shiplist.heading(name, text=label, anchor=anchor)
            self.shiplist.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        self.shiplist.bind('<<TreeviewOpen>>', self.ship_command)
        print('exit vie:setup_shiplist')
        return(self.shiplist)

    def display_firing_ships(self, *args):
        print('enter vie.gettargform.display_firing_ships')
        selected_id = int(self.forminfoa.selection()[0])
        print('num,selectors:',selected_id, self.forminfoa.selectors)
        selected_formation = self.forminfoa.selectors[selected_id]
        print('sel form:',selected_formation)
        print(self.forminfoa.selectors[selected_id])
# start changes here
#        self.firing_ships = self.formations[selected_formation]['ships']
        self.firing_ships = self.callbacks['battle->get_ship_targ_info'](selected_formation)
# possibly:
#       shipntarg = {}
#       for ship in self.firing_ships:
#           shipntarge = dict((ship, self.ships[ship].['main']['targ']))        
        shipntarg = []
        for ship in self.firing_ships:
            shipntarg.append((ship, self.firing_ships[ship]['targ']))
        print('shipntarg:',shipntarg)
        dictionary = dict((key,value) for (key,value) in shipntarg)
        print(f'dictionary: {dictionary}')
        
        for row in self.shipinfoa.get_children():
            self.shipinfoa.delete(row)
        self.shipinfoa.selectors.clear()

        rownum = 0
        for firer, target in list(dictionary.items()):
            self.form_label = firer
            values = (firer, target)
            self.shipinfoa.insert('', 'end', iid=str(rownum),
                                     text=str(rownum), values=values)
            self.shipinfoa.selectors.append(firer)
            rownum += 1
        print('shipinfoa',self.shipinfoa.selectors)
        print('exit vie.gettargform.display_firing_ships')
        
# note, need to store the list of ships in the second formation list somewhere
# this code is selecting the 1st entry into the self.ships list which is correct but we want the
# 1st one which is a Red ship - tho this may be the green ships when they are swapped around.

    def display_target_ships(self, *args):
        print('enter vie.gettargform.display_target_ships')
        selected_id = int(self.forminfob.selection()[0])
        self.selected_formation = self.forminfob.selectors[selected_id]
        print('sel form:',self.selected_formation)
        print(self.forminfob.selectors[selected_id])
        
#        self.target_ships = self.formations[self.selected_formation]['ships']
        self.target_ships = self.callbacks['battle->get_ship_targ_info'](self.selected_formation)
        shipntarg = []
        for ship in self.target_ships:
            shipntarg.append((ship, self.target_ships[ship]['targ']))
        print('shipntarg:',shipntarg)
        dictionary = dict((key,value) for (key,value) in shipntarg)
        print(f'dictionary: {dictionary}')
        
        for row in self.shipinfob.get_children():
            self.shipinfob.delete(row)
        self.shipinfob.selectors.clear()

        rownum = 0
        for firer, target in list(dictionary.items()):
            self.form_label = target
            values = (firer, target)
            self.shipinfob.insert('', 'end', iid=str(rownum),
                                     text=str(rownum), values=values)
# should this be firer or target, suspect it should be firer as the formation is the enemy side
            self.shipinfob.selectors.append(firer)
            rownum += 1
        print('shipinfob',self.shipinfob.selectors)
        print('exit vie.gettargform.display_target_ships')
        
    def store_firer_selected(self, *args):
        print('enter vie:gettargform.store_firer_selected')
        selected_id = int(self.shipinfoa.selection()[0])

        print(selected_id)
        print(self.shipinfoa.selectors)
        print('selected ship:',self.shipinfoa.selectors[selected_id])
        self.firer = self.shipinfoa.selectors[selected_id]
        print('firer is:', self.firer)
        print('exit vie:gettargform.store_firer_selected')
        
    def store_target_selected(self, *args):
        print('enter vie:gettargform.store_target_selected')
        selected_id = int(self.shipinfob.selection()[0])
        self.target = self.shipinfob.selectors[selected_id]
# need formation of second page not first
        print('id:',selected_id,'firer',self.firer,' targ:',self.target)
# replace targ for firer in self.ships, also add rangeband and arc
        result = self.callbacks['battle->update_firer_target'](self.firer,self.target,self.selected_formation)
        print('updating target of firer:',result)
        print('exit vie:gettargform.store_target_selected')

    def notarget(self, *args):
        print('enter vie:gettargform.notarget')
        self.target = ""
        self.selected_formation = ""
        result = self.callbacks['battle->update_firer_target'](self.firer,self.target,self.selected_formation)
        print('updating target of firer:',result)
        print('exit vie:gettargform.notarget')

    def finishtarg(self, *args):
        print('enter vie:gettargform.finishtarg')
        result = self.callbacks['battle->finishtarg'](self.finishtargbutton.config(text[9:]))
        print('finishing targs for ',self.finishtargbutton.config(text[9:]))
        self.finishtargbutton.text = result
        print('exit vie.gettargform.finishtarg')
        
class GetDamageForm(ttk.Frame):
    """ Display for Firings data - shows each pair of ships in range and gets the straddle and damage result for the firing """

    def __init__(self, parent, fields, callbacks, move_num, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:GetDamageForm.init')
        self.callbacks = callbacks
        self.fields = fields
        self.move_num = move_num

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel
        self.panel1 = tk.LabelFrame(
            self,
            text="Panel 1",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')
                                 
        # setup the second panel
        self.panel2 = tk.LabelFrame(
            self,
            text="Panel 2",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

#        self.columnconfigure(0, weight=1)
#        self.rowconfigure(1, weight=1)

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Waiting for User Menu Select')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=4, column = 0, sticky="we", padx=10)

    def setup_move_num(self, move_num):
        # move_num section
        print('enter vie:getdmgform.setup_move')
        util.setup_move_num(self, move_num)
        print('exit vie:getdmgform.setup_move')

    def setup_firing_info(self,firing_data):
        # adds the elements that displays the info for the next firing and gets the Straddle 
        # and Damage info - uses panel2 to place the elements
        print('enter vie:setup_firing_info')
        print(firing_data)
        if firing_data[0] == "":
            messagebox.showinfo("Firing Info",
                            """There are no more ships in Range""")
            return()
        
        self.firing_data = firing_data

        # setup the move panel
        self.move_label = tk.LabelFrame(
            self,
            text='Move Info',
            padx=10,
            pady=10
        )
        self.move_num = self.callbacks['battle->get_move_num']()
        self.move_value = ttk.Label(
            self.move_label,
            text= 'Move Number = ' + str(self.move_num))
        self.move_value.grid(row=0,column=0, sticky='w')
        self.move_label.grid(row=0, column=0, sticky='NW')
        # setup the firing data and inputs for the straddle and damage
        self.panel2 = tk.LabelFrame(
            self,
            text='Firing Info',
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        self.firer_label = tk.LabelFrame(self.panel2,
            text = "Firer")
        self.firer_value = ttk.Label(self.firer_label,
            text = firing_data[0])
        self.firer_value.grid(row=0, column=0, sticky='w')
        self.firer_label.grid(row=0, column=0)

        self.targ_label = tk.LabelFrame(self.panel2,
            text = "Target")
        self.targ_value = ttk.Label(self.targ_label,
            text = firing_data[1])
        self.targ_value.grid(row=0, column=0, sticky='w')
        self.targ_label.grid(row=0, column=1)

        self.targspd_label = tk.LabelFrame(self.panel2,
            text = "Targ Spd")
        self.targspd_value = ttk.Label(self.targspd_label,
            text = firing_data[2])
        self.targspd_value.grid(row=0, column=0, sticky='w')
        self.targspd_label.grid(row=0, column=2)

        self.range_label = tk.LabelFrame(self.panel2,
            text = "Range")
        self.range_value = ttk.Label(self.range_label,
            text = firing_data[3] + '-' + str(firing_data[4]))
        self.range_value.grid(row=0, column=0, sticky='w')
        self.range_label.grid(row=0, column=3)

        self.cal_label = tk.LabelFrame(self.panel2,
            text = "Calibre")
        self.cal_value = ttk.Label(self.cal_label,
            text = firing_data[5])
        self.cal_value.grid(row=0, column=0, sticky='w')
        self.cal_label.grid(row=0, column=4)

        self.maxguns_label = tk.LabelFrame(self.panel2,
            text = "Max Guns")
        self.maxguns_value = ttk.Label(self.maxguns_label,
            text = firing_data[6])
        self.maxguns_value.grid(row=1, column=0, sticky='w')
        self.maxguns_label.grid(row=0, column=5)

        self.xingt_label = tk.LabelFrame(self.panel2,
            text = "XingT")
        self.xingt_value = ttk.Label(self.xingt_label,
            text = firing_data[7])
        self.xingt_value.grid(row=0, column=0, sticky='w')
        self.xingt_label.grid(row=0, column=6)

        self.belt_label = tk.LabelFrame(self.panel2,
            text = "Belt")
        self.belt_value = ttk.Label(self.belt_label,
            text = firing_data[9])
        self.belt_value.grid(row=0, column=0, sticky='w')
        self.belt_label.grid(row=1, column=0)

        self.deck_label = tk.LabelFrame(self.panel2,
            text = "Deck")
        self.deck_value = ttk.Label(self.deck_label,
            text = firing_data[10])
        self.deck_value.grid(row=0, column=0, sticky='w')
        self.deck_label.grid(row=1, column=1)

        self.tn_label = tk.LabelFrame(self.panel2,
            text = "TN")
        self.tn_value = ttk.Label(self.tn_label,
            text = firing_data[8])
        self.tn_value.grid(row=0, column=0, sticky='w')
        self.tn_label.grid(row=1, column=2, columnspan=5)

        self.PenB_label = tk.LabelFrame(self.panel2,
            text = "PenB")
        self.PenB_value = ttk.Label(self.PenB_label,
            text = firing_data[11])
        self.PenB_value.grid(row=0, column=0, sticky='w')
        self.PenB_label.grid(row=2, column=0)

        self.PenD_label = tk.LabelFrame(self.panel2,
            text = "PenD")
        self.PenD_value = ttk.Label(self.PenD_label,
            text = firing_data[12])
        self.PenD_value.grid(row=0, column=0, sticky='w')
        self.PenD_label.grid(row=2, column=1)

        self.DmgShell_label = tk.LabelFrame(self.panel2,
            text = "Dmg/Shell")
        self.DmgShell_value = ttk.Label(self.DmgShell_label,
            text = firing_data[13])
        self.DmgShell_value.grid(row=0, column=0, sticky='w')
        self.DmgShell_label.grid(row=2, column=2,columnspan=2)

# this should be a combo box with 2 elements, 0 for no Straddle, -5 for a Straddle
        self.straddle = tk.IntVar(value=0)
        self.inputs['Straddle'] = wid.LabelInput(
            self.panel2, "Straddle",
            input_class = wid.ValidatedCombobox,
            input_var = self.straddle,
            input_args = {'values':[0, -5], 'width': 10},
# there is no definition in fields of "direction" bcos it is not a forms field, maybe this should be an int
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Straddle'].grid(row=0, column=9)

# this should be an entry for a number between 0 and probably 14x12
        self.inputs['Damage'] = wid.LabelInput(
            self.panel2, "Damage",
# this is not a forms field either
            input_args = {'width': 10},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Damage'].grid(row=0, column=10)

        # The finish button
        self.finishbutton = ttk.Button(
            self.panel2,
            text = "Finish",
            command = self.done_firing)
        self.finishbutton.grid(sticky="e", row=0, column=11, padx=10)

        print('exit vie:setup_firing_info')
        
    def done_firing(self):
#       the firing has been setup, save the Straddle and Damage back to the database in the model directory
        print('enter vie.done_firing', self.firing_data)
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()

        straddle = data['Straddle']
        damage = data['Damage']
        
        self.callbacks['battle->on_done_firing'](self.firing_data, straddle, damage)
        print('exit vie.done_firing')

class DispShipForm(ttk.Frame):
    """ Display for the ships of one or more sides data """

    dispship_column_defs = {
        '#0': {'label': 'Row', 'anchor': tk.W, 'width': 35, 'stretch': False},
        'Ship': {'label': 'Ship', 'width': 80, 'stretch': False},
        'Locn': {'label': 'Locn', 'width': 75, 'stretch': False},
        'BestSpd': {'label': 'BestSpd', 'width': 50, 'stretch': False},        
        'currblock': {'label': 'CurrBlk', 'width': 55, 'stretch': False},
        'blockfill': {'label': 'BlkFill', 'width': 55, 'stretch': False},
        'blocksize': {'label': 'BlkSize', 'width': 55, 'stretch': False},
        'tndamage': {'label': 'TNDmg', 'width': 55, 'stretch': False}
    }
    default_width = 12
    default_minwidth = 12
    default_anchor = tk.W

    def __init__(self, parent, fields, callbacks, move_num, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print('enter vie:DispShipForm.init')
        self.callbacks = callbacks
        self.fields = fields
        self.move_num = move_num

#        self.geometry("400x300")
#        self.resizable(width=False, height=False)

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel - for the Move Number
        self.panel1 = tk.LabelFrame(
            self,
            text="Panel 1",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')
                                 
        # setup the second panel - for the input info
        self.panel2 = tk.LabelFrame(
            self,
            text="Panel 2",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # setup the third panel for the Tree Display
        self.panel3 = tk.LabelFrame(
            self,
            text="Panel 3",
            padx=10,
            pady=10
        )
        self.panel3.grid(row=2,column=0, sticky='NW')

        # status bar
        self.statusbar = ttk.LabelFrame(
            self,
            text='Status')
        self.status = tk.Label(
            self.statusbar,
            text='Select the Side or Referee, then damaged states & side states')
        self.status.grid(row=0, column=0, sticky='we')
        self.statusbar.grid(row=4, column = 0, sticky="we", padx=10)

        print('exit vie:DispShipForm.init')

    def receive_dbs(self,move,fleets,formations,ships):
        # called from Application to pass the move_num, fleets, formations and ships to the views
        print('enter vie:DispShipForm.receive_dbs')
        self.move_num = move
        self.panel1.config(text='Move Info')
        self.moveinfo = ttk.Label(
            self.panel1,
            text='Move Num = ' + str(self.move_num))
        self.moveinfo.grid(row=0, column=0, sticky='NW')
        self.fleets = fleets
        self.formations = formations
        self.ships = ships
        print('exit vie:DispShipForm.receive_dbs')
        
    def setup_widgets_for_display_ships(self, ancestor):
        # adds the elements that gets the info for is the user a referee or which side
        # and selects whether they want to see undamaged/damaged or sunkships -
        # uses panel2 to place the elements
        print('enter vie:setup_widgets_for_display_ships')
#        print (self.fields)
        self.panel2.config(text='Display Ship Info')

        # this should be a combo box with 3 elements, Referee, Allied, Enemy
        self.user = tk.StringVar(value='Referee')
        self.inputs['User'] = wid.LabelInput(
            self.panel2, "User",
            input_class = wid.ValidatedCombobox,
            input_var = self.user,
            input_args = {'values':["Referee", "Allied", "Enemy"], 'width': 12},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['User'].grid(row=0, column=0)
        print('setup User')
        
# this should be an entry for the Password for that User
        self.password = tk.StringVar(value="")
        self.inputs['Password'] = wid.LabelInput(
            self.panel2, "Password",
            field_spec = {'req': True, 'type': wid.FT.string},
            input_var = self.password,
            input_args={'width': 12},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Password'].grid(row=0, column=1)
        print('setup Password')

        self.dmg_state_label = tk.LabelFrame(self.panel2,text = "Dmg State")

        self.undamaged_state = tk.BooleanVar(value=0)
        self.inputs['Undamaged'] = wid.LabelInput(
            self.dmg_state_label,
            "Undamaged",
            input_class=ttk.Checkbutton,
            input_var=self.undamaged_state)
        self.inputs['Undamaged'].grid(row=1,column=0, sticky="w")
        print('setup Undamaged')
        
        self.damaged_state = tk.BooleanVar(value=0)
        self.inputs['Damaged'] = wid.LabelInput(
            self.dmg_state_label,
            "Damaged",
            input_class=ttk.Checkbutton,
            input_var=self.damaged_state)
        self.inputs['Damaged'].grid(row=1,column=1, sticky="w")
        print('setup Damaged')
        
        self.sunk_state = tk.BooleanVar(value=0)
        self.inputs['Sunk'] = wid.LabelInput(
            self.dmg_state_label,
            "Sunk",
            input_class=ttk.Checkbutton,
            input_var=self.sunk_state)
        self.inputs['Sunk'].grid(row=1,column=2, sticky="w")
        print('setup Sunk')
        
        self.dmg_state_label.grid(row=0,column=3)

        self.side_label = tk.LabelFrame(self.panel2,text = "Sides")
        
        self.allied_selected = tk.BooleanVar(value=0)
        self.inputs['Allied'] = wid.LabelInput(
            self.side_label,"Allied",
            input_class=ttk.Checkbutton,
            input_var=self.allied_selected)
        self.inputs['Allied'].grid(row=1,column=0, sticky="w")
        print('setup Allied')
        
        self.enemy_selected = tk.BooleanVar(value=0)
        self.inputs['Enemy'] = wid.LabelInput(
            self.side_label,"Enemy",
            input_class=ttk.Checkbutton,
            input_var=self.enemy_selected)
        self.inputs['Enemy'].grid(row=1,column=1, sticky="w")
        print('setup Enemy')
        
        self.side_label.grid(row=0,column=4)

        # The finish button
        self.finishbutton = ttk.Button(
            self.panel2,
            text = "Finish",
            command = self.done_user_n_states)
        print('setup Finish Button-1')
        self.finishbutton.grid(sticky="e", row=0, column=5, padx=10)
        print('setup Finish Button-2')
        print('exit vie:setup_widgets_for_display_ships')

    def done_user_n_states(self):
#       the user has been selected and password entered, save the Damaged states and Side states back to the application
        print('enter vie.done_user_n_states')
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()

        self.user = data['User']
        self.password = data['Password']
        self.undamaged_selected = data['Undamaged']
        self.damaged_selected = data['Damaged']
        self.sunk_selected = data['Sunk']
        self.allied_selected = data['Allied']
        self.enemy_selected = data['Enemy']

        print('user:',self.user,' password:',self.password,
              'undamaged:',self.undamaged_selected,
              ' damaged:',self.damaged_selected,
              ' sunk:',self.sunk_selected,
              ' allied:',self.allied_selected,
              ' enemy:',self.enemy_selected)
        self.callbacks['battle->return_disp_ship_info'](self.user,self.password,
                                                        self.undamaged_selected,
                                                        self.damaged_selected,
                                                        self.sunk_selected,
                                                        self.allied_selected,
                                                        self.enemy_selected)
        print('exit vie.done_user_n_states')



    def setup_move_num(self, move_num):
        # move_num section
        print('enter vie:dispshipform.setup_move')
        util.setup_move_num(self, move_num)
        print('exit vie:dispshipform.setup_move')

    def setup_dispshipinfo(self, ancestor, tree_text, r=2, c=0):
        # dispshipinfo section - sets up the display for the tree info for the ships
        # ancestor is the label/labelframe in which this section will be displayed
        # BIG NOTE - to setup the correct command for the binding on the list, you need to set a variable:
        # self.formation_command to be the self... function that handles the command before calling this routine
        # eg self.dispship_command = self.dispship_on_open_record

#   ancestor.config(text="Ship List")
        print('enter vie:display_ships.setup_dispshipinfo')
        self.treelabel = tk.LabelFrame(
            ancestor,
            text=tree_text,
            width=155,
            padx=10,
            pady=10)
        self.dispshipinfo = ttk.Treeview(
            self.treelabel,
            columns=list(self.dispship_column_defs.keys())[1:],
            selectmode='none'
        )
#        self.dispshipinfo.selectors = list()            # will hold the list of items to display in this tree

        # configure scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self.treelabel,
            orient=tk.VERTICAL,
            command=self.dispshipinfo.yview
        )
        self.dispshipinfo.configure(yscrollcommand=self.scrollbar.set)
        self.dispshipinfo.grid(row=0, column=0, sticky='W')
        self.scrollbar.grid(row=0, column=1, sticky='NSW')
        self.treelabel.grid(row=r, column=c, stick='W')

        # Configure treeview columns
        for name, definition in self.dispship_column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.dispshipinfo.heading(name, text=label, anchor=anchor)
            self.dispshipinfo.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

#        self.treeview.bind('<<TreeviewOpen>>', self.dispship_command)

        print('exit vie:display_ships.setup_dispshipinfo')
        return(self.dispshipinfo)

    def populate_dispship(self, ancestor, g=True, r=True, column_def=0):
#       used to have ", rows" as the third parameter 
        # load the ship data into the treelist in panel3
        print('enter vie:dispshipform.populate_dispship')
        print('values:',self.allied_selected,self.enemy_selected,self.damaged_selected,self.undamaged_selected)
#        util.populate_formations(self, ancestor, g=g, r=r, column_def=column_def)

        # get formations from fleets for the selected fleets
        ship_to_disp = []
        if self.allied_selected:
            print('vie:display_ships.populate_dispship formations in fleets:',self.fleets)
            for i in range(len(self.fleets['Allied'])):
                selected_formations = self.fleets['Allied'][i]['formations']
                for selected_formation in selected_formations:
                    selected_ships = self.formations[selected_formation]['ships']
                    for selected_ship in selected_ships:
                        if self.undamaged_selected and self.ships[selected_ship]['currblock'] == 0 and self.ships[selected_ship]['blockfill'] == 0:
                            ship_to_disp.append(selected_ship)
                        if self.damaged_selected and (self.ships[selected_ship]['currblock'] > 0 or self.ships[selected_ship]['blockfill'] > 0):
                            ship_to_disp.append(selected_ship)
            print('ship to display:',ship_to_disp)
        if self.enemy_selected:
            for i in range(len(self.fleets['Enemy'])):
                selected_formations = self.fleets['Enemy'][i]['formations']
                for selected_formation in selected_formations:
                    selected_ships = self.formations[selected_formation]['ships']
                    for selected_ship in selected_ships:
                        if self.undamaged_selected and self.ships[selected_ship]['currblock'] == 0 and self.ships[selected_ship]['blockfill'] == 0:
                            ship_to_disp.append(selected_ship)
                        if self.damaged_selected and (self.ships[selected_ship]['currblock'] > 0 or self.ships[selected_ship]['blockfill'] > 0):
                            ship_to_disp.append(selected_ship)
                    
        for row in self.dispshipinfo.get_children():
            self.dispshipinfo.delete(row)

        rownum = 0
        for ship in ship_to_disp:
# is this correct            
            self.form_label = ship
            tndamage, maxspd = util.dmg_effect(self.ships[ship]['currblock'],
                                               self.ships[ship]['blockfill'],
                                               self.ships[ship]['dsgnspd'])
            values = (ship,self.ships[ship]['locn'],maxspd,
                      self.ships[ship]['currblock'],self.ships[ship]['blockfill'],
                      self.ships[ship]['blocksize'],tndamage)
            self.dispshipinfo.insert('', 'end', iid=str(rownum),
                                     text=str(rownum), values=values)
#            self.shipinfoa.selectors.append(firer)
            rownum += 1
#        print('dispshipinfo',self.dispshipinfo.selectors)

        print('exit vie:dispshipform.populate_dispship')


    def formation_on_null(self):
#       nothing should happen if the user clicks this button in this state
        messagebox.showinfo("Selecting a Formation",
                            """Double-click on a Formation line in the Formations List below:""")
    
    def formation_on_next(self):
        # called when Next button is pressed to form the Move string
        turn_conversion = {'Straight On': 'A', 'Port Together': 'TP', 'Port in Line': 'P',
                        'Stbd Together': 'TS', 'Stbd in Line': 'S'}
#        print('enter vie.formation_on_next')
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        if data['Direction'] == 'Complete Move':
            # complete the move as if the user had clicked the Finish button (currently Next is showing)
            self.formation_on_finish()
            return                  # ensure that the rest of the procedure is not run
        
        if int(self.b4turn) > 0 and data['Direction'] != 'Straight On':
            messagebox.showinfo("ERROR",
                                'You must continue in a straight line for at least {}'.
                                format(int(self.b4turn)))
        else:
            self.move += turn_conversion[data['Direction']] + str(data['Distance'])
            self.formations[self.formation]['move'] = self.move
            self.move_value.config(text = self.move)
            self.dist_moved = int(self.dist_moved) - int(data['Distance'])
# set b4turn to be (minturn - last distance) and update to database
# set min for Distance to be the same value
# set max for Distance to be the remaining currspd
            if data['Direction'] == 'Straight On':
                self.b4turn = str(max(0,int(self.b4turn) - int(data['Distance'])))
            else:
                self.b4turn = str(max(0,int(self.minturn) - int(data['Distance'])))
            self.formations[self.formation]['b4turn'] = self.b4turn
            self.b4turn_value.config(text=self.b4turn)
# don't know why but can't set the min/max value this way
#           self.inputs['Distance'].config(input_args ={'min_value':self.b4turn,'max_value':self.currspd})
            if int(self.dist_moved) <= 0:
                self.nextbutton.config(text = 'Finish', command=self.formation_on_finish)
# change the command on the button to point to putting the rows back to the model
            print(self.formation, self.formations[self.formation])
#            print('exit vie.formation_on_next')

    def dispship_on_finish(self):
#       the formation move has been setup, save the value back to the database in the model directory
#       reset the button to the null state
        print('enter vie.dispship_on_finish')
#        self.currspd = str(min(int(self.currspd)+ int(self.step),int(self.bestspd))
#                           + int(self.dist_moved))
#        print('after calculation', self.currspd)
#        self.currspd_value.config(text = self.currspd)
#        self.formations[self.formation]['currspd'] = self.currspd
#        print('selected line ',str(self.selected_formation))
#        print(self.forminfoa.get_children(self.selected_formation))
#        values = (self.formation, self.bestspd, self.move)
#        print('vie:formation_on_finish.forminfoa:',self.forminfoa.item(item=None))
#        self.dispshipinfo.set(self.selected_id, 1, self.bestspd)
#        self.dispshipinfo.set(self.selected_id, 2, self.move)

#        self.callbacks['battle->on_print_formation'](self.formation, self.formations[self.formation])
#        self.nextbutton.config(text='Select', command=self.formation_on_null)
#        self.dispship_on_finish()
        print('exit vie.dispship_on_finish')

    def send_move_num(self, move):
        print('enter vie.send_move_num')
        self.move_num = move
        print('move num ', self.move_num)
        print('exit vie.send_move_num')
        
    def update_status_bar(self,status_text='No Status Text Given'):
        print('enter vie.update_status_bar')
        self.status.config(text=status_text)
        print('exit vie.update_status_bar')

class design_class_record(tk.Frame):

    def __init__(self):
        print("entered design_class_record__init")
        print("exited design_class_record__init")
    
    def create_combo_frame(self):
        self.combo_frame = tk.Frame(self.parent, height=64, bg=BOARD_COLOR_2)
        self.nation_label = tk.Label(
            self.combo_frame, text="Nation", fg=BOARD_COLOR_2)
        self.nation_label.grid(row=0, column = 0, sticky='NSEW')
# pack(side=LEFT, padx=8, pady=5)
        self.nation_combo = ttk.Combobox(self.combo_frame, height=5, state='readonly',
            values=('ADL','Albion','America','Argentina','Austria','Brazil','Britain',
                    'Build Limit','Chile','China','Colonies','Denmark','Dwarf','Elf',
                    'France','Germany','Greece','HiberniaA','HiberniaB','Hybrid','Italy',
                    'Japan','Netherlands','Nippon','Norway','Prussia','PSI','Russia',
                    'Scandinavia','Spain','Sweden','TurkeyB','TurkeyG','TurkeyP'))
        self.nation_combo.grid(row=0, column=1,sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.nation_combo.set('ADL')
        print("Frame ",self.nation_combo.get())
        self.label2 = tk.Label(self.combo_frame, text="", fg=BOARD_COLOR_2)
        self.label2.grid(row=0, column=2, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.combo2 = ttk.Combobox(self.combo_frame, height=5, state='disabled')
        self.combo2.grid(row=0, column=3, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.label3 = tk.Label(self.combo_frame, text="", fg=BOARD_COLOR_2)
        self.label3.grid(row=0, column=4, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.combo3 = ttk.Combobox(self.combo_frame, height=5, state='disabled')
        self.combo3.grid(row=0, column=5, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.combo_frame.pack(fill="x", side="top")
# grid(row=0, column=5)
# 

    def create_frame2(self):
        self.frame2 = tk.Frame(self.parent, height=64, bg=BOARD_COLOR_1)
        self.label4 = tk.Label(
            self.frame2, text="", fg=BOARD_COLOR_2)
        self.label4.grid(row=1, column=0, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.combo4 = ttk.Combobox(self.frame2, height=5, state='disabled')
        self.nation_combo.grid(row=1, column=1, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.label5 = tk.Label(self.frame2, text="", fg=BOARD_COLOR_2)
        self.label5.grid(row=1, column=2, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.combo5 = ttk.Combobox(self.frame2, height=5, state='disabled')
        self.combo5.grid(row=1, column=3, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.label6 = tk.Label(self.frame2, text="", fg=BOARD_COLOR_2)
        self.label6.grid(row=1, column=4, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.combo6 = ttk.Combobox(self.frame2, height=5, state='disabled')
        self.combo6.grid(row=1, column=5, sticky="nsew")
# pack(side=LEFT, padx=8, pady=5)
        self.frame2.pack(fill="x", side="top")

