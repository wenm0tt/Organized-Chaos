# import everything required (explained in README.md)

from DEgraphics import *
from PIL import Image
import numpy as np
import math

# initialize the main plotting windows.
#   mainWindow will show the bifurcation diagram,
#   mainWindow2 will show the cobweb diagram, and
#   mainWindow3 will show the time series
mainWindow = DEGraphWin(title = "Logistic Map Explorer",defCoords=[-0.4,-0.1,4,1],width = 700,height = 350,offsets=[0,0],autoflush = True,hasTitlebar = False,hThickness=3,hBGColor="black")
mainWindow.setBackground(color_rgb(129,141,146))
mainWindow2 = DEGraphWin(title = "Logistic Map Explorer",defCoords=[-0.1,-0.1,1,1],width = 350,height = 350,offsets=[0,350],autoflush = True,hasTitlebar = False,hThickness=3,hBGColor="black")
mainWindow2.setBackground(color_rgb(129,141,146))
mainWindow3 = DEGraphWin(title = "Logistic Map Explorer",defCoords=[-0.5,-0.1,5,1],width = 350,height = 350,offsets=[350,350],autoflush = True,hasTitlebar = False,hThickness=3,hBGColor="black")
mainWindow3.setBackground(color_rgb(129,141,146))
    
# create two lists that hold lines
lines = []
rlines = []

