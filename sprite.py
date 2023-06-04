from tkinter import *
import time
import random
import os.path
import sys
import math

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
    def __init__(self, window: Toplevel, root: Tk) -> None:
        self.__load_image("orange_cat")
        #Create sprite canvas
        self.frame : int = 0
        self.__root : Tk = root
        self.__window : Toplevel = window
        self.sprite_width : int = self.__sprite_img_dict["drag_idle"][0].width()
        self.sprite_height : int = self.__sprite_img_dict["drag_idle"][0].height()
        self.__canvas : Canvas = Canvas(self.__window, width=self.sprite_width + 30, height=self.sprite_height, bg='#2E2E8B', highlightthickness=0)
        self.__canvas.place(x=(self.__window.winfo_screenwidth() / 2) - self.sprite_width, y= self.__window.winfo_screenheight() - self.sprite_height - 150)
        self.__sprite = self.__canvas.create_image(0, 0, anchor='nw', image=self.__sprite_img_dict["walk_l"][0])
        self.__canvas.prevX : int = (self.__window.winfo_screenwidth() / 2) - self.sprite_width
        self.__canvas.prevY : int = self.__window.winfo_screenheight() - self.sprite_height - 150
        self.__canvas.startX : int = self.__canvas.prevX
        self.__canvas.startY : int = self.__canvas.prevY
        self.__canvas.state : str = "move"
        self.bottom: int = self.__window.winfo_screenheight() - self.__sprite_img_dict["drag"][0].height()
        #Sprite binding
        self.__canvas.bind("<Button-1>", self.drag_start)
        self.__canvas.bind("<B1-Motion>", self.drag_motion)
        self.__canvas.bind("<ButtonRelease-1>", self.drag_stop)
        self.__canvas.bind("<Button-3>", self.right_click_popup)
        # canvas.bind("<Leave>", mouse_leave)
        #Create context menu
        self.__create_ctx_menu()

    """
    Load sprite's asset
    """
    def __load_image(self, catSkinName : str) -> None:
        #Set image list by behavior
        self.__sprite_img_detail : dict[str, int] = {"walk_l": 7, "walk_r": 7, "idle": 4, "sit": 6, "love": 6, "drag": 5, "drag_idle": 4}
        self.__sprite_img_dict : dict[str, list[any]] = {}
        for behave, frame in self.__sprite_img_detail.items():
            self.__sprite_img_dict[behave] = [PhotoImage(file=path(f"asset\\{catSkinName}\\sprite_{behave}_{i}.png"))  for i in range(0, frame)]
    
    """
    Change cat's skin
    """
    def change_skin(self, catSkinName : str) -> None:
        self.__load_image(catSkinName)
    
    """
    Create context menu (right click menu) on sprite
    """
    def __create_ctx_menu(self) -> None:
        #Right click menu
        self.__ctx_menu : Menu = Menu(self.__window, tearoff=0)
        self.__ctx_menu.add_command(label="Pet", command=self.pet)
        self.__ctx_menu.add_command(label="Ball", command=self.catching_ball)
        self.__ctx_menu.add_separator()
        self.__ctx_menu.add_command(label="Open Main Window", command=self.open_main_window)
        self.__ctx_menu.add_command(label="Close", command=self.__root.destroy)

    """
    Context menu popup event handler
    """
    def right_click_popup(self, event) -> None:
        try:
            self.__ctx_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.__ctx_menu.grab_release()

    """
    Back to main window
    """
    def open_main_window(self) -> None:
        self.__root.deiconify()
        self.__window.withdraw()
    
    """
    Sprite's movement and random behavior
    """
    def move(self) -> None:
        self.frame = 0
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
            if (self.__canvas.state == "move"):
                #Change direction when get to leftmost and rightmost of screen
                if (self.__canvas.prevX < 0):
                    if (step < 0):
                        step *= -1
                    randBehave = 1
                    # print("move right")
                elif (self.__canvas.prevX > self.__window.winfo_screenwidth()):
                    if (step > 0):
                        step *= -1
                    randBehave = 0
                    # print("move left")
                #Chech if current behavior event end and random new behavior and duration(frame)
                if (self.frame > frameLimit):
                    randBehave = random.randint(0, 3)
                    frameLimit = random.randint(0, 200)
                    self.frame = 0
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
                sprite_frame = (self.frame % self.__sprite_img_detail[behaveStr])
                self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict[behaveStr][sprite_frame])
                self.__canvas.prevX += step
                self.__canvas.place(x=self.__canvas.prevX)
                self.__window.update()
                self.frame += 1
                time.sleep(0.1)
            else:
                break
    
    """
    Check if draging stopped
    """
    # stopFrameCount: int = 0
    def check_stop(self):
        # global stopFrameCount
        if (self.__canvas.prevX == self.__canvas.winfo_x() and self.__canvas.prevY == self.__canvas.winfo_y() and self.__canvas.state == "drag_move"):
            self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag_idle"][self.frame % 4])
            #Count stop frame for drag idle animation
            self.frame += 1
            # print(f"Move Stop {self.frame}")
        self.__window.after(400, self.check_stop)    

    """
    Drag when start click event handler
    """
    def drag_start(self, event) -> None:
        self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag"][0])
        self.__canvas.startX = event.x
        self.__canvas.startY = event.y
        self.__canvas.prevX = self.__canvas.winfo_x()
        self.__canvas.prevY = self.__canvas.winfo_y()
        self.__canvas.state = "drag_start"

    """
    Drag move event handler
    """
    def drag_motion(self, event) -> None:
        x = self.__canvas.winfo_x() - self.__canvas.startX + event.x
        y = self.__canvas.winfo_y() - self.__canvas.startY + event.y
        self.__canvas.state = "drag_move"
        #Set zero to stop frame
        self.frame = 0
        #Detect which direction sprite has been move by draging
        if (self.__canvas.prevX + 8 < x):
            # self.__canvas.state = "move right"
            self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag"][2])
        elif (self.__canvas.prevX - 8 > x):
            # self.__canvas.state = "move left"
            self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag"][4])
        elif (self.__canvas.prevX + 3 < x):
            self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag"][1])
            # print("Slightly Move Right")
        elif (self.__canvas.prevX - 3 > x):
            self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag"][3])
            # print("Slightly Move Left")
        # if (self.__canvas.prevY < y):
        #     print("Move Down")
        # elif (self.__canvas.prevY > y):
        #     print("Move Up")
        #Check if sprite on bottom
        if (self.bottom >= y): 
            self.__canvas.place(x=x, y=y)
            self.__canvas.prevX = x
            self.__canvas.prevY = y
        else : 
            self.__canvas.place(x=x)
            self.__canvas.prevX = x

    """
    Stop dragging / Button leave event handler
    """
    def drag_stop(self, event=None) -> None:
        currentY: int = self.__canvas.prevY
        self.__canvas.state = "drag_stop"
        while True:
            #Fall event and animation
            if (self.bottom > currentY and self.__canvas.state != "drag_start"):
                self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["drag"][0])
                currentY += 6
                self.__canvas.place(x=self.__canvas.winfo_x(), y=currentY)
                self.__window.update()
                # time.sleep(0.05)
            elif (self.__canvas.state != "drag_move"):
                currentY = self.bottom
                self.__canvas.state = "move"
                self.move()
            else:
                break
        
    """
    Pet animation
    """
    def pet(self) -> None:
        self.__canvas.state = "pet"
        for i in range(0, 30):
            if (self.__canvas.state != "drag_move"):
                time.sleep(0.1)
                self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["love"][i % 6])
                self.__window.update()
            else:
                break

    """
    Ball catching behavior
    """
    def catching_ball(self) -> None:
        #Cancel behavior
        # if (self.__canvas.state not in ["catching_ball", "playing_ball") : 
        #     self.__canvas.state = "move"
        #     return
        self.__canvas.state = "catching_ball"
        #Get mouse position
        mousePos : list[int] = self.__window.winfo_pointerxy()
        #Create ball object
        ball : Ball = Ball(self.__window, mousePos)
        directionCatBehave : str = ""
        self.frame = 0
        step : int = 8
        while True:
            if (self.__canvas.state not in ["move", "drag_start", "drag_move", "playing_ball"]):
                mousePos = self.__window.winfo_pointerxy()
                ball.update_ball_position(mousePos)
                # print(ball.get_postion[0])
                currentX : int = self.__canvas.prevX
                if (currentX + (self.__sprite_img_dict["sit"][0].width() / 2) - 15 < ball.get_postion[0]) : 
                    directionCatBehave = "walk_r"
                    self.__canvas.prevX += step
                elif (currentX + (self.__sprite_img_dict["sit"][0].width() / 2) - 25 > ball.get_postion[0]) : 
                    directionCatBehave = "walk_l"
                    self.__canvas.prevX -= step
                else:
                    if (ball.get_ball_state == "ground") : 
                        self.frame = 0
                        self.__canvas.state = "playing_ball"
                    directionCatBehave = "sit"
                sprite_image : PhotoImage = self.__sprite_img_dict[directionCatBehave][self.frame % self.__sprite_img_detail[directionCatBehave]]
                self.__canvas.itemconfig(self.__sprite, image=sprite_image)
                self.__canvas.place(x = self.__canvas.prevX)
                self.frame += 1
                # print(abs(mousePos[0] - (self.__canvas.winfo_x() + 150)))
                time.sleep(1/(math.sqrt(abs(ball.get_postion[0] - (self.__canvas.winfo_x() + 150)) + 100)))
            elif (self.__canvas.state == "playing_ball") :
                if (self.frame == 60) : self.__canvas.state = "move"
                self.__canvas.itemconfig(self.__sprite, image=self.__sprite_img_dict["love"][self.frame % 6])
                self.frame += 1
                time.sleep(0.1)
            else :
                ball.clearing_ball() 
                break
            self.__window.update()

