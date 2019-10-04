# file contains helpers for game of life 

import curses
import random
import os 
import re
import time 
import pickle

random.seed() 

# master path 
currentPath = os.getcwd()

# file used for obtaining classifications of file 
classificationPath = currentPath + "/shapes/classif.txt" # TODO! check existence 

# folder used for saving games to 
gamesPath = currentPath + "/games/"

# DESCRIPTION 
# in instantiation of game, always check existence for both classificationPath and gamesPath, will create them if accidently deleted. 
def check_existence_data():
 
    # check if classificationPath exists 
    if os.path.exists(classificationPath) is False: 
        if os.path.exists(currentPath + "/shapes/") is False: 
            os.mkdir(currentPath + "/shapes/") 
        f = open(classificationPath, "w")
        D = {"spaceship" : [], "oscillator" : [], "still_life" : []}
        json.dump(D, f, sort_keys = True, indent = 4, ensure_ascii = False)

    # check if gamesPath exists 
    if os.path.exists(gamesPath) is False: 
        os.mkdir(gamesPath)

# create data folders if does not exist 
check_existence_data()
####################

 
# helper for calculating coordinates 
to_int_tuple = lambda L: tuple(int(l) for l in L)  # converts list of type<str> to type<int> 
tuple_to_string = lambda T : ' '.join([str(t) for t in T])

# used for determining extremum of shape 
get_max = lambda coords, index: max([c[index] for c in coords]) 
get_min = lambda coords, index: min([c[index] for c in coords])

# given origin and geometry, calculates exact coordinates of shape 
get_coords = lambda origin, coords: [(origin[0] + c[0], origin[1] + c[1]) for c in coords]    


### USED FOR OPTION 1  
# used for initializing board : want all shapes to be completely on board 
OCCUPIED_SPACES = [] # list of occupied spaces in board

# variable for keeping track of all shapes 
# key := shape 
# value := list of coordinate lists for particular shape 
EXISTING_SHAPES = {}

### USED FOR OPTION 2
OCCUPIED_SPACES_CREATE = [] 
EXISTING_SHAPES_CREATE = {} 

# variable to read all current shapes available for use 
POSSIBLE_SHAPES = []

# variable to read all games available 
POSSIBLE_GAMES = [] 


# DESCRIPTION 
## gets list of saved games 
def get_possible_games(): 
    files = os.listdir(gamesPath)
    POSSIBLE_GAMES.extend(files)
    POSSIBLE_GAMES.sort()


# DESCRIPTION 
# a method for the basic purpose to remove a specified element from a list 
def remove_helper(OCS, coord): 
    j = None 
    for i in range(len(OCS)): 
        if OCS[i] == coord: 
            j = i 
            break 
    return OCS[:i] + OCS[i + 1:]


################## 
# below are the strings used for instructions 
    
    # main introduction
s1 = "WELCOME   PLAYER" 
s2 = "THIS IS A PROGRAM FOR GAME OF LIFE"
s3 = "THIS PROGRAM COVERS ALL ASPECTS OF THE GAME OF LIFE" 
s4 = "CHOOSE OPTION BELOW FOR GAME OF LIFE"
s5 = "   1 : random generation" 
##s6 = "2 : player-determined shapes, random location" # custom and default  
s6 = "\t\t  2 : player-determined shapes and location"
s7 = "   3 : make custom shape"
s8 = "    4 : go to life library"
s9 = "5 : clean up world" 
s10 = ""
    # commands 
s11 = "BELOW ARE SOME VERY USEFUL COMMANDS"
s12 = "q : quit game/mode"
s13 = "spacebar : advance"
INTRO = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13]


    # option 2 introduction
s1 = "INSTRUCTIONS FOR CREATING GAME" 
s2 = "* can choose as many shapes as board will allow *" 
s3 = "* for each addition, player will choose one shape in options *"
s4 = "* player will then choose center point on board for this shape *"
s5 = "* if choice of center point does not work, then screen will flash *"
s6 = "* do not go near blue spaces, these are occupied"
s7 = "* if choice does work, then player can choose another shape or quit *"
s8 = "* IMPORTANT NOTE" 
s9 = "* when player quits, world will run *"
s10 = "* can save game by pressing S *"
s11 = ".......press ENTER to begin......."
INTRO_2 = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]

    # option 3 make custom shape 
s1 = "INSTRUCTIONS ON CREATING CUSTOM SHAPE" 
s2 = "given drawing board, player moves to their targeted blocks using arrow keys"
s3 = "illustration :  < ^ v >"
s4 = "mark target blocks for custom shape by space key ' '" 
s5 = "after construction of custom shape, press enter key ENTER" 
s6 = "yay, you made something! Don't forget to test it out in Life." 
s7 = ".......press ENTER to begin......."
INTRO_3 = [s1, s2, s3, s4, s5, s6, s7]

    # option 4 introduction 
s1 = "WELCOME TO LIFE LIBRARY" 
s2 = "CHOOSE BROWSING OPTION BELOW"
s3 = "1 : games"
s4 = "2 : shapes"
INTRO_4 = [s1, s2, s3, s4]

    # option 5 cleaning data 
s1 = "INSTRUCTIONS FOR CLEANING DATA" 
s2 = "* Input in name of object for the first entry and object type for second"
s3 = "* If you cannot recall the name or type, please refer back to the library" 
INTRO_5 = [s1, s2, s3]
ASK_SHAPE = ["Input item name"]
ASK_TYPE = ["Shape 1 or Game 2"]

    # scroll-down lists
SHAPE_TITLE1 = "SHAPE OPTIONS (press D for done)"

    # restart option for resuming game (option 2)
RESTART_MSG = ["ATTENTION : There is a previous game. Continue 1 Delete 2 ?"]

    # save message 
s1 = "TIME TO SAVE FILE"
s2 = "enter shape name, press enter when done" 
s3 = "(no spaces in shape name allowed!!)"
SAVE_MSG =[s1,s2,s3] 

    # excluded keys for personal input 
EXCLUDED = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_RIGHT, curses.KEY_LEFT, ord("\n")] 

    # error shape
s1 = "ERROR : Shape name and/or shape invalid."
s2 = "Try again. Press ENTER"
SHAPE_ERR = [s1, s2]
##DUP_MSG = ["There is a duplicate file! Overwrite 1 Do Not 2 ?"] 
