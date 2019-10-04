`'`''``''`'`'`'`````'```'```'``'```'``'```'```'`'``'`'``'``'`'``''`''``''`'`'`'`''`'
`'`''``''`'`'`'`````'```'```'``'```'``'```'```'`'``'`'``'``'`'``''`''``''`'`'`'`''`'
`'`''``''`'`'`'`````'```'```'``'```'``'```'```'`'``'`'``'``'`'``''`''``''`'`'`'`''`'
# CONWAY'S GAME OF LIFE 

This program is an working draft of Conway's Game of Life. Instructions are
hopefully easy enough to read, because this `README.md` file is too lazy to cover
the intricate details and specificities. However, the specifics that this file will
cover will include some notable bugs and attributes. 

* when creating your world in option 2, the blue spots are there to demarcate its 
  enclosed shape, stay away from them, or else the screen will flash error if you 
  attempt any space within this blue box and possibly its neighboring non-blue 
  spots.  
* note that the only way to choose between a variety of items is the scrollbar, 
  search bar currently does not exist. 
* the library option has not been thoroughly tested, descriptions for shapes 
  that are too big for the screen will be missing.  
* when creating your custom shape, the algorithm will classify it as either a 
  still-life, oscillator, or spaceship; the classifier algorithm is faulty. 
  For example, look at the shape `one`. It dies as soon as the world starts, but 
  it is labelled as an oscillator. It would be a poor spaceship and a poor 
  still-life. But it needs to belong somewhere, and the mechanizations behind my
  algorithm decided it to be an oscillator. This area would appreciate some
  improvement. 
* when naming your custom shape, please try to keep it under the magnitude of the
  width of the screen; excessively long names have not yet been tested. 
* the options scrollbar for browsing shapes and saved games is quirky. 
* a tip for playing this game is try to keep terminal screen size consistent, 
  this Game of Life does not take too kindly to big or small fluctuations.
* this game still needs to be refactored. 
* modify the folders `shape` and `games` at your discretion. 

# User instructions 
* Download this code. 
* `cd` into this code's folder. 
* Run `python3 main.py` 

#### Final Note 
I hope you enjoy playing and are inspired by this 0-player game and its many
findings, whether you are spectator or mechanic. For any questions, concerns, 
or inputs, please contact me. 

`'`''``''`'`'`'`````'```'```'``'```'``'```'```'`'``'`'``'``'`'``''`''``''`'`'`'`''`'
`'`''``''`'`'`'`````'```'```'``'```'``'```'```'`'``'`'``'``'`'``''`''``''`'`'`'`''`'
`'`''``''`'`'`'`````'```'```'``'```'``'```'```'`'``'`'``'``'`'``''`''``''`'`'`'`''`'

