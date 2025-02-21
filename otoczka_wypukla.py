import tkinter as tk
from tkinter import filedialog
import re
import numpy as np
from tkinter import messagebox
from tkinter import ttk
from tkinter.colorchooser import askcolor

aktualny_kolor_punktow = 'blue'
aktualny_kolor_prostokata = 'red'
aktualny_kolor_otoczki = 'green'
kolor_punktow = []
kolor_prostokata = []
kolor_otoczki = []
rozmiary_punktow = []
aktualny_rozmiar_punktow = 3
grubosc_prostokata = []
aktualna_grubosc_prostokata = 1
grubosc_otoczki = []
aktualna_grubosc_otoczki = 1
aktualny_styl_prostokata = ""
styl_prostokata = []
aktualny_styl_otoczki = ""
styl_otoczki = []
aktualny_styl_punktu = "Okrąg"
styl_punktu = []

def wczytaj():
    global punkty, rozmiary_punktow, aktualny_styl_punktu
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
                    rozmiary_punktow.append(aktualny_rozmiar_punktow) 
                    kolor_punktow.append(aktualny_kolor_punktow)  
        canvas.delete("all")
        dostosuj_widzenie()
        pasek_polecen.insert(tk.END, "Punkty wczytane z pliku: " + file_path + "\n")
        rysuj_punkty()

def dostosuj_widzenie():
    min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')  
    for i, (point, rozmiar, kolor) in enumerate(zip(punkty, rozmiary_punktow, kolor_punktow), start=1):
        min_x = min(min_x, point[0] - rozmiar)
        max_x = max(max_x, point[0] + rozmiar)
        min_y = min(min_y, point[1] - rozmiar)
        max_y = max(max_y, point[1] + rozmiar)
    canvas_x_range = max_x - min_x
    canvas_y_range = max_y - min_y
    padding = 20  
    if canvas_x_range > 0 and canvas_y_range > 0:
        canvas_ratio = canvas_x_range / canvas_y_range
        window_ratio = canvas.winfo_width() / canvas.winfo_height()
        if canvas_ratio > window_ratio:
            canvas_scale_factor = canvas.winfo_width() / (canvas_x_range + padding)
        else:
            canvas_scale_factor = canvas.winfo_height() / (canvas_y_range + padding)
        for i in range(len(punkty)):
            punkty[i] = (
                (punkty[i][0] - min_x) * canvas_scale_factor + padding / 2,
                (punkty[i][1] - min_y) * canvas_scale_factor + padding / 2
            )
        canvas.delete("all")
        rysuj_punkty()
        rysuj_otoczke()
        rysuj_prostokat_ograniczajacy()

def rysuj_punkty():
    canvas.delete("punkty")
    for i, (point, rozmiar, kolor) in enumerate(zip(punkty, rozmiary_punktow, kolor_punktow), start=1):
        if aktualny_styl_punktu == "Okrąg":
            rysuj_kolo(point, rozmiar, kolor)
        elif aktualny_styl_punktu == "Kwadrat":
            rysuj_kwadrat(point, rozmiar, kolor)
        elif aktualny_styl_punktu == "Trójkąt":
            rysuj_trojkat(point, rozmiar, kolor)
        if var_numeracja.get():
            canvas.create_text(point[0], point[1] - 10, text=str(i), fill='black', tags="numeracja")

def rysuj_kolo(point, rozmiar, kolor):
    canvas.create_oval(point[0] - rozmiar, point[1] - rozmiar, point[0] + rozmiar, point[1] + rozmiar, fill=kolor, tags="punkty")

def rysuj_kwadrat(point, rozmiar, kolor):
    canvas.create_rectangle(point[0] - rozmiar, point[1] - rozmiar, point[0] + rozmiar, point[1] + rozmiar, fill=kolor, tags="punkty")

def rysuj_trojkat(point, rozmiar, kolor):
    canvas.create_polygon(point[0], point[1] - rozmiar, point[0] - rozmiar, point[1] + rozmiar, point[0] + rozmiar, point[1] + rozmiar, fill=kolor, outline='', tags="punkty")

