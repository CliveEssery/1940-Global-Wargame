"""
Constants for Clive Essery's WW2 wargames rules
@ 2020

derived from:
@ Tkinter GUI Application Development Blueprints

Note Formations and Ships will eventually be removed and placed in a separate BATTLE file along with the move number
and a list of the Fleets used in this Battle.  At that point the Fleet number 0, 1, etc will be added to each Formation
They are placed here for early testing before the software is added to save and load a BATTLE file.

"""

NUMBER_OF_ROWS = 8
NUMBER_OF_COLUMNS = 8
DIMENSION_OF_EACH_SQUARE = 64 # denoting 64 pixels
BOARD_COLOR_1 = "#DDB88C"
BOARD_COLOR_2 = "#A66D4F"
FORMATION_LAYOUT = ["Ahead","AbeamL","AbeamR","Abreast","AbreastF","AbreastA","EchL","EchR"]
# note Abeam, Ech show location of flag – to left or right of the
# formation, Abreast flag is in centre of row, AbreastF has flag in front of row, AbreastA is aft
# the last two formations have the end ships either back from the line or ahead to provide AA or AU cover
ERAS = ["SDr","EDr","MDr","EW1","MW1","LW1","EIT","LIT","PLT","EW2","MW2","LW2"]
# the eras that ships can be built in
BUDGETS = ["DrBW","W1BW","ITBW","PLTBW","LW1CA","LW1CL","ITCr","PLTCr","EITDD","LITDD","PLTDD","W2"]
# the budget eras, Dr has no budget, 4 ships can be designed in EDr and 4 in MDr, 0 in LDr but all are mothballed
# W1 includes SDr(0-4),EW1(4),MW1(4),LW1(rest), any SDr BB not included are with the mothballs
# IT only BW for British Using Nations in EIT, BC&1xPB in LIT bought forward from PLT
# PLT incomplete ships on the slips and completion docks: BB,BC, PB(1 only)
# LW1CA AC, CA1, CA6; LW1CL CL1, CL6
# ITCr CA, CL, PB, CAM, CLM, CAH, CAS, CLG?
# PLTCr as IT plus CLS ?,
# need to add the M versions eg BBM, CAM etc
TYPES = {"SDr":["SDr","AC",],"EDr":["EDrBB","EDrBC",],"MDr":["MDrBB","MDrBC",],
"EW1":["EW1BB","EW1BC",],"MW1":["MW1BB","MW1BC",],"LW1":["LW1BB","LW1BC","CA1","CL1","CA6","CL6","MBH","MBM","MBL",],
"EIT":["EITBB","PB","CA","CL","DH","DS","DM","DL","DT",],"LIT":["LITBC","PB","CA","CL","DH","DS","DM","DL","DE",],
"PLT":["PLTBB","PLTBC","PB","CA","CL","CAA","CAS","CLA","DH","DS","DM","DL","DE",],
"EW2":["EW2BB","EW2BC","PB","CA","CL","CAA","CLA","DH","DS","DM","DL","DE",],
"MW2":["MW2BB","MW2BC","PB","CA","CL","CAA","CLA","DH","DS","DM","DL","DE",],
"LW2":["LW2BB","LW2BC","PB","CA","CL","CAA","CLA","DH","DS","DM","DL","DE",],}
RANGE_BANDS = {'IM':[42,109,208,251,252,999],'GM':[42,104,198,249,252,999],'CM':[42,99,188,239,252,999],'XM':[42,94,178,229,252,999],
               'HM':[42,89,167,219,252,999],'SM':[42,84,157,209,252,999],'MM':[42,84,125,179,252,999],'LM':[42,84,117,169,252,999],
               'GS':[31,63,116,147,199,999],'CS':[31,63,105,136,170,999],'XS':[31,63,94,125,141,999],'HS':[31,63,94,125,141,999],
               'SS':[21,42,73,94,112,999],'MS':[10,31,63,73,85,999],'LS':[10,31,63,73,85,999],'AAA':[1,3,4,6,8,999]}
BAND_NAMES = ['PB  ', 'Clos', 'Mid ', 'Long', 'Extr', 'Bynd']
# the fleets list, showing fleets in both 'allied' and 'enemy'
FLEETS = {"Allied":[{"name":'SlowABC',"colour":'G',"formations":["GBatRon1", "GBatRon2", "GCruDiv1a", "GCruDiv1b", "GDesRon1", "GDesRon2", "GRearDiv"]}],
          "Enemy": [{"name":"NeuLgIsle","colour":"R","formations":["RBatDiv1", "RCru1", "RCru2", "RDesRon1", "RDesRon2"]}]}
