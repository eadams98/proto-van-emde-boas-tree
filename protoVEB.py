from math import *
from random import *
import copy

# MAKE UNI AN EXPONENT OF 2 FOR TEST PURPOSES
# just so each bitvector is evenly split up

def getHigh(element):
    return floor(element/sqrt(u)) # FIX

def getLow(element):
    return element % sqrt(u) # FIX

Universe = [4,16,256,65536,4294967297] #possible universe sizes. Anything bigger will probably crash

def generateBitVector(universe):
    
    """
    powerOfTwo = 2
    print('universe: ', universe)
    while powerOfTwo < universe:
        powerOfTwo *= 2
        print(powerOfTwo)
    bitVector = [0]*powerOfTwo

    for x in range(universe):
        num = randrange(0,100,1)
        if num > 89:
            bitVector[x] = 1

    print('bit: ', bitVector, len(bitVector), '\n')
    return bitVector
    """
    for twoTower in Universe:
        if twoTower >= universe:
            bitVector = [0]*twoTower
            for x in range(universe):
                num = randrange(0,100,1)
                if num > 89:
                    bitVector[x] = 1

            print('bit: ', bitVector, len(bitVector), '\n')
            return twoTower,bitVector

    return "ERROR"

# lookup:   floor(x/sqrt(uni))
# spot:     x mod sqrt(uni)


#universe = int(input('please input a number that is an exponent of 2 (recommend 65536): '))
'''
low = floor(sqrt(universe))
bitVector = [0]*universe
summary = [0]*low

for x in range(len(bitVector)):
    num = randrange(0,100,1)
    if num > 89:
        bitVector[x] = 1
#print(self.bitVector)

for summaryChunk in range(low):
    
    for bitInChunk in range(low):
        
        if bitVector[(low * summaryChunk) + bitInChunk] == 1:
            summary[summaryChunk] = 1
            break
'''

'''
visual to make sure it worked
'''

# not too helpful to see, below this one is much better
#print('summary: ', summary)
#print('bit: ', bitVector, '\n')

'''
for x in range(low):
    print('summary[', x, ']: ', summary[x])
    print('bitVector[', (low*x), ':', (low*x)+low-1, ']: ', bitVector[(low * x):(low * x) + low ], '\n')
'''


class Veb:

    def __init__(self, universe, bitVector, index):
        #local variables to recursion depth level
        '''
        if len(index) == 0:
            self.universe = 2
            while self.universe <= universe:
                self.universe *= 2
        else:
            self.universe = universe
        '''

        self.bitVector = bitVector
        self.globalMax = None
        self.globalMin = None
        self.ptr = None
        self.end = True

        self.universe = universe

        #print(len(self.bitVector))
        #x = sqrt(self.universe)
        #print(x)
        #low = floor(x)
        self.low = floor(sqrt(universe))
        low = self.low
        #print('low: ',self.low)
        #high = ceil(x)
        #print(high)

        '''
        from our universe, generate an probablistic bitVector, where one appears roughly 10%
        of the time
        '''


        '''
        from our pseudorandom generated universe bit vector, generate the summary vector
        '''


        # ptr to smaller ones
        if universe > 2:
            self.summary = [0]*low
            #self.ptr = [Veb(low, bitVector)]*low
            self.ptr = [None]*low

            for idx in range(len(self.ptr)):
                cpyIndex = copy.deepcopy(index)
                cpyIndex.append((idx,low))
                self.ptr[idx] = Veb(low, bitVector, cpyIndex)
                if 1 in self.ptr[idx].summary:
                    self.summary[idx] = 1
            print('summary at break by ', cpyIndex,': ', self.summary)
        else:
            self.summary = [0]*1
            #self.data = [None]*universe
            position = 0
            '''
            CAN"T UNPACK TUPLE THIS WAY
            for x in index:

                print('x: ',x)
                for idx,piece in x:
            '''
#            print('index: ', index)
            for idx, piece in index:
                position += (idx * piece)
            end = position+universe
            self.data = self.bitVector[position:end]
            #self.data[1] = self.bitVector[end:end+universe]
            print('data chunk ', position,': ',self.data, 'piece: ', piece, 'index: ', index)
            self.populate(self.summary, universe)
            self.end = False