def dodaj_punkt():
    global rozmiary_punktow
    try:
        x = float(input_field1.get())
        y = float(input_field2.get())
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadzono nieprawidłowe dane. Podaj liczby.")
        return
    punkty.append((x, y))
    rozmiary_punktow.append(aktualny_rozmiar_punktow)
    kolor_punktow.append(aktualny_kolor_punktow)
    styl_punktu.append(aktualny_styl_punktu)
    dostosuj_widzenie()
    rysuj_punkty()
    toggle_numeracja()
    toggle_otoczka()
    input_field1.delete(0, tk.END)
    input_field2.delete(0, tk.END)
    zbuduj_otoczke()
    rysuj_prostokat_ograniczajacy()
    pasek_polecen.insert(tk.END, "Punkt dodany: (" + str(x) + ", " + str(y) + ")" + "\n")

def zbuduj_otoczke():
    global punkty, otoczka
    otoczka = graham_scan(punkty)
    rysuj_otoczke()

def zapisz_otoczke():
    global otoczka
    if not otoczka:
        messagebox.showwarning("Brak otoczki", "Nie zbudowano otoczki.")
        return
    if otoczka:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        pasek_polecen.insert(tk.END, "Otoczka zapisana do pliku: " + file_path  + "\n")
        if file_path:
            with open(file_path, 'w') as file:
                for point in otoczka:
                    file.write(f"{point[0]}, {point[1]}\n")
                    
def toggle_numeracja():
    if not punkty:
        messagebox.showwarning("Brak punktów", "Nie wprowadzono żadnych punktów.")
        return
    if var_numeracja.get():
        for i, point in enumerate(punkty, start=1):
            canvas.create_text(point[0], point[1] - 10, text=str(i), fill='black', tags="numeracja")
    else:
        canvas.delete("numeracja")

def rysuj_otoczke():
    canvas.delete("otoczka")

    style_mapping = {
        "Ciągła": "",       
        "Przerywana": (4, 4),     
        "Kreskowana": (8, 4),     
        "Kreskowo-kropkowa": (4, 4, 2, 4), 
        "Kropkowana": (2, 2),    
    }
    aktualny_styl_numeryczny = style_mapping.get(aktualny_styl_otoczki, "")
    if var_otoczka.get() and otoczka:
        for i in range(len(otoczka) - 1):
            canvas.create_line(
                otoczka[i][0], otoczka[i][1], otoczka[i + 1][0], otoczka[i + 1][1], fill=aktualny_kolor_otoczki, width=aktualna_grubosc_otoczki, dash = aktualny_styl_numeryczny,
                tags="otoczka"
            )
        canvas.create_line(
            otoczka[-1][0], otoczka[-1][1], otoczka[0][0], otoczka[0][1], fill=aktualny_kolor_otoczki, width=aktualna_grubosc_otoczki, dash = aktualny_styl_numeryczny, tags="otoczka"
        )

def rysuj_prostokat_ograniczajacy():
    canvas.delete("prostokat")
    if not punkty:
        messagebox.showwarning("Brak punktów", "Nie wprowadzono żadnych punktów.")
        return    
    style_mapping = {
        "Ciągła": "",       
        "Przerywana": (4, 4),     
        "Kreskowana": (8, 4),     
        "Kreskowo-kropkowa": (4, 4, 2, 4), 
        "Kropkowana": (2, 2),     
    }
    aktualny_styl_numeryczny = style_mapping.get(aktualny_styl_prostokata, "")
    if var_prostokat.get() and punkty:
        x_min = min(point[0] for point in punkty)
        x_max = max(point[0] for point in punkty)
        y_min = min(point[1] for point in punkty)
        y_max = max(point[1] for point in punkty)
        canvas.create_rectangle(
            x_min, y_min, x_max, y_max, outline=aktualny_kolor_prostokata, width=aktualna_grubosc_prostokata, dash=aktualny_styl_numeryczny, tags="prostokat"
        )

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else -1

