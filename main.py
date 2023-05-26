from tkinter import *
from tkinter import ttk
from win32api import GetMonitorInfo, MonitorFromPoint
import time
import random
import os.path
import sys

def path(target: str) -> str:
    return os.path.join(sys.path[0], target)
"""
Widget event handler
"""
def move():
    frameCounter: int = 0
    frameLimit: int = random.randint(0, 200)
    canvas.state = "move"
    time.sleep(0.6)
    #Random move direction
    randBehave : int = random.randint(0, 1)
    if(randBehave) : step: int = 2 
    else: step: int = -2
    while True:
        print(frameCounter)
        print(frameLimit)
        print(randBehave)
        if(canvas.state == "move"):
            frame: int = (frameCounter % 7)
            if(canvas.winfo_x() < 0):
                if(step < 0): step *= -1
                print("move right")
            elif(canvas.winfo_x() > root.winfo_screenwidth()):
                if(step > 0): step *= -1
                print("move left")

            if(frameCounter >frameLimit):
                randBehave = random.randint(0, 2)
                frameLimit = random.randint(0, 200)
                frameCounter = 0
                if(randBehave == 2): step = 0
                elif(randBehave == 1): step = 2
                else: step = -2
            canvas.prevX += step
            canvas.itemconfig(sprite,image=sprite_img[frame])
            canvas.place(x = canvas.prevX)
            root.update()
            time.sleep(0.1)
            frameCounter += 1
        else:
            break

def drag_start(event):
    canvas.itemconfig(sprite,image=sprite_img[0])
    canvas.startX = event.x
    canvas.startY = event.y
    canvas.prevX = canvas.winfo_x()
    canvas.prevY = canvas.winfo_y()
    canvas.state : str = "drag_start"

def drag_motion(event):
    x = canvas.winfo_x() - canvas.startX + event.x
    y = canvas.winfo_y() - canvas.startY + event.y
    canvas.place(x=x, y=y)
    canvas.itemconfig(sprite,image=sprite_img[0])
    if(canvas.prevX < x):
        print("Move Right")
        canvas.itemconfig(sprite,image=sprite_img[6])
    elif(canvas.prevX > x):
        canvas.itemconfig(sprite,image=sprite_img[2])
        print("Move Left")
    if(canvas.prevY < y):
        # canvas.itemconfig(sprite,image=sprite_img[0])
        print("Move Down")
    elif(canvas.prevY > y):
        # canvas.itemconfig(sprite,image=sprite_img[1])
        print("Move Up")
    canvas.prevX = x
    canvas.prevY = y
    # print(f"{canvas.prevX} <-> {canvas.prevY}")

def drag_stop(event):
    bottom: int = root.winfo_height() - canvas.winfo_height()
    currentY: int = canvas.winfo_y()
    canvas.state = "drag_stop"
    while True:
        if(bottom > currentY and canvas.state != "drag_start"):
            canvas.itemconfig(sprite,image=sprite_img[0])
            canvas.place(x = canvas.winfo_x(), y = currentY + 8)
            print("Fall")
            currentY += 8
            root.update()
            time.sleep(0.05)
        elif(canvas.state == "drag_start"):
            break
        else:
            currentY = bottom
            move()
        

root = Tk()
# width= root.winfo_screenwidth()               
# height= root.winfo_screenheight()               
# root.geometry("%dx%d" % (width, height))
"""
Set transparent and click-throught window
"""
root.state('zoomed')
root.attributes('-transparentcolor', '#2E2E8B')
root.config(bg='#2E2E8B') 

"""
Set borderless window
"""
# root.overrideredirect(True)

"""
Set working area (whole display except taskbar)
"""
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
root.geometry("%dx%d" % (work_area[2], work_area[3]))
print(root.winfo_screenheight())
print(work_area)

"""
Create sprite canvas
"""
# label = Label(root, bg="red", width=5, height=5)
# label.place(x=200, y=work_area[3] - 100, in_=root)
# label.prevX: int = 200
# label.prevY: int = work_area[3]- 100
sprite_img: list = []
for i in range(1, 8):
    sprite_img.append(PhotoImage(file=path(f"asset\playerfr{i}.png")))
canvas = Canvas(root, width=220, height=340, bg='#2E2E8B', highlightthickness=0)
canvas.place(x=200, y=work_area[3] -520)
sprite = canvas.create_image(0, 0, anchor='nw', image=sprite_img[0])
canvas.prevX: int = 200
canvas.prevY: int = work_area[3]- 520

"""
Label binding
"""
# label.bind("<Button-1>", drag_start)
# label.bind("<B1-Motion>", drag_motion)
# label.bind("<ButtonRelease-1>", drag_stop)

canvas.bind("<Button-1>", drag_start)
canvas.bind("<B1-Motion>", drag_motion)
canvas.bind("<ButtonRelease-1>", drag_stop)
move()
root.mainloop()