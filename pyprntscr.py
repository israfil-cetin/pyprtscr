import datetime
import time
import tkinter as tk # this is in python 3.4. For python 2.x import Tkinter
from PIL import Image, ImageTk, ImageGrab
from pytesseract import pytesseract

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0

        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        print(self.w, self.h)
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (self.w, self.h))
        self.focus_set()

        self.canvas = tk.Canvas(self, width=self.w, height=self.h, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.configure(background='black')
        self.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)


        self.rect = None

        self.start_x = None
        self.start_y = None


        self._draw_image()


    def _draw_image(self):
        self.im = ImageGrab.grab()
        imgWidth, imgHeight = self.im.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w / imgWidth, self.h / imgHeight)
            imgWidth = int(imgWidth * ratio)
            imgHeight = int(imgHeight * ratio)
            self.im = self.im.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)



    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y


        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline="red")

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)



    def on_button_release(self, event):
        X1,Y1,X2,Y2 = self.start_x,self.start_y,event.x,event.y
        if Y2 <= Y1:
            Y2, Y1 = Y1, Y2

        if X2 <= X1:
            X2, X1 = X1, X2

        im = ImageGrab.grab(bbox=(X1,Y1,X2,Y2))
        # im.save(f"box{time.mktime(datetime.datetime.today().timetuple())}.png")
        text = pytesseract.image_to_string(im, lang="tur")
        print(text[:-1])
        # print(" ".join(('*' + text[:-1] + '*').split())[1:-1])

        self.withdraw()
        self.quit()



if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()