def graham_scan(points):
    n = len(points)
    if n < 3:
        messagebox.showinfo("Błąd", "Potrzebujemy co najmniej 3 punktów do utworzenia otoczki wypukłej")
        return []
    pivot = min(points, key=lambda point: (point[1], point[0]))
    sorted_points = sorted(points, key=lambda point: np.arctan2(point[1] - pivot[1], point[0] - pivot[0]))
    stack = [pivot, sorted_points[0], sorted_points[1]]
    for i in range(2, n):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], sorted_points[i]) != -1:
            stack.pop()
        stack.append(sorted_points[i])
    return stack

def toggle_prostokat():
    rysuj_prostokat_ograniczajacy()

def toggle_otoczka():
    rysuj_otoczke()

def zmien_kolor_punktow():
    global aktualny_kolor_punktow
    nowy_kolor = askcolor(title="Wybierz kolor punktów")[1]
    if nowy_kolor:
        aktualny_kolor_punktow = nowy_kolor
        for i in range(len(punkty)):
            kolor_punktow[i] = aktualny_kolor_punktow
        rysuj_punkty()
        pasek_polecen.insert(tk.END, "Kolor punktów zmieniony na: " + nowy_kolor + "\n")
            
def zmien_kolor_otoczki():
    global aktualny_kolor_otoczki
    nowy_kolor = askcolor(title="Wybierz kolor otoczki")[1]
    if nowy_kolor:
        aktualny_kolor_otoczki = nowy_kolor
        zmien_kolor_elementow("otoczka", nowy_kolor)
        pasek_polecen.insert(tk.END, "Kolor otoczki zmieniony na: " + nowy_kolor +  "\n")

def zmien_kolor_prostokata():
    global aktualny_kolor_prostokata
    nowy_kolor = askcolor(title="Wybierz kolor prostokąta")[1]
    if nowy_kolor:
        aktualny_kolor_prostokata = nowy_kolor
        zmien_kolor_elementow("prostokat", nowy_kolor)
        pasek_polecen.insert(tk.END, "Kolor prostokąta zmieniony na: " + nowy_kolor + "\n")

def zmien_kolor_elementow(tag, nowy_kolor):
    global aktualny_kolor_otoczki, aktualny_kolor_punktow, aktualny_kolor_prostokata
    if tag == "punkt":
        aktualny_kolor_punktow = nowy_kolor
        for item in canvas.find_withtag("punkt"):
            canvas.itemconfig(item, fill=nowy_kolor)
    elif tag == "otoczka":
        aktualny_kolor_otoczki = nowy_kolor
        for item in canvas.find_withtag("otoczka"):
            canvas.itemconfig(item, fill=nowy_kolor)
    elif tag == "prostokat":
        aktualny_kolor_prostokata = nowy_kolor
        for item in canvas.find_withtag("prostokat"):
            canvas.itemconfig(item, outline=nowy_kolor)

def zmien_rozmiar_punktow(rozmiar):
    global aktualny_rozmiar_punktow
    aktualny_rozmiar_punktow = rozmiar
    for i in range(len(punkty)):
        rozmiary_punktow[i] = aktualny_rozmiar_punktow
    rysuj_punkty()
    label2.config(text=str(aktualny_rozmiar_punktow))
    value2.set(aktualny_rozmiar_punktow)
    pasek_polecen.insert(tk.END, "Rozmiar punktów zmieniony na: " + str(rozmiar) + "\n")

def zmien_grubosc_prostokata(grubosc):
    global aktualna_grubosc_prostokata
    aktualna_grubosc_prostokata = grubosc
    rysuj_prostokat_ograniczajacy()
    label1.config(text=str(aktualna_grubosc_prostokata))
    value1.set(aktualna_grubosc_prostokata)
    pasek_polecen.insert(tk.END, "Grubosæ prostokąta zmieniona na: " + str(grubosc) + "\n")

def zmien_grubosc_otoczki(grubosc):
    global aktualna_grubosc_otoczki
    aktualna_grubosc_otoczki = grubosc
    rysuj_otoczke()
    label3.config(text=str(aktualna_grubosc_otoczki))
    value3.set(aktualna_grubosc_otoczki)
    pasek_polecen.insert(tk.END, "Grubosæ otoczki zmieniona na: " + str(grubosc) + "\n")

