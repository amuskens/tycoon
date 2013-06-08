

from tkinter import *

class ScaleableImage():
    def __init__(self,x,y,img,scale,canvas,activeimage=None,anchor='cemter'):
        self.scale = scale
        self.x = x
        self.y = y
        self.anchor = anchor

        self.img = img
        if activeimage == None:
            self.aimg = img
        else:
            self.aimg = activeimage

        self.img40 = self.img.zoom(int(self.img.width() * 0.4),int(self.img.height() * 0.4))
        self.img60 = self.img.zoom(int(self.img.width() * 0.6),int(self.img.height() * 0.6))
        self.img80 = self.img.zoom(int(self.img.width() * 0.8),int(self.img.height() * 0.8))

        self.aimg40 = self.aimg.zoom(int(self.aimg.width() * 0.4),int(self.aimg.height() * 0.4))
        self.aimg60 = self.aimg.zoom(int(self.aimg.width() * 0.6),int(self.aimg.height() * 0.6))
        self.aimg80 = self.aimg.zoom(int(self.aimg.width() * 0.8),int(self.aimg.height() * 0.8))

        self.id = None
        self.canvas = canvas

    def rescale(self,scale):

        if self.id:
            self.canvas.delete(self.id)

        if scale == 0.4:
            self.canvas.create_image(self.x,self.y,
                                image=self.img40,
                                activeimage=self.aimg40,
                                anchor=self.anchor)
        elif scale == 0.6:
            self.canvas.create_image(self.x,self.y,
                                image=self.img60,
                                activeimage=self.aimg60,
                                anchor=self.anchor)

        elif scale == 0.8:
            self.canvas.create_image(self.x,self.y,
                                image=self.img80,
                                activeimage=self.aimg80,
                                anchor=self.anchor)

        else:
            self.canvas.create_image(self.x,self.y,
                                image=self.img,
                                activeimage=self.aimg,
                                anchor=self.anchor)
