from tkinter import *
from tkinter import ttk
from win32api import GetMonitorInfo, MonitorFromPoint
import time
import random

"""
Widget event handler
"""
def move():
    frameCounter: int = 0
    frameLimit: int = random.randint(0, 200)
    label.state = "move"
    time.sleep(0.6)
    #Random move direction
    randBehave : int = random.randint(0, 1)
    if(randBehave) : step: int = 2 
    else: step: int = -2
    while True:
        print(frameCounter)
        print(frameLimit)
        print(randBehave)
        if(label.state == "move"):
            if(label.winfo_x() < 0):
                if(step < 0): step *= -1
                print("move right")
            elif(label.winfo_x() > root.winfo_screenwidth()):
                if(step > 0): step *= -1
                print("move left")

            if(frameCounter >frameLimit):
                randBehave = random.randint(0, 2)
                frameLimit = random.randint(0, 200)
                frameCounter = 0
                if(randBehave == 2): step = 0
                elif(randBehave == 1): step = 2
                else: step = -2
            label.prevX += step
            label.place(x = label.prevX)
            root.update()
            time.sleep(0.1)
            frameCounter += 1
        else:
            break

def drag_start(event):
    label.startX = event.x
    label.startY = event.y
    label.prevX = event.x
    label.prevY = event.y
    label.state : str = "drag_start"
    print(event)

def drag_motion(event):
    x = label.winfo_x() - label.startX + event.x
    y = label.winfo_y() - label.startY + event.y
    label.place(x=x, y=y)
    if(label.prevX < x):
        print("Move Right")
    elif(label.prevX > x):
        print("Move Left")
    
    if(label.prevY < y):
        print("Move Down")
    elif(label.prevY > y):
        print("Move Up")
    
    label.prevX = x
    label.prevY = y
    print(f"{label.prevX} <-> {label.prevY}")

def drag_stop(event):
    bottom: int = root.winfo_height() - label.winfo_height()
    currentY: int = label.prevY
    label.state = "drag_stop"
    while True:
        if(bottom > currentY and label.state != "drag_start"):
            label.place(x = label.prevX, y = currentY + 8)
            print("Fall")
            currentY += 8
            root.update()
            time.sleep(0.05)
        elif(label.state == "drag_start"):
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
root.attributes('-transparentcolor', 'white')
root.config(bg='white') 

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
Create label widget
"""
label = Label(root, bg="red", width=5, height=5)
label.place(x=200, y=work_area[3] - 100, in_=root)
label.prevX: int = 200
label.prevY: int = work_area[3]- 100

"""
Label binding
"""
label.bind("<Button-1>", drag_start)
label.bind("<B1-Motion>", drag_motion)
label.bind("<ButtonRelease-1>", drag_stop)
move()
root.mainloop()