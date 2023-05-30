from tkinter import *
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
Class Sprite module
"""
class Sprite:
    def __init__(self, window, root) -> None:
        self.__load_image()
        #Create sprite canvas
        self.root = root
        self.window = window
        self.sprite_width : int = self.sprite_img_dict["walk_l"][0].width()
        self.sprite_height : int = self.sprite_img_dict["walk_l"][0].height()
        self.canvas = Canvas(self.window, width=self.sprite_width + 30, height=self.sprite_height, bg='#2E2E8B', highlightthickness=0)
        self.canvas.place(x=200, y=self.window.winfo_screenheight() - self.sprite_height)
        self.sprite = self.canvas.create_image(0, 0, anchor='nw', image=self.sprite_img_dict["walk_l"][0])
        self.canvas.prevX: int = 500
        self.canvas.prevY: int = self.window.winfo_screenheight() - self.sprite_height
        self.canvas.state: str = "move"
        #Sprite binding
        self.canvas.bind("<Button-1>", self.drag_start)
        self.canvas.bind("<B1-Motion>", self.drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.drag_stop)
        self.canvas.bind("<Button-3>", self.right_click_popup)
        # canvas.bind("<Leave>", mouse_leave)
        self.create_ctx_menu()

    def __load_image(self) -> None:
        #Set image list by behavior
        self.sprite_img_detail : dict[str, int] = {"walk_l": 7, "walk_r": 7, "idle": 4, "sit": 6, "love": 6, "drag": 5, "drag_idle": 4}
        self.sprite_img_dict : dict[str, list[any]] = {}
        for behave, frame in self.sprite_img_detail.items():
            self.sprite_img_dict[behave] = [PhotoImage(file=path(f"asset\sprite_{behave}_{i}.png"))  for i in range(0, frame)]
        
    def create_ctx_menu(self) -> None:
        #Right click menu
        self.ctx_menu = Menu(self.window, tearoff=0)
        self.ctx_menu.add_command(label="Pet", command=self.pet)
        self.ctx_menu.add_separator()
        self.ctx_menu.add_command(label="Open Main Window", command=self.open_main_window)
        self.ctx_menu.add_command(label="Close", command=self.root.destroy)

    """
    Back to main window
    """
    def open_main_window(self) -> None:
        self.root.deiconify()
        self.window.withdraw()
    """
    Sprite's movement and random behavior
    """
    def move(self) -> None:
        frameCounter: int = 0
        frameLimit: int = random.randint(0, 200)
        behaveStr: str = "idle"
        # Random move direction
        randBehave: int = random.randint(0, 1)
        if (randBehave):
            step: int = 2
        else:
            step: int = -2
        while True:
            # mouse_pos()
            if (self.canvas.state == "move"):
                #Change direction when get to leftmost and rightmost of screen
                if (self.canvas.prevX < 0):
                    if (step < 0):
                        step *= -1
                    randBehave = 1
                    # print("move right")
                elif (self.canvas.prevX > self.window.winfo_screenwidth()):
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
                    behaveStr = "sit"
                    step = 0
                #Idle
                elif (randBehave == 2):
                    behaveStr = "idle"
                    step = 0
                #Walk to right
                elif (randBehave == 1):
                    behaveStr = "walk_r"
                    step = 2
                #Walk to left
                else:
                    behaveStr = "walk_l"
                    step = -2
                #Update canvas
                frame = (frameCounter % self.sprite_img_detail[behaveStr])
                self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict[behaveStr][frame])
                self.canvas.prevX += step
                self.canvas.place(x=self.canvas.prevX)
                self.window.update()
                frameCounter += 1
                time.sleep(0.1)
            else:
                break
    
    """
    Check if draging stopped
    """
    stopFrameCount: int = 0
    def check_stop(self):
        global stopFrameCount
        if (self.canvas.prevX == self.canvas.winfo_x() and self.canvas.prevY == self.canvas.winfo_y()):
            self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag_idle"][stopFrameCount % 4])
            #Count stop frame for drag idle animation
            stopFrameCount += 1
            print(f"Move Stop {stopFrameCount}")
        self.window.after(400, self.check_stop)    

    """
    Drag when start click event handler
    """
    def drag_start(self, event) -> None:
        self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag"][0])
        self.canvas.startX = event.x
        self.canvas.startY = event.y
        self.canvas.prevX = self.canvas.winfo_x()
        self.canvas.prevY = self.canvas.winfo_y()
        # canvas.state = "drag_start"

    """
    Drag move event handler
    """
    def drag_motion(self, event) -> None:
        x = self.canvas.winfo_x() - self.canvas.startX + event.x
        y = self.canvas.winfo_y() - self.canvas.startY + event.y
        self.canvas.state = "drag_move"
        self.canvas.place(x=x, y=y)
        #Set zero to stop frame
        global stopFrameCount
        stopFrameCount = 0
        #Detect which direction sprite has been move by draging
        if (self.canvas.prevX + 8 < x):
            # self.canvas.state = "move right"
            self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag"][2])
        elif (self.canvas.prevX - 8 > x):
            # self.canvas.state = "move left"
            self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag"][4])
        elif (self.canvas.prevX + 3 < x):
            self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag"][1])
            # print("Slightly Move Right")
        elif (self.canvas.prevX - 3 > x):
            self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag"][3])
            # print("Slightly Move Left")
        if (self.canvas.prevY < y):
            print("Move Down")
        elif (self.canvas.prevY > y):
            print("Move Up")
        self.canvas.prevX = x
        self.canvas.prevY = y

    """
    Stop dragging / Button leave event handler
    """
    def drag_stop(self, event=None) -> None:
        self.bottom: int = self.window.winfo_screenheight() - self.sprite_img_dict["drag"][0].height()
        currentY: int = self.canvas.prevY
        self.canvas.state = "drag_stop"
        print(f"{self.canvas.prevY} {self.bottom}")
        while True:
            #Fall event and animation
            if (self.bottom > currentY and self.canvas.state != "drag_start"):
                self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["drag"][0])
                currentY += 5
                self.canvas.place(x=self.canvas.winfo_x(), y=currentY)
                self.window.update()
                # time.sleep(0.05)
            elif (self.canvas.state != "drag_move"):
                currentY = self.bottom
                self.canvas.state = "move"
                self.move()
            else:
                break
        
    """
    Pet animation
    """
    def pet(self) -> None:
        self.canvas.state = "pet"
        for i in range(0, 30):
            if (self.canvas.state != "drag_move"):
                time.sleep(0.1)
                self.canvas.itemconfig(self.sprite, image=self.sprite_img_dict["love"][i % 6])
                self.window.update()
            else:
                break

    # def mouse_pos():
        # x, y = root.winfo_pointerxy()
        # print(f"mouse on {x} - {y}")
        # canvas.state = "trigger"
    """
    Context menu popup event handler
    """
    def right_click_popup(self, event) -> None:
        try:
            self.ctx_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.ctx_menu.grab_release()