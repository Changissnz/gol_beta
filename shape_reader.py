from globals import * 
import json
import copy

###################################################
###################################################
###################################################
###### HELPERS FOR : 
###### retrieving and calculating shape attributes
###################################################
###################################################
###################################################


# DESCRIPTION 
## given shape, returns coordinates of its geometry 
# ARGUMENTS 
# shape := string  
# typeShape := string, one of 'still_life', 'oscillator', and 'spaceship'
# RETURN 
## list of coordinates, s.t. each element is in the form (y, x) 
def reader(shape):
    ##raise ValueError("SHAPE __{}__.  TYPE __{}__".format(shape, type(shape)))
    fn = "/shapes/" + shape + ".txt"  

    path = currentPath + fn 
    try: 
        with open(path) as f: 
            coords = [] 
            for line in f: 
                l = to_int_tuple(line.split()) 
                if l != (): coords.append(l) 
        return coords
    except: 
        return "ERROR : invalid shape!"

# DESCRIPTION 
## returns the greatest dimension of some currently existing shape; 
## this value will be used to create buffer for updating (to account for out-of-sights) 
def get_biggest_dim(mode):
    # uses variable : EXISTING_SHAPES
    if mode == '1':          
        shapes = list(EXISTING_SHAPES.keys()) 
    elif mode == '2': 
        shapes = list(EXISTING_SHAPES_CREATE.keys()) 

    c = 0 
    for s in shapes: 
        coords = reader(s)
        m = max(get_max(coords, 1), get_max(coords, 0))    
        if m > c: c = m 
    return c


# DESCRIPTION 
## retrieves all shapes available into `POSSIBLE_SHAPES`
# TODO : required at initial
def get_possible_shapes(): 

    with open(classificationPath) as df: 
        q = json.load(df)

    for k, v in q.items():
        POSSIBLE_SHAPES.extend(v)
    POSSIBLE_SHAPES.sort() 


# DESCRIPTION 
## given shape, returns its classification
def get_shape_classification(shape): 
    with open(classificationPath) as df: 
        q = json.load(df)

    for k, v in q.items(): 
        if shape in v: 
            return k 
    return False

# ~ 
# DESCRIPTION 
## given name of shape, returns its classification : still_life, oscillator, or spaceship
# ARGUMENTS 
## shape := <str> 
# RETURN 
## string denoting shape's type, or False if d.n.e  
## TODO : 
### cannot name custom shape as classification 
### cannot have space in name of custom shape
def typeof_shape(shape):
    if POSSIBLE_SHAPES == []: 
        print("ERROR : shapes have not been retrieved")

    for k, v in POSSIBLE_SHAPES: 
        for v_ in v: 
            if v_ == shape: 
                return k 
    return False 

# ~
# DESCRIPTION 
## given origin, returns coordinates corresponding to this specific shape 
# ARGUMENTS 
## shape := string 
## origin := coordinates in the form (y, x) 
## extreme := screen dimensions
# RETURN 
## list of coordinates, s.t. each element is in the form (y, x)  
def get_shape_coordinates(shape, origin, extreme, OCCUPIED, EXISTING): 

    # get geometry of shape 
    coords = reader(shape)

    # if geometry exists, calculate coordinates, make sure coordinates are not occupied  
    if type(coords) is list: 
        res = get_coords(origin, coords)
        occupied = get_occupied_spaces(res) 
        qual = is_valid(occupied, extreme, OCCUPIED) 
        if qual is True: 
            # add to occupied spaces : future additions cannot be in this region 
            OCCUPIED.extend(occupied)

            # add this shape to existing shapes (variable will be used for updating) 
            if shape in EXISTING:
                q = EXISTING[shape] 
                q.append(res)  
                EXISTING[shape] = q 
            else: 
                EXISTING[shape] = [res]  

            return res 
        return "ERROR : location already occupied!"
    return coords 

# ~ 
# DESCRIPTION 
## given coordinates of shape, returns list of coordinates that cannot be used for next round, this calculates a `safe space` for the coordinates 
def get_occupied_spaces(coords):

    get_box = lambda iX, sX, iY, sY: [(y, x) for y in range(iY- 1, sY + 2) for x in range(iX - 1, sX + 2)] 

    minX = get_min(coords, 1)  
    maxX = get_max(coords, 1)  
    minY = get_min(coords, 0)  
    maxY = get_max(coords, 0)

    box = get_box(minX, maxX, minY, maxY) 
    return box

# DESCRIPTION 
## given origin of shape, determines if shape can be drawn at that location
# ARGUMENTS 
# coords := list of coordinates (y, x) 
# extreme := (maxX, maxY) 
# RETURN 
## bool 
def is_valid(coords, extreme, OCCUPIED):
    for c in coords: 
        if c in OCCUPIED: 
            return False

    if get_min(coords, 1) < 0 or get_min(coords, 0) < 0\
        or get_max(coords, 1) > extreme[1] or get_max(coords, 0) > extreme[0]:
                return False      
    return True

# DESCRIPTION 
## used for creating new shapes, so that output is referenced at origin 
def scale_coords_to_origin(coords):
    if coords == []: return coords 

    minX = get_min(coords, 1)    
    minY = get_min(coords, 0) 

    newCoords = [] 
    for i in range(len(coords)):
        y = coords[i][0] - minY 
        x = coords[i][1] - minX
        newCoords.append((y, x))  
    return newCoords

# DESCRIPTION 
## returns all non-null coordinates for shape 
def get_nonnull_coords(info):
    coords = [] 
    for c in range(len(info)): 
        for r in range(len(info[c])): 
            if info[c][r] != '.': 
                coords.append((c, r)) 
    return coords

#### DELETION, CREATION, AND ADDITION OF SHAPES 

# ~
# DESCRIPTION 
## given the screen and the coordinates, draws the shape 
## TODO 
def draw_shape(screen, coords): 
    for c in coords:
        try:  
            screen.addstr(c[0], c[1], 'o')  
        except curses.error: 
            pass 

def delete_shape(shape): 

    with open(classificationPath) as df: 
        q = json.load(df) 

    for k, v in q.items(): 
        if shape in v: 
            v = [i for i in v if i != shape]
            q[k] = v 
            break      

    with open(classificationPath, 'w') as df: 
        json.dump(q, df, sort_keys = True, indent = 4, ensure_ascii = False)                  

# DESCRIPTION 
## records new shape and corresponding type in file `classif.txt`
def record_new_shape(shape, shapeType):

    with open(classificationPath) as df: 
        q = json.load(df) 
       
    q[shapeType] = q[shapeType] + [shape]

    with open(classificationPath, 'w') as df: 
        json.dump(q, df, sort_keys = True, indent = 4, ensure_ascii = False)
    POSSIBLE_SHAPES.append(shape) 
    POSSIBLE_SHAPES.sort()


# DESCRIPTION 
## choice 2, writes shape to file 
def write_shape_to_file(shape, info): 
    # scale coordinates to origin first 
    coords = scale_coords_to_origin(get_nonnull_coords(info))

    # empty 
    if coords == []: return False 

    # NOTE : assume shape currently does not exist 
    fn = "/shapes/" + shape + ".txt"  
    path = currentPath + fn

    if os.path.exists(path) is True: 
        return False 

    with open(path, 'w') as f: 
        for c in coords:
            s = tuple_to_string(c) 
            f.write(s + '\n') 
    return True 
