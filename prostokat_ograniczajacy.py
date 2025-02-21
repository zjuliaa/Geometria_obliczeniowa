import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import messagebox

wierzcholki = []
scaled_points = []
scaled =[]
punkty = []
punkty_w_prostokacie = []
punkty_z_klawiatury = []
prostokat_kolor = "red"
wielokat_kolor = "blue"
punkty_z_klawiatury_kolor = "pink"
punkty_w_wielokacie_kolor ="black"
prostokat_grubosc = 2 
wielokat_grubosc = 2

def wczytaj():
    global wierzcholki
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        lines = data.split('\n')
        wierzcholki = []
        for line in lines:
            if line:
                coordinates = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                if len(coordinates) >= 2:
                    x, y = map(float, coordinates[:2])
                    wierzcholki.append((x, y))
    rysuj()

def czytaj_punkty():
    global punkty
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        lines = data.split('\n')
        punkty = []
        for line in lines:
            if line:
                coordinates = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                if len(coordinates) >= 2:
                    x, y = map(float, coordinates[:2])
                    punkty.append((x, y))
    czy_punkt_w_prostokacie()
            
def wyczysc_pasek_wczytanych():
    pasek_wczytanych.delete(1.0, tk.END)

def skaluj(points, canvas_width, canvas_height):
    canvas_margin = 50
    canvas_width = canvas_frame.winfo_width()
    canvas_height = canvas_frame.winfo_height()
    x_min = min(x for x, y in points)
    y_min = min(y for x, y in points)
    x_max = max(x for x, y in points)
    y_max = max(y for x, y in points)
    x_range = x_max - x_min
    y_range = y_max - y_min
    s_x = x_max / (y_max - y_min) 
    s_y = y_max / (x_max - x_min)
    if s_x < s_y:
        s_x = s_y
    else:
        s_y = s_x
    scaled_points = [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in points]
    x_scale = (canvas_width - 2 * canvas_margin) / (x_range * s_x)
    y_scale = (canvas_height - 2 * canvas_margin) / (y_range * s_y)
    scale = min(x_scale, y_scale)
    if x_scale < y_scale:
        x_offset = (canvas_width - x_range * s_x * scale) / 2
        y_offset = canvas_margin
    else:
        x_offset = canvas_margin
        y_offset = (canvas_height - y_range * s_y * scale) / 2
    scaled_points = [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in points]
    scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled_points]
    return x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset
    
def rysuj():
    global x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, wierzcholki, scaled_points
    canvas.delete("all")
    if len(wierzcholki) >= 3:
        x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset = skaluj(wierzcholki, canvas_frame.winfo_width(), canvas_frame.winfo_height())
        scaled =  [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in wierzcholki]
        scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled]
        canvas.create_polygon(scaled_points, outline=wielokat_kolor, fill="", width=wielokat_grubosc)
        x_min_scaled = min(x for x, y in scaled_points)
        y_min_scaled = min(y for x, y in scaled_points)
        x_max_scaled = max(x for x, y in scaled_points)
        y_max_scaled = max(y for x, y in scaled_points)

def rysuj_prostokat():
    global x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, prostokat_kolor
    canvas.create_rectangle(x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, outline=prostokat_kolor, width=prostokat_grubosc)

def czy_punkt_w_prostokacie():
    global x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, punkty, punkty_w_prostokacie
    punkty_w_prostokacie = []
    liczba_punktow = 0   
    if len(punkty) >= 3:
        x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset = skaluj(wierzcholki, canvas_frame.winfo_width(), canvas_frame.winfo_height())
        scaled =  [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in punkty]
        scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled]
        for x, y in scaled_points:
            if x_min_scaled <= x <= x_max_scaled and y_min_scaled <= y <= y_max_scaled:
                #pasek_wczytanych.insert(tk.END, f'Point: ({x:.2f}, {y:.2f}) belongs to the area\n')
                #canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline="black", fill="black", width=2)
                punkty_w_prostokacie.append((x, y)) 
                liczba_punktow += 1
        #pasek_wczytanych.insert(tk.END, f'Liczba punktów w prostokącie ograniczającym: {liczba_punktow}\n')
    czy_punkt_w_wielokacie()

