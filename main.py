from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
import random
import os.path
import sys

"""
Get absolute path to resource, works for dev and for PyInstaller
"""
def path(target: str) -> str:
    # return os.path.join(sys.path[0], target)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, target)
    
"""
Check if draging stopped
"""
stopFrameCount: int = 0
def check_stop():
    global stopFrameCount
    if (canvas.prevX == canvas.winfo_x() and canvas.prevY == canvas.winfo_y()):
        canvas.itemconfig(sprite, image=sprite_img_dict["drag_idle"][stopFrameCount % 4])
        #Count stop frame for drag idle animation
        stopFrameCount += 1
        print(f"Move Stop {stopFrameCount}")
    overlayWin.after(400, check_stop)

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
            elif (canvas.prevX > overlayWin.winfo_screenwidth()):
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
                frame = (frameCounter % sprite_img_detail["sit"])
                step = 0
                canvas.itemconfig(sprite, image=sprite_img_dict["sit"][frame])
            #Idle
            elif (randBehave == 2):
                frame = (frameCounter % sprite_img_detail["idle"])
                step = 0
                canvas.itemconfig(sprite, image=sprite_img_dict["idle"][frame])
            #Walk to right
            elif (randBehave == 1):
                frame = (frameCounter % sprite_img_detail["walk_r"])
                step = 2
                canvas.itemconfig(sprite, image=sprite_img_dict["walk_r"][frame])
            #Walk to left
            else:
                frame = (frameCounter % sprite_img_detail["walk_l"])
                step = -2
                canvas.itemconfig(sprite, image=sprite_img_dict["walk_l"][frame])
            #Update canvas
            canvas.prevX += step
            canvas.place(x=canvas.prevX)
            overlayWin.update()
            frameCounter += 1
            time.sleep(0.1)
        else:
            break

"""
Drag when start click event handler
"""
def drag_start(event):
    canvas.itemconfig(sprite, image=sprite_img_dict["drag"][0])
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
        canvas.itemconfig(sprite, image=sprite_img_dict["drag"][2])
    elif (canvas.prevX - 8 > x):
        # canvas.state = "move left"
        canvas.itemconfig(sprite, image=sprite_img_dict["drag"][4])
    elif (canvas.prevX + 3 < x):
        canvas.itemconfig(sprite, image=sprite_img_dict["drag"][1])
        # print("Slightly Move Right")
    elif (canvas.prevX - 3 > x):
        canvas.itemconfig(sprite, image=sprite_img_dict["drag"][3])
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
    bottom: int = overlayWin.winfo_screenheight() - sprite_img_dict["drag"][0].height()
    currentY: int = canvas.prevY
    canvas.state = "drag_stop"
    print(f"{canvas.prevY} {bottom}")
    while True:
        #Fall event and animation
        if (bottom > currentY and canvas.state != "drag_start"):
            canvas.itemconfig(sprite, image=sprite_img_dict["drag"][0])
            currentY += 5
            canvas.place(x=canvas.winfo_x(), y=currentY)
            overlayWin.update()
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
            canvas.itemconfig(sprite, image=sprite_img_dict["love"][i % 6])
            overlayWin.update()
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
Start overlay screen (cat screen)
"""
def start_overlay_screen():
    #Start animate sprite
    root.withdraw()
    overlayWin.deiconify()
    overlayWin.state('zoomed')
    drag_stop()
    overlayWin.after(400, check_stop)

"""
Back to main window
"""
def open_main_window():
    root.deiconify()
    overlayWin.withdraw()


"""
Create window
"""
if __name__ == "__main__":
    #Create root window
    root = Tk()
    root.geometry("255x90")
    root.title("Naughty Cat")
    root.resizable(0,0)

    #Root/main window widget and layout
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    mainFrame = ttk.Frame(root).grid(row=1, sticky="nsew")
    image = Image.open(path("icon.png"))
    image = image.resize((30, 30))
    photo = ImageTk.PhotoImage(image)
    img = ttk.Label(mainFrame, image=photo)
    img.place(relx=0.15, rely=0.1)
    titleLabel = ttk.Label(mainFrame, text="Naughty Cat", font=('Arial', 18))
    titleLabel.place(relx=0.3, rely=0.13)
    initOverlayButton = ttk.Button(mainFrame, text="Start", command=start_overlay_screen)
    initOverlayButton.place(relx=0.5, rely=0.7, anchor=CENTER )

    #Create overlay window
    overlayWin = Toplevel(root)
    #Set transparent and click-throught window
    overlayWin.config(bg='#2E2E8B')
    overlayWin.attributes('-transparentcolor', '#2E2E8B', '-topmost', 1)
    overlayWin.attributes("-topmost", True)
    overlayWin.overrideredirect(True)   #Set borderless window
    
    

    #Set image list by behavior
    sprite_img_detail : dict[str, int] = {"walk_l": 7, "walk_r": 7, "idle": 4, "sit": 6, "love": 6, "drag": 5, "drag_idle": 4}
    sprite_img_dict : dict[str, list[any]] = {}
    for behave, frame in sprite_img_detail.items():
        sprite_img_dict[behave] = [PhotoImage(file=path(f"asset\sprite_{behave}_{i}.png"))  for i in range(0, frame)]

    #Create sprite canvas
    sprite_width : int = sprite_img_dict["walk_l"][0].width()
    sprite_height : int = sprite_img_dict["walk_l"][0].height()
    canvas = Canvas(overlayWin, width=sprite_width + 30, height=sprite_height, bg='#2E2E8B', highlightthickness=0)
    canvas.place(x=200, y=overlayWin.winfo_screenheight() - sprite_height)
    sprite = canvas.create_image(0, 0, anchor='nw', image=sprite_img_dict["walk_l"][0])
    canvas.prevX: int = 500
    canvas.prevY: int = overlayWin.winfo_screenheight() - sprite_height
    canvas.state: str = "move"
    overlayWin.withdraw()

    #Right click menu
    ctx_menu = Menu(overlayWin, tearoff=0)
    ctx_menu.add_command(label="Pet", command=pet)
    ctx_menu.add_separator()
    ctx_menu.add_command(label="Open Main Window", command=open_main_window)
    ctx_menu.add_command(label="Close", command=root.destroy)

    #Sprite binding
    canvas.bind("<Button-1>", drag_start)
    canvas.bind("<B1-Motion>", drag_motion)
    canvas.bind("<ButtonRelease-1>", drag_stop)
    canvas.bind("<Button-3>", right_click_popup)
    # canvas.bind("<Leave>", mouse_leave)

    root.mainloop()
