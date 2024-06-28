import tkinter as tk

#root = tk.Tk()
'''
root.geometry("800x500")
root.title("LUMO")

label = tk.Label(root, text = "Welcome to LUMO", font = ("Arial, 18"))
label.pack(padx = 20, pady = 20)


textbox = tk.Text(root, height = 3, font = ("Arial", 16))
textbox.pack()

myEntry = tk.Entry(root)
myEntry.pack(padx = 10)

#button = tk.Button(root, text = "Talk To LUMO", font = ("Arial", 18))
#button.pack(padx = 10, pady = 10)

buttonFrame = tk.Frame(root)
buttonFrame.columnconfigure(0, weight = 1)
buttonFrame.columnconfigure(1, weight = 1)
buttonFrame.columnconfigure(2, weight = 1)

btn1 = tk.Button(buttonFrame, text = "1", font = ("Arial", 18))
btn1.grid(row = 0, column = 0, sticky = tk.W + tk.E)

btn2 = tk.Button(buttonFrame, text = "2", font = ("Arial", 18))
btn2.grid(row = 0, column = 1, sticky = tk.W + tk.E)

btn3 = tk.Button(buttonFrame, text = "3", font = ("Arial", 18))
btn3.grid(row = 0, column = 2, sticky = tk.W + tk.E)

buttonFrame.pack(fill = "x")

extraButton = tk.Button(root, text = "TEST")
extraButton.place(x = 200, y = 300, height = 100, width = 100)
'''
class MyGUI:

    def __init__(self):
        '''
        self.root = tk.Tk()

        self.label = tk.Label(self.root, text = "message", font = ("Arial", 18))
        self.label.pack(padx = 10, pady = 10)

        self.textbox = tk.Text(self.root, height = 5, font = ("Arial", 16))
        self.textbox.pack(padx = 10, pady = 10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text = "Show Messagebox", font = ("Arial", 16))
        self.check.pack(padx = 10, pady = 10)

        self.button = tk.Button(self.root, text = "Show Message", font = ("Arial", 18), command = self.show_message)
        self.button.pack(padx = 10, pady = 10)
        '''
        self.root = tk.Tk()
        
        self.root.geometry("800x500")
        self.root.title("LUMO")

        label = tk.Label(self.root, text = "Welcome to LUMO", font = ("Arial, 18"))
        label.pack(padx = 20, pady = 20)


        textbox = tk.Text(self.root, height = 3, font = ("Arial", 16))
        textbox.pack()

        myEntry = tk.Entry(self.root)
        myEntry.pack(padx = 10)

        #button = tk.Button(root, text = "Talk To LUMO", font = ("Arial", 18))
        #button.pack(padx = 10, pady = 10)

        buttonFrame = tk.Frame(self.root)
        buttonFrame.columnconfigure(0, weight = 1)
        buttonFrame.columnconfigure(1, weight = 1)
        buttonFrame.columnconfigure(2, weight = 1)

        btn1 = tk.Button(buttonFrame, text = "1", font = ("Arial", 18))
        btn1.grid(row = 0, column = 0, sticky = tk.W + tk.E)

        btn2 = tk.Button(buttonFrame, text = "2", font = ("Arial", 18))
        btn2.grid(row = 0, column = 1, sticky = tk.W + tk.E)

        btn3 = tk.Button(buttonFrame, text = "3", font = ("Arial", 18))
        btn3.grid(row = 0, column = 2, sticky = tk.W + tk.E)

        buttonFrame.pack(fill = "x")

        extraButton = tk.Button(self.root, text = "TEST")
        extraButton.place(x = 200, y = 300, height = 100, width = 100)

        self.button = tk.Button(self.root, text = "Show Message", font = ("Arial", 18), command = self.show_message)
        self.button.pack(padx = 10, pady = 10)
        
        self.root.mainloop()

    def show_message(self):
        print(self.check_state.get())

MyGUI()