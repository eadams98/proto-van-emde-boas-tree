#from math import *
from random import *


# MAKE UNI AN EXPONENT OF 2 FOR TEST PURPOSES
# just so each bitvector is evenly split up

def getHigh(element):
    return floor(element/sqrt(u)) # FIX

def getLow(element):
    return element % sqrt(u) # FIX

def generateBitVector(num_of_potential_elements):
    """ Returns a bit vector

    Keyword arguments:
    universe -- int size of current universe (Potential universe sizes: u = 2^2^k)

    Returns a bit vector the size of the smallest universe (u = 2^2^k) that is larger 
    than num_of_potential_elements. This bit vector is assigned values of 0's and 1's
    from the start all the way up to the given argument num_of_potential_element. If
    there are more values past the stop point, they will all be left as zero
    """


    Universe = [4,16,256,65536,4294967297] #possible universe sizes. Anything bigger will probably crash

    for twoTower in Universe:
        if twoTower >= num_of_potential_elements:
            bitVector = [0]*twoTower
            for x in range(num_of_potential_elements):
                num = randrange(0,100,1)
                if num > 89:
                    bitVector[x] = 1

            print('bit: ', bitVector, len(bitVector), '\n')
            return twoTower,bitVector

    return "ERROR"

# lookup:   floor(x/sqrt(uni))
# spot:     x mod sqrt(uni)


def recursiveLook(veb,depth=1):

        """function prints how structure is formulated

        Keyword Arguments:
        veb -- takes a veb object
        depth -- starting point

        prints a textual representation of how the recursive data structure is formulated
        underneath. For the most part this is for debugging purposes, but can be used for
        its textual representation
        """

    #if veb.ptr:
        print('depth: ' + str(depth))
        if veb.ptr: # if not == None
            print(len(veb.ptr),veb.summary)
            for idx,x in enumerate(veb.ptr):
                #print(x.summary)
                recursiveLook(x,depth+1)
        else:
            print(len(veb.data), veb.summary)

def getPartitions(veb):

    """returns

    Keyword Arguments:
    veb -- takes a veb object
    depth -- starting point

    returns a tuple of 2 elements
    1st element: list of universe/structure at that particular depth
    2nd element: a list of the first veb's at every depth

    This was most likey for error checking or pertained to the 
    function of the GUI, however I believe it is now a useless function
    and will be re-evaluated for deletion
    """

    temp = []
    vebs = []
    go = True
    while(go):

        print("veb low: ", veb.low)
        temp.append(veb.low)
        vebs.append(veb)
        if(veb.end):
            veb = veb.ptr[0]
        else:
            go = False
    print('partitions: ', temp)
    return temp, vebs