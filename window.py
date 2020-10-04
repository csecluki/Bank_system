from tkinter import *


class Window(Tk):

    def __init__(self):
        Tk.__init__(self)
        frame = Frame(self)
        self.title("Bank Application")
        self.geometry("360x270")
