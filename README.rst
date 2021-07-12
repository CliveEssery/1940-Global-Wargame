===================================================
Clive Essery's Fictional 1940 World Wide Campaign
=================================================

Description
===========

I originally intended to publish these rules and the computer game,
but unfortunately I have been diagnosed with a series of TIAs, ie 
mini-strokes and don't know how long I will remain compus mentis  
enough to complete the work.

Hence I have decided to keep the copywrite on all the files and data 
in the Rules directory, but release the software into the Open Source
environment to allow anyone who is interested to play the game.

Anyone may use the data and contents of the Rules directory but cannot sell 
any of that content or make a profit from it, and the content remains mine 
to adjust and modify as I see fit.

The game represents a fictional world with multiple players (or just one) and 
probably a referee and can either be played with pencil/paper and models or 
using the computer programmes included in these directories.  

The game starts on 1st January 1940.

Features
========

Not all features are currently working, and I apolgise for the quality of the
code, I have only started using Python and Tkinter in the last six months.

I intend to add to this code base as and when I get time, as well as the database.

Currently a battle may be fought out between 2 or more fleets, but the code to 
put together the file for the battle is incomplete.  There are known bugs and 
one of the files in the Docs directory lists the bugs that I am aware of.

In addition, I have got the menu option to Build a Formation working, which 
at the moment has no known bugs.  This allows the player to build Formations 
from the ships in their fleet.  I have yet to write the code to build a Fleet
from those formations but that is high up the to do list, as is combining two 
formations that are in the same location, or splitting one formation into two.


Authors
=======

Clive Essery, 2021
Alan D Moore, 2018 for the widget code from his excelling book "Python GUI Programming
with Tkinter" published by Packt (www.packt.com)

Requirements
============

* Python 3
* Tkinter
* widget code from Alan D Moore's book as above

Usage
=====

To start the application, start IDLE, import the my_ww2_rules.py file from the root 
directory and hit the F5 key.

General Notes
=============

At present in the Data directory, there is a directory containing the Neutral 
forces for the Ficticious Fleets version of the game, and the players forces for
the GB1 Nation for that game.  These will need to be combined into one set of files 
and the Build Formation Option used to build the player's formations and fleets.  At
the moment, the players ships contain only a suggested code and the name of the ship,
other data, such as the armour and weapons will have to be added later.

There will ultimately be directories for the GB2, US1, US2, Jap1 and Jap2 Nations 
as well which the Neutral forces will also have to be added.

For the Ficticious Ships version of the game, I have been testing the code using
a Nation based on a slow speed South American - SlowABC.  This includes those ships
that I have designed that are in the primary fleet and the Neutrals that are on the
largest Neutral Island.  This need to be expanded to include the remaining Neutral 
fleets, the remaining SlowABC ships, those on slips or in completion docks in ports
and all other entities for the campaign, such as the Air Forces, Army Forces, possibly 
Railway Trains.  SlowABC also includes the only Battlefile at the moment - until the 
code is written to create this, the player will have to copy that file and hand amend 
it - carefully (see LgIsle-0BAT.json).

Each Data directory currently has a ships.json, a formations.json, a fleets.json and 
a cities.json file that contains all of the relevant info currently being used.  The 
current formats for these files will be described in the root directory of /Data, but 
they will almost certainly be expanded - for example the secondary and tertiary mounts
on each ship is currently not included.

When the Battle code saves a view of the battle, it does so into a file with an ending
of <move number>BAT.json as in the example above.  If you want to have two different 
snapshots of the battle in the same move, then you will need to use some other software
to add extra characters before the ending described above on the first file to be saved,
before the second is saved otherwise the second will overwrite the first
 - eg LgIsle-after move-1BAT.json.  This would be after the ships have moved but before 
the targets have been assigned and firing taken place.

Note also that in the rules directory I have used the convention of placing XXXX as an 
indicator that something (either before or after that marker) needs to be changed or checked.

Note also that the rules for the ground combat doesn't work in the same way that all the 
other rules work and I would like to complete rework them but keeping the positioning information
and the contents of each force.
