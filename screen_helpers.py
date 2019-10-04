# file contains methods for writing to and from screen 
from shape_reader import * 


################### UPDATING THE GAME

# DESCRIPTION 
## given list representation of buffered window, updates each cell
# ARGUMENTS 
## info := list, representation of buffered window 
## rules := list of length 4; see arguments of method `update`
# RETURN 
# updated list representation of buffered window    
def update_info(info, rules): 
    newInfo = [] 

    for j in range(len(info)):
        newRow = []  
        for i in range(len(info[j])):
            n = get_num_neighbors(info, i, j)

            if info[j][i] == 'o': 
                if n >= rules[1][0] and n <= rules[1][1]: 
                    newRow.append('o') 
                else: 
                    newRow.append('.') 
            else: 
                if n == rules[3]: 
                    newRow.append('o') 
                else: 
                    newRow.append('.') 
                      
        newInfo.append(newRow) 
    return newInfo 

# DESCRIPTION 
## updates one generation of board 
# ARGUMENTS 
## screen := object to read/write 
## rules := by default, Conway's, an int. list of the form 
##          [< underpop, range(live), > overpop, == reprod]            
# RETURN 
## array of n x m characters
def update(screen, mode = '1', rules = [2, [2, 3], 3, 3]): 

    info = screen_to_list(screen) # get list repr. of screen             

    if mode == '1' or mode == '2': 
        d = get_biggest_dim(mode) ## get buffered screen 
    else: 
        d = mode
    
    bufferedInfo = get_buffered_screen(info, d) ## 
    bufferedUpdate = update_info(bufferedInfo, rules) # update this buffered screen 
    newInfo = parse_buffer(bufferedUpdate, d) ## parse the results 

    # copy the results to screen 
    for j in range(len(newInfo)):
        for i in range(len(newInfo[j])): 
            try: 
                screen.addstr(j, i, newInfo[j][i])
            except curses.error: pass
 
################## screen-list conversions 

# DESCRIPTION 
## returns a list of strings, s.t. each string corresponds to a row on curses screen 
# ARGUMENTS 
## screen := type<curses.window>
def screen_to_list(screen):
    (screenHeight, screenWidth) = screen.getmaxyx() 
    info = [] 
    
    for j in range(screenHeight):
        s = screen.instr(j, 0)
        s = s.decode('utf-8') 
        info.append(list(s))

    return info

# DESCRIPTION 
## given screen and new screen (argument : info), copies new screen to screen 
# ARGUMENTS 
## screen := type<curses.window> 
## info := list<str> 
# RETURN 
## none 
def list_to_screen(screen, info):
    screen.clear()
    (screenHeight, screenWidth) = screen.getmaxyx() 

    for j in range(len(info)):
        s = ''.join(info[j])
        try:  
            screen.addstr(j, 0, info[j]) 
        except: 
            pass

# DESCRIPTION 
## constructs initial board, that consists of all periods. 
def construct_initial_board(screen): 
    screen.clear() 
    (screenHeight, screenWidth) = screen.getmaxyx() 

    s = "." * screenWidth 
    for j in range(screenHeight):
        try:  
            screen.addstr(j, 0, s) 
        except: pass 

# DESCRIPTION 
## reconstructs a game based on mode 1 (choice 1) or mode 2 (choice 2) 
def reconstruct(screen, mode = '1'): 

    screen.clear() 
    screenHeight, screenWidth = screen.getmaxyx() 
 
    # construct empty screen   
    construct_initial_board(screen)

    ##screen_loop(screen)
    if mode == '1':
        if OCCUPIED_SPACES == []: return 
        OC = copy.deepcopy(OCCUPIED_SPACES) 
    else: 
        if OCCUPIED_SPACES_CREATE == []: return 
        OC = copy.deepcopy(OCCUPIED_SPACES_CREATE) 

    # add shapes 
    if mode == '1': 
        for k, v in EXISTING_SHAPES.items(): 
            for shape in v:
                for coord in shape:  
                    if coord in OC: 
                        OC = remove_helper(OC, coord)     
                    screen.addstr(coord[0], coord[1], 'o')   
    else: 
        for k, v in EXISTING_SHAPES_CREATE.items(): 
            for shape in v:
                for coord in shape:  
                    if coord in OC: 
                        OC = remove_helper(OC, coord)     
                    screen.addstr(coord[0], coord[1], 'o') 
        
    # add occupied spaces
    for coord in OC:
        try: 
            screen.addstr(coord[0], coord[1], 'x', curses.color_pair(5)) 
        except: pass     
    screen.move(0, 0)
        
####################################### 

