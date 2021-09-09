# SUMMARY

This is a Proto Van Emde Boas Tree Class as well as a GUI to help visualize the underlying data structure. This was a joint final project for my Advanced Data Structures class with the lovely Skylar.

#FILES

## protoGUI.py
Run the protoGUI.py file if you would like to see the visual as well as textual representation of the data structure at hand. 

## protoVEB.py
protoVEB.py strictly contains the VEB class with all its methods and variables

## protoHelperFunctions
These are just function used in the underlying code to help make the VEB structure.

## graphicsHandling
This is a work in progress. Currently the Tkinter elements are handles in the file protoGUI.py itself. 

# HOW IT WORKS

You can give the size of the bit vector you want and the backend will handle the rest. Essential if the size of your bit vector doesn't match an allowable universe size (Tower of 2: universe = 2^2^k) the bit vector will be extended to match this size. Your give bit vector value will be used to let this bit vector know which indicies to populate. It will start from 0 and go up to the number you indicated. Weather a indicies gets a 0 or 1 is dependent on a probabilistic value

# FUTURE

Extract the GUI elements and operations on them to graphicsHandling.py

# TECHNOLOGIES/TECHNIQUES USED
Python, Recursion, OOP principals and Tkinter (GUI)
