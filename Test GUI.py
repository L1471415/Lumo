import tkinter as tk
from tkinter import ttk   
from PIL import Image, ImageTk
from datetime import datetime
import pytz
from config import config_variables
import requests, json

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
        #self.new_window_frame.pack(side=tk.BOTTOM)
        self.new_window_frame.grid(column=0, row=5)


        self.enterText = tk.Text(self.new_window_frame, width=60, height=4)
        #self.enterText = tk.Entry(self.new_window_frame)
        self.submitButton = ttk.Button(self.new_window_frame, text="submit", command=self.submission)

        self.enterText.grid(column=1, row = 1)
        self.submitButton.grid(column=2, row = 1)

    def submission(self):
        what = "User: "
        what += self.enterText.get("1.0", 'end-1c')
        textStorage.append(what)
        print(textStorage)
        self.enterText.delete('1.0', tk.END)

    def destroyItself(self):
        self.new_window_frame.destroy()

class VoiceInput(tk.Tk):
    def __init__(self, window):
        print("test")

class DisplayInputNew(tk.Tk):
    def __init__(self, Window, messageNumber):
        self.window = Window
        self.messageNumber = messageNumber
        self.displayedMessages = []
        self.messageHistory = tk.Text()

        self.InputWindowFrame = tk.Frame(master=self.window, bg="#2F34A5")
        self.InputWindowFrame.grid(column=0, row=6)
        #self.InputWindowFrame.pack(side=tk.BOTTOM)
        #self.scrollbar = tk.Scrollbar(master=self.InputWindowFrame)
        #self.scrollbar.grid(column=9, row=7)

    def destroyItself(self):
        self.InputWindowFrame.destroy()

    def updateText(self):
        self.messageHistory.destroy()
        
        
        self.messageHistory = tk.Text(self.InputWindowFrame, width=60, height=15)
        self.messageHistory.grid(column=1, row=0)


        self.messageScrollbar = tk.Scrollbar(self.InputWindowFrame, orient="vertical", command=self.messageHistory.yview)
        self.messageScrollbar.grid(column=3, row=0, sticky='ns')
        self.messageHistory.configure(yscrollcommand=self.messageScrollbar.set)

        if (self.messageNumber <= 0):
            for i in range(len(textStorage)):
                self.messageHistory.insert(tk.END, textStorage[len(textStorage)-i-1] + "\n")

        else:
            for i in range(self.messageNumber):
                self.messageHistory.insert(tk.END, textStorage[len(textStorage)-i-1] + "\n")


class ShowVideo(tk.Tk):
    def __init__(self, Window):
        videoplayer = TkinterVideo(master=root)
        self.window = self.InputWindowFrame = tk.Frame(master=self.window, bg="#2F34A5")

    # video code

class HomeScreen(tk.Tk):
    def __init__(self, Window):
        self.Window = Window
        self.HomeScreenWindowFrame  = tk.Frame(master=self.Window, bg="#188FA7")
        self.HomeScreenWindowFrame.grid(column = 0, row = 0)
        self.current_time = tk.Label(self.HomeScreenWindowFrame, text="null").grid(column= 0, row = 0)
        # Get the timezone object for New York

    def updateTime(self):

        timeZ= pytz.timezone(config_variables.country+"/"+config_variables.city) 
        date = datetime.now(timeZ)
        self.current_time.configure(text=date.strftime("%H:%M:%S"))

    def loadWeather(self, Time):
        self.url = "http://api.openweathermap.org/data/2.5/weather?appid=" + config_variables.api_credentials["openWeatherMap"]["key"] + config_variables.city
        weather_data = requests.get(self.url).json()
        tk.Label(self.HomeScreenWindowFrame, text="Tempature:" + weather_data["daily"]["temp"][Time]).grid(column=0, row=1)
        tk.Label(self.HomeScreenWindowFrame, text="Weather:" + weather_data["daily"]["weather"]["main"]).grid(column=0, row=2)
        tk.Label(self.HomeScreenWindowFrame, text="News:" + weather_data["daily"]["alerts"]["sender_name"]).grid(column=0, row=3)
        tk.Label(self.HomeScreenWindowFrame, text="News:" + weather_data["daily"]["alerts"]["description"]).grid(column=0, row=4)

        # config variables are different in the main branch so it will just be a proof of concept for now

    def destroyItself(self):
        self.HomeScreenWindowFrame.destroy()
        
