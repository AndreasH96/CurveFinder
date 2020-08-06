import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np

class CurvePlotter():
    def __init__(self):
        # Init 
        self.fig, self.ax = plt.subplots(figsize=(5,3), dpi=100)
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')

        plt.subplots_adjust(bottom=0.2)
        self.line, = self.ax.plot([], [], 'k')
        self.ax.set_xlim(-10,10); self.ax.set_ylim(-10,10)
        print(type(self.line))
        print(type(self.ax))
        self.cid = self.fig.canvas.mpl_connect('motion_notify_event', self.moved_and_pressed)
        self.initTextBoxes()
        self.initButtons()
    def initTextBoxes(self):
        axbox = plt.axes([0.1, 0.05, 0.05, 0.05])
        self.textbox = TextBox(axbox,"Evaluate",initial="Test")

    def initButtons(self):
        pass


    def moved_and_pressed(self,event):
        if event.button==1:
            x = np.append(self.line.get_xdata(), event.xdata)
            y = np.append(self.line.get_ydata(), event.ydata)
            self.line.set_data(x, y)
            self.fig.canvas.draw()
        
    def show(self):
        plt.show()
c = CurvePlotter()


c.show()



