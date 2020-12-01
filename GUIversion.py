#from combat import Node 

import math
import sys
from itertools import product
from pip._vendor.distlib.compat import raw_input
import random
import tkinter as tk
<<<<<<< HEAD
#from PIL import ImageTK, Image
=======
>>>>>>> a05b0c598ce78694d2049f651ab8865ee542b4e9

class App(tk.Frame):
   
    #def  int lengthOfGrid():
     #   for rows in buildGrid():
      #      return rows.length
    #create the canvas 
    def __init__(self, parent, rows, columns ):
        '''size is the size of a square, in pixels'''
        self.size=32
        self.rows = rows
        self.columns = columns
        
<<<<<<< HEAD
        self.pieces = {}
        self.color1="white",
        self.color2="blue"
        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        
        #self.W = ImageTK.PhotoImage(Image.open("Wumpus.png"))
        #self.H = ImageTK.PhotoImage(Image.open("Hero.png"))
        #self.M = ImageTK.PhotoImage(Image.open("Mage.png"))
=======
        self.canvas = tk.Canvas(self, width=540, height=540, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 9
        self.columns = 9
        self.cellwidth = 60
        self.cellheight = 60
>>>>>>> a05b0c598ce78694d2049f651ab8865ee542b4e9
        self.rect = {}
        self.oval = {}

         # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}


        # create a couple of movable objects
        self.create_token(100, 100, "white")
        self.create_token(200, 100, "black")
        self.create_token(200, 100, "blue")

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)
    def create_token(self, x, y, color):
    #Create a token at the given coordinate in the given color
        self.canvas.create_oval(
            x - 25,
            y - 25,
            x + 25,
            y + 25,
            outline=color,
            fill=color,
            tags=("token",),)

        #for column in range(10):
           # for row in range(10):
            #x1 = column*self.cellwidth
           # y1 = row * self.cellheight
           # x2 = x1 + self.cellwidth
            #y2 = y1 + self.cellheight
          #  self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
            
            #self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")
    def drag_start(self, event):
    #Begining drag of an object
    # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        #End drag of an object
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        #Handle dragging of an object
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        
if __name__ == "__main__":
    root = tk.Tk()
    board = App(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
   
    root.mainloop()
    


#root = Tk()
#topFrame = Frame(root)
#topFrame.pack()
#bottomFrame = Frame(root)
#bottomFrame.pack(side = BOTTOM)

#button = Button(topFrame, text = "button 1")
#theLabel = Label(root, text ="Label")
#theLabel.pack()



#frame = Frame(root, width =600, height=500)
#frame.pack()






    

#def main():
    








#if __name__ == '__main__':
    #main()