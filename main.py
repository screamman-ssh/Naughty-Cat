from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from sprite import Sprite, path
    
"""
Start overlay screen (cat screen)
"""
def start_overlay_screen() -> None:
    #Start animate sprite
    root.withdraw()
    overlayWin.deiconify()
    overlayWin.state('zoomed')
    sprite.drag_stop()
    overlayWin.after(400, sprite.check_stop)

"""
Create window
"""
if __name__ == "__main__":
    BG_CLR = "#FBEADA"
    #Create root window
    root : Tk = Tk()
    root.geometry("255x200")
    root.title("Naughty Cat")
    root.resizable(0,0)
    root.config(bg=BG_CLR)
    iconImg : Image  = Image.open(path("icon.png"))
    iconImg = iconImg.resize((30, 30))
    icon: any = ImageTk.PhotoImage(iconImg)
    root.iconphoto(False, icon)

    #Root/main window widget and layout
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=3)
    labelFrame : ttk.Frame = ttk.Frame(root).grid(row=0, column=0, padx=10,  pady=27)
    iconLabel : ttk.Label = ttk.Label(labelFrame, image=icon, background=BG_CLR)
    iconLabel.place(relx=0.15, rely=0.08)
    titleLabel : ttk.Label = ttk.Label(labelFrame, text="Naughty Cat", font=('Arial', 18), background=BG_CLR)
    titleLabel.place(relx=0.3, rely=0.1)
    #Create cat button to select cat skin
    catNameList : list[str] = ["orange_cat", "black_cat", "stripe_cat"]
    catButtonList : list[ttk.Button] = []
    catIcon : list[any] = []
    for i in range(0, 3):
        catImg : Image  = Image.open(path(f"asset\{catNameList[i]}\sprite_idle_0.png"))
        catImg = catImg.resize((75, 75))
        catIcon.append(ImageTk.PhotoImage(catImg))
        catButton : ttk.Button = ttk.Button(root, image=catIcon[i], command=lambda catName = catNameList[i] : sprite.change_skin(catName)).grid(row=1, column=i, pady=10)
        catButtonList.append(catButton)
    initOverlayButton : ttk.Button = ttk.Button(root, text="Start", command=start_overlay_screen)
    initOverlayButton.grid(row=2, column=1, pady=10)

    #Create overlay window
    overlayWin : Toplevel = Toplevel(root)
    #Set transparent and click-throught window
    overlayWin.config(bg='#2E2E8B')
    overlayWin.attributes('-transparentcolor', '#2E2E8B', '-topmost', 1)
    overlayWin.attributes("-topmost", True)
    overlayWin.overrideredirect(True)   #Set borderless window
    overlayWin.withdraw()

    #Create sprite
    sprite : Sprite = Sprite(window=overlayWin, root=root)

    root.mainloop()
