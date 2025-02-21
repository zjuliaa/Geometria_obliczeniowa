import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random


etykiety_widoczne = True
aktualny_wyglad_punktu = {"fill": "blue", "radius": 3}


def oblicz():
    xa = float(input_field1.get())
    xb = float(input_field2.get())
    xc = float(input_field3.get())
    xd = float(input_field4.get())
    ya = float(input_field5.get())
    yb = float(input_field6.get())
    yc = float(input_field7.get())
    yd = float(input_field8.get())
    det = (xb - xa) * (yd - yc) - (yb - ya) * (xd - xc)
    t1 = ((xc - xa) * (yd - yc) - (yc - ya) * (xd - xc)) / det
    t2 = ((xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)) / det

    if t1 < 0 or t1 > 1 or t2 < 0 or t2 > 1:
        dodaj_do_paska_polecen("Odcinki się nie przecinają")
    else:
        dodaj_do_paska_polecen("Odcinki się przecinają")

    xp = xa + t1 * (xb - xa)
    yp = ya + t1 * (yb - ya)

    xp = "{:.3f}".format(xp)
    yp = "{:.3f}".format(yp)

    output_field1.delete(0, tk.END)
    output_field1.insert(0, str(xp))
    output_field2.delete(0, tk.END)
    output_field2.insert(0, str(yp))
    file_path = r"C:\Sem3\GO\zad2" #zrobic tak zeby wywolanie oblicz nie wywolalo zapisu, moze chodzi o przekazanie danych???
    zapisz(xp, yp, file_path)
    rysuj()
    dodaj_do_paska_polecen("Obliczono xp i xy.")
    
def zapisz(xp, yp, file_path):
    try:
        file_path = os.path.join(file_path, "wyniki.txt")
        with open(file_path, "w") as file:
            file.write("Wyniki:\n")
            file.write(f"xp: {xp}\n")
            file.write(f"yp: {yp}\n")
        print("Wyniki zapisane do pliku 'wyniki.txt'")
    except Exception as e:
        print("Błąd podczas zapisywania wyników:", str(e))
 


aktualny_kolor_linii1 = "blue"
aktualny_kolor_linii2 = "red"
aktualna_grubosc_linii1 = 1
aktualna_linia1 = None
aktualna_grubosc_linii2= 1
aktualna_linia2 = None


def rysuj(kolor = "blue"):
    global aktualna_linia1, aktualna_linia2

    xa_str = input_field1.get()
    xb_str = input_field2.get()
    xc_str = input_field3.get()
    xd_str = input_field4.get()
    xp_str = output_field1.get()
    ya_str = input_field5.get()
    yb_str = input_field6.get()
    yc_str = input_field7.get()
    yd_str = input_field8.get()
    yp_str= output_field2.get()


    if not xa_str or not xb_str or not xc_str or not xd_str or not ya_str or not yb_str or not yc_str or not yd_str:
        print("Wprowadź wszystkie dane przed rysowaniem.")
        return

    xa = float(xa_str)
    xb = float(xb_str)
    xc = float(xc_str)
    xd = float(xd_str)
    ya = float(ya_str)
    yb = float(yb_str)
    yc = float(yc_str)
    yd = float(yd_str)
    xp = float(xp_str)
    yp = float(yp_str)

    canvas_margin = 50  
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    canvas_width_with_margin = canvas_width - 2 * canvas_margin
    canvas_height_with_margin = canvas_height - 2 * canvas_margin

    min_x = min(xa, xb, xc, xd)
    max_x = max(xa, xb, xc, xd)
    min_y = min(ya, yb, yc, yd)
    max_y = max(ya, yb, yc, yd)

    x_range = max_x - min_x
    y_range = max_y - min_y

    x_scale = canvas_width_with_margin / x_range
    y_scale = canvas_height_with_margin / y_range

    xa_scaled = (xa - min_x) * x_scale + canvas_margin
    xb_scaled = (xb - min_x) * x_scale + canvas_margin
    xc_scaled = (xc - min_x) * x_scale + canvas_margin
    xd_scaled = (xd - min_x) * x_scale + canvas_margin
    ya_scaled = (ya - min_y) * y_scale + canvas_margin
    yb_scaled = (yb - min_y) * y_scale + canvas_margin
    yc_scaled = (yc - min_y) * y_scale + canvas_margin
    yd_scaled = (yd - min_y) * y_scale + canvas_margin
    xp_scaled = (xp - min_x) * x_scale + canvas_margin
    yp_scaled = (yp - min_y) * y_scale + canvas_margin

    canvas.delete("all")  
    canvas.create_oval(xa_scaled - 3, ya_scaled - 3, xa_scaled + 3, ya_scaled + 3, fill="red", tags="punkt")  # punkt A
    canvas.create_oval(xb_scaled - 3, yb_scaled - 3, xb_scaled + 3, yb_scaled + 3, fill="red", tags="punkt")  # punkt B
    canvas.create_oval(xc_scaled - 3, yc_scaled - 3, xc_scaled + 3, yc_scaled + 3, fill="red", tags="punkt")  # punkt C
    canvas.create_oval(xd_scaled - 3, yd_scaled - 3, xd_scaled + 3, yd_scaled + 3, fill="red", tags="punkt")  # punkt D
    canvas.create_oval(xp_scaled - 3, yp_scaled - 3, xp_scaled + 3, yp_scaled + 3, fill="blue", tags="punkt")  # punkt P

    linia1 = canvas.create_line(xa_scaled, ya_scaled, xb_scaled, yb_scaled, fill=aktualny_kolor_linii1, width=aktualna_grubosc_linii1)
    linia2 = canvas.create_line(xc_scaled, yc_scaled, xd_scaled, yd_scaled, fill=aktualny_kolor_linii2, width=aktualna_grubosc_linii2)

    aktualna_linia1 = linia1
    aktualna_linia2 = linia2

    canvas.create_text(xa_scaled + 10, ya_scaled - 10, text="A", tags="etykieta")
    canvas.create_text(xb_scaled + 10, yb_scaled - 10, text="B", tags="etykieta")
    canvas.create_text(xc_scaled + 10, yc_scaled - 10, text="C", tags="etykieta")
    canvas.create_text(xd_scaled + 10, yd_scaled - 10, text="D", tags="etykieta")
    canvas.create_text(xp_scaled + 10, yp_scaled - 10, text="P", tags="etykieta")

    dodaj_do_paska_polecen("Narysowano linię o grubości {}.".format(aktualna_grubosc_linii1))


