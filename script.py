import tkinter as tk
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab


def com1():
    log_box.insert(tk.END, "com1")
    log_box.see(tk.END)
    root.update()

def capturer_ecran():
    screenshot = np.array(ImageGrab.grab())
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
   
    return screenshot

def afficher_capture(capture):
    cv2.imshow("capture",capture)

def ouvrir_menu_dragodinde():
    current_image = capturer_ecran()
    info_ferme_pattern = cv2.imread('./img/info_ferme.png')
    w, h = info_ferme_pattern.shape[:-1]
    res = cv2.matchTemplate(current_image, info_ferme_pattern, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    if np.any(res >= threshold):
        print("j'ai trouvé le menu ferme")
        print(loc)
        statistiques = cv2.imread('./img/statistiques.png')
        h, w = statistiques.shape[:-1]
        res = cv2.matchTemplate(current_image, statistiques, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            print("j'ai trouvé stat")
            cv2.rectangle(current_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            #cv2.imshow('result.jpg', current_image)
            center_x = pt[0] + w //2
            center_y = pt[1] +h //2
            pyautogui.moveTo(center_x,center_y)
            pyautogui.click()

def cliquer_sur_pattern(pattern_path):
    current_image = capturer_ecran()
    pattern = cv2.imread(pattern_path)
    h, w = pattern.shape[:-1]
    res = cv2.matchTemplate(current_image,pattern, cv2.TM_CCOEFF_NORMED)
    treshold = 0.9
    loc = np.where(res >= treshold)
    for pt in zip(*loc[::-1]):
        center_x = pt[0] +w//2
        center_y = pt[1] +h//2
        pyautogui.moveTo(center_x,center_y)
        pyautogui.click()
        log_box.insert("pattern de "+pattern_path+" trouvé en ["+center_x+","+center_y+"] click")

def pattern_est_present(pattern_path):
    current_image = capturer_ecran()
    pattern = cv2.imread(pattern_path)
    h, w = pattern.shape[:-1]
    res = cv2.matchTemplate(current_image,pattern, cv2.TM_CCOEFF_NORMED)
    treshold = 0.9
    #loc = np.where(res >= treshold)
    if(np.any(res >= treshold)):
        log_box.insert("pattern de "+pattern_path+" trouvé")
        return True
    return False


root = tk.Tk()
root.title("Bot Récolte Dofus")

frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

btns = tk.Frame(frame)
btns.pack()
tk.Button(btns, text="Caresseur", width=10,command=capturer_ecran).grid(row=0, column=0)
tk.Button(btns, text="Baffeur", width=10, command=ouvrir_menu_dragodinde).grid(row=0, column=1)
tk.Button(btns, text="Dragofesse", width=10, command=lambda: ajouter_direction("bas")).grid(row=0, column=2)
tk.Button(btns, text="Foudroyeur", width=10, command=lambda: ajouter_direction("droite")).grid(row=0, column=3)


tk.Label(frame, text="Action en cours :").pack(pady=(10, 0))


log_box = tk.Listbox(root, width=60, height=10)
log_box.pack(padx=10, pady=10)

root.mainloop()