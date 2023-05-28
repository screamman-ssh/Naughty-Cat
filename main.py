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
Check if draging stopped
"""
def check_stop():
    # print(f"{canvas.prevX} - {canvas.prevY} & {canvas.winfo_x()} - {canvas.winfo_y()}")
    if(canvas.prevX == canvas.winfo_x() and canvas.prevY ==  canvas.winfo_y()):
        if(canvas.state == "move right"):
            canvas.itemconfig(sprite,image=sprite_drag_img[1])
        elif(canvas.state == "move left"):
            canvas.itemconfig(sprite,image=sprite_drag_img[3])
        canvas.itemconfig(sprite,image=sprite_drag_img[0])
        print("Move Stop")
    root.after(600, check_stop)

"""
Widget event handler
"""
def move():
    frameCounter: int = 0
    frameLimit: int = random.randint(0, 200)
    canvas.state = "move"
    time.sleep(0.4)
    #Random move direction
    randBehave : int = random.randint(0, 1)
    if(randBehave) : step: int = 2 
    else: step: int = -2
    while True:
        # print(frameCounter)
        # print(frameLimit)
        # print(randBehave)
        # mouse_pos()
        if(canvas.state == "move"):
            if(canvas.prevX < 0):
                if(step < 0): step *= -1
                randBehave = 1
                print("move right")
            elif(canvas.prevX > root.winfo_screenwidth()):
                if(step > 0): step *= -1
                randBehave = 0
                print("move left")

            if(frameCounter >frameLimit):
                randBehave = random.randint(0, 3)
                frameLimit = random.randint(0, 200)
                frameCounter = 0
            
            if(randBehave == 3):
                frame = (frameCounter % 6)
                step = 0
                canvas.itemconfig(sprite,image=sprite_sit_img[frame])
            elif(randBehave == 2):
                frame = (frameCounter % 4)
                step = 0
                canvas.itemconfig(sprite,image=sprite_idle_img[frame])
            elif(randBehave == 1): 
                frame = (frameCounter % 7)
                step = 2
                canvas.itemconfig(sprite,image=sprite_walk_r_img[frame])
            else: 
                frame = (frameCounter % 7)
                step = -2
                canvas.itemconfig(sprite,image=sprite_img[frame])    
            canvas.prevX += step
            canvas.place(x = canvas.prevX)
            root.update()
            frameCounter += 1
            time.sleep(0.1)
        elif(canvas.state != "move"):
            return
        else:
            break
        

def drag_start(event):
    canvas.itemconfig(sprite,image=sprite_drag_img[0])
    canvas.startX = event.x
    canvas.startY = event.y
    canvas.prevX = canvas.winfo_x()
    canvas.prevY = canvas.winfo_y()
    canvas.state : str = "drag_start"

def drag_motion(event):
    x = canvas.winfo_x() - canvas.startX + event.x
    y = canvas.winfo_y() - canvas.startY + event.y
    print(f"{x} - {y}")
    print(f"{canvas.prevX} = {canvas.prevY}")
    canvas.place(x=x, y=y)
    # canvas.itemconfig(sprite,image=sprite_img[0])
    if(canvas.prevX + 8 < x):
        print("Move Right")
        canvas.state = "move right"
        canvas.itemconfig(sprite,image=sprite_drag_img[2])
        print("Move Right")
    elif(canvas.prevX - 8 > x):
        canvas.state = "move left"
        canvas.itemconfig(sprite,image=sprite_drag_img[4])
        print("Move Left")
    elif(canvas.prevX + 3 < x):
        canvas.itemconfig(sprite,image=sprite_drag_img[1])
        print("Slightly Move Right")
    elif(canvas.prevX - 3 > x):
        canvas.itemconfig(sprite,image=sprite_drag_img[3])
        print("Slightly Move Left")

    if(canvas.prevY < y):
        # canvas.itemconfig(sprite,image=sprite_img[0])
        print("Move Down")
    elif(canvas.prevY > y):
        # canvas.itemconfig(sprite,image=sprite_img[1])
        print("Move Up")
    canvas.prevX = x
    canvas.prevY = y
    # print(f"{canvas.prevX} <-> {canvas.prevY}")

def drag_stop(event = None):
    bottom: int =  root.winfo_screenheight() - sprite_img[0].height()
    currentY: int = canvas.prevY
    canvas.state = "drag_stop"
    while True:
        currentY += 1
        if(bottom > currentY and canvas.state != "drag_start"):
            canvas.itemconfig(sprite,image=sprite_img[0])
            currentY += 6
            canvas.place(x = canvas.winfo_x(), y = currentY)
            root.update()
            # time.sleep(0.05)
        elif(canvas.state == "drag_start"):
            break
        else:
            currentY = bottom
            move()
            

# def mouse_pos():
    # x, y = root.winfo_pointerxy()
    # print(f"mouse on {x} - {y}")
    # canvas.state = "trigger"

def handle_double_click(event):
    print("Double Click")
        
def right_click_popup(event):
    try:
        ctx_menu.tk_popup(event.x_root, event.y_root)
    finally:
        ctx_menu.grab_release()


"""
Create root window
Set transparent and click-throught window
"""
root = Tk()
root.state('zoomed')
root.attributes('-transparentcolor', '#2E2E8B', '-topmost', 1)
root.config(bg='#2E2E8B') 
root.attributes("-topmost", True)

"""
Set borderless window
"""
root.overrideredirect(True)

"""
Set working area (whole display except taskbar)
"""
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
print(root.winfo_screenheight())
print(work_area)

"""
Create sprite canvas
"""
sprite_img: list = []
for i in range(0, 7):
    sprite_img.append(PhotoImage(file=path(f"asset\sprite_walk_l_{i}.png")))

sprite_walk_r_img: list = []
for i in range(0, 7):
    sprite_walk_r_img.append(PhotoImage(file=path(f"asset\sprite_walk_r_{i}.png")))

sprite_idle_img: list = []
for i in range(0, 4):
    sprite_idle_img.append(PhotoImage(file=path(f"asset\sprite_idle_{i}.png")))

sprite_sit_img: list = []
for i in range(0, 6):
    sprite_sit_img.append(PhotoImage(file=path(f"asset\sprite_sit_{i}.png")))

sprite_drag_img: list = []
for i in range(0, 5):
    sprite_drag_img.append(PhotoImage(file=path(f"asset\sprite_drag_{i}.png")))

canvas = Canvas(root, width=sprite_img[0].width() + 30, height=sprite_img[0].height(), bg='#2E2E8B', highlightthickness=0)
canvas.place(x=200, y=root.winfo_screenheight() - sprite_img[0].height())
sprite = canvas.create_image(0, 0, anchor='nw', image=sprite_img[0])
canvas.prevX: int = 500
canvas.prevY: int = root.winfo_screenheight() - sprite_img[0].height()
canvas.state: str = "init"

"""
Right click menu
"""
ctx_menu = Menu(root, tearoff=0)
ctx_menu.add_command(label="Close", command=root.destroy)
"""
Sprite binding
"""
canvas.bind("<Button-1>", drag_start)
canvas.bind("<B1-Motion>", drag_motion)
canvas.bind("<ButtonRelease-1>", drag_stop)
# root.bind("<Double-1>", handle_double_click)
canvas.bind("<Button-3>", right_click_popup)
# canvas.bind("<Leave>", mouse_leave)
move()
root.after(400, check_stop)
root.mainloop()