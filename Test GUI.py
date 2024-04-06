import tkinter as tk
from tkinter import ttk   

#color palette black: #000000, Egyptian blue: #2F34A5, Blue (Munsell): #188FA7, Air superiority blue: #769FB6, Princeton orange: #F88F1E

class TextInput(tk.Frame):
    def __init__(self, parent):

        #frame2 = tk.Frame(parent, text="Vegetable", bg="yellow", padx=15, pady=15) 

        self.parent = parent
        
        tk.Frame.__init__(self, parent)

        self.input = tk.Entry(master=parent)

        self.input.grid(column=1, row=2)
        self.input_button = ttk.Button(parent, text="submit??", command=self.display_input).grid(column=10, row=0)

        self.storage = []

    def display_input(self):
        display_frame = tk.Frame(master=self.parent, bg="black")

        what = self.input.get()
        self.storage.append(what)
        #tk.Label(self.parent, text=what, background = "green").grid(column=1, row=3)

        for i in range(len(self.storage)):
            tk.Label(self.parent, text=self.storage[len(self.storage)-i-1], background = "#188FA7").grid(column=1, row=10+i)

    def get_inupt():
        what = input.get()


textStorage = []

class TextInputNew(tk.Tk):
    def __init__(self, Window):
        self.window = Window
        self.new_window_frame = tk.Frame(master=self.window, bg="#188FA7")
        self.new_window_frame.pack(side=tk.RIGHT)

        self.enterText = tk.Entry(self.new_window_frame)
        self.submitButton = ttk.Button(self.new_window_frame, text="example", command=self.submission)
    def submission(self):
        what = self.enterText.get()
        textStorage.append(what)

class DisplayInputNew(tk.Tk, int):
    def __init__(self, Window, messageNumber):
        self.window = Window
        self.messageNumber = messageNumber
        self.scrollbar = tk.Scrollbar(master=self.new_window_frame)

        if (self.messageNumber > len(textStorage) or self.messageNumber < 0):
            self.messageNumber = len(textStorage)

        for i in range(len(textStorage)):
            tk.Label(self.new_window_frame, text=textStorage[len(textStorage)-i-1], background = "#188FA7").grid(column=1, row=0+i)

class ShowVideo(tk.Tk):
    def __init__(self, Window):
        videoplayer = TkinterVideo(master=root)
        self.window = Window
    # video code

class Window:
    def __init__(self):
        self.tk = tk.Tk()

        self.tk.geometry('600x400') 

        self.tk.title("Lumo? I hardely Know her!!!!")
        self.window_frame = tk.Frame(master=self.tk, bg="#769FB6")
        self.window_frame.pack(fill = tk.BOTH, side=tk.LEFT, expand=True)
        ttk.Label(self.window_frame, text="Hello Lumo!").grid(column=1, row=0)
        button = tk.Button(self.window_frame, text="Kill myself nowwwww!!!!.", command=self.destroy).grid(column = 1, row = 99)

        #self.text_input = TextInput(self.window_frame)

        button = tk.Button(self.window_frame, text="switch to input mode", command=self.writeToLumo).pack()

        

        self.tk.mainloop()

    def displayHomeScreen(self):
        print("test")
    def writeToLumo(self):
        TextInputNew(self.tk)
        DisplayInputNew(self.tk, 10)
    def displayVideo():
        print("test")
    

    def destroy(self):
        self.tk.destroy()


window = Window()