# the formation list, includes both sides, bestspd is the bestspeed of the slowest vessel in the formation
# b4turn is the minimum distance they must travel in a straight line until they can turn, once they turn this will be set to the (straight - amount they moved in
#    a straight line), limited to zero
# straight is the minimum distance the formation must move before it can start to turn after it turned previously
# move is the next turns movement,
# ships is a list of the ships in the formation with the first one
# being the lead ship, usually a flagship, an AAship will be in a 
# different formation so it can maneouver independently
#
# changes made to GBatDiv4 (GB1,7,5,4) to remove 1 mid turret and increase speed to 24 knots Div3 and 4 now combined at Ron2 to force them to move as one unit
# it is expected that all battle formations will move two moves forward so that cruisers and destroyers can turn away earlier to avoid
# being engaged by otherwise target free battleships
# note all green formations travelling at 21 knots at end of last move, some increasing to 24 this move then 27 and 30 in the subsequent moves
# red formations are travelling at 15 knots at end of last move because RB1 is limited to that speed due to damage
# because Red is Morale 1 and Green Morale 3, the Red units can't respond to movement of the Green Battle Rons for 2 moves
# Red Cru/Des divs are using smoke screens to block fire to red BB until they are at close range so won't respond to Green light div moves
# red des odd numbers on both sides will start a smoke screen just before first BB get into range, this lasts 4 moves and will lay where it is laid as there is no wind
# red des even numbers will take over on move 5 after BB units reach engagement range and continue (max 4) until ordered to desist by Red Admiral.
# the RearDiv doesn't expect to get into combat but are in place in case any Red light forces attempt to attack the rear of either battle squadron
# note, facing is the facing of the lead ship in the formation, following ones may have a different facing, added so the user can see which way they face
FORMATIONS = {"GBatRon1":{"currspd":21,"step":3,"bestspd":21,"b4turn": 0,"straight":8,"move":"A21","facing":0,"ships":["GB10","GB11","GB12","GB13","GB9","GB14","GB15","GB8"]},
              "GBatRon2":{"currspd":21,"step":3,"bestspd":24,"b4turn": 0,"straight":8,"move":"A24","facing":0,"ships":["GB1","GB7","GB2","GB5","GB4"]},
              "RBatDiv1":{"currspd":15,"step":3,"bestspd":21,"b4turn": 0,"straight":8,"move":"A18","facing":4,"ships":["RB2","RB4","RB5","RB6","RB7","RB8","RB3","RB1"]},
              "GCruDiv1a":{"currspd":21,"step":6,"bestspd":30,"b4turn": 0,"straight":6,"move":"S24","facing":0,"ships":["GCr21","GCr23"]},
              "GCruDiv1b":{"currspd":21,"step":6,"bestspd":30,"b4turn": 0,"straight":6,"move":"A24","facing":0,"ships":["GCr22","GCr24"]},
              "GDesRon1":{"currspd":21,"step":6,"bestspd":30,"b4turn": 0,"straight":6,"move":"A16S8","facing":0,"ships":["GCr39","GDH1","GDH2","GDH3","GDH4","GDH5","GDH6","GDH7","GDH8"]},
              "GDesRon2":{"currspd":21,"step":6,"bestspd":30,"b4turn": 0,"straight":6,"move":"A24","facing":0,"ships":["GCr25","GDH9","GDH10","GDH11","GDH12","GDH13","GDH14","GDH15","GDH16"]},
              "GRearDiv":{"currspd":21,"step":6,"bestspd":21,"b4turn": 0,"straight":6,"move":"A21","facing":0,"ships":["GCr36","GDH17","GDH18","GDH19","GDH20","GCr1"]},
"RCru1":{"currspd":15,"step":6,"bestspd":30,"b4turn": 0,"straight":6,"move":"A18","facing":4,"ships":["RC1","RC2"]},
"RCru2":{"currspd":15,"step":6,"bestspd":30,"b4turn": 0,"straight":6,"move":"A18","facing":4,"ships":["RC3","RC4"]},
"RDesRon1":{"currspd":15,"step":6,"bestspd":30,"b4turn": 0,"straight":4,"move":"A18","facing":4,"ships":["RD1","RD2","RD3","RD4","RD5","RD6","RD7","RD8"]},              
"RDesRon2":{"currspd":15,"step":6,"bestspd":30,"b4turn": 0,"straight":4,"move":"A18","facing":4,"ships":["RD9","RD10","RD11","RD12","RD13","RD14","RD15","RD16"]},
"sunk":{"currspd":0,"step":0,"bestspd":0,"b4turn": 0,"straight":0,"move":" ","facing":0,"ships":[]}              
}
# the ship list, includes both sides, locn is the current location of that ship, showing angle of facing, and position x and y.
# turn_points is a list of points where the lead ship of the formation turned and where the following ships need to turn
# main is the info for the main guns, its target, its calibre(*), the number of guns firing forwards(*), to the side(*) and aft(*), range to the target, rangeband,
# arc is the angle of the target from the firer rounded to the nearest degree to choose between the fore/mid/aft number of guns (45-135 is mid)
# xingt is the angle in degrees of the firer from the target for Crossing T calculations where direction of travel is zero
# note starred items (*) are fixed for the duration of the battle, all other items are calculated and may have presets such as locn and targ.
# straddle is 0 or -5 and indicates if the ship achieved a straddle (includes a hit) last turn (-5)
# tntime is 0 to 8 to indicate how many moves the ship has fired at the target. 0 is for the first move of firing, it is incremented every consequetive time the ship fires and reduced if a shot is missed
#    or an adjacent ship is targeted - reduced twice if the second ship away is targeted, etc
# tndamage is 0, 2, 4, etc for each damage block that has at least 1 point of damage in it, if a 22 size block receives 48 damage, 2 blocks will be full and 4 points in the 3rd - the tndamage=4
#    (and speed will be reduced by 6)
# blocksize is the amount of damage a ship can take before a damage block is full
# currblock is the current block that is being filled
# blockfill is the amount of damage in that block, if it is > 0 then the effect of that block will take place
#    a ship with a blocksize of 22 takes two 24 point hits, so block 0 and 1 are full and there is 4 in block 2 (currblock=2,blockfill=4, tndamage will be reduced by 4 and dsgnspd reduced by 6, ie RB1)
#    a ship with a blocksize of 24 takes two 24 point hits, so block 0 and 1 are full and there is 0 in block 2 (currblock=2,blockfill=0, tndamage will be reduced by 2 and dsgnspd reduced by 3)
#    a ship with a blocksize of 18 takes three 24 point hits, so blocks 0 to 3 are full and there is 0 in block 4 (currblock=4,blockfill=0, tndamage will be reduced by 6 and dsgnspd reduced by 9)
SHIPS = {"GB1":{"locn":[0,942,63],"formation":"GBatRon2","turn_points": [],'dsgnspd':24,'currspd':21,'belt':13,'deck':2.5,'main': {"targ":"RB7","calibre":"LM","fore":4,"mid":12,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB2":{"locn":[0,942,63],"formation":"GBatRon2","turn_points": [],'dsgnspd':24,'currspd':21,'belt':13,'deck':2.5,'main': {"targ":"RB8","calibre":"MM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB3":{"locn":[0,0,0],"formation":"","turn_points": [],'dsgnspd':21,'currspd':24,'belt':13,'deck':2.5,'main': {"targ":"","calibre":"MM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB4":{"locn":[0,942,45],"formation":"GBatRon2","turn_points": [],'dsgnspd':24,'currspd':21,'belt':13,'deck':2.5,'main': {"targ":"RB3","calibre":"LM","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB5":{"locn":[0,942,51],"formation":"GBatRon2","turn_points": [],'dsgnspd':24,'currspd':21,'belt':14,'deck':3,'main': {"targ":"RB8","calibre":"LM","fore":4,"mid":12,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB6":{"locn":[0,0,0],"formation":"","turn_points": [],'dsgnspd':21,'currspd':24,'belt':14,'deck':3,'main': {"targ":"","calibre":"MM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB7":{"locn":[0,942,57],"formation":"GBatRon2","turn_points": [],'dsgnspd':24,'currspd':21,'belt':14,'deck':3,'main': {"targ":"RB7","calibre":"MM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB8":{"locn":[0,1049,33],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':14,'deck':3,'main': {"targ":"RB6","calibre":"MM","fore":4,"mid":12,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB9":{"locn":[0,1049,51],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB5","calibre":"MM","fore":4,"mid":14,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB10":{"locn":[0,1049,75],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB2","calibre":"SM","fore":4,"mid":14,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB11":{"locn":[0,1049,69],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB2","calibre":"HM","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB12":{"locn":[0,1049,63],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB4","calibre":"HM","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB13":{"locn":[0,1049,57],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB4","calibre":"HM","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB14":{"locn":[0,1049,45],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB5","calibre":"MM","fore":4,"mid":12,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GB15":{"locn":[0,1049,39],"formation":"GBatRon1","turn_points": [],'dsgnspd':21,'currspd':21,'belt':15,'deck':3,'main': {"targ":"RB6","calibre":"MM","fore":4,"mid":12,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':24,'currblock':0,'blockfill':0},
         "GCr1":{"locn":[0,996,15],"formation":"GRearDiv","turn_points": [],'dsgnspd':21,'currspd':21,'belt':6,'deck':2,'main': {"targ":"","calibre":"GS","fore":3,"mid":6,"aft":3,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':15,'currblock':0,'blockfill':0},
         "GCr21":{"locn":[0,1065,90],"formation":"GCruDiv1a","turn_points": [],'dsgnspd':30,'currspd':21,'belt':5.5,'deck':2,'main': {"targ":"","calibre":"CS","fore":4,"mid":12,"aft":3,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':12,'currblock':0,'blockfill':0},
         "GCr22":{"locn":[0,933,90],"formation":"GCruDiv1b","turn_points": [],'dsgnspd':30,'currspd':21,'belt':5.5,'deck':2,'main': {"targ":"","calibre":"CS","fore":4,"mid":12,"aft":3,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':12,'currblock':0,'blockfill':0},
         "GCr23":{"locn":[0,1065,84],"formation":"GCruDiv1a","turn_points": [],'dsgnspd':30,'currspd':21,'belt':4.5,'deck':2,'main': {"targ":"","calibre":"CS","fore":3,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':12,'currblock':0,'blockfill':0},
         "GCr24":{"locn":[0,933,84],"formation":"GCruDiv1b","turn_points": [],'dsgnspd':30,'currspd':21,'belt':5.25,'deck':2,'main': {"targ":"","calibre":"CS","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':12,'currblock':0,'blockfill':0},
         "GCr25":{"locn":[0,933,78],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':4.5,'deck':2,'main': {"targ":"","calibre":"XS","fore":3,"mid":12,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':10,'currblock':0,'blockfill':0},
         "GCr36":{"locn":[0,996,33],"formation":"GRearDiv","turn_points": [],'dsgnspd':30,'currspd':21,'belt':4.75,'deck':2,'main': {"targ":"","calibre":"XS","fore":3,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':10,'currblock':0,'blockfill':0},
         "GCr39":{"locn":[0,1065,78],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':13,'deck':5.25,'main': {"targ":"","calibre":"CS","fore":3,"mid":15,"aft":3,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':15,'currblock':0,'blockfill':0},
         "GDH1":{"locn":[0,1065,72],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH2":{"locn":[0,1065,69],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH3":{"locn":[0,1065,66],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH4":{"locn":[0,1065,63],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH5":{"locn":[0,1065,60],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH6":{"locn":[0,1065,57],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH7":{"locn":[0,1065,54],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH8":{"locn":[0,1065,51],"formation":"GDesRon1","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH9":{"locn":[0,933,72],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH10":{"locn":[0,933,69],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH11":{"locn":[0,933,66],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH12":{"locn":[0,933,63],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH13":{"locn":[0,933,60],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH14":{"locn":[0,933,57],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH15":{"locn":[0,933,54],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH16":{"locn":[0,933,51],"formation":"GDesRon2","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH17":{"locn":[0,996,27],"formation":"GRearDiv","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH18":{"locn":[0,996,24],"formation":"GRearDiv","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH19":{"locn":[0,996,21],"formation":"GRearDiv","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "GDH20":{"locn":[0,996,18],"formation":"GRearDiv","turn_points": [],'dsgnspd':30,'currspd':21,'belt':0,'deck':0,'main': {"targ":"","calibre":"SS","fore":2,"mid":7,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':6,'currblock':0,'blockfill':0},
         "RB1":{"locn":[4,1056,475],"formation":"RBatRon1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':12,'deck':4,'main': {"targ":"GB15","calibre":"MM","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':22,'currblock':2,'blockfill':4},
         "RB2":{"locn":[4,1056,433],"formation":"RBatRon1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':12,'deck':4,'main': {"targ":"GB10","calibre":"MM","fore":4,"mid":10,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':22,'currblock':0,'blockfill':0},
         "RB3":{"locn":[4,1056,469],"formation":"RBatRon1","turn_points": [],'dsgnspd':27,'currspd':15,'belt':9,'deck':2.5,'main': {"targ":"GB15","calibre":"MM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':18,'currblock':4,'blockfill':0},
         "RB4":{"locn":[4,1056,439],"formation":"RBatRon1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':11,'deck':4,'main': {"targ":"GB11","calibre":"LM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':22,'currblock':0,'blockfill':0},
         "RB5":{"locn":[4,1056,445],"formation":"RBatRon1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':10,'deck':3,'main': {"targ":"GB12","calibre":"LM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':22,'currblock':0,'blockfill':0},
         "RB6":{"locn":[4,1056,451],"formation":"RBatRon1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':10,'deck':4,'main': {"targ":"GB13","calibre":"LM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':22,'currblock':0,'blockfill':0},
         "RB7":{"locn":[4,1056,457],"formation":"RBatRon1","turn_points": [],'dsgnspd':24,'currspd':15,'belt':6,'deck':2.5,'main': {"targ":"GB9","calibre":"LM","fore":4,"mid":6,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':16,'currblock':0,'blockfill':0},
         "RB8":{"locn":[4,1056,463],"formation":"RBatRon1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':11,'deck':3,'main': {"targ":"GB14","calibre":"LM","fore":4,"mid":8,"aft":4,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':22,'currblock':0,'blockfill':0},
         "RC1":{"locn":[4,1047,439],"formation":"RCru1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':0,'deck':2,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':8,'currblock':0,'blockfill':0},
         "RC2":{"locn":[4,1047,460],"formation":"RCru1","turn_points": [],'dsgnspd':21,'currspd':15,'belt':0,'deck':2,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':8,'currblock':0,'blockfill':0},
         "RC3":{"locn":[4,1065,439],"formation":"RCru2","turn_points": [],'dsgnspd':21,'currspd':15,'belt':0,'deck':2,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':8,'currblock':0,'blockfill':0},
         "RC4":{"locn":[4,1065,460],"formation":"RCru2","turn_points": [],'dsgnspd':21,'currspd':15,'belt':0,'deck':2,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':8,'currblock':0,'blockfill':0},
         "RD1":{"locn":[4,1047,433],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD2":{"locn":[4,1047,439],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD3":{"locn":[4,1047,445],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD4":{"locn":[4,1047,451],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD5":{"locn":[4,1047,457],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD6":{"locn":[4,1047,463],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD7":{"locn":[4,1047,469],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD8":{"locn":[4,1047,475],"formation":"RDesRon1","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD9":{"locn":[4,1074,433],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD10":{"locn":[4,1074,439],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD11":{"locn":[4,1074,445],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD12":{"locn":[4,1074,451],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD13":{"locn":[4,1074,457],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD14":{"locn":[4,1074,463],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD15":{"locn":[4,1074,469],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
         "RD16":{"locn":[4,1074,475],"formation":"RDesRon2","turn_points": [],'dsgnspd':30,'currspd':15,'belt':0,'deck':0,'main': {"targ":"","calibre":"XS","fore":2,"mid":5,"aft":2,"range":0,"rangeband":'Bynd',"arc":0,"xingt":0,"time":0,'straddle':0},'firedat':-5,'blocksize':2,'currblock':0,'blockfill':0},
}

SUNK_SHIPS = {}

TNRANGESPD = {'PB  ': [0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15],
              'Clo ': [2, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20],
              'Mid ': [5, 8, 8, 9, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24],
              'Long': [9, 12, 12, 13, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 28],
              'Extr': [14, 17, 17, 18, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 33]}

BELTDECK = {'PB  ': 2, 'Clo ': 4, 'Mid ': 6, 'Long': 8, 'Extr': 10}

TNTIME = [5, 3, 1, 0, -1, -2, -3, -4, -5]


class FieldTypes:
    string = 1
    string_list = 2
    iso_date_string = 3
    long_string = 4
    decimal = 5
    integer = 6
    boolean = 7
    roman_date_string = 8
    int_list = 9
