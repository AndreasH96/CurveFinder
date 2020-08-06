import sys
import time

import numpy as np
from numpy.polynomial import Polynomial as Poly
import copy
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.evaluating = False
        self.polynomial = []
        
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        # Initialize QT layout
        layout = QtWidgets.QVBoxLayout(self._main)
        
        # Create the dynamic canvas and add it as a widget to the layout
        self.dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3),dpi=100))
        layout.addWidget(self.dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(self.dynamic_canvas, self))
        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        
        
        self.dataPoints, = self._dynamic_ax.plot([], [], color="k",linestyle="--",antialiased=True)
        self.dynamic_canvas.mpl_connect('motion_notify_event', self.moved_and_pressed)
        resetButton = QtWidgets.QPushButton("Reset Drawed Curve")
        resetButton.clicked.connect(self.clearData)
        layout.addWidget(resetButton)
        
        evaluateButton = QtWidgets.QPushButton("Find Curve")
        evaluateButton.clicked.connect(self.findCurve)
        layout.addWidget(evaluateButton)
        self.configAxis()
        
        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        self._timer = self.dynamic_canvas.new_timer(
            50, [(self._update_canvas, (), {})])
        self._timer.start()

    def clearData(self):
        self.dataPoints.set_xdata([])
        self.dataPoints.set_ydata([])
        self.evaluating = False
        self.polynomial.clear()
        self._dynamic_ax.clear()
        self.dataPoints, = self._dynamic_ax.plot([], [], color="k",linestyle="--",antialiased=True)
        self.configAxis()
        
        self._dynamic_ax.figure.canvas.draw()

    def configAxis(self):
        
        
        self._dynamic_ax.set_xlim(-1, 1)
        self._dynamic_ax.set_ylim(-1, 1)
        # Center the axes
        self._dynamic_ax.spines['left'].set_position('center')
        self._dynamic_ax.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        self._dynamic_ax.spines['right'].set_color('none')
        self._dynamic_ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        self._dynamic_ax.xaxis.set_ticks_position('bottom')
        self._dynamic_ax.yaxis.set_ticks_position('left')
        self._dynamic_ax.figure.canvas.draw()
        
        
    def _update_canvas(self):
        if(self.evaluating):
            self._dynamic_ax.clear()
            # Use fixed vertical limits to prevent autoscaling changing the scale
            # of the axis.
            #self._dynamic_ax.set_xlim(-1, 1)
            #self._dynamic_ax.set_ylim(-1, 1)
            
            # Center the axes
            self._dynamic_ax.spines['left'].set_position('center')
            self._dynamic_ax.spines['bottom'].set_position('center')
            # Eliminate upper and right axes
            self._dynamic_ax.spines['right'].set_color('none')
            self._dynamic_ax.spines['top'].set_color('none')

            # Show ticks in the left and lower axes only
            self._dynamic_ax.xaxis.set_ticks_position('bottom')
            self._dynamic_ax.yaxis.set_ticks_position('left')

            self._dynamic_ax.plot(self.dataPoints.get_xdata(),self.dataPoints.get_ydata())
            

            

        self._dynamic_ax.figure.canvas.draw()
    
    def moved_and_pressed(self,event):
   
        if event.button==1 and not self.evaluating:
            x = np.append(self.dataPoints.get_xdata(), event.xdata)
            y = np.append(self.dataPoints.get_ydata(), event.ydata)
            self.dataPoints.set_data(x, y)
            self.dynamic_canvas.draw()


    def errorFunction(self):
        pass

    def findCurve(self):
        #self.evaluating = True

        gradient = self.getGradient()
        C0 = self.getC0()


        self._dynamic_ax.plot(gradient.get_xdata(),gradient.get_ydata())
        roots = self.getRoots(gradient)

        self._dynamic_ax.scatter(roots[0,:],roots[1,:])
        curveDegree = len(roots[0,:]) + 1
        start_Coefficients = np.ones(curveDegree)
        start_Coefficients[0] = C0
        polynom = Poly(start_Coefficients)

        prediction = polynom(self.dataPoints.get_xdata())
        
        print(gradient.get_ydata())
        print(self.dataPoints.get_ydata())
        #print(C0)
        self._dynamic_ax.plot(gradient.get_xdata(),prediction)

        self.dynamic_canvas.draw()

    def getGradient(self,data = None):
        if(data == None):
            gradient =  copy.copy(self.dataPoints)
        else:
            gradient = copy.copy(data)
        gradient.set_ydata(np.gradient(np.array(gradient.get_ydata())))
        
        return gradient
        
    def getC0(self):

        dataPoints = np.array(self.dataPoints.get_data())

        print(dataPoints)
        for index in range(len(dataPoints) -1 ):
            if(dataPoints[0,index] < 0 and dataPoints[0,index+1] >= 0):
                #print(dataPoints[1,index+1])
                return dataPoints[1,index+1]
        return 0



    def getRoots(self,grad,grad2=None):
        roots = list()
        gradData = np.array(grad.get_data())
        
        for index in range(1,len(gradData[1]) - 1):
            if np.sign(gradData[1,index]) != np.sign(gradData[1,index+1]):
                root = [gradData[0,index],gradData[1,index]]
                roots.append(root)
        roots = np.transpose(np.array(roots))

        if(grad2 != None):
            terraces = list()

            grad2Data = np.array(grad2.get_data())
            for index in range(1,len(grad2Data[1]) - 1):
                if np.sign(grad2Data[1,index]) != np.sign(grad2Data[1,index+1]):
                    terrace = [grad2Data[0,index],grad2Data[1,index]]
                    terraces.append(terrace)
            terraces = np.transpose(np.array(terraces))

            return roots,terraces
        
        return roots

    
        

if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()