def czy_punkt_w_wielokacie():
    global punkty_w_prostokacie, scaled_points, punkty_w_wielokacie
    punkty_w_wielokacie = []
    liczba_punktow = 0
    if len(punkty_w_prostokacie) > 0:
        for x, y in punkty_w_prostokacie:
            is_inside = False
            j = len(scaled_points) - 1
            for i in range(len(scaled_points)):
                xi, yi = scaled_points[i]
                xj, yj = scaled_points[j]
                on_edge = (yi <= y <= yj or yj <= y <= yi) and min(xi, xj) <= x <= max(xi, xj) and abs((xj - xi) * (y - yi) - (x - xi) * (yj - yi)) < 1e-5
                if on_edge:
                    is_inside = True
                    break
                intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
                if intersect:
                    is_inside = not is_inside
                j = i
            if is_inside:
                #pasek_wczytanych.insert(tk.END, f'Punkt: ({x:.2f}, {y:.2f}) należy do wielokąta\n')
                canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline=punkty_w_wielokacie_kolor, fill=punkty_w_wielokacie_kolor, width=2, tags="punkt_" + str(x) + "_" + str(y))
                punkty_w_wielokacie.append((x, y))
                liczba_punktow += 1
        pasek_wczytanych.insert(tk.END, f'Liczba punktów w wielokąta: {liczba_punktow}\n')
        messagebox.showinfo("Informacja", f'Liczba punktów w wielokącie: {liczba_punktow}')

def dodaj_punkt():
    global punkt_z_klawiatury, x_min_scaled, y_min_scaled, x_max_scaled, y_max_scaled, punkty_z_klawiatury_w_prostokacie, x1, y1

    if not wierzcholki:
        messagebox.showinfo("Błąd", "Wczytaj wielokąt przed dodaniem punktów.")
        return 
    
    x1 = float(entry_x.get())
    y1 = float(entry_y.get())
    punkty_z_klawiatury.append((x1, y1))
    entry_x.delete(0, tk.END)
    entry_y.delete(0, tk.END)
    punkty_z_klawiatury_w_prostokacie = []
    liczba_punktow = 0
    x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset = skaluj(wierzcholki, canvas_frame.winfo_width(), canvas_frame.winfo_height())
    scaled = [(s_x * (y1 - y_min), y_max - s_y * (x1 - x_min)) for x1, y1 in punkty_z_klawiatury]
    scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled]   
    if len(punkty_z_klawiatury) >= 0:
        x_min, y_min, x_max, y_max, s_x, s_y, scale, x_offset, y_offset = skaluj(wierzcholki, canvas_frame.winfo_width(), canvas_frame.winfo_height())
        scaled =  [(s_x * (y - y_min), y_max - s_y * (x - x_min)) for x, y in punkty_z_klawiatury]
        scaled_points = [(x * scale + x_offset, y * scale + y_offset) for x, y in scaled]
        for x, y in scaled_points:
            if x_min_scaled <= x <= x_max_scaled and y_min_scaled <= y <= y_max_scaled:
                punkty_z_klawiatury_w_prostokacie.append((x, y)) 
                liczba_punktow += 1
            else:
                messagebox.showinfo("Błąd", f'Punkt: ({x1:.2f}, {y1:.2f}) nie należy do prostokąta ograniczającego')
    punkty_z_klawiatury.clear()
    punkt_w_wielokacie()

