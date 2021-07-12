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
        self.create_formations_menu()
        self.create_fleets_menu()
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

    def create_formations_menu(self):
        self.formations_menu = tk.Menu(self, tearoff=False)
        self.formations_menu.add_command(label="Build Formation", command=self.callbacks['formation->build_formation'])
        self.formations_menu.add_command(label="Join Formations", command=self.callbacks['formation->join_formations'])
        self.formations_menu.add_command(label="Split Formation", command=self.callbacks['formation->split_formation'])
        self.formations_menu.add_command(label="Rename Formation", command=self.callbacks['formation->rename_formation'])
        self.formations_menu.add_command(label="Delete Formation", command=self.callbacks['formation->delete_formation'])
        self.add_cascade(label="Formations", menu=self.formations_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_fleets_menu(self):
        self.fleets_menu = tk.Menu(self, tearoff=False)
        self.fleets_menu.add_command(label="Build Fleets", command=self.on_build_fleets_menu_clicked)
        self.fleets_menu.add_command(label="Join Fleets", command=self.on_join_fleets_menu_clicked)
        self.fleets_menu.add_command(label="Split Fleets", command=self.on_break_fleets_menu_clicked)
        self.fleets_menu.add_command(label="Execute Movement", command=self.on_execute_movement_menu_clicked)
        self.fleets_menu.add_command(label="Engage Enemy", command=self.on_engage_enemy_menu_clicked)
        self.add_cascade(label="Fleets", menu=self.fleets_menu)
#        self.parent.config(menu=self.menu_bar)

    def create_slips_menu(self):
        self.slips_menu = tk.Menu(self, tearoff=False)
        self.slips_menu.add_command(label="Build Ship", command=self.on_build_ship_menu_clicked)
        self.slips_menu.add_command(label="Convert_Ship", command=self.on_convert_ship_menu_clicked)
        self.slips_menu.add_command(label="Repair Ship", command=self.on_repair_ship_menu_clicked)
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
        messagebox.showinfo("Clive Essery's WW2 Rules",
                            """Programme to aid playing the game
                               Only the Battle Part is partially working at the moment""")

# Files click commands
    def on_open_builds_menu_clicked(self):
        print(" get ",self.nation_combo.get())        
        self.nation_label["text"] = self.nation_combo.get()
        self.label2["text"] = self.combo2.get()
        self.label3["text"] = self.combo3.get()
        
    def on_open_classes_menu_clicked(self):
        pass

    def on_save_builds_menu_clicked(self):
        self.nation_combo.set('Albion')
        self.combo2.set('BatGrp')
        self.combo3.set('BatRon2')
       
    def on_save_fleets_menu_clicked(self):
        pass

    def on_exit_menu_clicked(self):
        pass

# Fleets menu clicked commands
    def on_build_fleets_menu_clicked(self):
        if self.nation_combo.get() == "Albion":
           self.pair2_set("Fleet",('BatGrp','CarGrp1','CarGrp2','CarGrp3','CvyGrp1',
                                   'CvyGrp2','CvyGrp3'),4)
        if self.nation_combo.get() == "Scandinavia":
           self.pair2_set("Fleet",('BatGrpS','BatGrpH','BatGrpN','BatGrpD','CarGrpS','CarGrpH',
                                   'CarGrpN','CarGrpD','CvyGrpS','CvyGrpH','CvyGrpN','CvyGrpD'),4)
	
    def on_join_fleets_menu_clicked(self):
        pass

    def on_break_fleets_menu_clicked(self):
        pass

    def on_execute_movement_menu_clicked(self):
        pass

    def on_engage_enemy_menu_clicked(self):
        pass

# Slips menu clicked commands
    def on_build_ship_menu_clicked(self):
        pass

    def on_convert_ship_menu_clicked(self):
        pass

    def on_repair_ship_menu_clicked(self):
        pass

    def on_build_slip_menu_clicked(self):
        pass

    def on_enlarge_slip_menu_clicked(self):
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
class BuildFormation(ttk.Frame):
    """ Build a new Formation for the Nation that has already been selected """

    buildform_column_defs = {
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
        print('enter vie:BuildFormation.init')
        self.callbacks = callbacks
        self.fields = fields

        # A dict to keep track of input widgets
        self.inputs = {}

        # setup the first panel - for the input info
        self.panel1 = tk.LabelFrame(
            self,
            text="Select Nation, Red, Port and Formation Name",
            padx=10,
            pady=10
        )
        self.panel1.grid(row=0,column=0, sticky='NW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # setup the second panel for the Tree Display
        self.panel2 = tk.LabelFrame(
            self,
            text="Select All Ships for this Formation",
            padx=10,
            pady=10
        )
        self.panel2.grid(row=1,column=0, sticky='NW')

        print('exit vie:BuildFormation.init')

    def buildformation_info(self, nations):
        ########################################################################
        # setup the combo boxes for Nation and Port, the checkbox for Neutral
        # and the entry box for the formation name which must be unique for that
        # Nation
        ########################################################################
        print('enter vie:buildformation_info')
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

        # this should be a checkbutton to indicate that the formation is a neutral one
        self.red_neutrals = tk.BooleanVar(value=False)
        self.inputs['Red'] = wid.LabelInput(
            self.panel1,
            "Red=Neutral",
            input_class=ttk.Checkbutton,
            input_var=self.red_neutrals)
        self.inputs['Red'].grid(row=0,column=1, sticky="w")
        print('vie:buildformation.Red=Neutral')
        
        # this should be a combo box with the options for the Ports
        self.port = tk.StringVar(value='North')
        self.inputs['Port'] = wid.LabelInput(
            self.panel1, "Port",
            input_class = wid.ValidatedCombobox,
            input_var = self.port,
            input_args = {'values':['North','East','South','West'], 'width': 10},
            field_spec = {'req': True, 'type': wid.FT.integer}, 
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['Port'].grid(row=0, column=2)

        # this should be an entry for the new Formation Name
        self.formation_name = tk.StringVar(value="")
        self.inputs['FormName'] = wid.LabelInput(
            self.panel1, "FormName",
            field_spec = {'req': True, 'type': wid.FT.string},
            input_var = self.formation_name,
            input_args={'width': 20},
            label_args={'style': 'RecordInfo.TLabel'}
        )
        self.inputs['FormName'].grid(row=0, column=3)

        # The get_ships button
        self.get_ships_button = ttk.Button(
            self.panel1,
            text = "Get Ships",
            command = self.get_unassigned_ships)
        self.get_ships_button.grid(sticky="e", row=0, column=4, padx=10)

        # The finish button
        self.finish_button = ttk.Button(
            self.panel1,
            text = "Finish",
            command = self.finish_buildformation)
        self.finish_button.grid(sticky="e", row=0, column=5, padx=10)

    def get_unassigned_ships(self):
        # the Nation has been selected,
        # and indication made if the formation is Neutral (Red)
        # the Port selected and new Formation Name entered
        print('enter vie.get_unassigned_ships')
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()

        self.nation = data['Nation']
        self.red = data['Red']
        self.port = data['Port']
        self.formation_name = data['FormName']

        if self.formation_name == "":
            messagebox.showinfo("ERROR",
                                "You must enter a valid formation that doesn't already exist")
            return()

        print('nation:',self.nation,self.red, self.port,' formation_name:',self.formation_name)
        print('exit vie.get_unassigned_ships')
        self.callbacks['formation->get_unassigned_ships'](self.nation,self.red, self.port, self.formation_name)

    def finish_buildformation(self):
        ####################################################
        # all the ships have been selected for the formation
        # pass the information back to the model for storage
        ####################################################
        print('enter finish_buildformation')
        print('vie:finish_buildformation',self.buildforminfo.selected_ships)

        self.callbacks['formation->complete_formation'](self.buildforminfo.selected_ships)

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
            columns=list(self.buildform_column_defs.keys())[1:],
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
        for name, definition in self.buildform_column_defs.items():
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
#        return(self.buildforminfo)

    def record_selection(self, *args):
        # save the list of selectors that have been clicked
        print('enter vie:record_selection')
        print('selections ',self.buildforminfo.selection())
        selected_id = int(self.buildforminfo.selection()[-1])
        next_selection = list(self.unassigned_ships)[selected_id]
        self.buildforminfo.selected_ships.append(next_selection)
        print('vie:record_selector ',self.buildforminfo.selected_ships)

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

#    def send_move_num(self, move):
#        print('enter vie.send_move_num')
#        self.move_num = move
#        print('move num ', self.move_num)
#        print('exit vie.send_move_num')
        
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

