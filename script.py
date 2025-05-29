import tkinter as tk
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab

NIVEAU_PRINT = 3
MAXDDCARESSEUR =5
ACTUALDDCARESSEUR = 0

def script_caresseur():
    ouvrir_menu_dragodinde()
    cocher_stats_caresseur()
    remplir_enclos_caresseur()

def afficher_message(message):
    log_box.insert(tk.END, message)
    log_box.see(tk.END)
    root.update()

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
    if pattern_est_present("./img/info_ferme.png"):
        if NIVEAU_PRINT > 1:
            afficher_message("Menu fermé detecté")
        cliquer_sur_pattern('./img/statistiques.png')
        if NIVEAU_PRINT > 0:
            afficher_message("Statistique ouverte")
    else :
        if NIVEAU_PRINT > 1:
            afficher_message("Menu ouvert detecté")


def cocher_stats_caresseur():
    cliquer_sur_pattern('./img/serenite_negative.png')
    if NIVEAU_PRINT > 1:
        afficher_message("click sur serenité négative")
    cliquer_sur_pattern('./img/endurance_suffisante.png')
    if NIVEAU_PRINT > 1:
        afficher_message("click sur endurance suffisante")
    cliquer_sur_pattern('./img/besoin_damour.png')
    if NIVEAU_PRINT > 1:
        afficher_message("click sur besoin d'amour")
    if NIVEAU_PRINT > 0:
        afficher_message("stats pour caresseur activé")
        

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
        if NIVEAU_PRINT > 2:
            afficher_message(f"pattern de {pattern_path} trouvé en [{center_x},{center_y}] click")

def pattern_est_present(pattern_path):
    current_image = capturer_ecran()
    pattern = cv2.imread(pattern_path)
    h, w = pattern.shape[:-1]
    res = cv2.matchTemplate(current_image,pattern, cv2.TM_CCOEFF_NORMED)
    treshold = 0.9
    #loc = np.where(res >= treshold)
    if(np.any(res >= treshold)):
        if NIVEAU_PRINT > 2:
            afficher_message(f"pattern de {pattern_path} trouvé")
            return True
    return False

def reste_dragodinde_etable():
    if pattern_est_present('./img/dragodinde_presente_etable.png'):
        if NIVEAU_PRINT > 1:
            afficher_message("dragodinde detecté dans l'étable")
        return True
    else:
        return False
    
def ajouter_premiere_dragodinde():
    cliquer_sur_pattern('./img/dragodinde_presente_etable.png')
    pyautogui.click()
    
def placer_curseur_premiere_dd():
    cliquer_sur_pattern('./img/premiere_dragodinde_etable.png')

def remplir_enclos_caresseur():
    placer_curseur_premiere_dd()
    global ACTUALDDCARESSEUR,MAXDDCARESSEUR
    while ACTUALDDCARESSEUR <= MAXDDCARESSEUR or reste_dragodinde_etable():
        print(ACTUALDDCARESSEUR <= MAXDDCARESSEUR)
        print(reste_dragodinde_etable())
        if NIVEAU_PRINT > 1:
            afficher_message("ajout d'une draoginde dans l'enclos")
        ajouter_premiere_dragodinde()
        ACTUALDDCARESSEUR +=1


root = tk.Tk()
root.title("Bot Récolte Dofus")

frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

btns = tk.Frame(frame)
btns.pack()
tk.Button(btns, text="Caresseur", width=10,command=script_caresseur).grid(row=0, column=0)
tk.Button(btns, text="Baffeur", width=10, command=ouvrir_menu_dragodinde).grid(row=0, column=1)
tk.Button(btns, text="Dragofesse", width=10, command=lambda: ajouter_direction("bas")).grid(row=0, column=2)
tk.Button(btns, text="Foudroyeur", width=10, command=lambda: ajouter_direction("droite")).grid(row=0, column=3)


tk.Label(frame, text="Action en cours :").pack(pady=(10, 0))


log_box = tk.Listbox(root, width=60, height=10)
log_box.pack(padx=10, pady=10)

root.mainloop()