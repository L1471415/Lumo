import tkinter as tk
#from tkinter import Tk, Label
from PIL import Image, ImageTk
#from tkinter import * 
#from tkinter.ttk import *
from datetime import datetime
from functions.new_assistant_function import get_weather
from new_server_architecture.lumo_chat_management import LumoChatManager

with open("./files/gpt_prompts/commands.yaml", "r", encoding="utf8") as commands:
        lumo_chat_manager = LumoChatManager(model_name="gpt-3.5", initial_prompts=[
            {"role": "system", "content": "You are Lumo, a helpful and friendly voice assistant AI. Only respond as Lumo, and never a user. As Lumo, you have a list of commands you can call by responding to a user with '> command_name', which give you added functionality. Each command must be on its own line and begin with >. A list of the commands you can call and their function is provided: "},
            {"role": "system", "content": commands.read()},
            {"role": "user", "content": "User @ Mon 2024-05-06 12:25:24:Hey Lumo, what's the weather like today?"},
            {"role": "assistant", "content": "Let me check that for you!\n> get_weather"}
        ])

root = tk.Tk()
root.geometry('1200x600')
root.title("Page Testing")

def get_user_voice(voiceInput: str, role: str):
    #Will display user's side of convo\ersation history on a column
    if (role == "user"):
        pass # will implement later
    if (role == "assistant"):
        responseBox.tag_configure("center", justify='left')
        responseBox.delete('1.0', tk.END)
        responseBox.insert(tk.INSERT, voiceInput)
        #text.insert(tk.INSERT, """Ive got a river running right into you I've got a blood trail, red in the blue Something you say or something you do. A taste of the divine. Youve got my body, flesh and bone, yeah. The sky above, the Earth below. Raise me up again. Take me past the edge. I want to see the other side See the other side""")
        responseBox.tag_add("center", 1.0, "end")
        responseBox.place(x = 50, y = 250)

def get_user_text():
    historyBox.insert(tk.INSERT, "User: " + data.get() + "\n\nLumo: ")
    for line in lumo_chat_manager.chat(message = data.get()):
        responseBox.tag_configure("center", justify='left')
        responseBox.delete('1.0', tk.END)
        responseBox.insert(tk.INSERT, line)
        responseBox.tag_add("center", 1.0, "end")
        responseBox.place(x = 50, y = 250)

        historyBox.tag_configure("center", justify='left')
        historyBox.insert(tk.INSERT, line + "\n----------\n")
        historyBox.tag_add("center", 1.0, "end")
    
def home_page():
    home_frame = tk.Frame(main_frame)

    #Header: "Welcome to LUMO"
    lb = tk.Label(home_frame, text = "Welcome to LUMO", font = ("Bold", 30))
    lb.pack()

    #Button: "Talk to LUMO", goes to talk options page
    talkMenuNew_btn = tk.Button(main_frame, text = "Talk to LUMO", image = talkToLumoButtonIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                        command = lambda: indicate(talkMenuNew_indicate, talk_options_page))
    talkMenuNew_btn.place(x = 175, y = 200)
    talkMenuNew_indicate = tk.Label(home_frame, text = "", bg = "#c3c3c3")
    talkMenuNew_indicate.place(x = 3, y = 50, width = 5, height = 40)

    update_weather()

    home_frame.pack(pady = 20)