def punkt_w_wielokacie():
    global punkty_z_klawiatury_w_prostokacie, scaled_points
    punkty_z_klawiatury_w_wielokacie = []
    liczba_punktow = 0
    if len(punkty_z_klawiatury_w_prostokacie) > 0:
        for x, y in punkty_z_klawiatury_w_prostokacie:
            is_inside = False
            j = len(scaled_points) - 1
            for i in range(len(scaled_points)):
                xi, yi = scaled_points[i]
                xj, yj = scaled_points[j]
                on_edge = (yi <= y <= yj or yj <= y <= yi) and min(xi, xj) <= x <= max(xi, xj) and abs((xj - xi) * (y - yi) - (x - xi) * (yj - yi)) < 1e-5
                if on_edge:
                    is_inside = True
                    break
                intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
                if intersect:
                    is_inside = not is_inside
                j = i
            if is_inside:
                pasek_wczytanych.insert(tk.END, f'Punkt: ({x1:.2f}, {y1:.2f}) należy do wielokąta\n')
                messagebox.showinfo("Informacja", f'Punkt: ({x1:.2f}, {y1:.2f}) należy do wielokąta')
                canvas.create_oval(x - 2, y - 2, x + 2, y + 2, outline=punkty_z_klawiatury_kolor, fill=punkty_z_klawiatury_kolor, width=4)
                punkty_z_klawiatury_w_wielokacie.append((x, y))
                liczba_punktow += 1
            else:
                pasek_wczytanych.insert(tk.END, f'Punkt: ({x1:.2f}, {y1:.2f}) nie należy do wielokąta\n')
                messagebox.showinfo("Informacja", f'Punkt: ({x1:.2f}, {y1:.2f}) nie należy do wielokąta')

def zmien_kolor_prostokata():
    global prostokat_kolor
    _, prostokat_kolor = colorchooser.askcolor(initialcolor=prostokat_kolor)
    rysuj_prostokat()

def zmien_kolor_wielokata():
    global wielokat_kolor
    _, wielokat_kolor = colorchooser.askcolor(initialcolor=wielokat_kolor)
    rysuj()

def zmien_kolor_punktu_z_klawiatury():
    global punkty_z_klawiatury_kolor
    _, punkty_z_klawiatury_kolor = colorchooser.askcolor(initialcolor=punkty_z_klawiatury_kolor)
    punkt_w_wielokacie()

def zmien_kolor_punkty_w_wielokacie():
    global punkty_w_wielokacie_kolor
    _, punkty_w_wielokacie_kolor = colorchooser.askcolor(initialcolor=punkty_w_wielokacie_kolor)
    czy_punkt_w_wielokacie()

def usun_punkty_w_wielokacie():
    global punkty_w_wielokacie
    for x, y in punkty_w_wielokacie:
        canvas.delete("punkt_" + str(x) + "_" + str(y))  
    punkty_w_wielokacie.clear()

def zmien_grubosc_wielokata(event):
    global wielokat_grubosc
    wielokat_grubosc = int(combo_grubosc_wielokata.get())
    rysuj()

def zmien_grubosc_prostokata(event):
    global prostokat_grubosc
    prostokat_grubosc = int(combo_grubosc_prostokata.get())
    rysuj_prostokat()

root = tk.Tk()
root.title("Python GUI Example")
root.geometry('3000x3000')

canvas_frame = tk.Frame(root, width=1350, height=750, bg="white")
canvas_frame.place(x=550, y=25)
canvas = tk.Canvas(canvas_frame, width=1350, height=750, bg="white")
canvas.pack()
pasek_wczytanych = tk.Text(root, width=55, height=30)
pasek_wczytanych.place(x=40, y=440)
scrollbar = tk.Scrollbar(root, command=pasek_wczytanych.yview)
scrollbar.place(x=467, y=442, height=480)
pasek_wczytanych.config(yscrollcommand=scrollbar.set)

entry_x = tk.Entry(root, width=20)
entry_x.place(x=50, y=20)
entry_y = tk.Entry(root, width=20)
entry_y.place(x=220, y=20)

