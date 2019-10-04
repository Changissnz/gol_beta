'''
file contains pertinent methods for cleaning data folders of any 
user-specified item (shape or world) 
'''
from screen_helpers import * 

# DESCRIPTION 
## cleans folders and logs of arg `item` (string) 
# TODO : will not show msg if does not exist
def clean_data_helper(item, mode = 'S'):

    # using global 
    global POSSIBLE_SHAPES 
    global POSSIBLE_GAMES

    # filter variable    
    # delete from data folder 
    # delete from classification path 

    # shapes 
    if mode == 'S':     
        
        # # TODO simplify
        j = None  
        for i in range(len(POSSIBLE_SHAPES)): 
            if POSSIBLE_SHAPES[i] == item: 
                j = i 
                break 
        if j is not None: 
            POSSIBLE_SHAPES.pop(j) 

            PAT =  currentPath + "/shapes/" + item + ".txt"
            os.remove(PAT)
            delete_shape(item) 
    # game 
    elif mode == 'G': 
        # item does not exist 
        j = None  
        for i in range(len(POSSIBLE_GAMES)): 
            if POSSIBLE_GAMES[i] == item: 
                j = i 
                break 
        if j is not None: 
            POSSIBLE_GAMES.pop(j) 
            PAT =  gamesPath + item
            os.remove(PAT)

    return

# DESCRIPTION 
## main method for choice 
def clean_data(screen): 

    display_message(screen, INTRO_5)
    S = input_screen(screen, ASK_SHAPE)
    
    display_message(screen, ASK_TYPE)
    inp = None
    retList = [ord('1'), ord('2')] 
    T = screen_loop_return(screen, retList, term = None) 
    if T == ord('1'): 
        T = 'S' 
    else: 
        T = 'G' 

    clean_data_helper(S, mode = T)
    return 

