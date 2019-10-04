'''
main file for 5 choices 
'''
from choice1 import * 
from choice2 import * 
from choice3 import * 
from choice4 import * 
from choice5 import * 

get_possible_shapes()
get_possible_games()

def run_life(screen):
    curses.start_color() 
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    screen.clear() 

    ##main_intro(screen)
    display_message(screen, INTRO) 

    # reset cursor to origin
    screen.move(0, 0)

    while 1: 
        # get input 
        choice = screen.getch() 

        # break out of loop if input is valid 
        if choice == ord('1') or choice == ord('2') or choice == ord('3') or choice == ord('4') or choice == ord('5') or choice == ord('q'): 
            break 

    if choice == ord('1'): 
        random_assign(screen, None)
        
    elif choice == ord('2'): 
        determine_shapes_and_loc(screen)

    elif choice == ord('3'): 
        make_custom_shape(screen)

    elif choice == ord('4'): 
        browse_library(screen)

    elif choice == ord('5'): 
        clean_data(screen)

    if choice == ord('q'): return         
    run_life(screen)


curses.wrapper(run_life) 

