from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from sprite import Sprite, path
    
"""
Start overlay screen (cat screen)
"""
def start_overlay_screen() -> None:
    #Start animate sprite
    sprite = Sprite(window=overlayWin, root=root)
    root.withdraw()
    overlayWin.deiconify()
    overlayWin.state('zoomed')
    sprite.drag_stop()
    print(sprite.canvas)
    overlayWin.after(400, sprite.check_stop)

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
    overlayWin.withdraw()

    root.mainloop()
