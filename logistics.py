# import that which is necessary

from calendar import c
from re import L
from urllib.parse import _ResultMixinBytes
from sympy import Q, solve
from DEgraphics import *
from PIL import Image
import random
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import math


mainWindow = DEGraphWin(title = "Logistic Map Explorer",defCoords=[-0.4,-0.1,4,1],width = 700,height = 350,offsets=[0,0],autoflush = True,hasTitlebar = False,hThickness=3,hBGColor="black")
mainWindow.setBackground(color_rgb(129,141,146))
mainWindow2 = DEGraphWin(title = "Logistic Map Explorer",defCoords=[-0.1,-0.1,1,1],width = 350,height = 350,offsets=[0,350],autoflush = True,hasTitlebar = False,hThickness=3,hBGColor="black")
mainWindow2.setBackground(color_rgb(129,141,146))
mainWindow3 = DEGraphWin(title = "Logistic Map Explorer",defCoords=[-0.5,-0.1,5,1],width = 350,height = 350,offsets=[350,350],autoflush = True,hasTitlebar = False,hThickness=3,hBGColor="black")
mainWindow3.setBackground(color_rgb(129,141,146))
    
lines = []
rlines = []

btnWindow = DEGraphWin(title = "Buttons",defCoords=[-10,-10,10,10],width = 700,height = 200,offsets=[0,700],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
btnWindow.setBackground(color_rgb(129,141,146))
entryWindow = DEGraphWin(title = "Buttons",defCoords=[-10,-10,10,10],width = 300,height = 900,offsets=[700,0],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
entryWindow.setBackground(color_rgb(129,141,146))
enteriterations = IntEntry(Point(0,4), width = 6, span = [0,500],colors = ['gray','black'],errorColors = ['red','white'])
enterinitx = DblEntry(Point(0,0), width = 6, span = [0,1],colors = ['gray','black'],errorColors = ['red','white'])
enteriterations.draw(entryWindow)
enterinitx.draw(entryWindow)

textEnterIterations = Text(Point(-6,4), "# of Iterations?")
textEnterIterations.draw(entryWindow)
textEnterIterations.setSize(10)
textEnterInitx = Text(Point(-6,0), "Initial x?")
textEnterInitx.draw(entryWindow)
textEnterInitx.setSize(10)
textR = Text(Point(0,2), "R = ")
textR.draw(entryWindow)
textR.setSize(10)
textTitle = Text(Point(0,8), "Organized Chaos:\nA Demonstration")
textTitle.draw(entryWindow)
textTitle.setSize(18)
textTitle.setStyle('italic')
textCredits = Text(Point(0,-8), "@wenm0tt")
textCredits.draw(entryWindow)
textCredits.setSize(8)
textCredits.setStyle('italic')

# now we define all buttons.
btnSettings = Button(
                    btnWindow,
                    Point(-10,10),
                    width = 4,
                    height = 20,
                    edgeWidth = 2,
                    label = u"\u2699",
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )   
btnSettings.activate()

btnFetchR = Button(
                    btnWindow,
                    Point(-6,10),
                    width = 16,
                    height = 20,
                    edgeWidth = 2,
                    label = 'Fetch R',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
btnFetchR.activate()



# finally, we define all the entries. We want the user to be able to change the R value, initial x, and # of iterations.
# when changing the R value, if we are plotting a cobweb we just plot the pertaining graph. If plotting the bifurcation, we plot a 
#   line at the R value.
# Initial x and # of iterations are self explanatory.
# note that the span I've set for each entry is appropriate to the domain. I've set max iterations to 500 because 
#   past that it is meaningless to see the cobweb diagram.
    



# and add the axes labels.
rAxis = Text(Point(2,0), "R")
rAxis.draw(mainWindow)
rAxis.setStyle("italic")
xnAxis = Text(Point(0,0.5), "Xn")
xnAxis.draw(mainWindow)
xnAxis.setStyle("italic")
xAxis = Text(Point(0.5,0),"x")
xAxis.draw(mainWindow2)
xAxis.setStyle("italic")
fxAxis = Text(Point(0,0.5),"f(x)")
fxAxis.draw(mainWindow2)
fxAxis.setStyle("italic")
timeAxis = Text(Point(2.5,0),"Time")
timeAxis.draw(mainWindow3)
timeAxis.setStyle("italic")
xn2Axis = Text(Point(0,0.5),"Xn")
xn2Axis.draw(mainWindow3)
xn2Axis.setStyle("italic")

# define the main method

# R, by default, will be equal to 2
R = 2
def main():
    global lines
    global clickPoint2

    # turn axes on.
    mainWindow.toggleAxes()
    mainWindow2.toggleAxes()
    mainWindow3.toggleAxes()

    # while the program is running . . .
    while True:
        global R
        global textR
        global rlines

         # fetch the mouse
        if btnWindow.isOpen():
            clickPoint = btnWindow.getMouse()   
            mainWindow.flush()  
        else:
            break 

        # if the settings button is clicked . . .
        if (btnSettings.clicked(clickPoint)):
            settingsWindow = DEGraphWin(title = "Settings",defCoords=[-10,-10,10,10],width = 700,height = 200,offsets=[0,700],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
            settingsWindow.setBackground(color_rgb(129,141,146))

            btnZoomIn = Button(
                    settingsWindow,
                    Point(-10,10),
                    width = 20,
                    height = 4,
                    edgeWidth = 2,
                    label = 'Zoom In',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnZoomIn.activate()
            btnZoomOut = Button(
                    settingsWindow,
                    Point(-10,6),
                    width = 20,
                    height = 4,
                    edgeWidth = 2,
                    label = 'Zoom Out',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnZoomOut.activate()
            btnClear = Button(
                    settingsWindow,
                    Point(-10,2),
                    width = 20,
                    height = 4,
                    edgeWidth = 2,
                    label = 'Clear All',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnClear.activate()
            btnExit = Button(
                    settingsWindow,
                    Point(-10,-2),
                    width = 20,
                    height = 4,
                    edgeWidth = 2,
                    label = 'Back',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnExit.activate()
            btnQuit = Button(
                    settingsWindow,
                    Point(-10,-6),
                    width = 20,
                    height = 4,
                    edgeWidth = 2,
                    label = 'Quit',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnQuit.activate()
            
            while True:
                if settingsWindow.isOpen():
                    settingsClick = settingsWindow.getMouse()
                    coords = mainWindow.currentCoords

                    if btnZoomIn.clicked(settingsClick):
                        textZooming = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Click Two Points on the Graph to Zoom")
                        textZooming.draw(mainWindow)
                        textZooming.setSize(12)
                        textZooming.setStyle('italic')
                    
                        # zoom in
                        mainWindow.zoom(whichWay = ZOOM_IN, keepRatio = False)

                        textZooming.setText("")
                        plotBifur(R)
                        settingsWindow.close()
                        break
                    if btnZoomOut.clicked(settingsClick):
                        mainWindow.zoom(whichWay = ZOOM_OUT, keepRatio = False)
                        plotBifur(R)
                        settingsWindow.close()
                        break
                        
                    if btnClear.clicked(settingsClick):
                        coords = mainWindow.currentCoords
                        textClearing = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Clearing...")
                        textClearing.draw(mainWindow)
                        textClearing.setSize(12)
                        textClearing.setStyle('italic')
                        mainWindow.clear()
                        mainWindow2.clear()
                        mainWindow3.clear()
                        for line in lines:
                            line.undraw()
                        lines = []
                        textClearing.setText("")
                        settingsWindow.close()
                        break
                    if btnExit.clicked(settingsClick):
                        settingsWindow.close()
                        break
                    if btnQuit.clicked(settingsClick):
                        mainWindow.close()
                        mainWindow2.close()
                        mainWindow3.close()
                        entryWindow.close()
                        btnWindow.close()
                        settingsWindow.close()
                        break                 


        # if the Fetch R button is clicked . . .
        if(btnFetchR.clicked(clickPoint)):
            for rline in rlines:
                rline.undraw()
            coords = mainWindow.currentCoords
            textGetR = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Click an R Value on This Graph")
            textGetR.draw(mainWindow)
            textGetR.setSize(12)
            textGetR.setStyle('italic')
            
            clickPoint2 = mainWindow.getMouse()
            textGetR.setText("")
            R = clickPoint2.getX()
                    
            textR.setText("R = " + str(R))
            plotBifur(R)
            

            plotCobwebs(R)
            plotTimeSeries(R)
            

def plotCobwebs(R):
            global lines

            

  # call the currentCoords and graph x and f(x) from the xmin to xmax
            coords = mainWindow2.currentCoords
            for line in lines:
                line.undraw()
            lines = []

            # set up loading text
            textLoading = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Loading...")
            textLoading.draw(mainWindow)
            textLoading.setSize(12)
            textLoading.setStyle('italic')

            # clear the window
            mainWindow2.clear()

            # for each possible iteration in max iterations undraw each instance of the line if it was drawn.
            for line in lines:
                line.undraw()
            lines = []
            line = Line(Point(R,0), Point(R,1), style = 'solid')
            lines.append(line)
            line.draw(mainWindow)

            i = coords[0]
            while i < coords[2]:
                mainWindow2.plot(i,i)
                mainWindow2.plot(i,R*i*(1-i))
                i += 0.005
            # clear loading text
            textLoading.setText("")
            # flush the window
            mainWindow.flush()

            # update coords
            coords = mainWindow2.currentCoords

           
            # x equals the initial x, and y = f(x)
            initx = enterinitx.getValue()
            iterations = enteriterations.getValue()
            x = initx
            y = R*initx*(1-initx)

            # set up loading text
            textLoading = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Loading...")
            textLoading.draw(mainWindow2)
            textLoading.setSize(12)
            textLoading.setStyle('italic')

            # for each iteration . . .
            for i in range(int(iterations)):
                
                # draw a line at the y value from x to y 
                line = Line(Point(x, y), Point(y,y),style='solid')
                line.draw(mainWindow2)
                lines.append(line)
                # draw another line from y to f(y)
                line2 = Line(Point(y, y), Point(y,R*y*(1-y)),style='solid')
                line2.draw(mainWindow2)
                lines.append(line2)
                # update the x and y to y and f(y)
                x = y
                y = R*y*(1-y)

            # remove loading text
            textLoading.setText("")



def plotBifur(R):
            mainWindow.clear()
            mainWindow.update()
            mainWindow.flush()
            global rlines
            for rline in rlines:
                rline.undraw()
            rline = Line(Point(R,0), Point(R,1), style = 'solid')
            rlines.append(rline)
            rline.draw(mainWindow)

            coords = mainWindow.currentCoords
            textLoading = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Loading...")
            textLoading.draw(mainWindow)
            textLoading.setSize(12)
            textLoading.setStyle('italic')

           
            if coords[0] < 0:
                rvalue = 0
            else:
                rvalue = coords[0]
            if coords[2] > 3:
                rmax = 3
            else:
                rmax = coords[2]
            
            while rvalue <= rmax:

                x = np.random.random()
                
                for i in range(1000):
                    if abs(rvalue*x*(1-x)) != math.inf:
                        x = rvalue*x*(1-x)

                mainWindow.plot(rvalue, (x))
                
                rvalue += (coords[2]-coords[0])/1000
            
            if coords[2] > 3.5:
                rmax = 3.5
            else:
                rmax = coords[2]
            while rvalue <= rmax:
                x = np.random.random()
                for i in range(1000):
                    if abs(rvalue*x*(1-x)) != math.inf:
                        x = rvalue*x*(1-x)
                mainWindow.plot(rvalue, (x))
                rvalue += (coords[2]-coords[0])/3000
            if coords[2] > 4:
                rmax = 4
            else:
                rmax = coords[2]
            while rvalue <= rmax:
                x = np.random.random()
                for i in range(1000):
                    if abs(rvalue*x*(1-x)) != math.inf:
                        x = rvalue*x*(1-x)
                mainWindow.plot(rvalue, (x))
                rvalue += (coords[2]-coords[0])/50000
               
            textLoading.setText("")

           
            saveWindow = DEGraphWin(title = "Buttons",defCoords=[-10,-10,10,10],width = 300,height = 100,offsets=[0,0],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
            saveWindow.setBackground(color_rgb(129,141,146))

            btnSave = Button(
                    saveWindow,
                    Point(-4,0),
                    width = 4,
                    height = 4,
                    edgeWidth = 1,
                    label = 'Save',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnSave.activate()
            btnDontSave = Button(
                    saveWindow,
                    Point(0,0),
                    width = 4,
                    height = 4,
                    edgeWidth = 1,
                    label = 'Exit',
                    buttonColors = [color_rgb(239,71,111),color_rgb(0,16,33),color_rgb(0,16,33)],
                    clickedColors = ['white',color_rgb(0,16,33),color_rgb(0,16,33)],
                    font=('courier',10),
                    timeDelay = 0.25
                    )
            btnDontSave.activate()

            while True:
                if saveWindow.isOpen():
                    
                    clickToSave = Text(Point(0,5), "Save a Higher Definition Image?")
                    clickToSave.draw(saveWindow)
                    clickToSave.setSize(12)
                    clickToSave.setStyle('italic')

                    clickPoint2 = saveWindow.getMouse()

                    if btnSave.clicked(clickPoint2):

                        # THE FOLLOWING IS NOT MY CODE. IT IS FROM STACK OVERFLOW:
                        #   https://stackoverflow.com/questions/47021057/bifurcation-diagram-with-python/47023163
                        
                        imgx = 1000
                        imgy = 500
                        image = Image.new("RGB", (imgx, imgy))

                        xa = 0
                        xb = 4.0
                        maxit = 1000

                        for i in range(imgx):
                            r = xa + (xb - xa) * float(i) / (imgx - 1)
                            x = 0.5
                            for j in range(maxit):
                                x = r * x * (1 - x)
                                if j > maxit / 2:
                                    image.putpixel((i, int(x * imgy)), (255, 255, 255))
                        
                        image.save("Bifurcation.png", "PNG")

                        saveWindow.close()

                        print("Saved as Bifurcation.png")
                        break
                    if btnDontSave.clicked(clickPoint2):
                        saveWindow.close()      
                        break    

def plotTimeSeries(R):
    global lines
    x = np.random.random()
    i = 0
    while i < 5:
        line = Line(Point(i,x),Point(i+0.1,R*x*(1-x)),style = 'solid')
        line.draw(mainWindow3)
        lines.append(line)
        x = R*x*(1-x)
        i += 0.075

if __name__ == "__main__":
    main()
