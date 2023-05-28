from tkinter import *
from tkinter import ttk
from win32api import GetMonitorInfo, MonitorFromPoint
import time
import random
import os.path
import sys

"""
Path join function
"""
def path(target: str) -> str:
    return os.path.join(sys.path[0], target)

"""
Check if draging stopped
"""
stopFrameCount: int = 0
def check_stop():
    global stopFrameCount
    if (canvas.prevX == canvas.winfo_x() and canvas.prevY == canvas.winfo_y()):
        canvas.itemconfig(sprite, image=sprite_drag_idle_img[stopFrameCount % 4])
        #Count stop frame for drag idle animation
        stopFrameCount += 1
        print(f"Move Stop {stopFrameCount}")
    root.after(500, check_stop)

"""
Sprite's movement and random behavior
"""
def move():
    frameCounter: int = 0
    frameLimit: int = random.randint(0, 200)
    # Random move direction
    randBehave: int = random.randint(0, 1)
    if (randBehave):
        step: int = 2
    else:
        step: int = -2
    while True:
        # mouse_pos()
        if (canvas.state == "move"):
            #Change direction when get to leftmost and rightmost of screen
            if (canvas.prevX < 0):
                if (step < 0):
                    step *= -1
                randBehave = 1
                # print("move right")
            elif (canvas.prevX > root.winfo_screenwidth()):
                if (step > 0):
                    step *= -1
                randBehave = 0
                # print("move left")
            #Chech if current behavior event end and random new behavior and duration(frame)
            if (frameCounter > frameLimit):
                randBehave = random.randint(0, 3)
                frameLimit = random.randint(0, 200)
                frameCounter = 0
            #Animate behavior
            #Sit
            if (randBehave == 3):
                frame = (frameCounter % 6)
                step = 0
                canvas.itemconfig(sprite, image=sprite_sit_img[frame])
            #Idle
            elif (randBehave == 2):
                frame = (frameCounter % 4)
                step = 0
                canvas.itemconfig(sprite, image=sprite_idle_img[frame])
            #Walk to right
            elif (randBehave == 1):
                frame = (frameCounter % 7)
                step = 2
                canvas.itemconfig(sprite, image=sprite_walk_r_img[frame])
            #Walk to left
            else:
                frame = (frameCounter % 7)
                step = -2
                canvas.itemconfig(sprite, image=sprite_img[frame])
            #Update canvas
            canvas.prevX += step
            canvas.place(x=canvas.prevX)
            root.update()
            frameCounter += 1
            time.sleep(0.1)
        else:
            break

"""
Drag when start click event handler
"""
def drag_start(event):
    canvas.itemconfig(sprite, image=sprite_drag_img[0])
    canvas.startX = event.x
    canvas.startY = event.y
    canvas.prevX = canvas.winfo_x()
    canvas.prevY = canvas.winfo_y()
    # canvas.state = "drag_start"

"""
Drag move event handler
"""
def drag_motion(event):
    x = canvas.winfo_x() - canvas.startX + event.x
    y = canvas.winfo_y() - canvas.startY + event.y
    canvas.state = "drag_move"
    canvas.place(x=x, y=y)
    #Set zero to stop frame
    global stopFrameCount
    stopFrameCount = 0
    #Detect which direction sprite has been move by draging
    if (canvas.prevX + 8 < x):
        # canvas.state = "move right"
        canvas.itemconfig(sprite, image=sprite_drag_img[2])
    elif (canvas.prevX - 8 > x):
        # canvas.state = "move left"
        canvas.itemconfig(sprite, image=sprite_drag_img[4])
    elif (canvas.prevX + 3 < x):
        canvas.itemconfig(sprite, image=sprite_drag_img[1])
        # print("Slightly Move Right")
    elif (canvas.prevX - 3 > x):
        canvas.itemconfig(sprite, image=sprite_drag_img[3])
        # print("Slightly Move Left")
    if (canvas.prevY < y):
        print("Move Down")
    elif (canvas.prevY > y):
        print("Move Up")
    canvas.prevX = x
    canvas.prevY = y

