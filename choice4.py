from screen_helpers import * 

# TODO : scroll-down menu, message menu 
# DESCRIPTION
## gives a description of chosen shape 
def description_of_shape(screen, choice, indent = 4):     
    screen.clear() 

    coords = reader(choice)         
    clf = get_shape_classification(choice)
    s1 = "* Illustration"
    s2 = "* number of coordinates : {}".format(len(coords))
    s3 = "* classification of coordinate : {}".format(clf) 

    startY = 0 
    screen.addstr(startY, 0, s1)
    startY += 2
    startY = sample_image(screen, coords, startY, indent)
    startY += 2
    screen.addstr(startY, 0, s2)
    startY += 2
    screen.addstr(startY, 0, s3)

    inp = None 
    while inp != ord('\n'): 
        inp = screen.getch() 
    return

# DESCRIPTION
## gives a description of chosen shape 
def description_of_game(screen, choice): 
    
    info, dim = open_game(choice)
    info = parse_saved_game(screen, info) # TODO attention funky 

    #TODO : make method 
    list_to_screen(screen, info)

    inp = None
    screen.nodelay(True) 
    while inp != ord('q'):
        inp = screen.getch() 
        update(screen, dim)
        time.sleep(0.8)
    return

# DESCRIPTION 
## helper for showing description of image 
def sample_image(screen, coords, startY, startX): 
    for c in coords:  
        x = [c[0] + startY, c[1] + startX]
        try:  
            screen.addstr(x[0], x[1], "o")
        except curses.error: 
            pass
    return x[0] 
     
# DESCRIPTION 
## main method for choice 4 
def browse_library(screen): 
    display_message(screen, INTRO_4)
    retList = [ord('1'), ord('2'), ord('q')] 
    opt = screen_loop_return(screen, retList)

    # browse games 
    if opt == ord('1'): 
        title = "AVAILABLE GAMES"
        choice = display_options(screen, title, "G") 
        if choice == -1 or choice is True: 
            return
        description_of_game(screen, choice)
        return

    # browse shapes  
    elif opt == ord('2'): 
        title = "AVAILABLE SHAPES"
        choice = display_options(screen, title, "S")
        if choice == -1 or choice is True: 
            return # TODO 
        description_of_shape(screen, choice) 
    # quit 
    else: 
        return 
    # continue browsing 
    browse_library(screen)