"""
Ball Class
"""
class Ball:
    """
    Create ball object
    """
    def __init__(self, window : Toplevel, currentPos : list[int]) -> None:
        self.__window : Toplevel = window
        self.__ballImage : PhotoImage = PhotoImage(file=path("asset\\ball.png"))
        self.__ballCanvas : Canvas = Canvas(self.__window, width=self.__ballImage.width(), height=self.__ballImage.height(), bd=0, highlightthickness=0)
        self.__ballCanvas.create_image(0, 0, anchor='nw', image=self.__ballImage)
        self.__ballCanvas.place(x=currentPos[0] - 10, y=currentPos[1])
        self.__ballCanvas.prevX : int = currentPos[0]
        self.__ballCanvas.prevY : int = currentPos[1]
        self.__ballCanvas.state : str = "normal"
        self.__ballCanvas.bind("<Button-1>", self.ball_fall)

    """
    Update ball postion
    """
    def update_ball_position(self, position : list[int]) -> None:
        #Check if ball state is falling
        if (self.__ballCanvas.state == "fall") :
            bottom : int = self.__window.winfo_screenheight() - self.__ballImage.height() - 48 #48 is taskbar height
            if (self.__ballCanvas.prevY + 15 < bottom) :
                self.__ballCanvas.prevY += 15
                self.__ballCanvas.place(y=self.__ballCanvas.prevY)
            else :
                self.__ballCanvas.state = "ground"
                self.__ballCanvas.place(y=bottom)
            return
        elif (self.__ballCanvas.state == "ground") :
            return
        #if not fall, update position from parameter
        self.__ballCanvas.place(x=position[0] - 20, y=position[1] - 20)
        self.__ballCanvas.prevX = position[0]
        self.__ballCanvas.prevY= position[1]
        self.__window.update()

    """
    Ball fall state changing
    """
    def ball_fall(self, event) -> None :
        self.__ballCanvas.state = "fall"

    """
    Clear ball canvas
    """
    def clearing_ball(self) -> None :
        self.__ballCanvas.destroy()
    
    """
    Get ball position as a list
    """
    @property
    def get_postion(self) -> list[int] :
        return [self.__ballCanvas.prevX - (self.__ballImage.width() / 2), self.__ballCanvas.prevY]

    """
    Get current ball's state
    """
    @property
    def get_ball_state(self) -> str :
        return self.__ballCanvas.state