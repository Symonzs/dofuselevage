import tkinter as tk
import numpy as np
import cv2
import random
import pyautogui
import time as t
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import ImageGrab

NIVEAU_PRINT = 3
MAXDDCARESSEUR =5
ACTUALDDCARESSEUR = 0

def script_caresseur():
    global ACTUALDDCARESSEUR
    ouvrir_menu_dragodinde()
    cocher_stats_caresseur()
    while reste_dragodinde_etable():
        placer_curseur_premiere_dd()
        remplir_enclos_caresseur()
        aller_a_random_dragodinde()
        if analyser_fiche_dragodinde():
            pyautogui.click()
            pyautogui.click()
            ACTUALDDCARESSEUR -=1
        





def afficher_message(message):
    log_box.insert(tk.END, message)
    log_box.see(tk.END)
    root.update()

def com1():
    return test_zone_capture(1120, 300, 400, 500)

def test_zone_capture(x, y, w, h):
    # Capture écran complet
    screen = np.array(ImageGrab.grab())

    # Découpe la zone souhaitée
    zone = screen[y:y+h, x:x+w]
    return zone
    # Affiche la zone
    #cv2.imshow("Zone capturée", zone)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

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

def placer_sur_pattern(pattern_path):
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
        
        if NIVEAU_PRINT > 2:
            afficher_message(f"pattern de {pattern_path} trouvé en [{center_x},{center_y}] placement")

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
    afficher_message("je tente de trouver si ya une dd")
    if pattern_est_present('./img/dragodinde_presente_etable.png') or pattern_est_present('./img/premiere_dragodinde_etable.png'):
        if NIVEAU_PRINT > 1:
            afficher_message("dragodinde detecté dans l'étable")
        return True
    else:
        return False
    
def ajouter_premiere_dragodinde():
    cliquer_sur_pattern('./img/dragodinde_presente_etable.png')
    pyautogui.click()
    
def placer_curseur_premiere_dd():
    placer_sur_pattern('./img/premiere_dragodinde_etable.png')

def aller_a_random_dragodinde():
    current_image = capturer_ecran()
    pattern = cv2.imread('./img/dragodinde_dans_enclos.png')
    h, w = pattern.shape[:-1]
    res = cv2.matchTemplate(current_image,pattern, cv2.TM_CCOEFF_NORMED)
    treshold = 0.95
    loc = np.where(res >= treshold)
    points = []
    for pt in zip(*loc[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        points.append((center_x, center_y))
    if not points:
        if NIVEAU_PRINT > 1:
            afficher_message("Aucune dragodinde détectée dans l'enclos.")
        return
    choisi = random.choice(points)
    pyautogui.moveTo(*choisi)

def remplir_enclos_caresseur():
    placer_curseur_premiere_dd()
    global ACTUALDDCARESSEUR,MAXDDCARESSEUR
    while ACTUALDDCARESSEUR < MAXDDCARESSEUR and reste_dragodinde_etable():
        if NIVEAU_PRINT > 1:
            afficher_message("ajout d'une draoginde dans l'enclos")
        ajouter_premiere_dragodinde()
        ACTUALDDCARESSEUR +=1

def analyser_fiche_dragodinde():
    fiche = com1()  # → doit retourner l'image découpée de la fiche
    fiche = cv2.cvtColor(fiche, cv2.COLOR_RGB2BGR)
    afficher_message("je scan la fiche")
    if fiche is None:
        return False

    # -- Détection du sexe --
    sexe = "inconnu"
    try:
        male_icon = cv2.imread('./img/male.png')
        femelle_icon = cv2.imread('./img/femelle.png')
        #cv2.imshow("icon",femelle_icon)
        #cv2.imshow("fiche",fiche)

        if male_icon is not None:
            res_male = cv2.matchTemplate(fiche, male_icon, cv2.TM_CCOEFF_NORMED)
            afficher_message("je vais check si c'est un male")
            if np.max(res_male) > 0.9:
                sexe = "male"
                afficher_message("je detecte un male")

        if femelle_icon is not None:
            res_femelle = cv2.matchTemplate(fiche, femelle_icon, cv2.TM_CCOEFF_NORMED)
            afficher_message("je vais check si c'est une femelle")
            if np.max(res_femelle) > 0.9:
                sexe = "femelle"
                afficher_message("je detecte une femelle")
    except:
        return False

    # -- Lecture de l’humeur --
    try:
        x, y, w, h = 140, 385, 70, 30  # zone relative à la fiche (à ajuster)
        humeur_zone = fiche[y:y+h, x:x+w]
        cv2.imshow("humeur drago",humeur_zone)
        afficher_message("analyse de l'humeur de la dragodinde")
        gray = cv2.cvtColor(humeur_zone, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        config = "--psm 7 -c tessedit_char_whitelist=-0123456789"
        texte = pytesseract.image_to_string(thresh, config=config).strip()
        humeur1 = int(texte)
        x, y, w, h = 140, 385, 70, 30  # zone relative à la fiche (à ajuster)
        humeur_zone = fiche[y:y+h, x:x+w]
        cv2.imshow("humeur drago",humeur_zone)
        afficher_message("analyse de l'humeur de la dragodinde")
        gray = cv2.cvtColor(humeur_zone, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        config = "--psm 7 -c tessedit_char_whitelist=-0123456789"
        texte = pytesseract.image_to_string(thresh, config=config).strip()
        humeur2 = int(texte)
        if humeur1 == humeur2:
            afficher_message(f"j'ai trouver une humeur de {humeur1}")
        else:
            return False
    except:
        return False

    # -- Vérifie les règles --
    if sexe == "femelle" and humeur1 > 0 and humeur2 >0:
        return True
    elif sexe == "male" and humeur1 > 700 and humeur2 > 700:
        return True
    else:
        return False


root = tk.Tk()
root.title("Bot Récolte Dofus")

frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

btns = tk.Frame(frame)
btns.pack()
tk.Button(btns, text="Caresseur", width=10,command=script_caresseur).grid(row=0, column=0)
tk.Button(btns, text="Baffeur", width=10, command=ouvrir_menu_dragodinde).grid(row=0, column=1)
tk.Button(btns, text="Dragofesse", width=10, command=com1).grid(row=0, column=2)
tk.Button(btns, text="Foudroyeur", width=10, command=lambda: ajouter_direction("droite")).grid(row=0, column=3)


tk.Label(frame, text="Action en cours :").pack(pady=(10, 0))


log_box = tk.Listbox(root, width=60, height=10)
log_box.pack(padx=10, pady=10)

root.mainloop()