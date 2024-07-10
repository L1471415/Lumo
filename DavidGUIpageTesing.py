import tkinter as tk

root = tk.Tk()
root.geometry('500x400')
root.title("Page Testing")

def home_page():
    home_frame = tk.Frame(main_frame)

    lb = tk.Label(home_frame, text = "Home Page", font = ("Bold", 30))
    lb.pack()

    home_frame.pack(pady = 20)

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

def hide_indicators():
    home_indicate.config(bg = "#c3c3c3")
    menu_indicate.config(bg = "#c3c3c3")
    settings_indicate.config(bg = "#c3c3c3")

def indicate(lb, page):
    hide_indicators()
    lb.config(bg = "#158aff")
    delete_pages()
    page()

options_frame = tk.Frame(root, bg = "#c3c3c3")

home_btn = tk.Button(options_frame, text = "Home", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(home_indicate, home_page))
home_btn.place(x = 10, y = 50)
home_indicate = tk.Label(options_frame, text = "", bg = "#c3c3c3")
home_indicate.place(x = 3, y = 50, width = 5, height = 40)

menu_btn = tk.Button(options_frame, text = "Home", font = ("Bold", 15), fg = "#158aff", bd = 0,
                     command = lambda: indicate(menu_indicate, menu_page))
menu_btn.place(x = 10, y = 100)
menu_indicate = tk.Label(options_frame, text = "", bg = "#c3c3c3")
menu_indicate.place(x = 3, y = 100, width = 5, height = 40)

settings_btn = tk.Button(options_frame, text = "Home", font = ("Bold", 15), fg = "#158aff", bd = 0,
                         command = lambda: indicate(settings_indicate, settings_page))
settings_btn.place(x = 10, y = 150)
settings_indicate = tk.Label(options_frame, text = "", bg = "#c3c3c3")
settings_indicate.place(x = 3, y = 150, width = 5, height = 40)

options_frame.pack(side = tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width = 100, height = 400)

main_frame = tk.Frame(root)

main_frame.pack(side = tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height = 400, width = 500)

root.mainloop()