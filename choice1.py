'''
file contains pertinent methods for adding random shapes to world, this 
is option 1
'''

from screen_helpers import * 

# ~ 
# DESCRIPTION
## returns list of random shapes, size n 
def get_random_shapes(n): 

    assert POSSIBLE_SHAPES != [], "ERROR : shapes have not been retrieved"
    shapes = [] # list of strings of shape names 
    for _ in range(n): 
        i = random.randrange(len(POSSIBLE_SHAPES)) 
        shapes.append(POSSIBLE_SHAPES[i])
    return shapes 


def random_assign_helper(screen, shape, numShapes): 

    (screenHeight, screenWidth) = screen.getmaxyx() 
        # with specified shape 
    if shape != None: 

        for i in range(numShapes): 
            # TODO add more shapes
            randY, randX = random.randrange(0, screenHeight), random.randrange(0, screenWidth)   
            origin = (randY, randX)

            coords = get_shape_coordinates(shape, origin,\
                (screenHeight, screenWidth), OCCUPIED_SPACES,\
                EXISTING_SHAPES)

            if type(coords) is list:
                draw_shape(screen, coords)
            elif type(coords) is tuple: 
                draw_shape(screen, coords[0])
        # with random shapes   
    else:
        shapes = get_random_shapes(numShapes) 

        for s in shapes: 
            randY, randX = random.randrange(0, screenHeight), random.randrange(0, screenWidth)   
            origin = (randY, randX)
            coords = get_shape_coordinates(s, origin,\
                (screenHeight, screenWidth), OCCUPIED_SPACES,\
                EXISTING_SHAPES)

            if type(coords) is list:
                draw_shape(screen, coords)
            elif type(coords) is tuple: 
                draw_shape(screen, coords[0]) 

# ~ 
# DESCRIPTION 
## places <= `numShapes` shapes onto board, and runs game of life 
# ARGUMENTS 
## screen := curses.window object 
## shape := str, used for single-object drawing mode (mainly used for testing purposes)  
## numShapes := number of shapes to attempt to draw on screen 
# RETURN 
## None 
def random_assign(screen, shape = None, numShapes = 200): 

    if len(OCCUPIED_SPACES) == 0: 
        # construct initial board of periods 
        construct_initial_board(screen)
        # initialize board of shapes 
        random_assign_helper(screen, shape, numShapes)
    else: 
        reconstruct(screen)
        
    inp = None 
    screen.nodelay(True) 
    while inp != ord('q'): 
        inp = screen.getch() 
        update(screen, mode = '1')
        time.sleep(0.7)
