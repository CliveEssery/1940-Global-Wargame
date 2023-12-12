==============================
Files in this (Data) directory
==============================

The files in the this directory all describe the contents of the major files in the sub-directories 
in the DATA directory:

Currently only ships.json, formations.json, fleets.json and cities.json are being used, others will 
be added as the coding progresses.

Non-RST file formats have been used for these as with the advent of Libre Office and other free 
office programmes there is no longer a need for a simpler format type in my view.

Each sub-directory below the DATA directory will hold all the data bases relating to a single Nation or variant
of a Nation (eg there might be an ABC Nation and a SlowABC Nation), all Battles in which that 
Nation is the primary player (ie the Battle takes place on their map) and any specific data files
required by the rules to build other data (such as building the Fictional Ships for example).

A Player may only have one sub-directory, unless they want to trial other Nations.

The Referee (if there is one) will have many (at least two) which will be copies of the Player's
current directory.

A Player playing the game Solo will also have multiple directories, at least two but probably four.

Note, json files and Python Dictionaries are formed of key/value pairs where the format is key:value 
and key can be any string or decimal value but must be unique within the file/dictionary.  Value can 
be any item including another dictionary.  The ships description in this directory will give examples 
of how the key can be formed to ensure this uniqueness.