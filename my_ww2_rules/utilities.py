# file containing utility routines for Clive Essery's WW2 Rules
# (c) May 2021
import tkinter as tk
from tkinter import ttk

def setup_move_num(ancestor, move_num):
    # move_num section
    print('enter vie:util.setup_move')
#    ancestor.panel1.config(text='Move Info')
# no need to do the above, should already be setup
    ancestor.moveinfo = ttk.Label(
        ancestor.panel1,
        text='Move Num = ' + str(move_num))
    ancestor.moveinfo.grid(row=0, column=0, sticky='NW')
    print('exit vie:util.setup_move')


def setup_forminfo(self,ancestor, tree_text, r=2, c=0):
        # forminfo section - sets up the display for the tree info for the formations
        # ancestor is the label/labelframe in which this section will be displayed
        # BIG NOTE - to setup the correct command for the binding on the list, you need to set a variable:
        # self.formation_command to be the self... function that handles the command before calling this routine
        # eg self.formation_command = self.formation_on_open_record

    print('enter util.setup_forminfo:',ancestor,tree_text,'r=',r,' c=',c)
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

    print('enter util.setup_forminfo:')
    return(self.treeview)

def populate_formations(self, ancestor, form_info={}, column_def=0):
    # ancestor is a treelist that has already been setup
    # form_info is a dictionary of key and a list of bestspd, b4turn, straight and move
    # column_def is the column in which to insert the data, 0 or 1
    # load the formation data into the treelist in panel3
    print('enter util:populate_formations')

    """Clear the treeview and write the supplied data rows to it."""

    for row in ancestor.get_children():
        ancestor.delete(row)

    rownum = 0

    print(form_info)
# routine fails here stating that there are too many items to unpack, expecting 2
    for key in form_info:
        self.form_label = key
        self.formation_label = key
#        self.bestspd_label = values[0]
#        self.b4turn_label = values[1]
#        self.straight_label = values[2]
#        self.move_label = values[3]
        form = form_info[key]
        values = (key,form['bestspd'],form['b4turn'],form['straight'],form['move'])

        ancestor.insert('', 'end', iid=str(rownum),
                        text=str(rownum), values=values)
        ancestor.selectors.append(key)

        rownum += 1

    if rownum > 0:
        ancestor.focus_set()
        ancestor.selection_set(0)
        ancestor.focus('0')
    print('exit util:populate_formations')

def dmg_effect(currblock, blockfill,dsgnspd):
    # calculates and returns the tndamage and maxspd values
    # currblock indicates which block is currently being filled
    # blockfill indicates how much damage is in that block (note, if that is 0
    #  then the effects of that block are not taken into account
    # dsgnspd is the ship's designed speed
    # tndamage is 2 for every block that is counted
    # maxspd is dsgnspd - 3 * number of blocks being taken into account

    if blockfill == 0:
        multiplier = max(0, currblock - 1)
    else:
        multiplier = currblock

    tndamage = 2 * multiplier

    maxspd = max(0, dsgnspd - 3 * multiplier)

    return(tndamage, maxspd)