"""
Stop dragging / Button leave event handler
"""
def drag_stop(event=None):
    bottom: int = root.winfo_screenheight() - sprite_img[0].height()
    currentY: int = canvas.prevY
    canvas.state = "drag_stop"
    print(f"{canvas.prevY} {bottom}")
    while True:
        #Fall event and animation
        if (bottom > currentY and canvas.state != "drag_start"):
            canvas.itemconfig(sprite, image=sprite_img[0])
            currentY += 5
            canvas.place(x=canvas.winfo_x(), y=currentY)
            root.update()
            # time.sleep(0.05)
        elif (canvas.state != "drag_move"):
            currentY = bottom
            canvas.state = "move"
            move()
        else:
            break
"""
Pet animation
"""
def pet():
    canvas.state = "pet"
    for i in range(0, 30):
        if (canvas.state != "drag_move"):
            time.sleep(0.1)
            canvas.itemconfig(sprite, image=sprite_love_img[i % 6])
            root.update()
        else:
            break

# def mouse_pos():
    # x, y = root.winfo_pointerxy()
    # print(f"mouse on {x} - {y}")
    # canvas.state = "trigger"
"""
Context menu popup event handler
"""
def right_click_popup(event):
    try:
        ctx_menu.tk_popup(event.x_root, event.y_root)
    finally:
        ctx_menu.grab_release()


"""
Create root window
"""
root = Tk()
root.state('zoomed')
#Set transparent and click-throught window
root.attributes('-transparentcolor', '#2E2E8B', '-topmost', 1)
root.config(bg='#2E2E8B')
root.attributes("-topmost", True)
#Set borderless window
root.overrideredirect(True)
#Set working area (whole display except taskbar)
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")
print(root.winfo_screenheight())
print(work_area)

"""
Set image list by behavior
"""
sprite_img: list = []
for i in range(0, 7):
    sprite_img.append(PhotoImage(file=path(f"asset\sprite_walk_l_{i}.png")))

sprite_walk_r_img: list = []
for i in range(0, 7):
    sprite_walk_r_img.append(PhotoImage(
        file=path(f"asset\sprite_walk_r_{i}.png")))

sprite_idle_img: list = []
for i in range(0, 4):
    sprite_idle_img.append(PhotoImage(file=path(f"asset\sprite_idle_{i}.png")))

sprite_sit_img: list = []
for i in range(0, 6):
    sprite_sit_img.append(PhotoImage(file=path(f"asset\sprite_sit_{i}.png")))

sprite_love_img: list = []
for i in range(0, 6):
    sprite_love_img.append(PhotoImage(file=path(f"asset\sprite_love_{i}.png")))

sprite_drag_img: list = []
for i in range(0, 5):
    sprite_drag_img.append(PhotoImage(file=path(f"asset\sprite_drag_{i}.png")))

sprite_drag_idle_img: list = []
for i in range(0, 4):
    sprite_drag_idle_img.append(PhotoImage(file=path(f"asset\sprite_drag_idle_{i}.png")))

"""
Create sprite canvas
"""
canvas = Canvas(root, width=sprite_img[0].width() + 30, height=sprite_img[0].height(), bg='#2E2E8B', highlightthickness=0)
canvas.place(x=200, y=root.winfo_screenheight() - sprite_img[0].height())
sprite = canvas.create_image(0, 0, anchor='nw', image=sprite_img[0])
canvas.prevX: int = 500
canvas.prevY: int = root.winfo_screenheight() - sprite_img[0].height()
canvas.state: str = "move"

"""
Right click menu
"""
ctx_menu = Menu(root, tearoff=0)
ctx_menu.add_command(label="Pet", command=pet)
ctx_menu.add_separator()
ctx_menu.add_command(label="Close", command=root.destroy)

"""
Sprite binding
"""
canvas.bind("<Button-1>", drag_start)
canvas.bind("<B1-Motion>", drag_motion)
canvas.bind("<ButtonRelease-1>", drag_stop)
canvas.bind("<Button-3>", right_click_popup)
# canvas.bind("<Leave>", mouse_leave)

"""
Start animate sprite
"""
drag_stop()
root.after(500, check_stop)
root.mainloop()
