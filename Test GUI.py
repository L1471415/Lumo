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
        self.new_window_frame.pack(side=tk.BOTTOM)

        self.enterText = tk.Entry(self.new_window_frame)
        self.submitButton = ttk.Button(self.new_window_frame, text="example", command=self.submission)

        self.enterText.grid(column=1, row = 1)
        self.submitButton.grid(column=2, row = 1)

    def submission(self):
        what = self.enterText.get()
        textStorage.append(what)

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
        self.InputWindowFrame.pack(side=tk.BOTTOM)
        #self.scrollbar = tk.Scrollbar(master=self.InputWindowFrame)
        #self.scrollbar.grid(column=9, row=7)

    def destroyItself(self):
        self.InputWindowFrame.destroy()

    def updateText(self):
        #for i in self.displayedMessages:
        #    i.destroy()
        #
        self.messageHistory.destroy()
        
        messageHistory = tk.Text(self.InputWindowFrame, width= 50, scroll='x')
        messageHistory.grid(column=1, row=0)

        if (self.messageNumber <= 0):
            for i in range(len(textStorage)):
                #newMessage = tk.Label(self.InputWindowFrame, text=textStorage[len(textStorage)-i-1], background = "#188FA7")
                #newMessage = tk.Text(self.InputWindowFrame, height = 3, width= 50)
                #newMessage.grid(column=1, row=0+i)
                #newMessage.insert(tk.END, textStorage[len(textStorage)-i-1])
                
                
                #self.displayedMessages.append(newMessage)

                messageHistory.insert(tk.End, "\n" + textStorage[len(textStorage)-i-1])

        else:
            for i in range(self.messageNumber):
                #newMessage = tk.Label(self.InputWindowFrame, text=textStorage[len(textStorage)-i-1], background = "#188FA7")
                #newMessage = tk.Text(self.InputWindowFrame, height = 3, width= 50)
                #newMessage.grid(column=1, row=0+i)
                #newMessage.insert(tk.END, textStorage[len(textStorage)-i-1])
                #self.displayedMessages.append(newMessage)
                messageHistory.insert(tk.End, "\n" + textStorage[len(textStorage)-i-1])


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
        self.window_frame.pack(fill = tk.BOTH, expand=True)
        ttk.Label(self.window_frame, text="Hello Lumo!").grid(column=1, row=0)
        button = tk.Button(self.window_frame, text="Kill myself nowwwww!!!!.", command=self.destroy).grid(column = 99, row = 99)

        #self.text_input = TextInput(self.window_frame)

        self.button = tk.Button(self.window_frame, text="switch to input mode", command=self.writeToLumo)
        self.button.grid(column= 1, row = 2)

        self.updateTextTest = tk.Button(self.window_frame, text="update text", command=self.textUpdate)
        self.updateTextTest.grid(column=1, row= 4)

        self.destructionButton = tk.Button(self.window_frame, text="destroy all", command=self.destroyAll)
        self.destructionButton.grid(column=1, row= 3)

        self.text = tk.Text(self.window_frame, height = 5, width = 52)
        temp = """WHAT WHAT WHAT WHAT WHAT WHAT WHAT
        fdsafkdsanfkdsaf
            oinoindsaf
        """

        self.text.insert(tk.INSERT, temp)

        self.tk.mainloop()

    def displayHomeScreen(self):
        print("test")

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