def zmien_styl_prostokata(*args):
    global aktualny_styl_prostokata
    aktualny_styl_prostokata = selected_value_prostokat.get()
    rysuj_prostokat_ograniczajacy()
    pasek_polecen.insert(tk.END, "Styl prostokąta zmieniony na: " + aktualny_styl_prostokata + "\n")

def zmien_styl_otoczki(*args):
    global aktualny_styl_otoczki
    aktualny_styl_otoczki = selected_value_otoczka.get()
    rysuj_otoczke()
    pasek_polecen.insert(tk.END, "Styl otoczki zmieniony na: " + aktualny_styl_otoczki + "\n")

def zmien_ksztalt_punktow(styl):
    global aktualny_styl_punktu
    aktualny_styl_punktu = styl
    rysuj_punkty()
    pasek_polecen.insert(tk.END, "Styl punktów zmieniony na: " + styl + "\n")

punkty = []
otoczka = []

root = tk.Tk()
root.title("Python GUI Example")
root.geometry('1500x1000')

canvas_frame = tk.Frame(root, width=1350, height=925, bg="white")
canvas_frame.place(x=550, y=25)
canvas = tk.Canvas(canvas_frame, width=1350, height=925, bg="white")
canvas.pack()

pasek_polecen = tk.Text(root, width=55, height=33)
pasek_polecen.place(x=35, y=70)
scrollbar = tk.Scrollbar(root)
scrollbar.place(x=465, y=70, height=530)
scrollbar.config(command=pasek_polecen.yview)

ramka = tk.Frame(root, width=425, height=55, highlightbackground="black", highlightthickness=1)
ramka.place(x=33, y=636)
ramka2 = tk.Frame(root, width=425, height=55, highlightbackground="black", highlightthickness=1)
ramka2.place(x=33, y=707)
ramka3 = tk.Frame(root, width=425, height=200, highlightbackground="black", highlightthickness=1)
ramka3.place(x=33, y=778)

button1 = tk.Button(root, text="Wczytaj wykaz punktów", width=20, command=wczytaj)
button1.place(x=60, y=20)
button2 = tk.Button(root, text="Dodaj punkt", width=20, command=dodaj_punkt)
button2.place(x=300, y=650)
button3 = tk.Button(root, text="Zbuduj otoczkę", width=20, command=zbuduj_otoczke)
button3.place(x=40, y=725)
button4 = tk.Button(root, text="Zapisz otoczkę", width=20, command=zapisz_otoczke)
button4.place(x=250, y=725)
button5 = tk.Button(root, text="Zamknij program", width=20, command=root.destroy)
button5.place(x=230, y=20)
button6 = tk.Button(root, text="Prostokąt", width=18, command=zmien_kolor_prostokata)
button6.place(x=35, y=840)
button7 = tk.Button(root, text="Punkty", width=18, command=zmien_kolor_punktow)
button7.place(x=180, y=840)
button8 = tk.Button(root, text="Otoczka", width=18, command=zmien_kolor_otoczki)
button8.place(x=320, y=840)

label1 = tk.Label(root, text="Sprawdzenie pojedynczego punktu:")
label1.place(x=35, y=625)
label2 = tk.Label(root, text="X:")
label2.place(x=35, y=650)
label3 = tk.Label(root, text="Y:")
label3.place(x=190, y=650)
label4 = tk.Label(root, text="Budowanie otoczki wypukłej")
label4.place(x=35, y=700)
label5 = tk.Label(root, text="Parametry rysunku")
label5.place(x=35, y=767)
label6 = tk.Label(root, text="Rozmiar")
label6.place(x=35, y=920)
label7 = tk.Label(root, text="Styl")
label7.place(x=35, y=870)
label8 = tk.Label(root, text="Zmień kolor")
label8.place(x=35, y=820)

input_field1 = tk.Entry(root, width=10)
input_field1.place(x=55, y=650)
input_field2 = tk.Entry(root, width=10)
input_field2.place(x=210, y=650)

