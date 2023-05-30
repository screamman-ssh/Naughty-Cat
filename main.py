from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from sprite import Sprite, path
    
"""
Start overlay screen (cat screen)
"""
def start_overlay_screen() -> None:
    #Start animate sprite
    sprite : Sprite = Sprite(window=overlayWin, root=root)
    root.withdraw()
    overlayWin.deiconify()
    overlayWin.state('zoomed')
    sprite.drag_stop()
    overlayWin.after(400, sprite.check_stop)

"""
Create window
"""
if __name__ == "__main__":
    #Create root window
    root : Tk = Tk()
    root.geometry("255x90")
    root.title("Naughty Cat")
    root.resizable(0,0)

    #Root/main window widget and layout
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    mainFrame : ttk.Frame = ttk.Frame(root).grid(row=1, sticky="nsew")
    iconImg : Image  = Image.open(path("icon.png"))
    iconImg = iconImg.resize((30, 30))
    icon: any = ImageTk.PhotoImage(iconImg)
    iconLabel : ttk.Label = ttk.Label(mainFrame, image=icon)
    iconLabel.place(relx=0.15, rely=0.1)
    titleLabel : ttk.Label = ttk.Label(mainFrame, text="Naughty Cat", font=('Arial', 18))
    titleLabel.place(relx=0.3, rely=0.13)
    initOverlayButton : ttk.Button = ttk.Button(mainFrame, text="Start", command=start_overlay_screen)
    initOverlayButton.place(relx=0.5, rely=0.7, anchor=CENTER )

    #Create overlay window
    overlayWin : Toplevel = Toplevel(root)
    #Set transparent and click-throught window
    overlayWin.config(bg='#2E2E8B')
    overlayWin.attributes('-transparentcolor', '#2E2E8B', '-topmost', 1)
    overlayWin.attributes("-topmost", True)
    overlayWin.overrideredirect(True)   #Set borderless window
    overlayWin.withdraw()

    root.mainloop()