def zmien_kolor_losowy1():
    global aktualny_kolor_linii1
    losowy_kolor = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    aktualny_kolor_linii1 = losowy_kolor
    rysuj(losowy_kolor)
    dodaj_do_paska_polecen("Zmieniono kolor linii 1.")


def zmien_kolor_losowy2():
    global aktualny_kolor_linii2
    losowy_kolor = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    aktualny_kolor_linii2 = losowy_kolor
    rysuj(losowy_kolor)
    dodaj_do_paska_polecen("Zmieniono kolor linii 2.")


def zmien_grubosc1():
    global aktualna_grubosc_linii1
    aktualna_grubosc_linii1 = random.randint(1, 5)
    rysuj()

def zmien_grubosc2():
    global aktualna_grubosc_linii2
    aktualna_grubosc_linii2 = random.randint(1, 5)
    rysuj()

def wczytaj():
    file_path = "C:\Sem3\GO\zad2\dane2.txt"
    if file_path:
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                if len(lines) >= 8:
                    input_field1.delete(0, tk.END)
                    input_field1.insert(0, lines[0].strip())
                    input_field2.delete(0, tk.END)
                    input_field2.insert(0, lines[1].strip())
                    input_field3.delete(0, tk.END)
                    input_field3.insert(0, lines[2].strip())
                    input_field4.delete(0, tk.END)
                    input_field4.insert(0, lines[3].strip())
                    input_field5.delete(0, tk.END)
                    input_field5.insert(0, lines[4].strip())
                    input_field6.delete(0, tk.END)
                    input_field6.insert(0, lines[5].strip())
                    input_field7.delete(0, tk.END)
                    input_field7.insert(0, lines[6].strip())
                    input_field8.delete(0, tk.END)
                    input_field8.insert(0, lines[7].strip())

                    xa = float(lines[0].strip())
                    xb = float(lines[1].strip())
                    xc = float(lines[2].strip())
                    xd = float(lines[3].strip())
                    ya = float(lines[4].strip())
                    yb = float(lines[5].strip())
                    yc = float(lines[6].strip())
                    yd = float(lines[7].strip())

        except Exception as e:
            print("Error while loading file:", str(e))
        dodaj_do_paska_polecen("Wczytano dane.")


def dodaj_do_paska_polecen(tekst):
    pasek_polecen.insert(tk.END, tekst + "\n")

def wyczysc_pasek_polecen():
    pasek_polecen.delete(1.0, tk.END)

def ukryj():
    global etykiety_widoczne
    etykiety_widoczne = not etykiety_widoczne  # Odwróć stan etykiet (ukryj, jeśli widoczne, lub pokaż, jeśli ukryte)
    
    if etykiety_widoczne:
        # Pętla w celu odnalezienia i ukrycia etykiet
        for etykieta_id in canvas.find_withtag("etykieta"):
            canvas.itemconfigure(etykieta_id, state="normal")
        
        # Pętla w celu odnalezienia i ukrycia punktów
        for punkt_id in canvas.find_withtag("punkt"):
            canvas.itemconfigure(punkt_id, state="normal")
    else:
        # Pętla w celu odnalezienia i ukrycia etykiet
        for etykieta_id in canvas.find_withtag("etykieta"):
            canvas.itemconfigure(etykieta_id, state="hidden")
        
        # Pętla w celu odnalezienia i ukrycia punktów
        for punkt_id in canvas.find_withtag("punkt"):
            canvas.itemconfigure(punkt_id, state="hidden")