#            print('summary: ', self.summary)
            #return (1 in self.data)

    def populate(self, summary, universe):

        #for idx, x in enumerate(self.data):
            if 1 in self.data:
                self.summary[0] = 1
            else:
                self.summary[0] = 0

    ######### class methods ##############

    def maximum(self):
        #base case
        if self.universe == 2:
            if self.data[0] == 1:
                return 0
            elif self.data[1] == 1:
                return 1
            else:
                return -1

        else:
            index = -1
            cpySummaryReversed = self.summary[::-1]
            for idx, x in enumerate(cpySummaryReversed):
                if x ==1:
                    index = (len(cpySummaryReversed)-1) - idx
                    break
            
            if index == -1:
                return -1
            else:
                position = self.ptr[index].maximum()
                return index * self.low + position

    def minimum(self):
        #base case
        if self.universe == 2:
            if self.data[0] == 1:
                return 0
            elif self.data[1] == 1:
                return 1
            else:
                return -1

        else:
            index = -1
            for idx, x in enumerate(self.summary):
                if x == 1:
                    index = idx
                    break

            if index == -1:
                return -1
            else:
                position = self.ptr[index].minimum()
                return index * self.low + position

    def successor(self, element): # FLAWWED LOGIC (FUNCTION INCOMPLETE)
        #base case
        if self.universe == 2:
            if element == 0: #and # SOMETHING MISSING 
                return 1
            else:
                return -1

        else:
            veb = self.ptr[self.highElem(element)]
            position = veb.successor(self.lowElem(element))

            if position != -1:
                return self.highElem(element) * position
            else:
                index = -1
                summarySlice = self.summary[self.highElem(element)+1:] # everything after current cluster
                for idx, x in enumerate(summarySlice):
                    if x == 1:
                        index = idx + self.highElem(element)+1
                
                if index == -1:
                    return -1
                else:
                    successor_cluster = self.ptr[index]
                    offset = successor_cluster.minimum()
                    return index * self.low + offset
    

    def highElem(self, element):
        return int(element // sqrt(self.universe))

    def lowElem(self, element):
        return int(element % sqrt(self.universe))

    def isMember(self, element):
        # base case
        if element >= self.universe:
            return False

        if self.universe == 2:
            return self.data[element] == 1
        else:
            print('high: ',self.highElem(element), ' low: ', self.lowElem(element))
            veb = self.ptr[self.highElem(element)]
            return veb.isMember(self.lowElem(element))

    def insert(self, element):
        # base case
        if self.universe == 2:
            #self.summary[0] = 1 # ONLY EVERY one at this depth
            self.data[element] = 1 
        else:
            print('high: ',self.highElem(element), ' low: ', self.lowElem(element))
            self.summary[self.highElem(element)] = 1 # update summary
            veb = self.ptr[self.highElem(element)]
            veb.insert(self.lowElem(element))
            

    def delete(self, element): #top most summary vector doesn't update. need to do that
        # base case
        if (self.universe  == 2):
            self.data[element] = 0
            if 1 not in self.data:
                self.summary = [0]
        else:
            print('high: ',self.highElem(element), ' low: ', self.lowElem(element))
            if self.summary[self.highElem(element)] != 0:
                veb = self.ptr[self.highElem(element)]
                print('not equal= ',veb.summary)
                veb.delete(self.lowElem(element))
                print('not equal after= ',veb.summary)
                if 1 not in veb.summary:
                    self.summary[self.highElem(element)] = 0



            #self.delete(self.ptr[])




#test = Veb(256)
# JESUS TAKE THE WHEEL


#print('\n\n')
#print('depth 1')
#print(test.summary)

def recursiveLook(veb,depth=1):
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

    temp = []
    vebs = []
    go = True
    while(go):

        print(veb.low)
        temp.append(veb.low)
        vebs.append(veb)
        if(veb.end):
            veb = veb.ptr[0]
        else:
            go = False
    print('partitions: ', temp)
    return temp, vebs

if __name__ == '__main__':
    # TESTING PURPOSES #

    u = int(input('universe size'))
    u = generateBitVector(u)
    test = Veb(u[0], u[1], [])