# DESCRIPTION 
## adds frame of width `bufferSize` to list representation of screen, `info` 
# ARGUMENTS 
## info := list, representation of window 
## bufferSize := int, width of buffer 
## character := str, filler for buffer 
# RETURN 
## list representation of screen with width 
def get_buffered_screen(info, bufferSize, character = '.'): 
    lenRow = len(info[0]) + 2 * bufferSize # new length of row 

    emptyRow = [character for i in range(lenRow)] # empty row of buffers 
    bufferOther = [character for i in range(bufferSize)] # buffer on each side for all other rows  
 
    newInfo = [] 
    for i in range(bufferSize): 
        newInfo.append(emptyRow) 

    for i in range(len(info)): 
        s = bufferOther + info[i] + bufferOther 
        newInfo.append(s)

    for i in range(bufferSize): 
        newInfo.append(emptyRow) 
    return newInfo  

# DESCRIPTION
## given a cell at position (j, i) in screen (info), determines the number of neighbors
## ;max is 8 
# ARGUMENTS 
## info := n x m array, list representation of curses window
## i, j := integers for (x, y) position 
# RETURN 
## int
def get_num_neighbors(info, i, j):
    n = 0

    if j > 0: 
        if info[j - 1][i] == 'o': n += 1 # top 
    if i > 0: 
        if info[j][i - 1] == 'o': n += 1 # middle left 
    if j > 0 and i > 0: 
        if info[j - 1][i - 1] == 'o': n += 1 # top left
    if j < len(info) - 1: 
        if info[j + 1][i] == 'o': n += 1 # bottom 
    if j < len(info) - 1 and i > 0: 
        if info[j + 1][i -1] == 'o': n += 1 # bottom left 
    if j < len(info) -1 and i < len(info[0]) - 1: 
        if info[j + 1][i + 1] == 'o': n += 1 # bottom right 
    if i < len(info[0]) - 1: 
        if info[j][i+ 1] == 'o': n += 1 # right 
    if j > 0 and i < len(info[0]) - 1: 
        if info[j -1][i + 1] == 'o': n += 1 # upper right                  
    return n 

# DESCRIPTION 
## `cuts` off the buffered frame used for updating objects that might go off-screen 
# ARGUMENTS 
## bufferedInfo := screen with empty values on all four edges 
## bufferSize := width of the buffer frame around screen 
# RETURN 
## list, representation of screen, original size 
def parse_buffer(bufferedInfo, bufferSize): 
    newInfo = [] 

    bufferedInfo = bufferedInfo[bufferSize:] # remove top 
    bufferedInfo = bufferedInfo[:-bufferSize] # remove bottom 

    for i in range(len(bufferedInfo)): 
        s = bufferedInfo[i] 
        s = s[bufferSize:] # remove left side 
        s = s[:-bufferSize] # remove right side             
        newInfo.append(s)
    return newInfo

# TODO : max input
def input_screen(screen, msg):
    display_message(screen, msg)

    maxY, maxX = screen.getmaxyx() 
    inp = None 
    startY = len(msg) + 1
    startX = 0

    text = "" 
    curses.echo()     
    while inp != ord("\n"):
        inp = screen.getch()
            
        if inp == curses.KEY_BACKSPACE: 
            onScreen = screen.instr(0, 0).decode().strip() 
            onScreen = onScreen[:-1]
            display_message(screen, msg) 
            screen.addstr(0, 0, onScreen)
        elif inp in EXCLUDED: continue

    curses.echo(False)
    text = screen.instr(0, 0).decode().strip()
    return text  

# DESCRIPTION 
## for option 2, saves game to specified file 
def save_game(screen):
    info = screen_to_list(screen)
    # clear screen and get file name
    s1 = "SAVE GAME TO FILE :\t"
    gameTitle = input_screen(screen, [s1])
    if gameTitle == "": save_game(screen) 

    # file has already been taken
    path = gamesPath + gameTitle  
    if os.path.exists(path) is True: 
        screen.addstr("FILE HAS ALREADY BEEN TAKEN. OVERWRITE? Y N") 
        
        while True: 
            inp = screen.getch() 
            if inp == ord('y'): 
                break 
            elif inp == ord('n'): 
                return save_game(screen)

    f = open(path, 'wb')
    biggestDim = get_biggest_dim(mode = '2')
    pickle.dump((info, biggestDim), f)
    POSSIBLE_GAMES.append(gameTitle)

