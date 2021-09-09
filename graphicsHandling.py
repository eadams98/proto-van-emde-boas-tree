import os
import protoHelperFunctions as helper
from protoVEB import *
"""
Definitions
"""
def create_window(given_Tk):
    window = Toplevel(given_Tk)
    print('done')

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

def back(event, canvas, layers, depth, location):
    #print('go back', layers[depth]) IMPORTANT FOR DEBUGING 
    location.pop()
    #canvas.delete('all')
    for obj in canvas.find_all():
        canvas.itemconfigure(obj, state='hidden')
    for obj in layers[depth]:
        canvas.itemconfigure(obj, state='normal')

def clicked(event,ptr,canvas, vebs, indexPtrIds, layers, partitions, depth, location):
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
    visual(canvas, vebs, indexPtrIds, layers, partitions, depth+1, location)

def visual(canvas, vebs, indexPtrIds, layers, partitions, depth, location):
    objects = set()
    veb = traverse(vebs, location)

    # DONT DELETE
    #canvas.delete('all')
    for obj in canvas.find_all():
        canvas.itemconfigure(obj, state='hidden')

    #RECTANGLE_MAX = 900
    #canvasHeight = 500  #TAKE INPUT FROM USER
    #canvasWidth = 1000  #TAKE INPUT FROM USER
    global canvasHeight
    global canvasWidth
    RECTANGLE_MAX = canvasWidth - 100
    shove_down = canvasHeight/4

    localRectangle = RECTANGLE_MAX/partitions[depth]
    #localRectangle = localRectangle - (localRectangle/partition) # NEW
    #temp = localRectangle/partition
    #print(localRectangle)
    colors = ['black', 'green',  'cyan', 'yellow','magenta']
    half = (depth*100)/2                # BECAUSE I CLEARY CAN"T DO MATH

    #go back up
    if depth != 0:
        mid = canvasWidth/2
        y1 = ((depth)*100) + shove_down - half            # Bottom Y - 
        y2 = 0+(depth*100) + shove_down              # Top Y - SEEMS FINE
        up = canvas.create_rectangle(
                mid-localRectangle/2 + 50,
                y1,
                mid+localRectangle/2 + 50,
                y2,
                fill = 'white'
                )
        objects.add(up)
        canvas.tag_bind(up,
                '<Button-1>',
                lambda event, l=layers, d=depth-1, c=canvas, loc=location:
                back(event, c, l, d, loc)  
        )
        up = canvas.create_text(mid+50,y1+half/2, text= 'Up to depth '+str(depth-1))
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
        summary = canvas.create_rectangle(x1, y1, x2 ,y2, fill = 'white')
        objects.add(summary)

        # SUMMARY - text
        bits = canvas.create_text(localRectangle/2+current+100,(depth*100)+30+shove_down, text= str(veb.summary[x]))
        index = canvas.create_text(localRectangle/2+current+100,(depth*100)+10+shove_down, text= 'i: '+ str(x))
        objects.add(bits)
        objects.add(index)

        # PTR: bottom half
        ptr = canvas.create_rectangle(x1, y2, x2, yPrime, fill = alt)
        objects.add(ptr)
        indexPtrIds[ptr] = x
        if depth != len(partitions)-1:
            canvas.tag_bind(ptr,
                '<Button-1>',
                lambda event, arg=ptr, canvas=canvas, veb=vebs, idx=indexPtrIds, p=partitions, d=depth, l=layers, loc=location:
                clicked(event, arg, canvas, veb, idx, l, p, d, loc)  
            )
            down = canvas.create_text(x1+localRectangle/2,(y2+yPrime)/2, text= 'Down')
            objects.add(down)
        else:
            data = canvas.create_text(x1+localRectangle/2,(y2+yPrime)/2, text= veb.data)

        #print('item id: ',ptr)

    # LEGEND - text
    pos = depth*100
    legend = canvas.create_text(50,pos+10+shove_down, text= 'LEGEND '+str(depth))
    objects.add(legend)

    # LEGEND - key
    key = canvas.create_rectangle(50, pos+20+shove_down, 75, pos+45+shove_down, fill = 'white')
    Max = canvas.create_text(62.5,pos+shove_down+32.5, text= veb.maximum())
    MaxText = canvas.create_text(62.5,pos+shove_down+52, text='max')
    objects.add(key)
    objects.add(Max)
    objects.add(MaxText)
    key = canvas.create_rectangle(10, pos+20+shove_down, 35, pos+45+shove_down, fill = 'white')
    Min = canvas.create_text(22.5,pos+shove_down+32.5, text= veb.minimum())
    MinText = canvas.create_text(22.5,pos+shove_down+52, text= 'min')
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

def run(): # CURRENTLY BAD (every run just stacks another canvas on top of current canvas
    
    try:
        os.system('clear')
        universe = int(entry_universe.get())
        bitVector = helper.generateBitVector(universe)
        print("bitvector= ", bitVector)
        veb = Veb(bitVector[0],bitVector[1], [])
        print("max: " ,veb.maximum(), " min: ", veb.minimum()) ##
        indexPtrIds = {}
        layers = {}
        print('\n\n')
        helper.recursiveLook(veb)
        tup = helper.getPartitions(veb) # partitions, vebs (!!!!!!! WHY DOES THIS WORK WITHOUT helper. but generateBitVector won't work without helper.?)
        print("tup =", tup)
        partitions = tup[0]
        vebs = tup[1]
        
        global canvasHeight
        canvasHeight = 500 #int(input('canvas Height (500 recommended): ')) #500 TAKE INPUT FROM USER
        global canvasWidth
        canvasWidth = 1000 #int(input('cavas Width (1000 recommended): '))#1000 TAKE INPUT FROM USER
        canvas = Canvas(app, width = canvasWidth, height = canvasWidth, background = 'AntiqueWhite3')
        #canvas.pack()
        canvas.grid(row=3)

        #partitions = [6561,81,9,3]
        visual(canvas, veb, indexPtrIds, layers, partitions, 0, [])

        #canvas.create_rectangle(50,0,500,500, fill ='black')
    except ValueError:
        print("That's not a valid integer. Please enter a valid integer.")