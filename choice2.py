'''
file contains pertinent methods for choosing shapes and their locations 
for your world that you can save
'''

from screen_helpers import * 
import math 

def determine_shapes_and_loc(screen): 
    # introduction 
    display_message(screen, INTRO_2) 
    screen_loop(screen) 

    # world creation 
    while True: 
        # choose from scroll-down 
        choice = display_options(screen, SHAPE_TITLE1, toDisplay = 'S') 

        # done creating, run game 
        if choice is True: 
            break
        # done with mode : early quit 
        elif choice == -1: 
            reset_world() 
            return 
        success = add_one(screen, choice)
     
    # run game 
    reconstruct(screen, '2') 
    inp = None 
    screen.nodelay(True) 
    while inp != ord('q'): 
        inp = screen.getch()
        if inp == ord('s'): 
            save_game(screen)
            break 

        update(screen, '2') 
        time.sleep(0.5) 
    reset_world() 

def reset_world(): 
    OCCUPIED_SPACES_CREATE.clear() 
    k = list(EXISTING_SHAPES_CREATE.keys()) 
    for k_ in k: 
        del EXISTING_SHAPES_CREATE[k_] 

def add_one(screen, shape): 

    screen.clear()
    screenHeight, screenWidth = screen.getmaxyx() 

    reconstruct(screen, '2')  
    screen.move(0, 0) 

    # now user can input center of origin 
    inp = None
    origin = None 

    status = True 

    while True:
        inp = screen.getch() 
        y, x = screen.getyx() 
        #raise ValueError(y, screenHeight)

        if inp == curses.KEY_DOWN: 
            if y < screenHeight - 1: 
                y += 1 
                screen.move(y, x) 

        elif inp == curses.KEY_UP: 
            if y > 0: 
                y -= 1 
                screen.move(y, x) 

        elif inp == curses.KEY_RIGHT:  
            if x < screenWidth -1: 
                x += 1 
                screen.move(y, x) 

        elif inp == curses.KEY_LEFT:  
            if x > 0: 
                x -= 1 
                screen.move(y, x) 

        elif inp == ord('\n'): 
            origin = (y, x) 

            # retrieve coordinates of new shape
            coords = get_shape_coordinates(shape, origin,\
                    (screenHeight, screenWidth),\
                    OCCUPIED_SPACES_CREATE, EXISTING_SHAPES_CREATE) 

            # draw shape
            if type(coords) is list:
                draw_shape(screen, coords) 
                break 

            elif type(coords) is tuple:
                draw_shape(screen, coords[0])
                break    

            else:
                status = False 
                flash(screen) 
                return status 
    time.sleep(0.5) 
    return status
            
# TODO refactor
def flash(screen):
    screen.clear()

    screenHeight, screenWidth = screen.getmaxyx() 

    msg = "_ERROR-PRESS-ENTER_" 
    ERROR = (msg * math.ceil(screenWidth / len(msg)))[:screenWidth] 
    for y in range(screenHeight): 
        try: 
            screen.addstr(y, 0, ERROR) 
        except curses.error: pass

    screen_loop(screen)