class Testscreen(tk.Tk):
    def __init__(self, Window):
        self.tk = Window

        self.window_frame = tk.Frame(master=self.tk, bg="#769FB6")
        #self.window_frame.pack(fill = tk.BOTH, expand=True)
        self.window_frame.grid(column=0, row=0)

        canvas = tk.Canvas(master=self.window_frame)
        canvas.create_oval(10, 10, 10, 10, outline = "blue", fill = "white",width = 2)
        #canvas.grid(column=0, row=0)

        image = Image.open("./new_logo.png")
        image = image.resize((100, 100))
        tk_image = ImageTk.PhotoImage(image)
        tk.Label(self.window_frame, image=tk_image).grid(column = 0, row = 0)

        self.button = tk.Button(self.window_frame, text="switch to input mode", command=self.writeToLumo)
        self.button.grid(column= 1, row = 2, padx=100)

        self.updateTextTest = tk.Button(self.window_frame, text="update text", command=self.textUpdate)
        self.updateTextTest.grid(column=1, row= 4)

        self.destructionButton = tk.Button(self.window_frame, text="destroy all", command=self.destroyAll)
        self.destructionButton.grid(column=1, row= 3)


class Window:
    def __init__(self):
        self.tk = tk.Tk()

        self.tk.geometry('550x500') 
        self.tk.title("Lumo")

        # Homescreen is broken for now fix later
        self.loadHomeScreen()
        self.tempFrame = tk.Frame(master=self.tk, bg="#769FB6").grid(column=0, row=1)
        #tk.Button(self.tempFrame, text="Exit HomeScreen", command=self.ExitHomeScreen()).grid(column=0, row=0)

        self.tk.mainloop()

    def loadHomeScreen(self):
        self.HomeScreen = HomeScreen(self.tk)

    def ExitHomeScreen(self):
        self.HomeScreen.destroyItself()
        self.loadTestScreen()

    def loadTestScreen(self):
        self.window_frame = tk.Frame(master=self.tk, bg="#769FB6")
        #self.window_frame.pack(fill = tk.BOTH, expand=True)
        self.window_frame.grid(column=0, row=0)

        canvas = tk.Canvas(master=self.window_frame)
        canvas.create_oval(10, 10, 10, 10, outline = "blue", fill = "white",width = 2)
        #canvas.grid(column=0, row=0)

        image = Image.open("./new_logo.png")
        image = image.resize((100, 100))
        tk_image = ImageTk.PhotoImage(image)
        tk.Label(self.window_frame, image=tk_image).grid(column = 0, row = 0)

        self.button = tk.Button(self.window_frame, text="switch to input mode", command=self.writeToLumo)
        self.button.grid(column= 1, row = 2, padx=100)

        self.updateTextTest = tk.Button(self.window_frame, text="update text", command=self.textUpdate)
        self.updateTextTest.grid(column=1, row= 4)

        self.destructionButton = tk.Button(self.window_frame, text="destroy all", command=self.destroyAll)
        self.destructionButton.grid(column=1, row= 3)

    def writeToLumo(self):
        self.TextInput = TextInputNew(self.tk)
        self.DisplayInput = DisplayInputNew(self.tk, -1)

    def textUpdate(self):
        self.DisplayInput.updateText()

    def displayVideo():
        print("test")

    def destroyAll(self):
        self.TextInput.destroyItself()
        self.DisplayInput.destroyItself()
        
    def destroy(self):
        self.tk.destroy()


window = Window()