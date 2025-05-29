import tkinter as tk

def com1():
    log_box.insert(tk.END, "com1")
    log_box.see(tk.END)
    root.update()




root = tk.Tk()
root.title("Bot Récolte Dofus")

frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

btns = tk.Frame(frame)
btns.pack()
tk.Button(btns, text="Caresseur", width=10, command=lambda: ajouter_direction("haut")).grid(row=0, column=0)
tk.Button(btns, text="Baffeur", width=10, command=lambda: ajouter_direction("gauche")).grid(row=0, column=1)
tk.Button(btns, text="Dragofesse", width=10, command=lambda: ajouter_direction("bas")).grid(row=0, column=2)
tk.Button(btns, text="Foudroyeur", width=10, command=lambda: ajouter_direction("droite")).grid(row=0, column=3)


tk.Label(frame, text="Action en cours :").pack(pady=(10, 0))


log_box = tk.Listbox(root, width=60, height=10)
log_box.pack(padx=10, pady=10)

root.mainloop()