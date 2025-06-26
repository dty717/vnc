import tkinter as tk

class VirtualKeyboard(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Keyboard")
        self.overrideredirect(True)  # Remove window decorations
        self.entryFocused = True
        self.keyboardFocused = False
        # 
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace'
        ]
        # 
        for i, key in enumerate(keys):
            action = lambda x=key: self.insert_key(x)
            btn = tk.Button(self, text=key, width=5, command=action)
            btn.grid(row=i//10, column=i%10)
        # asddd
        # Close keyboard when clicking anywhere outside
    def setEntry(self,entry_widget):
        self.entry = entry_widget
        self.bind("<FocusIn>", lambda event:setattr(self, 'keyboardFocused', True) or  print("keyboard focus", self.entryFocused))
        self.bind("<FocusOut>", lambda event:(not self.entryFocused ) and (print("keyboard unfocus") or self.withdraw()))
        self.entry.bind("<FocusOut>", lambda event: setattr(self, 'entryFocused', False) or print("entry unfocus") or ((not self.keyboardFocused) and (self.withdraw())))
    # 
    def insert_key(self, key):
        if key == "Backspace":
            self.entry.delete(len(self.entry.get()) - 1, tk.END)
        else:
            self.entry.insert(tk.END, key)

def show_keyboard(keyboard,event):
    keyboard.setEntry(event.widget)
    keyboard.deiconify()
    keyboard.geometry(f"+{event.widget.winfo_rootx()}+{event.widget.winfo_rooty() + 30}")  # Position below entry


def on_click_keyboard(keyboard,event):
    if not isinstance(event.widget, tk.Entry):
        keyboard.withdraw()
    else:
        keyboard.deiconify()

# root = tk.Tk()
# root.title("Tkinter Virtual Keyboard")
# root.geometry("%dx%d+0+0" % (500, 500))
# keyboard = VirtualKeyboard()

# entry = tk.Entry(root)
# entry.pack()
# entry.forget()

# entry2 = tk.Entry(root, width=30)
# entry2.pack(pady=10)
# entry2.bind("<FocusIn>", show_keyboard)

# entry3 = tk.Entry(root, width=30)
# entry3.pack(pady=10)
# entry3.bind("<FocusIn>", show_keyboard)

# entry4 = tk.Entry(root, width=30)
# entry4.pack(pady=10)
# entry4.bind("<FocusIn>", show_keyboard)

# button_yes = tk.Button(root, text="textYES")
# button_yes.pack(pady=10)

# def on_click(event):
#     if not isinstance(event.widget, tk.Entry):
#         keyboard.withdraw()
#     else:
#         keyboard.deiconify()
#     # if event.widget not in [entry]:  # Ignore clicks inside Entry
#     #     entry.focus_set()  # Removes focus from Entry

# root.bind("<Button-1>", on_click)                    

# root.mainloop()
