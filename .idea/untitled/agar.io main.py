from tkinter import *
from tkinter import simpledialog
import time
import random
import math



class Sprite:
    def __init__(self, canvas):
        self.endgame = False
        self.coordinates = None

class PlayerSprite(Sprite):
    def __init__(self, canvas):
        self.canvas = canvas
        self.endgame = False
        self.id = self.canvas.create_oval(350, 350, 400, 400, tag='User', fill=random.choice(colors))
        self.id2 = self.canvas.create_text(375, 375, text=nick, font=('Helvetica', 15), tag='User')
    def coords(self):
        coords = self.canvas.coords(2)
        return coords
    def mouseCoords(self):
        rawMouseX, rawMouseY =   tk.winfo_pointerx(), tk.winfo_pointery()
        self.mousecoords = rawMouseX  - tk.winfo_rootx(), rawMouseY - tk.winfo_rooty()
        return self.mousecoords
    def moveTowardMouse(self):
        selfx, selfy = self.coords()
        mousex, mousey = self.mousecoords
        directDist = math.sqrt(((mousex-selfx) ** 2) + ((mousey-selfy) ** 2))
        self.speed = 4
        movex = (mousex-selfx) / directDist
        movey = (mousey-selfy) / directDist
        self.canvas.move('User', movex*self.speed, movey*self.speed)
    def end(self, event):
        print(event.keysym, 'recieved quitting')
        tk.quit()
        tk.destroy()

class FoodSprite(Sprite):
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = self.canvas.create_oval(1, 1, 10, 10, fill=random.choice(colors))
        x, y = self.getRandomCoords()
        self.canvas.move(self.id, x, y)
    def getRandomCoords(self):
        randomx1 = random.randint(0, self.canvas.winfo_reqwidth())
        randomx2 = random.randint(0, self.canvas.winfo_reqwidth())
        randomy1 = random.randint(0, self.canvas.winfo_reqheight())
        randomy2 = random.randint(0, self.canvas.winfo_reqheight())
        print(randomx1, randomy1)
        return randomx1, randomy1#, randomx2, randomy2
    def getEaten(self):
        self.id.config(state='Hidden')
        
            
tk = Tk()
nick = simpledialog.askstring('nickname', 'Nickname')
tk.title("My Agar.io Clone")
tk.wm_attributes('-topmost', 1)
tk.resizable(0, 0)
canvas = Canvas(tk, width=750, height=750)
center =  (canvas.winfo_reqwidth()/2), (canvas.winfo_reqheight()/2)
colors = ['red', 'blue', 'green', 'yellow']
canvas.pack()

player = PlayerSprite(canvas)
player.mouseCoords()

f = FoodSprite(canvas)
canvas.bind_all(sequence='<Control-c>', func=player.end)

while player.endgame == False:
    try:
        player.moveTowardMouse()
        player.mouseCoords()
        tk.update_idletasks()
        tk.update()
        time.sleep(.01)
    except KeyboardInterrupt:
        print('CRL-C recieved, quitting')
        tk.quit()
        break
