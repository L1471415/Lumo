import tkinter as tk

root = tk.Tk()
root.geometry('500x400')
root.title("Page Testing")

def home_page():
    home_frame = tk.Frame(main_frame)

    #Header: "Welcome to LUMO"
    lb = tk.Label(home_frame, text = "Welcome to LUMO", font = ("Bold", 30))
    lb.pack()

    #Button: "Talk to LUMO", goes to talk options page
    talkMenuNew_btn = tk.Button(main_frame, text = "Talk to LUMO", font = ("Bold", 15), fg = "#158aff", bd = 0,
                        command = lambda: indicate(talkMenuNew_indicate, talk_options_page))
    talkMenuNew_btn.place(x = 175, y = 200)
    talkMenuNew_indicate = tk.Label(home_frame, text = "", bg = "#c3c3c3")
    talkMenuNew_indicate.place(x = 3, y = 50, width = 5, height = 40)

    home_frame.pack(pady = 20)

def talk_options_page():
    talkOptions_frame = tk.Frame(main_frame)

    #Header: "How do you want to talk to LUMO?"
    lb = tk.Label(talkOptions_frame, text = "How do you want to talk to LUMO?", font = ("Bold", 20))
    lb.pack()

    #Button: "Talk to LUMO through Voice, goes to voice prompt page"
    talkVoice_btn = tk.Button(main_frame, text = "Talk to LUMO through Voice", font = ("Bold", 15), fg = "#158aff", bd = 0,
                              command = lambda: indicate(talkVoice_indicate, voice_prompt_page))
    talkVoice_btn.place(x = 125, y = 150)
    talkVoice_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkVoice_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Button: "Talk to LUMO through Text", goes to text prompt page
    talkText_btn = tk.Button(main_frame, text = "Talk to LUMO through Text", font = ("Bold", 15), fg = "#158aff", bd = 0,
                             command = lambda: indicate(talkText_indicate, text_prompt_page))
    talkText_btn.place(x = 125, y = 250)
    talkText_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkText_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Button: "Home", goes to home page
    home_btn = tk.Button(main_frame, text = "Home", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
    home_btn.place(x = 10, y = 50)
    home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    home_indicate.place(x = 3, y = 50, width = 5, height = 40)

    talkOptions_frame.pack(pady = 20)

def voice_prompt_page():
    voicePrompt_frame = tk.Frame(main_frame)
    
    #Header: "Hello, how can I help you today?"
    lb = tk.Label(voicePrompt_frame, text = "Hello, how can I help you today?", font = ("Bold", 20))
    lb.pack()

    #Subheader: "Speak request"
    subHeadLb = tk.Label(main_frame, text = "Speak request", font = ("Bold", 12))
    subHeadLb.place(x = 200, y = 75)

    #Button: "Home", goes to home page
    home_btn = tk.Button(main_frame, text = "Home", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
    home_btn.place(x = 10, y = 50)
    home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    home_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Textbox: takes in requests from user
    textbox = tk.Text(main_frame, height = 3, font = ("Arial", 16))
    textbox.place(x = 50, y = 150, width = 400, height = 50)

    #Button: "Talk to LUMO through Text", goes to text prompt page
    talkText_btn = tk.Button(main_frame, text = "Talk to LUMO through Text", font = ("Bold", 15), fg = "#158aff", bd = 0,
                             command = lambda: indicate(talkText_indicate, text_prompt_page))
    talkText_btn.place(x = 125, y = 350)
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
    home_btn = tk.Button(main_frame, text = "Home", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
    home_btn.place(x = 10, y = 50)
    home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    home_indicate.place(x = 3, y = 50, width = 5, height = 40)

    #Textbox: takes in requests from user
    textbox = tk.Text(main_frame, height = 3, font = ("Arial", 16))
    textbox.place(x = 50, y = 150, width = 400, height = 50)

    #Button: "Talk to LUMO through Voice, goes to voice prompt page"
    talkVoice_btn = tk.Button(main_frame, text = "Talk to LUMO through Voice", font = ("Bold", 15), fg = "#158aff", bd = 0,
                              command = lambda: indicate(talkVoice_indicate, voice_prompt_page))
    talkVoice_btn.place(x = 125, y = 350)
    talkVoice_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
    talkVoice_indicate.place(x = 3, y = 50, width = 5, height = 40)

    textPrompt_frame.pack(pady = 20)

def menu_page():
    menu_frame = tk.Frame(main_frame)

    lb = tk.Label(menu_frame, text = "Menu Page", font = ("Bold", 30))
    lb.pack()

    menu_frame.pack(pady = 20)

def settings_page():
    settings_frame = tk.Frame(main_frame)

    lb = tk.Label(settings_frame, text = "Settings Page", font = ("Bold", 30))
    lb.pack()

    settings_frame.pack(pady = 20)

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

#def hide_indicators():
    #home_indicate.config(bg = "#c3c3c3")
    #talkMenu_indicate.config(bg = "#c3c3c3")
    #menu_indicate.config(bg = "#c3c3c3")
    #settings_indicate.config(bg = "#c3c3c3")

def indicate(lb, page):
    #hide_indicators()
    lb.config(bg = "#158aff")
    delete_pages()
    page()

main_frame = tk.Frame(root)

#Header: "Welcome to LUMO"
lb = tk.Label(main_frame, text = "Welcome to LUMO", font = ("Bod", 30))
lb.pack()

main_frame.pack(side = tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height = 400, width = 500)

#Button: "Talk to LUMO", goes to talk options page
talkMenu_btn = tk.Button(main_frame, text = "Talk to LUMO", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(talkMenu_indicate, talk_options_page))
talkMenu_btn.place(x = 175, y = 200)
talkMenu_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
talkMenu_indicate.place(x = 3, y = 50, width = 5, height = 40)






#home_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
'''
menu_btn = tk.Button(main_frame, text = "Menu", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(menu_indicate, menu_page))
menu_btn.place(x = 10, y = 100)
menu_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
menu_indicate.place(x = 3, y = 100, width = 5, height = 40)

settings_btn = tk.Button(main_frame, text = "Settings", font = ("Bold", 15), fg = "#158aff", bd = 0,
                         command = lambda: indicate(settings_indicate, settings_page))
settings_btn.place(x = 10, y = 150)
settings_indicate = tk.Label(main_frame, text = "", bg = "#c3c3c3")
settings_indicate.place(x = 3, y = 150, width = 5, height = 40)
'''
#options_frame.pack(side = tk.LEFT)
#options_frame.pack_propagate(False)
#options_frame.configure(width = 500, height = 400)



root.mainloop()