def talk_options_page():
    talkOptions_frame = tk.Frame(main_frame)

    #Header: "How do you want to talk to LUMO?"
    lb = tk.Label(talkOptions_frame, text = "How do you want to talk to LUMO?", font = ("Bold", 20))
    lb.pack()

    #Button: "Talk to LUMO through Voice, goes to voice prompt page"
    talkVoice_btn = tk.Button(main_frame, text = "Talk to LUMO through Voice", image = talkLumoVoiceIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                              command = lambda: indicate(talkVoice_indicate, voice_prompt_page))
    talkVoice_btn.place(x = 125, y = 150)
    talkVoice_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkVoice_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Button: "Talk to LUMO through Text", goes to text prompt page
    talkText_btn = tk.Button(main_frame, text = "Talk to LUMO through Text", image = talkLumoTextIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                             command = lambda: indicate(talkText_indicate, text_prompt_page))
    talkText_btn.place(x = 125, y = 250)
    talkText_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkText_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Button: "Home", goes to home page
    home_btn = tk.Button(main_frame, text = "Home", image = homeButtonIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
    home_btn.place(x = 10, y = 10)
    home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    home_indicate.place(x = 3, y = 50, width = 5, height = 40)

    talkOptions_frame.pack(pady = 20)
    #img_label.pack()

def voice_prompt_page():
    voicePrompt_frame = tk.Frame(main_frame)
    
    #Header: "Hello, how can I help you today?"
    lb = tk.Label(voicePrompt_frame, text = "Hello, how can I help you today?", font = ("Bold", 20))
    lb.pack()

    #Subheader: "Speak request"
    subHeadLb = tk.Label(main_frame, text = "Speak request", font = ("Bold", 12))
    subHeadLb.place(x = 200, y = 75)

    #Button: "Home", goes to home page
    home_btn = tk.Button(main_frame, text = "Home", image = homeButtonIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
    home_btn.place(x = 10, y = 10)
    home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    home_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Textbox: takes in requests from user
    textBox = tk.Text(main_frame, height = 3, font = ("Arial", 16))
    textBox.place(x = 50, y = 150, width = 400, height = 50)

    #Button: "Talk to LUMO through Text", goes to text prompt page
    talkText_btn = tk.Button(main_frame, text = "Talk to LUMO through Text", image = talkLumoTextIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                             command = lambda: indicate(talkText_indicate, text_prompt_page))
    talkText_btn.place(x = 125, y = 400)
    talkText_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkText_indicate.place(x = 3, y = 50, width = 5, height = 40)

    voicePrompt_frame.pack(pady = 20)  

def text_prompt_page():
    textPrompt_frame = tk.Frame(main_frame)

    #Header: "Hello, how can I help you today?"
    lb = tk.Label(textPrompt_frame, text = "Hello, how can I help you today?", font = ("Bold", 20))
    lb.pack()

    #Subheader: "Type request below"
    subHeadLb = tk.Label(main_frame, text = "Type request below", font = ("Bold", 12))
    subHeadLb.place(x = 175, y = 75)

    #Button: "Home", goes to home page
    home_btn = tk.Button(main_frame, text = "Home", image = homeButtonIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
    home_btn.place(x = 10, y = 10)
    home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    home_indicate.place(x = 3, y = 50, width = 5, height = 40)

    global data
    data = tk.StringVar() # Holds user input text

    #Textbox: takes in requests from user
    inputBox = tk.Entry(main_frame, textvariable = data)
    inputBox.place(x = 50, y = 150, width = 800, height = 50)

    #Button: Enter
    enter_btn = tk.Button(main_frame, text = "Enter", command = get_user_text)
    enter_btn.place(x = 50, y = 200, width = 50, height = 20)

    #Response Box
    global responseBox
    responseBox = tk.Text(main_frame, width = 100, height = 6)

    #Label: "History"
    historyLabel = tk.Label(main_frame, text = "History", font = ("Bold", 20))
    historyLabel.place(x = 980, y = 90)
    
    #History Box
    global historyBox
    historyBox = tk.Text(main_frame, width = 32, height = 25)
    historyBox.place(x = 895, y = 130)

    #Button: "Talk to LUMO through Voice, goes to voice prompt page"
    talkVoice_btn = tk.Button(main_frame, text = "Talk to LUMO through Voice", image = talkLumoVoiceIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                              command = lambda: indicate(talkVoice_indicate, voice_prompt_page))
    talkVoice_btn.place(x = 125, y = 400)
    talkVoice_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkVoice_indicate.place(x = 3, y = 50, width = 5, height = 40)

    textPrompt_frame.pack(pady = 20)

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def update_date_time():
    #Label: current date/time
    currentDateTime = datetime.now().strftime("%a %m/%d/%Y\n%H:%M:%S")
    dateTime = tk.Label(main_frame, text = currentDateTime, font = ("Bod", 18))
    dateTime.place(x = 1020, y = 10)
    main_frame.after(1000, update_date_time)

def update_weather():
    #Label: current weather
    currentWeather = get_weather()
    for (day, weather) in currentWeather["daily"].items():
        print(day)
        print(weather)
        if (day == "Today"):
            weatherData = tk.Label(main_frame, text = str(weather["temp"]) + "° F\n" 
                                   + "High: " + str(weather["high"]) + "° F\n"
                                   + "Low: " + str(weather["low"]) + "° F" , font = ("Bod", 18))
            weatherData.place(x = 1030, y = 100)
            main_frame.after(1_800_000, update_weather)
    

def indicate(lb, page):
    #hide_indicators()
    lb.config(bg = "#158aff")
    delete_pages()
    page()

#Image Files
global homeButtonIcon
homeButtonIcon = ImageTk.PhotoImage(Image.open("HomeButtonIconNew.png").resize((45, 45)))
global talkToLumoButtonIcon
talkToLumoButtonIcon = ImageTk.PhotoImage(Image.open("TalkToLumoButtonIcon.png").resize((300, 105)))
global talkLumoVoiceIcon
talkLumoVoiceIcon = ImageTk.PhotoImage(Image.open("talkLumoVoiceIcon.png").resize((225, 75)))
global talkLumoTextIcon
talkLumoTextIcon = ImageTk.PhotoImage(Image.open("talkLumoTextIcon.png").resize((225, 75)))

main_frame = tk.Frame(root)

#Header: "Welcome to LUMO"
lb = tk.Label(main_frame, text = "Welcome to LUMO", font = ("Bod", 30))
lb.pack()

main_frame.pack(side = tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height = 10000, width = 10000)

#Button: "Talk to LUMO", goes to talk options page
talkMenu_btn = tk.Button(main_frame, text = "Talk to LUMO", image = talkToLumoButtonIcon, font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(talkMenu_indicate, talk_options_page))
talkMenu_btn.place(x = 175, y = 200)
talkMenu_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
talkMenu_indicate.place(x = 3, y = 50, width = 5, height = 40)

#Updates date/time display
update_date_time()

#Updates weather display
update_weather()

root.mainloop()