var_prostokat = tk.BooleanVar()
checkbox_prostokat = tk.Checkbutton(root, text="Prostokąt ograniczający", variable=var_prostokat, command=toggle_prostokat)
checkbox_prostokat.place(x=40, y=785)

var_numeracja = tk.BooleanVar()
checkbox_numeracja = tk.Checkbutton(root, text="Numeracja punktów", variable=var_numeracja, command=toggle_numeracja)
checkbox_numeracja.place(x=200, y=785)

var_otoczka = tk.BooleanVar(value=True)
checkbox_otoczka = tk.Checkbutton(root, text="Otoczka wypukła", variable=var_otoczka, command=toggle_otoczka)
checkbox_otoczka.place(x=335, y=785)

values_prostokat = ["Ciągła", "Przerywana", "Kreskowana", "Kreskowo-kropkowa", "Kropkowana"]
selected_value_prostokat = tk.StringVar()
selected_value_prostokat.set(values_prostokat[0])
combobox1 = ttk.Combobox(root, values=values_prostokat, textvariable=selected_value_prostokat, width=10)
combobox1.place(x=35, y=890)
selected_value_prostokat.trace_add('write', zmien_styl_prostokata)

values_ksztalty_punktow = ["Okrąg", "Kwadrat", "Trójkąt"]
selected_value_ksztalt_punktow = tk.StringVar()
selected_value_ksztalt_punktow.set(values_ksztalty_punktow[0])
combobox_ksztalt_punktow = ttk.Combobox(root, values=values_ksztalty_punktow, textvariable=selected_value_ksztalt_punktow, width=10)
combobox_ksztalt_punktow.place(x=200, y=890)
selected_value_ksztalt_punktow.trace_add('write', lambda *args: zmien_ksztalt_punktow(selected_value_ksztalt_punktow.get()))

values_otoczka = ["Ciągła", "Przerywana", "Kreskowana", "Kreskowo-kropkowa", "Kropkowana"]
selected_value_otoczka = tk.StringVar()
selected_value_otoczka.set(values_otoczka[0])
combobox3 = ttk.Combobox(root, values=values_otoczka, textvariable=selected_value_otoczka, width=10)
combobox3.place(x=350, y=890)
selected_value_otoczka.trace_add('write', zmien_styl_otoczki)

canvas.bind("<Up>", zmien_rozmiar_punktow)
canvas.bind("<Down>", zmien_rozmiar_punktow)

value1 = tk.IntVar()
value1.set(1)
label1 = tk.Label(root, textvariable=value1, font=("Arial", 12))
label1.place(x=60, y=950)
button_increase1 = tk.Button(root, text="↑", command=lambda: zmien_grubosc_prostokata(min(value1.get() + 1, 10)))
button_increase1.place(x=35, y=950)
button_decrease1 = tk.Button(root, text="↓", command=lambda: zmien_grubosc_prostokata(max(value1.get() - 1, 1)))
button_decrease1.place(x=85, y=950)

value2 = tk.IntVar()
value2.set(3)
label2 = tk.Label(root, textvariable=value2, font=("Arial", 12))
label2.place(x=240, y=950)
button_increase2 = tk.Button(root, text="↑", command=lambda: zmien_rozmiar_punktow(min(value2.get() + 1, 10)))
button_increase2.place(x=215, y=950)
button_decrease2 = tk.Button(root, text="↓", command=lambda: zmien_rozmiar_punktow(max(value2.get() - 1, 1)))
button_decrease2.place(x=265, y=950)

value3 = tk.IntVar()
value3.set(1)
label3 = tk.Label(root, textvariable=value3, font=("Arial", 12))
label3.place(x=370, y=950)
button_increase3 = tk.Button(root, text="↑", command=lambda: zmien_grubosc_otoczki(min(value3.get() + 1, 10)))
button_increase3.place(x=345, y=950)
button_decrease3 = tk.Button(root, text="↓", command=lambda: zmien_grubosc_otoczki(max(value3.get() - 1, 1)))
button_decrease3.place(x=395, y=950)

root.mainloop()