button1 = tk.Button(root, text="Wybierz plik z wielokątem i narysuj go", font=("Arial", 12), width=50,height=2, command=wczytaj)
button1.place(x=40, y=150)
button2 = tk.Button(root, text="Zamknij program", font=("Arial", 12), width=50,height=2, command=root.destroy)
button2.place(x=1400, y=800)
button3 = tk.Button(root, text="Wyczyść pasek poleceń", width=20, command=wyczysc_pasek_wczytanych)
button3.place(x=35, y=950)
# button4 = tk.Button(root, text="Rysuj wielokąt", font=("Arial", 12), width=50,height=2, command=rysuj)
# button4.place(x=40, y=140)
button5 = tk.Button(root, text="Wybierz plik z punktami i sprawdź je", font=("Arial", 12), width=50,height=2, command=czytaj_punkty)
button5.place(x=40, y=260)
# button6 = tk.Button(root, text="Sprawdz punkt", font=("Arial", 12), width=50,height=2, command=czy_punkt_w_prostokacie)
# button6.place(x=40, y=320)
# button7= tk.Button(root, text="Sprawdz wielokąt", font=("Arial", 12), width=50,height=2, command=czy_punkt_w_wielokacie)
# button7.place(x=40, y=380)
button8 = tk.Button(root, text="Sprawdź", width=20, command=dodaj_punkt)
button8.place(x=360, y=20)
button9 = tk.Button(root, text="Wyczyść onko", font=("Arial", 12), width=50,height=2, command=lambda: canvas.delete("all"))
button9.place(x=1400, y=850)
button10 = tk.Button(root, text="Narysuj prostokąt ograniczający", font=("Arial", 12), width=50,height=2, command=rysuj_prostokat)
button10.place(x=40, y=200)
button11 = tk.Button(root, text="prostokata ograniczającego", font=("Arial", 12), width=50,height=2, command = zmien_kolor_prostokata)
button11.place(x=650, y=850)
button12 = tk.Button(root, text="wielokąta", font=("Arial", 12), width=50,height=2, command = zmien_kolor_wielokata)
button12.place(x=650, y=800)
button13 = tk.Button(root, text="punktu z klawiatury", font=("Arial", 12), width=50,height=2, command = zmien_kolor_punktu_z_klawiatury)
button13.place(x=650, y=900)
button14 = tk.Button(root, text="punkty w wielokącie", font=("Arial", 12), width=50,height=2, command = zmien_kolor_punkty_w_wielokacie)
button14.place(x=650, y=950)
button15 = tk.Button(root, text="Usuń punkty w wielokącie", font=("Arial", 12), width=50, height=2, command=usun_punkty_w_wielokacie)
button15.place(x=1400, y=900)

label_grubosc_wielokata = tk.Label(root, text="Grubość linii wielokąta:", font=("Arial", 12))
label_grubosc_wielokata.place(x=1150, y=800)
combo_grubosc_wielokata = ttk.Combobox(root, values=[1, 2, 3, 4, 5], width=5)
combo_grubosc_wielokata.set(wielokat_grubosc)
combo_grubosc_wielokata.place(x=1150, y=825)
combo_grubosc_wielokata.bind("<<ComboboxSelected>>", zmien_grubosc_wielokata)

label_grubosc_prostokata = tk.Label(root, text="Grubość linii prostokąta:", font=("Arial", 12))
label_grubosc_prostokata.place(x=1150, y=850)
combo_grubosc_prostokata = ttk.Combobox(root, values=[1, 2, 3, 4, 5], width=5)
combo_grubosc_prostokata.set(prostokat_grubosc)
combo_grubosc_prostokata.place(x=1150, y=875)
combo_grubosc_prostokata.bind("<<ComboboxSelected>>", zmien_grubosc_prostokata)

label1 = tk.Label(root, text="X:", font=("Arial", 12))
label1.place(x=30, y=20)
label2=tk.Label(root, text="Y:", font=("Arial", 12))
label2.place(x=200, y=20)
label3=tk.Label(root, text="Zmień kolor:", font=("Arial", 12))
label3.place(x=550, y=800)
root.mainloop()