def zmien():
    aktualny_rozmiar_punktu = 1
    global aktualny_wyglad_punktu
    nowy_wyglad_punktu = {"fill": random_color(), "radius": aktualny_rozmiar_punktu}

    aktualny_wyglad_punktu = nowy_wyglad_punktu

    for punkt_id in canvas.find_withtag("punkt"):
        aktualny_radius = aktualny_rozmiar_punktu
        if aktualny_radius > 3:
            aktualny_radius = 3

        canvas.itemconfig(punkt_id, fill=nowy_wyglad_punktu["fill"])
        x0, y0, x1, y1 = canvas.coords(punkt_id)
        canvas.coords(punkt_id, x0 - aktualny_radius, y0 - aktualny_radius,
                       x1 + aktualny_radius, y1 + aktualny_radius)
    
def random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

root = tk.Tk()
root.title("Python GUI Example")
root.geometry('3000x3000')

canvas_frame = tk.Frame(root, width=1350, height=750, bg="white")
canvas_frame.place(x=550, y=25)
canvas = tk.Canvas(canvas_frame, width=1350, height=750, bg="white")
canvas.pack()
pasek_polecen = tk.Text(root, width=55, height=33)
pasek_polecen.place(x=35, y=400)

label1 = tk.Label(root, text="Xa:", font=("Arial", 12))
label1.place(x=10, y=20)
label2 = tk.Label(root, text="Xb:", font=("Arial", 12))
label2.place(x=10, y=50)
label3 = tk.Label(root, text="Xc:", font=("Arial", 12))
label3.place(x=10, y=80)
label4 = tk.Label(root, text="Xd:", font=("Arial", 12))
label4.place(x=10, y=110)
label5 = tk.Label(root, text="Ya:", font=("Arial", 12))
label5.place(x=270, y=20)
label6 = tk.Label(root, text="Yb:", font=("Arial", 12))
label6.place(x=270, y=50)
label6 = tk.Label(root, text="Yc:", font=("Arial", 12))
label6.place(x=270, y=80)
label6 = tk.Label(root, text="Yd:", font=("Arial", 12))
label6.place(x=270, y=110)
label6 = tk.Label(root, text="Xp:", font=("Arial", 12))
label6.place(x=10, y=200)
label6 = tk.Label(root, text="Yp:", font=("Arial", 12))
label6.place(x=270, y=200)
label7 = tk.Label(root, text="Pasek poleceń:", font=("Arial", 12))
label7.place(x=10, y=370)

button1 = tk.Button(root, text="Oblicz", width=30, command=oblicz)
button1.place(x=150, y=150)
button2 = tk.Button(root, text="Wczytaj dane z pliku", width=30, command=wczytaj)
button2.place(x=150, y=250)
button3 = tk.Button(root, text="Zapisz raport do pliku tekstowego", width=30, command=zapisz)
button3.place(x=150, y=300)
button4 = tk.Button(root, text="Odśwież", width=20, command=rysuj)
button4.place(x=1400, y=800)
button5 = tk.Button(root, text="Zmień kolor lini 1", width=20, command=zmien_kolor_losowy1)
button5.place(x=900, y=800)
button6 = tk.Button(root, text="Zmień kolor lini 2", width=20, command=zmien_kolor_losowy2)
button6.place(x=900, y=830)
button6 = tk.Button(root, text="Zmień grubość lini 1", width=20, command=zmien_grubosc1)
button6.place(x=1100, y=800)
button6 = tk.Button(root, text="Zmień grubość lini 2", width=20, command=zmien_grubosc2)
button6.place(x=1100, y=830)
button7 = tk.Button(root, text="Zamknij program", width=20, command=root.destroy)
button7.place(x=1700, y=800)
button8 = tk.Button(root, text="Wyczyść pasek poleceń", width=20, command=wyczysc_pasek_polecen)
button8.place(x=35, y=950)
button9 = tk.Button(root, text="Ukryj etykietę punktu", width=20, command=ukryj)
button9.place(x=700, y=800)
button10 = tk.Button(root, text="Zmień wyglad punktu", width=20, command=zmien)
button10.place(x=700, y=830)

input_field1 = tk.Entry(root, width=30)
input_field1.place(x=40, y=20)
input_field2 = tk.Entry(root, width=30)
input_field2.place(x=40, y=50)
input_field3 = tk.Entry(root, width=30)
input_field3.place(x=40, y=80)
input_field4 = tk.Entry(root, width=30)
input_field4.place(x=40, y=110)
input_field5 = tk.Entry(root, width=30)
input_field5.place(x=300, y=20)
input_field6 = tk.Entry(root, width=30)
input_field6.place(x=300, y=50)
input_field7 = tk.Entry(root, width=30)
input_field7.place(x=300, y=80)
input_field8 = tk.Entry(root, width=30)
input_field8.place(x=300, y=110)

output_field1 = tk.Entry(root, width=30)
output_field1.place(x=35, y=200)
output_field2 = tk.Entry(root, width=30)
output_field2.place(x=300, y=200)

root.mainloop()
