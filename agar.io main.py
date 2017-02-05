from tkinter import *
from tkinter import simpledialog
import time, random, numpy, math


#Mom was here

class Sprite:
    def __init__(self, canvas):
        self.endgame = False
        self.coordinates = None
        self.canvas = canvas
        self.id = None
    def getEaten(self):
        pass
    def coords(self):
        return self.canvas.coords(self.id)

class PlayerSprite(Sprite):
    def __init__(self, canvas):
        self.canvas = canvas
        self.endgame = False
        self.size = 50
        self.inc = 0
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
        print(event.keysym, 'Recieved quitting')
        self.canvas.quit()
        self.canvas.destroy()
    def collision(self, object):
        for obj in object:
            x, y = self.coords()
            fx, fy = obj.coords()
            if fx is not None and fy is not None:
                if ((fx - x)**2 + (fy-y)**2) <= (5 + (self.size/2))**2:
                    obj.getEaten()
                else:
                    pass
            else:
                continue
    def updateSize(self, increment=.4):
        self.inc = increment
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        self.canvas.coords(self.id, x1-(increment/2), y1-(increment/2), x2+(increment/2), y2+(increment/2))

class FoodSprite(Sprite):
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = self.canvas.create_oval(0, 0, 10, 10, fill=random.choice(colors), tag = 'food')
        x, y = self.getRandomCoords()
        self.canvas.move(self.id, x, y)
    def getRandomCoords(self):
        randomx1 = random.randint(0, self.canvas.winfo_reqwidth())

        randomy1 = random.randint(0, self.canvas.winfo_reqheight())
        return randomx1, randomy1
    def getEaten(self):
        self.canvas.delete(self.id)
        player.size += player.inc
        player.updateSize()
        print(player.size)
    def coords(self):
        try:
            coords = self.canvas.coords(self.id)
            retx = coords[0] + 5
            rety = coords[1] + 5
            return retx, rety
        except IndexError:
            return None, None
tk = Tk()
nick = simpledialog.askstring('nickname', 'Nickname')
tk.title("My Agar.io Clone")
tk.wm_attributes('-topmost', 1)
tk.resizable(0, 0)
canvas = Canvas(tk, width=750, height=750)
center =  (canvas.winfo_reqwidth()/2), (canvas.winfo_reqheight()/2)
colors = ['red', 'blue', 'green', 'yellow']

canvas.pack()
foods = []

player = PlayerSprite(canvas)
player.mouseCoords()

canvas.bind_all('<Control-c>', player.end)
count = 0
while player.endgame == False:
    try:
        player.moveTowardMouse()
        player.mouseCoords()
        player.collision(foods)
        if count >= 10:
            food = FoodSprite(canvas)
            foods.append(food)
            count = 0
        count += 1
        tk.update_idletasks()
        tk.update()
        time.sleep(.01)
    except TclError:
        break