# initialize the btnWindow, entryWindow, and entries.
btnWindow = DEGraphWin(title = "Buttons",defCoords=[-10,-10,10,10],width = 700,height = 200,offsets=[0,700],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
btnWindow.setBackground(color_rgb(129,141,146))
entryWindow = DEGraphWin(title = "Buttons",defCoords=[-10,-10,10,10],width = 300,height = 900,offsets=[700,0],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
entryWindow.setBackground(color_rgb(129,141,146))
enteriterations = IntEntry(Point(0,4), width = 6, span = [0,500],colors = ['gray','black'],errorColors = ['red','white'])
enterinitx = DblEntry(Point(0,0), width = 6, span = [0,1],colors = ['gray','black'],errorColors = ['red','white'])
enteriterations.draw(entryWindow)
enterinitx.draw(entryWindow)

# Some text to help the user know what's going on
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

# the only two buttons we need. Isn't that nice?
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

# draw the axes' labels
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

# R, by default, will be 2.
R = 2
def main():
    # globalize lines and clickPoint2. This will be useful later.
    global lines
    global clickPoint2

    # turn on the axes
    mainWindow.toggleAxes()
    mainWindow2.toggleAxes()
    mainWindow3.toggleAxes()
    
    # MAIN RUNNING WINDOW
    while True:
        
        # globalize R, the text that shows R, and the list that holds the R line
        global R
        global textR
        global rlines
        
        # as long as the btnWindow is open we know the program is running.
        #   So if it's open we know we can run the getmouse and flush the window.
        #   Otherwise, break from the while loop and end the program
        if btnWindow.isOpen():
            clickPoint = btnWindow.getMouse()   
            mainWindow.flush()  
        else:
            break 
            
        # there are two possibilities: settings is clicked or fetch R is clicked
        #   therefore if settings is clicked . . .
        if (btnSettings.clicked(clickPoint)):
            # create a new window that holds the settings
            settingsWindow = DEGraphWin(title = "Settings",defCoords=[-10,-10,10,10],width = 700,height = 200,offsets=[0,700],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
            settingsWindow.setBackground(color_rgb(129,141,146))

            # initialize all the buttons on settings
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
            
            # while true . . .
            while True:
                
                # if the window is open get the clickpoint and coords
                if settingsWindow.isOpen():
                    settingsClick = settingsWindow.getMouse()
                    coords = mainWindow.currentCoords
                    
                    # if the zoom in button is clicked . . .
                    if btnZoomIn.clicked(settingsClick):
                        
                        # prompt the user to zoom and give instructions
                        textZooming = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Click Two Points on the Graph to Zoom")
                        textZooming.draw(mainWindow)
                        textZooming.setSize(12)
                        textZooming.setStyle('italic')
                        
                        # run the zoom function
                        mainWindow.zoom(whichWay = ZOOM_IN, keepRatio = False)
                        
                        # clear the zoom prompt
                        textZooming.setText("")
                        
                        # replot
                        plotBifur(R)
                        
                        # close the settings window and break the loop
                        settingsWindow.close()
                        break
                        
                    # if zoom out is clicked . . .
                    if btnZoomOut.clicked(settingsClick):
                        
                        # zoom out, replot, and close the settings window
                        mainWindow.zoom(whichWay = ZOOM_OUT, keepRatio = False)
                        plotBifur(R)
                        settingsWindow.close()
                        break
                    
                    # if the user wants to clear all . . . 
                    if btnClear.clicked(settingsClick):
                        
                        # update coords
                        coords = mainWindow.currentCoords
                        
                        # let the user know that we're working on it (because it takes some time to clear)
                        textClearing = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Clearing...")
                        textClearing.draw(mainWindow)
                        textClearing.setSize(12)
                        textClearing.setStyle('italic')
                        
                        # clear all windows
                        mainWindow.clear()
                        mainWindow2.clear()
                        mainWindow3.clear()
                        
                        # undraw all cobweb and time series lines. DO NOT undraw the r line because the user might want to keep it
                        for line in lines:
                            line.undraw()
                        lines = []
                        
                        # clear the clearing text and close the window
                        textClearing.setText("")
                        settingsWindow.close()
                        break
                    
                    # if the user wants to escape . . .
                    if btnExit.clicked(settingsClick):
                        
                        # close the settings window and break
                        settingsWindow.close()
                        break
                    
                    # if the user wants to quit . . .
                    if btnQuit.clicked(settingsClick):
                        
                        # close all windows, break from the settings loop. keep in mind that the 
                        #   fetch R / settings window loop will also be broken because it checks if the windows are open and 
                        #   breaks if they aren't
                        mainWindow.close()
                        mainWindow2.close()
                        mainWindow3.close()
                        entryWindow.close()
                        btnWindow.close()
                        settingsWindow.close()
                        break                 

        # if the fetch R button was clicked . . .
        if(btnFetchR.clicked(clickPoint)):
            
            # undraw the rlines
            for rline in rlines:
                rline.undraw()
                
            # prompt the user to get an R value
            coords = mainWindow.currentCoords
            textGetR = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Click an R Value on This Graph")
            textGetR.draw(mainWindow)
            textGetR.setSize(12)
            textGetR.setStyle('italic')
            
			# grab the x axis value (R value)
            clickPoint2 = mainWindow.getMouse()
            textGetR.setText("")
            R = clickPoint2.getX()
                    
            # update the r text with the new r value
            textR.setText("R = " + str(R))
            
            # plot everything
            plotBifur(R)
            plotCobwebs(R)
            plotTimeSeries(R)
            
# plot cobwebs
def plotCobwebs(R):

            # globalize lines
            global lines

            # update coords
            coords = mainWindow2.currentCoords

            # undraw all lines 
            for line in lines:
                line.undraw()
            lines = []

            # create a loading screen
            textLoading = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Loading...")
            textLoading.draw(mainWindow)
            textLoading.setSize(12)
            textLoading.setStyle('italic')

            # clear the previously plotted graph, if there was one
            mainWindow2.clear()

            # create a line at R
            line = Line(Point(R,0), Point(R,1), style = 'solid')
            lines.append(line)
            line.draw(mainWindow)

            # i starts at the left x value, plots till the right x value, incrementing by 0.005
            i = coords[0]
            while i < coords[2]:

                # plot the steady state line
                mainWindow2.plot(i,i)

                # plot the graph of the logistic map
                mainWindow2.plot(i,R*i*(1-i))
                i += 0.005
            
            # clear the loading text
            textLoading.setText("")

            # flush the window
            mainWindow.flush()

            # update coords
            coords = mainWindow2.currentCoords

            # grab all values required for the cobweb part
            initx = enterinitx.getValue()
            iterations = enteriterations.getValue()

            # set y to f(x), x to the initial x
            x = initx
            y = R*initx*(1-initx)

            # redo the loading prompt
            textLoading = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Loading...")
            textLoading.draw(mainWindow2)
            textLoading.setSize(12)
            textLoading.setStyle('italic')

            # for every iteration the user wants . . .
            for i in range(int(iterations)):
                
                # draw a horizontal line from the graph to the steady state line and append it to lines
                line = Line(Point(x, y), Point(y,y),style='solid')
                line.draw(mainWindow2)
                lines.append(line)
                
                # draw a vertical line from the steady state line to the graph and append it to lines
                line2 = Line(Point(y, y), Point(y,R*y*(1-y)),style='solid')
                line2.draw(mainWindow2)
                lines.append(line2)
               
                # update the x,y
                x = y
                y = R*y*(1-y)

            # after all lines are drawn clear the loading
            textLoading.setText("")


# plot bifurcation
def plotBifur(R):

            # clear, update, flush the window. 
            mainWindow.clear()
            mainWindow.update()
            mainWindow.flush()

            # globalize rlines and undraw all the rlines
            global rlines
            for rline in rlines:
                rline.undraw()

            # draw an rline
            rline = Line(Point(R,0), Point(R,1), style = 'solid')
            rlines.append(rline)
            rline.draw(mainWindow)

            # update coords
            coords = mainWindow.currentCoords

            # create loading text
            textLoading = Text(Point((coords[2]+coords[0])/2,(coords[3]+coords[1])/2), "Loading...")
            textLoading.draw(mainWindow)
            textLoading.setSize(12)
            textLoading.setStyle('italic')

            # MAIN GRAPHING SEGMENT
            #   Split into 3 parts: (0,3), (3,3.5), (3.5,4)
            #   We will graph these at different detail levels to improve user experience. 
            #   We don't need to graph the straight line part or even past a couple period-doubling bifurcations 
            #      with high detail; that being said, it would be nice to see past 3.5 a more detailed graph
            #   The bifurcation diagram is graphed with the following algorithm:
            #       create a random x between 0 and 1, iterate it on the logistic map and see what fixed point it goes to.
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

            # clear the loading text
            textLoading.setText("")

            # create a save window
            saveWindow = DEGraphWin(title = "Buttons",defCoords=[-10,-10,10,10],width = 300,height = 100,offsets=[0,0],autoflush = False,hasTitlebar = False,hThickness=3,hBGColor="black")
            saveWindow.setBackground(color_rgb(129,141,146))
            
            # create a save and don't save button
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
            
            # prompt the user to save
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

# plot time series
def plotTimeSeries(R):

    # globalize lines
    global lines

    # pick a random x value
    x = np.random.random()

    # start i at the left of the window and increment it to the right, plotting as we go
    i = 0
    while i < 5:

        # draw a line from i,x to the next i, f(x)
        line = Line(Point(i,x),Point(i+0.1,R*x*(1-x)),style = 'solid')
        line.draw(mainWindow3)

        # append it to lines
        lines.append(line)
        x = R*x*(1-x)
        i += 0.075

# run the main method
if __name__ == "__main__":
    main()
