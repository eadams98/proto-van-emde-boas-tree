import os
import protoHelperFunctions as helper
from protoVEB import *
from tkinter import *

class Application():

    def __init__(self):
        self.app = None
        self.entry_universe = None
        self.universe = None # might not need self button

        self.canvas = None
        self.canvasHeight = None
        self.canvasWidth = None

        self.veb = None
        self.vebs = None

    def initGui(self):
        self.app = Tk()
        self.app.title("VEB toy")
        self.canvasHeight = self.canvasWidth = 0

        label_universe = Label(self.app, text="Enter an integer (2^x = #):")
        label_universe.grid(row=0)

        self.entry_universe = Entry(self.app)
        self.universe = Button(self.app, text="integer", command= self.run)
        self.entry_universe.grid(row=1,column=0)
        self.universe.grid(row=1, column=1)

        self.app.mainloop()

    def traverse(self, vebs, location):
        #bits = canvas.create_text(localRectangle/2+current+100,(depth*100)+30+shove_down, text= str(vebs[depth].summary[x]))
        if location != []:
            veb = copy.deepcopy(vebs)

            for loc in location:
                veb = veb.ptr[loc]

            # return the approriate veb structure
            #print("max: " ,veb.maximum(), " min: ", veb.minimum()) ##
            return veb
        else:
            #input(dir(vebs))
            return vebs

    def clicked(self, event,ptr,canvas, vebs, indexPtrIds, layers, partitions, depth, location):
        location.append(indexPtrIds[ptr])
        '''
        print('hellow WORLD!')
        print(ptr)
        print(indexPtrIds)
        print(vebs)
        print(canvas.find_all())
        '''
        #canvas.itemconfigure(ptr, state='hidden')
        #input('satisfied')
        self.visual(canvas, vebs, indexPtrIds, layers, partitions, depth+1, location)

    def back(self, event, layers, depth, location):
        #print('go back', layers[depth]) IMPORTANT FOR DEBUGING 
        location.pop()
        #canvas.delete('all')
        for obj in self.canvas.find_all():
            self.canvas.itemconfigure(obj, state='hidden')
        for obj in layers[depth]:
            self.canvas.itemconfigure(obj, state='normal')

    def run(self): # CURRENTLY BAD (every run just stacks another canvas on top of current canvas
    
        try:
            os.system('clear')
            universe = int(self.entry_universe.get())
            bitVector = helper.generateBitVector(universe)
            print("bitvector= ", bitVector)
            self.veb = Veb(bitVector[0],bitVector[1], [])
            print("max: " ,self.veb.maximum(), " min: ", self.veb.minimum()) ##

            # might need to be class variables (self variables)
            indexPtrIds = {}
            layers = {}
            
            print('\n\n')
            helper.recursiveLook(self.veb)
            tup = helper.getPartitions(self.veb) # partitions, vebs (!!!!!!! WHY DOES THIS WORK WITHOUT helper. but generateBitVector won't work without helper.?)
            print("tup =", tup)
            partitions = tup[0]
            vebs = tup[1]
            
            self.canvasHeight = 500 #int(input('canvas Height (500 recommended): ')) #500 TAKE INPUT FROM USER
            self.canvasWidth = 1000 #int(input('cavas Width (1000 recommended): '))#1000 TAKE INPUT FROM USER
            self.canvas = Canvas(self.app, width = self.canvasWidth, height = self.canvasWidth, background = 'AntiqueWhite3')
            #canvas.pack()
            self.canvas.grid(row=3)

            #partitions = [6561,81,9,3]
            self.visual(self.canvas, self.veb, indexPtrIds, layers, partitions, 0, [])

            #canvas.create_rectangle(50,0,500,500, fill ='black')
        except ValueError:
            print("That's not a valid integer. Please enter a valid integer.")

    def visual(self, canvas, vebs, indexPtrIds, layers, partitions, depth, location):
        objects = set()
        veb = self.traverse(vebs, location)

        # DONT DELETE
        #canvas.delete('all')
        for obj in canvas.find_all():
            canvas.itemconfigure(obj, state='hidden')

        #RECTANGLE_MAX = 900
        #canvasHeight = 500  #TAKE INPUT FROM USER
        #canvasWidth = 1000  #TAKE INPUT FROM USER
        
        RECTANGLE_MAX = self.canvasWidth - 100
        shove_down = self.canvasHeight/4

        localRectangle = RECTANGLE_MAX/partitions[depth]
        #localRectangle = localRectangle - (localRectangle/partition) # NEW
        #temp = localRectangle/partition
        #print(localRectangle)
        colors = ['black', 'green',  'cyan', 'yellow','magenta']
        half = (depth*100)/2                # BECAUSE I CLEARY CAN"T DO MATH

        #go back up
        if depth != 0:
            mid = self.canvasWidth/2
            y1 = ((depth)*100) + shove_down - half            # Bottom Y - 
            y2 = 0+(depth*100) + shove_down              # Top Y - SEEMS FINE
            up = self.canvas.create_rectangle(
                    mid-localRectangle/2 + 50,
                    y1,
                    mid+localRectangle/2 + 50,
                    y2,
                    fill = 'white'
                    )
            objects.add(up)
            self.canvas.tag_bind(up,
                    '<Button-1>',
                    lambda event, l=layers, d=depth-1, loc=location:
                    self.back(event, l, d, loc)  
            )
            up = self.canvas.create_text(mid+50,y1+half/2, text= 'Up to depth '+str(depth-1))
            objects.add(up)
            

        print(partitions[depth])
        for x in range(int(partitions[depth])):
                    
            if x % 2 == 0:
                alt = 'red'
            else:
                alt = 'blue'
                    
            color = colors[x % 5]

            current = x*localRectangle          # how far to move over

            # SIMPLE MATH....
            x1 = 100+current                      # Top X - THIS IS FINE
            if depth != 0:
                print('depth!')
                y1 = 0+(depth*100) + shove_down              # Top Y - SEEMS FINE
                y2 = (depth*100) + 50 + shove_down             # Bottom Y - 
                yPrime = (depth*100) + 100 + shove_down             # Bottom Y - 
                #yPrime = 2*(depth*100) + shove_down              # BOTTOM-BOTTOM: 
            else:
                y1 = 0 + shove_down
                y2 = 50 + shove_down
                yPrime = 100 + shove_down
            x2 = 100+current+localRectangle         # Bottom X = THIS IS FINE

            #(x1,y1,x2,y2)
            # SUMMARY: top half
            summary = self.canvas.create_rectangle(x1, y1, x2 ,y2, fill = 'white')
            objects.add(summary)

            # SUMMARY - text
            bits = self.canvas.create_text(localRectangle/2+current+100,(depth*100)+30+shove_down, text= str(veb.summary[x]))
            index = self.canvas.create_text(localRectangle/2+current+100,(depth*100)+10+shove_down, text= 'i: '+ str(x))
            objects.add(bits)
            objects.add(index)

            # PTR: bottom half
            ptr = self.canvas.create_rectangle(x1, y2, x2, yPrime, fill = alt)
            objects.add(ptr)
            indexPtrIds[ptr] = x
            if depth != len(partitions)-1:
                self.canvas.tag_bind(ptr,
                    '<Button-1>',
                    lambda event, arg=ptr, canvas=self.canvas, veb=vebs, idx=indexPtrIds, p=partitions, d=depth, l=layers, loc=location:
                    self.clicked(event, arg, canvas, veb, idx, l, p, d, loc)  
                )
                down = self.canvas.create_text(x1+localRectangle/2,(y2+yPrime)/2, text= 'Down')
                objects.add(down)
            else:
                data = self.canvas.create_text(x1+localRectangle/2,(y2+yPrime)/2, text= veb.data)

            #print('item id: ',ptr)

        # LEGEND - text
        pos = depth*100
        legend = self.canvas.create_text(50,pos+10+shove_down, text= 'LEGEND '+str(depth))
        objects.add(legend)

        # LEGEND - key
        key = self.canvas.create_rectangle(50, pos+20+shove_down, 75, pos+45+shove_down, fill = 'white')
        Max = self.canvas.create_text(62.5,pos+shove_down+32.5, text= veb.maximum())
        MaxText = self.canvas.create_text(62.5,pos+shove_down+52, text='max')
        objects.add(key)
        objects.add(Max)
        objects.add(MaxText)
        key = self.canvas.create_rectangle(10, pos+20+shove_down, 35, pos+45+shove_down, fill = 'white')
        Min = self.canvas.create_text(22.5,pos+shove_down+32.5, text= veb.minimum())
        MinText = self.canvas.create_text(22.5,pos+shove_down+52, text= 'min')
        objects.add(key)
        objects.add(Min)
        objects.add(MinText)
        #input(str(depth))
        #print(indexPtrIds)

        #if depth > 0:
            #temp = create_window()
            #temp.title("depth "+ str(depth))
            #canvasTmp = Canvas(temp, width = canvasWidth, height = canvasWidth)
            #canvasTmp.grid(row=1)
        
        layers[depth] = objects
        print('\n\n')

"""
Variables
"""
entry_universe = None

"""
Definitions
"""



def traverse(vebs, location):
        #bits = canvas.create_text(localRectangle/2+current+100,(depth*100)+30+shove_down, text= str(vebs[depth].summary[x]))
   if location != []:
       veb = copy.deepcopy(vebs)

       for loc in location:
           veb = veb.ptr[loc]

    # return the approriate veb structure
       #print("max: " ,veb.maximum(), " min: ", veb.minimum()) ##
       return veb
   else:
       #input(dir(vebs))
       return vebs