# DESCRIPTION 
## to be used alongside `open_game` to calibrate stored game size into 
## current terminal size 
def parse_saved_game(screen, info): 
    maxY, maxX = screen.getmaxyx() 
    dX = len(info[0]) - maxX 
    dY = len(info) - maxY 

    ## fit x-dimension
    # saved game greater  
    if dX > 0: 
        for i in range(len(info)): 
            info[i] = info[i][:-dX]
    # saved game less than 
    elif dX < 0: 
        a = ["."] * (-dX) 
        for i in range(len(info)):
            info[i] = info[i] + a 
        
    ## fit y-dimension 
    # saved game greater than screen, shrink 
    if dY > 0:
        info = info[:-dY]
    # saved game less than screen, grow 
    elif dY < 0:  
        s = ["."] * maxX
        for i in range(-dY): 
            info.append(s)

    # join each element in info
    for i in range(len(info)): 
        info[i] = ''.join(info[i])

    return info # TODO 1

# DESCRIPTION 
## opens game of corresponding `gameTitle`
def open_game(gameTitle): 
    path = gamesPath + gameTitle 

    if os.path.exists(path) is False: 
        return False
     
    f = open(path, 'rb')
    info, biggestDim = pickle.load(f)
    return info, biggestDim

############# SCROLL-DOWN MENU 
# DESCRIPTION
## helper for converting shape str to display text on screen
def name_to_text(shape):
    return "[ ]\t{}".format(shape)

# DESCRIPTION
## helper for converting retrieved screen line into shape
def bytes_to_name(bytes):
    text = bytes.decode().strip() 

    x = re.search(" ", text[::-1])
    # case no space 
    if x is None: 
        return text 
    i = x.span()[0] 
    shape = text[::-1][:i][::-1]
    if shape == '': return False 
    return shape

def display_options_helper(screen, actualY, title, options): 
    # reset screen and gather pertinent variables
    screen.clear()
    (screenHeight, screenWidth) = screen.getmaxyx()
    startX = int((screenWidth // 2) - (len(title) // 2) - len(title) % 2)

    # cursor is not past screen
    if actualY < screenHeight:
        screen.addstr(0, startX, title)  # title
        for i in range(len(options)):  # all other shapes
            # more shapes than screen
            if i + 1 >= screenHeight:
                break
            screen.addstr(i + 1, 0, \
                          name_to_text(options[i]))
        screen.move(1, 1)
    else:
        startX = 0
        for i in range(screenHeight):
            si = actualY + i - screenHeight + 1
            if si >= len(options):
                break
            screen.addstr(i, startX, \
                          name_to_text(options[si]))

            # move cursor back to origin
        screen.move(0, 1)

# DESCRIPTION 
## displays options in a scrol down menu 
# ARGS 
## toDisplay := 'S' for shape, 'G' for game 
def display_options(screen, title, toDisplay = 'S'):
    # choose list 

    if toDisplay == 'S': 
        opt = copy.deepcopy(POSSIBLE_SHAPES)
    elif toDisplay == 'G': 
        opt = copy.deepcopy(POSSIBLE_GAMES)
    else: 
        raise ValueError("Wrong option")

    screenY, actY = 0, 0
    display_options_helper(screen, actY, title, opt)

    screen.move(1, 1)
    screenY, actY = 1, 1

    inp = True
    screenHeight = screen.getmaxyx()[0]

    while True:
        inp = screen.getch()

        # done creating --> run
        if inp == ord('d'):
            return True

        # done with mode
        elif inp == ord('q'):
            return -1

        # choose a shape
        if inp == ord('\n'):
            choice_ = screen.instr()
            choice = bytes_to_name(choice_)
            if choice is not False:
                break

                # arrow key down
        elif inp == curses.KEY_DOWN:
            # actual y also inc.
            actY += 1
            # if greater than height then needs change
            display_options_helper(screen, actY, title, opt)

            # if cursor less than height, move down
            if screenY < screenHeight - 1:
                screenY += 1
                screen.move(screenY, 1)

        # arrow key up
        elif inp == curses.KEY_UP:
            actY -= 1
            display_options_helper(screen, actY, title, opt)
            if screenY > 0:
                screenY -= 1
                screen.move(screenY, 1)
    return choice

####### COMMON METHODS FOR MESSAGES AND LOOPS
def display_message(screen, messageList):
    screen.clear()  
    (screenHeight, screenWidth) = screen.getmaxyx() 
    startY = int(screenHeight // 2) - 4 

    for s in messageList:
        startX = int((screenWidth // 2) - (len(s) // 2) - len(s) % 2)   
        try: 
            screen.addstr(startY, startX, s) 
            startY += 1
        except curses.error: 
            pass
    screen.move(0, 0)
    
    #### 2 variations for this loop 
def screen_loop(screen, term = ord('\n')): 
    inp = None
    while inp != term: 
        inp = screen.getch()

# TODO clean up 
def screen_loop_return(screen, retList, term = ord("\n")):  
    inp = None
    if term == None: 
        while True: 
            inp = screen.getch() 
            if inp in retList: 
                return inp

    while inp != term: 
        inp = screen.getch() 
        if inp in retList: 
            return inp

