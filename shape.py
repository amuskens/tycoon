

from _tkinter import *

class Shape():
    def __init__(self,x,y,img,scale,canvas,activeimage=image,anchor='cemter'):
        self.scale = scale
        self.x = x
        self.y = y
        self.anchor = anchor

        self.img = img
        iw, ih = self.img.size

        size = int(iw * 0.5), int(ih * 0.5)
        self.img50 = PhotoImage(self.img.resize(size))
        size = int(iw * 0.25), int(ih * 0.25)
        self.img25 = PhotoImage(self.img.resize(size))
        size = int(iw * 0.10), int(ih * 0.10)
        self.img10 = PhotoImage(self.img.resize(size))

        self.aimg = activeimage
        iw, ih = self.aimg.size

        size = int(iw * 0.5), int(ih * 0.5)
        self.aimg50 = PhotoImage(self.aimg.resize(size))
        size = int(iw * 0.25), int(ih * 0.25)
        self.aimg25 = PhotoImage(self.aimg.resize(size))
        size = int(iw * 0.10), int(ih * 0.10)
        self.aimg10 = PhotoImage(self.aimg.resize(size))

        self.id = None
        self.canvas = canvas

    def rescale(self,scale):

        if self.id:
            self.canvas.delete(self.id)

        if scale == 0.1:
            self.canvas.create_image(self.x,self.y,
                                image=self.img10,
                                activeimage=self.aimg10,
                                anchor=self.anchor)
        elif scale == 0.25:
            self.canvas.create_image(self.x,self.y,
                                image=self.img25,
                                activeimage=self.aimg25,
                                anchor=self.anchor)

        elif scale == 0.5:
            self.canvas.create_image(self.x,self.y,
                                image=self.img50,
                                activeimage=self.aimg50,
                                anchor=self.anchor)

        else:
            self.canvas.create_image(self.x,self.y,
                                image=self.img,
                                activeimage=self.aimg,
                                anchor=self.anchor)
