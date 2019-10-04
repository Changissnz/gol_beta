'''
file contains pertinent methods for creating, classifying, and
storing custom shape
'''

from screen_helpers import * 

def make_custom_shape(screen):
    # two screens 
    # screen 1: read out instructions 
    # screen 2 : draw with cursor 

    # instructions 
    display_message(screen, INTRO_3) 
    screen_loop(screen)  

    # create board
    inp = None 
    construct_initial_board(screen) 

    (screenHeight, screenWidth) = screen.getmaxyx()
    currX, currY = 0, 0 

    info = None 

    u = False # used to make sure creation is not empty 
    while True:
        inp = screen.getch()

        if inp == curses.KEY_DOWN: 
            if currY < screenHeight: 
                currY += 1 
                screen.move(currY, currX) 

        elif inp == curses.KEY_UP: 
            if currY > 0: 
                currY -= 1
                screen.move(currY, currX) 
  
        elif inp == curses.KEY_LEFT: 
            if currX > 0: 
                currX -= 1  
                screen.move(currY, currX) 

        elif inp == curses.KEY_RIGHT: 
            if currX < screenWidth: 
                currX += 1  
                screen.move(currY, currX) 

        elif inp == ord(' '):
            screen.addstr(currY, currX, 'N')
            u = True
        elif inp == ord('\n'): 
            info = screen_to_list(screen)
            break            

    screen.clear()
    if u is False: return 
 
    # save screen 
    save_shape(screen, info)

def save_shape(screen, info):
    # show msg 
    shape = input_screen(screen, SAVE_MSG)
    # try writing to file  
    saveBool = write_shape_to_file(shape, info) 
    if saveBool is False:
        display_message(screen, SHAPE_ERR)
        screen_loop(screen)
        save_shape(screen, info)
    else: 
        shapeCoord = get_nonnull_coords(info)
        c = classify_new_shape(screen.getmaxyx(), shapeCoord)  
        record_new_shape(shape, c)


# DESCRIPTION 
## helper method for below 
def get_test_screen(extremes, shapeCoord): 
    T = [] 
    for i in range(extremes[0]): 
        T.append(['.' for j in range(extremes[1])]) 

    for s in shapeCoord: 
        T[s[0]][s[1]] = 'o'

    return T

# DESCRIPTION 
## procedure: gets test screen, loops until all coordinate configurations have been
## accounted for, used for classification 
def test_update(extremes, shapeCoord, rules = [2, [2, 3], 3, 3]): 

    allCoords = [sorted(shapeCoord)]
    # gets test screen 

    # gets biggest dimension
    while True:
        # get biggest dimension of current shape 
        dy = get_max(shapeCoord, 1)
        dx = get_max(shapeCoord, 0)
        D = max(dy, dx) 
        ##D = max(get_max(shapeCoord, 1), get_max(shapeCoord, 0))    
        testScreen = get_test_screen(extremes, shapeCoord) # get base screen 
        ##raise ValueError("SHAPE COORD : {}".format(shapeCoord))
        bufferedInfo = get_buffered_screen(testScreen, D) # add buffer
        bufferedUpdate = update_info(bufferedInfo, rules) #
        q = get_nonnull_coords(bufferedUpdate)

        # empty coords: 
        if q == []: 
            return len(allCoords) + 1 

        q2 = sorted(scale_coords_to_origin(q))
        # spaceship : same formation, different coordinates 
        if q2 in allCoords and q not in allCoords: 
            return 'spaceship' 

        # check coords for existence in `allCoords`
        if q2 in allCoords: 
            return len(allCoords)             
        else:
            allCoords.append(q2) 
            shapeCoord = q2

    return len(allCoords) 

# DESCRIPTION 
## classifies shape according to periods. 
def classify_new_shape(extremes, shapeCoord):

    q = test_update(extremes, shapeCoord)
    if q == 'spaceship': 
        return q 
    elif q == 1: 
        return 'still_life'
    else: 
        return 'oscillator'
