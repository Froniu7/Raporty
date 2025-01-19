import datetime, openpyxl
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import ttk
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl, os, shutil, pygame



muzyka_co_godzina = True
rozmiar_fonta = 20
Dane_z_dnia = ["" for i in range(12)]
widok_podstawowy = False
columnspan_scrolledtext = 3
wiersz = 0
aktualny_wiersz_tabeli = ".!frame3"
ostatni_wiersz_tabeli = ".!frame3"
aktulany_widok_przyciski = ""
xz = 1
pob_zaw_kolumny_exel = ["" for i in range(12)]  # pobierz zawartosc kolumny z pliku exel



def okno():
    root = tk.Tk()

    root.geometry('1100x630') # szerokosc xwysokosc
    root.title('Send informations to Rafal')
    root.option_add('*tearOff', False) # odpowiada za design rozwijanego menu
    menubar = Menu(root)
    root.config(menu = menubar)
    plik = Menu(menubar)
    edytuj = Menu(menubar)
    widok = Menu(menubar)
    pomoc = Menu(menubar)

    menubar.add_cascade(menu=plik, label="Plik")
    menubar.add_cascade(menu=edytuj, label="Edytuj")
    menubar.add_cascade(menu=widok, label="Widok")
    menubar.add_cascade(menu=pomoc, label="Pomoc")

    #---funkcjonalnosc dla menu/Plik

    plik.add_command(label='Zapis do pliku exel', command= zapisDoExel())
    plik.add_command(label='Wyslij email z plikiem exel', command=wyslijPlikExel())
    plik.add_separator()
    plik.add_command(label='Ustawienia', command= oknoUstawienia())

    # ---funkcjonalnosc dla menu/Edytuj
    edytuj.add_command(label='Ustaw przyciski tekstowe', command=lambda: print('Ustaw przyciski tekstowe'))

    # ---funkcjonalnosc dla menu/Widok
    edytuj.add_command(label='Tabela rozszerzona', command=lambda: print('Tabela rozszerzona'))

    return root

    #---instrukcja odpowiedzialan za wyswietlanie daty

def dataPobrana(root):
    data = tk.Label(root, bg='#2b2b2b', fg='white', font=('Verdana', 12), width=16)
    data.grid(row=0, column=0, columnspan=2, sticky="W")
    aktualizujDate(root, data)

    return data

def aktualizujDate(root, data):
    #global CZAS
    #CZAS += 1
    data_wyswietlana = str(datetime.datetime.now())
    data['text'] = "data : " + data_wyswietlana[0:10]
    root.after(100, aktualizujDate, root, data)

def zegarPobrany(root): # ---instrukcja odpowiedzialna za wyswietlanie czasu
    czas = tk.Label(root, bg='#2b2b2b', fg='white', font=('Verdana', 12), width=16)
    czas.grid(row=1, column=0, columnspan=2, sticky="W")
    aktualizujCzas(root, czas)

    return czas

def aktualizujCzas(root, czas):
    global muzyka_co_godzina
    czas_wyswietlana = str(datetime.datetime.now())
    czas['text'] = "czas :  " + czas_wyswietlana[10:19] + "  "
    root.after(100, aktualizujCzas, root, czas)
    if czas_wyswietlana[11:19] == czas_wyswietlana[11:13] + ":00:00" and muzyka_co_godzina==True:
        lista = open("pliki/dzwieki/DzwiekiLista.txt", 'r')
        lista_dzwieki_tablica = ["" for i in range(12)]
        for i in range(12):
            lista_dzwieki_tablica[i] = lista.readline()
            lista_dzwieki_tablica[i] = lista_dzwieki_tablica[i].rstrip("\n")
        lista.close()
        print("nr_dla_elementu_tablicy")
        print("play sound")
        pygame.mixer.music.load(f"pliki/dzwieki/{lista_dzwieki_tablica[int(czas_wyswietlana[11:13])-7]}")
        pygame.mixer.music.play()
        muzyka_co_godzina = False
    if int(czas_wyswietlana[18:19]) % 2 == 0 and muzyka_co_godzina==False:
        print("tlo kolor czerwony")
        root['bg'] = ('red')
    if int(czas_wyswietlana[18:19]) % 2 != 0 and muzyka_co_godzina==False:
        print("tlo kolor szary : #f0f0f0")
        root['bg'] = ('#f0f0f0')

def boxListaUrzadzen(root):
    urzadzenie = StringVar()
    combobox = ttk.Combobox(root, textvariable=urzadzenie)
    combobox.grid(row=0, column=4, columnspan=2)

    lista = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
    x = 1
    licznik = 0
    while(x == 1): #----sprawdzamy ile urzadzen jest w pliku UrzadzeniaLista.txt
        licznik += 1
        urzadzenie_z_lista = lista.readline()
        urzadzenie_z_lista = urzadzenie_z_lista.rstrip("\n")
        if urzadzenie_z_lista == "":
            x = 0
            print("wychodze z petli")
    print(f"wartosc licznika to {licznik - 1}")
    lista.close()
    lista = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
    lista_urzadzen_tablica = ["" for i in range(licznik - 1)]
    for i in range(licznik - 1):
        lista_urzadzen_tablica[i] = lista.readline()
        lista_urzadzen_tablica[i] = lista_urzadzen_tablica[i].rstrip("\n")
        print(lista_urzadzen_tablica[i])
    lista.close()
    combobox.config(values=(lista_urzadzen_tablica))

    return combobox

def tabela(root):
    global columnspan_scrolledtext
    tabela_z_godzinami_i_polami = [[tk.Label(root) for i in range(12)], [ScrolledText(root) for i in range(12)]]
    for i in range (12):
        tabela_z_godzinami_i_polami[0][i].config(text=str(6 + i)+":00 - "+str(7+i)+":00" , bg='#2b2b2b', fg='white', font=('Verdana', 12), width=16)
        tabela_z_godzinami_i_polami[1][i].config(width=40, height=4, bg='white', fg='black')
        if i>1 and i <10:
            tabela_z_godzinami_i_polami[0][i].grid(row=2 + i, column=0)
            tabela_z_godzinami_i_polami[1][i].grid(row=2 + i, column=1, columnspan=columnspan_scrolledtext)
    tabela_z_godzinami_i_polami[0][2]['bg']=('red')

    return tabela_z_godzinami_i_polami

def wstawaineZExelDoTabeli():
    global pob_zaw_kolumny_exel, aktualny_wiersz_tabeli, tabela_ramek
    for i in range(12):
        if pob_zaw_kolumny_exel[i] == None:
            print("brak tekstu do umieszczenia w wierszach programu")
        else:
            lines = pob_zaw_kolumny_exel[i].split('\n')
            print(lines)
            x = 0
            for j in lines:
                print(f"zawartosc pob_zaw_kolumny_exel[{i}] dla x :{x} to : {j}")
                tabela_ramek[1][i].insert(float(x) + 1.0, j + '\n')
                x += 1




def pobieranieZExel():
    global pob_zaw_kolumny_exel
    data_dla_exel = str(datetime.datetime.now())
    wb = openpyxl.load_workbook(f'raport{data_dla_exel[0:4]}.xlsx')
    aktualna_nazwa_arkusza = wb.sheetnames[0]
    sheet1 = wb[aktualna_nazwa_arkusza]
    print(f"zostal otwarty plik raport{data_dla_exel[0:4]}.xlsx")
    print("zostana pobrane dane z odpowiedniej kolumny")
    max_ilosc_kolumn = sheet1.max_column
    print(f"max_ilosc_kolumn to {max_ilosc_kolumn}")
    nr_kolumny = 0
    for i in range(max_ilosc_kolumn):
        if sheet1.cell(row=1, column=i + 1).value == data_dla_exel[0:10]:
            nr_kolumny = i + 1
            for k in range(12):
                pob_zaw_kolumny_exel[k] = sheet1.cell(row=k + 3, column=nr_kolumny).value
            print(f"pobrana zawartosc kolumny {data_dla_exel[0:10]} to {pob_zaw_kolumny_exel}")


def liczenieWierszy():
    global aktualny_wiersz_tabeli, tabela_ramek
    licznik_wiersze = 0
    # sprawdzamy jaki mamy aktualnie frame
    if aktualny_wiersz_tabeli == '.!frame':
        nr_wiersza_tabeli = 1
    else:
        if aktualny_wiersz_tabeli == "." or aktualny_wiersz_tabeli == ".!combobox":
            nr_wiersza_tabeli = 3
        else:
            nr_wiersza_tabeli = aktualny_wiersz_tabeli[7:9]
            print(f"mamy wartosc z !frame o nr : {nr_wiersza_tabeli}")
    for i in range(10):
        if tabela_ramek[1][int(nr_wiersza_tabeli)-1].get(f'{i+1}.0', f'{i+1}.end') == "":
            print("brak tekstu")
        else:
            licznik_wiersze += 1
    print(f"mamy wierszy {licznik_wiersze}")

    return licznik_wiersze

def funkcjaWpiszTekst(nr_przycisku):
    def f():
        global aktualny_wiersz_tabeli, tabela_ramek, aktulany_widok_przyciski, widok_podstawowy, tabela_ramek
        pygame.mixer.music.load("pliki/dzwieki/click.wav.")
        pygame.mixer.music.play()
        if aktualny_wiersz_tabeli == '.!frame' or aktualny_wiersz_tabeli == "." or aktualny_wiersz_tabeli == ".!combobox" :
            x = 1
        else:
            x = aktualny_wiersz_tabeli[7:9]
        print(f"wartosc x to {x}")
        print(f"wcisnieto przycisk nr: {nr_przycisku}")
        print(f"aktualny widok na przyciski to {aktulany_widok_przyciski}")
        plik_przyciski = open(f"pliki\{aktulany_widok_przyciski}.txt", 'r')
        for i in range(nr_przycisku):
            for j in range(4):
                nr = plik_przyciski.readline()
                nr = nr.rstrip("\n")
                linia1 = plik_przyciski.readline()
                linia1 = linia1.rstrip("\n")
                linia2 = plik_przyciski.readline()
                linia2 = linia2.rstrip("\n")
                linia3 = plik_przyciski.readline()
                linia3 = linia3.rstrip("\n")
                if nr == str(nr_przycisku):
                    print(f"widok tabeli to : {widok_podstawowy}")
                    if aktualny_wiersz_tabeli == ".!frame":
                        frame = "1"
                    elif aktualny_wiersz_tabeli == "." or aktualny_wiersz_tabeli == ".!combobox":
                        frame = "3"
                    else:
                        frame =  aktualny_wiersz_tabeli[7:9]
                    if liczenieWierszy() == 10:
                        print("pelne pole")
                    else:
                        if (frame == "1" or frame == "2" or frame == "11" or frame== "12") and widok_podstawowy == True:
                            if linia1 == "":
                                print("brak tekstu")
                            else:
                                    tabela_ramek[1][int(frame) - 1].insert(float(liczenieWierszy()) + 1, linia1 + '\n')
                            if linia2 == "":
                                    print("brak tekstu")
                            else:
                                    tabela_ramek[1][int(frame) - 1].insert(float(liczenieWierszy()) + 1, linia2 + '\n')
                            if linia3 == "":
                                    print("brak tesktu")
                            else:
                                    tabela_ramek[1][int(frame) - 1].insert(float(liczenieWierszy()) + 1, linia3 + '\n')
                        elif int(frame) >= 3 and int(frame) <= 10:
                            if linia1 == "":
                                print("brak tekstu")
                            else:
                                    tabela_ramek[1][int(frame) - 1].insert(float(liczenieWierszy()) + 1, linia1 + '\n')
                            if linia2 == "":
                                    print("brak tekstu")
                            else:
                                    tabela_ramek[1][int(frame) - 1].insert(float(liczenieWierszy()) + 1, linia2 + '\n')
                            if linia3 == "":
                                    print("brak tesktu")
                            else:
                                    tabela_ramek[1][int(frame) - 1].insert(float(liczenieWierszy()) + 1, linia3 + '\n')



        plik_przyciski.close()

    return f

def przyciskZapisDoExel(root):
    przycisk_zapisz = tk.Button(root, text='Zapisz do pliku exel', font=('Verdana', 8))
    przycisk_zapisz.grid(row=0, column=2)
    przycisk_zapisz.configure(command=zapisDoExel())

    return przycisk_zapisz

def przyciskWyslijPlikExel(root):
    przycisk_wyslij = tk.Button(root, text=' Wyslij email z zal.  ', font=('Verdana', 8))
    przycisk_wyslij.grid(row=1, column=2)
    przycisk_wyslij.configure(command=wyslijPlikExel())

    return przycisk_wyslij

def przyciskWidokTabela(root):
    przycisk_widok_tabela = tk.Button(root, text='Widok podstawowy')
    przycisk_widok_tabela.grid(row=0, column=3)
    przycisk_widok_tabela.configure(command = zmienWidokTabeli())

    return przycisk_widok_tabela

def zmienWidokTabeli():
    def a():
        global tabela_ramek, widok_podstawowy, columnspan_scrolledtext, root, wiersz, przyciski_tekstowe
        if widok_podstawowy == True:
            widok_podstawowy = False
            print("Zmieniamy widok tabeli")
            #---pierwsze dwa wiersze
            tabela_ramek[0][0].grid_remove()
            tabela_ramek[0][1].grid_remove()
            tabela_ramek[1][0].grid_remove()
            tabela_ramek[1][1].grid_remove()
            #---ostatnie dwa wiersze
            tabela_ramek[0][10].grid_remove()
            tabela_ramek[0][11].grid_remove()
            tabela_ramek[1][10].grid_remove()
            tabela_ramek[1][11].grid_remove()
            for i in range(12):
                tabela_ramek[1][i]['height']=(4)
            for i in range(8):
                for j in range(2):
                    przyciski_tekstowe[1][i][j]['height']=(4)
            root.geometry('1100x630')


        else:
            widok_podstawowy = True
            # ---pierwsze dwa wiersze
            tabela_ramek[0][0].grid(row=2, column=0)
            tabela_ramek[0][1].grid(row=3, column=0)
            tabela_ramek[1][0].grid(row=2, column=1, columnspan=columnspan_scrolledtext)
            tabela_ramek[1][1].grid(row=3, column=1, columnspan=columnspan_scrolledtext)
            # ---ostatnie dwa wiersze
            tabela_ramek[0][10].grid(row=12, column=0)
            tabela_ramek[0][11].grid(row=13, column=0)
            tabela_ramek[1][10].grid(row=12, column=1, columnspan=columnspan_scrolledtext)
            tabela_ramek[1][11].grid(row=13, column=1, columnspan=columnspan_scrolledtext)
            print("bedzie tabela wyswietlona w wersji rozszerzonej")
            for i in range(12):
                tabela_ramek[1][i]['height']=(3)
            for i in range(8):
                for j in range(2):
                    przyciski_tekstowe[1][i][j]['height']=(3)
            root.geometry('1100x720')

    return a

def wyslijPlikExel():
    def d():
        pobieranieDoExel(tabela_ramek)
        pygame.mixer.music.load("pliki/dzwieki/chimes.wav")
        pygame.mixer.music.play()
        now = str(datetime.datetime.now())
        now = now[0:10]
        rok_pobrany = now[0:3]
        plik_email = open("pliki/plikiTekstowe/email.txt", 'r')
        plik_email.readline()
        smtp_serwer = plik_email.readline()
        smtp_serwer = smtp_serwer.rstrip("\n")
        plik_email.readline()
        port = plik_email.readline()
        port = port.rstrip("\n")
        plik_email.readline()
        haslo = plik_email.readline()
        haslo = haslo.rstrip("\n")
        plik_email.readline()
        nadawca = plik_email.readline()
        nadawca = nadawca.rstrip("\n")
        plik_email.readline()
        odbiorca = plik_email.readline()
        odbiorca = odbiorca.rstrip("\n")
        plik_email.readline()
        temat = plik_email.readline()
        temat = temat.rstrip("\n")
        if temat.find(rok_pobrany) != -1:
            rok = temat.find(rok_pobrany)
            temat = temat[0: rok] + now
        plik_email.readline()
        tresc = plik_email.readline()
        tresc = tresc.rstrip("\n")
        tresc_b = plik_email.readline()
        tresc_b = tresc_b.rstrip("\n")
        tresc_c = plik_email.readline()
        tresc_c = tresc_c.rstrip("\n")
        tresc_d = plik_email.readline()
        tresc_d = tresc_d.rstrip("\n")
        tresc_e = plik_email.readline()
        tresc_e = tresc_e.rstrip("\n")
        tresc_f = plik_email.readline()
        tresc_f = tresc_f.rstrip("\n")
        tresc_g = plik_email.readline()
        tresc_g = tresc_g.rstrip("\n")
        tresc_h = plik_email.readline()
        tresc_h = tresc_h.rstrip("\n")
        tresc_i = plik_email.readline()
        tresc_i = tresc_i.rstrip("\n")
        tresc_j = plik_email.readline()
        tresc_j = tresc_j.rstrip("\n")
        plik_email.close()
        tresc = tresc+"\n"+tresc_b+"\n"+tresc_c+"\n"+tresc_d+"\n"+tresc_e+"\n"+tresc_f+"\n"+tresc_g+"\n"+tresc_h+"\n"+tresc_i+"\n"+tresc_j
        print(haslo)
        print(port)
        print(smtp_serwer)
        print(temat)
        print(tresc)
        print("wysylanie wiadomosci email z zalaczonym plikiem exel")
        #kod = "mdgkrptzzheekttd"
        #port = 465
        # port uzywany przez protokol ssl
        #smtp_serwer = "smtp.gmail.com"
        #nadawca = "mfmarcinfrontczak@gmail.com"
        #odbiorca = "mfmarcinfrontczak@gmail.com"
        #temat = "mail testowy z zalacznikiem"
        #tresc = "<h1>To jest wiadomosc wyslana w pythonie.</h1>"

        wiadomosc = MIMEMultipart()
        wiadomosc["From"] = nadawca
        wiadomosc["To"] = odbiorca
        wiadomosc["Subject"] = temat
        wiadomosc.attach(MIMEText(tresc, "plain"))

        #haslo = "mdgkrptzzheekttd"
        data = datetime.datetime.now()
        rok = str(data)
        plik = f"raport{rok[0:4]}.xlsx"

        with open(plik, "rb") as f:
            zalacznik = MIMEBase("application", "octet-stream")
            zalacznik.set_payload(f.read())
        encoders.encode_base64(zalacznik)
        zalacznik.add_header(
            "Content-Disposition",
            f"attachment; filename= {plik}"
        )
        wiadomosc.attach(zalacznik)
        tekst = wiadomosc.as_string()

        ssl_pol = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_serwer, port, context=ssl_pol) as serwer:
            serwer.login(nadawca, haslo)
            serwer.sendmail(nadawca, odbiorca, tekst)

    return d

def pobieranieDoExel(t): #funkcja jest wywolana w instrukcji funkcji zapisz do exel
    global Dane_z_dnia
    for i in range(12):
        for j in range(10):
            if t[1][i].get(f'{j+1}.0', f'{j+1}.end') == "":
                print(f"brak tekstu do zapisu dla wiersz w tabeli : {i+1}, linia : {j+1}")
            else:
                Dane_z_dnia[i] += t[1][i].get(f'{j+1}.0', f'{j+1}.end')
                if t[1][i].get(f'{j+2}.0', f'{j+2}.end') == "":
                    print("koniec zapisu tekstu z tabeli")
                else:
                    Dane_z_dnia[i] += "\n"
    data = datetime.datetime.now()
    data_dla_exel = str(data)

    if os.path.exists(f'raport{data_dla_exel[0:4]}.xlsx'):
        print(f"Plik o nazwie raport{data_dla_exel[0:4]}jest w katalogu z programem")
    else:
        shutil.copyfile(f"pliki/raport{data_dla_exel[0:4]}.xlsx", f"raport{data_dla_exel[0:4]}.xlsx")
        print(f"Zostal utworzony plik o nazwie raport{data_dla_exel[0:4]}")
    wb = openpyxl.load_workbook(f'raport{data_dla_exel[0:4]}.xlsx')
    #------pobieranie nazwy uzytkownika , zostanie nazwany tak arkusz------
    plik_uzytkownik = open("pliki/plikiTekstowe/uzytkownik.txt", 'r')
    nazawa_uzytkownika = plik_uzytkownik.readline()
    nazawa_uzytkownika = nazawa_uzytkownika.rstrip("\n")
    plik_uzytkownik.close()

    aktualna_nazwa_arkusza = wb.sheetnames[0]
    sheet1 = wb[aktualna_nazwa_arkusza]
    sheet1.title = nazawa_uzytkownika
    max_ilosc_kolumn = sheet1.max_column
    print(max_ilosc_kolumn)
    for i in range(max_ilosc_kolumn):
        if sheet1.cell(row=1, column=i+1).value == data_dla_exel[0:10]:
            print(f"zapis do kolumny z data : {data_dla_exel[0:10]}")
            for k in range(12):
                sheet1.cell(row=3+k, column=i+1).value = Dane_z_dnia[k]
    wb.save(f'raport{data_dla_exel[0:4]}.xlsx')

    return Dane_z_dnia

def zapisDoExel():
    def f():
        print("zapisywanie do exel")
        pygame.mixer.music.load("pliki/dzwieki/chimes.wav")
        pygame.mixer.music.play()
        pobieranieDoExel(tabela_ramek)
    return f

def shortcut(action, tabela_do_wpisywania):
    global aktualny_wiersz_tabeli, ostatni_wiersz_tabeli, muzyka_co_godzina, root
    print(tabela_do_wpisywania[1][1].focus_get())
    aktualny_wiersz_tabeli = str(tabela_do_wpisywania[1][1].focus_get())
    print(f"aktualny wiersz tabli: {aktualny_wiersz_tabeli}")
    if aktualny_wiersz_tabeli == '.!combobox' or aktualny_wiersz_tabeli == ".":
        aktualny_wiersz_tabeli = ostatni_wiersz_tabeli
    else:
        ostatni_wiersz_tabeli = aktualny_wiersz_tabeli
    pygame.mixer.music.stop()
    czas_wyswietlana = str(datetime.datetime.now())
    if czas_wyswietlana[11:19] != czas_wyswietlana[11:13] + ":00:00" and muzyka_co_godzina == False:
        muzyka_co_godzina = True
        root['bg'] = ('#f0f0f0')
    frame = ""
    if aktualny_wiersz_tabeli == ".!frame":
        frame = "1"
    elif aktualny_wiersz_tabeli == "." or aktualny_wiersz_tabeli == ".!combobox":
        frame = "3"
    else:
        frame = aktualny_wiersz_tabeli[7:9]
    for i in range(12):
        tabela_ramek[0][i]['bg'] = ('#2b2b2b')
    tabela_ramek[0][int(frame)-1]['bg'] = ('red')
    print(f"zmieniamy kolor tla godziny przy tabelce")


####-------Combobox-----------

def comboboxOdswiez():
    global lista_urzadzen
    lista_urzadzen.grid_remove()
    lista = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
    x = 1
    licznik = 0
    while (x == 1):  # ----sprawdzamy ile urzadzen jest w pliku UrzadzeniaLista.txt
        licznik += 1
        urzadzenie_z_lista = lista.readline()
        urzadzenie_z_lista = urzadzenie_z_lista.rstrip("\n")
        if urzadzenie_z_lista == "":
            x = 0
            print("wychodze z petli")
    print(f"wartosc licznika to {licznik - 1}")
    lista.close()
    lista = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
    lista_urzadzen_tablica = ["" for i in range(licznik - 1)]
    for i in range(licznik - 1):
        lista_urzadzen_tablica[i] = lista.readline()
        lista_urzadzen_tablica[i] = lista_urzadzen_tablica[i].rstrip("\n")
        print(lista_urzadzen_tablica[i])
    lista.close()
    lista_urzadzen.config(values=(lista_urzadzen_tablica))
    lista_urzadzen.grid(row=0, column=4, columnspan=2)

def callbackFunc(event):   #funkcja ktora wyswietla to co wybralem
    global aktulany_widok_przyciski, przyciski_tekstowe
    zaznaczone_na_lista = event.widget.get()
    print(zaznaczone_na_lista)
    aktulany_widok_przyciski = zaznaczone_na_lista
    deletePrzyciskiTekstowe(przyciski_tekstowe)
    przyciski_tekstowe = przyciskiTekstowe(root, opcjePrzycisk)


def pierwszeUrzadzenie():
    global aktulany_widok_przyciski
    urzadzenie1 = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
    urzadzenie_z_lista = urzadzenie1.readline()
    urzadzenie_z_lista = urzadzenie_z_lista.rstrip("\n")
    urzadzenie1.close()
    aktulany_widok_przyciski = urzadzenie_z_lista

#----------------Przyciski wyswietlane po prawej stronie--------------------

def przyciskiTekstowe(root, opcjePrzycisk):
    global aktulany_widok_przyciski
    plik_przyciski = open(f"pliki\{aktulany_widok_przyciski}.txt", 'r')
    przyciski_tekstowe = [[["N"  for i in range(2)] for j in range(8)], [[tk.Button(root) for i in range(2)] for i in range(8)]]
    x = 0
    for i in range(8):
        for j in range(2):
            x+=1
            przyciski_tekstowe[0][i][j] = str(x)
            przyciski_tekstowe[1][i][j].grid(row=4+i, column=4+j)
            nr = plik_przyciski.readline()
            nr = nr.rstrip("\n")
            print(f"mamy wiec nr z tekstu: {nr}")
            linia1 = plik_przyciski.readline()
            linia1 = linia1.rstrip("\n")
            print(f"tekst z linia1 to : {linia1}")
            linia2 = plik_przyciski.readline()
            linia2 = linia2.rstrip("\n")
            print(f"tekst z linia1 to : {linia2}")
            linia3 = plik_przyciski.readline()
            linia3 = linia3.rstrip("\n")
            print(f"tekst z linia1 to : {linia3}")
            if linia1 == "" and linia2 == "" and  linia3=="":
                przyciski_tekstowe[1][i][j].config(width=40, height=4, command=funkcjaWpiszTekst(x), text=przyciski_tekstowe[0][i][j])
            else:
                przyciski_tekstowe[0][i][j] = linia1 + '\n' + linia2 +'\n' + linia3
                przyciski_tekstowe[1][i][j].config(width=40, height=4, command=funkcjaWpiszTekst(x),
                                                   text=przyciski_tekstowe[0][i][j])
    plik_przyciski.close()
    przyciski_tekstowe[1][0][0].bind("<Button-3>", lambda e: opcjePrzycisk(1))
    przyciski_tekstowe[1][0][1].bind("<Button-3>", lambda e: opcjePrzycisk(2))
    przyciski_tekstowe[1][1][0].bind("<Button-3>", lambda e: opcjePrzycisk(3))
    przyciski_tekstowe[1][1][1].bind("<Button-3>", lambda e: opcjePrzycisk(4))
    przyciski_tekstowe[1][2][0].bind("<Button-3>", lambda e: opcjePrzycisk(5))
    przyciski_tekstowe[1][2][1].bind("<Button-3>", lambda e: opcjePrzycisk(6))
    przyciski_tekstowe[1][3][0].bind("<Button-3>", lambda e: opcjePrzycisk(7))
    przyciski_tekstowe[1][3][1].bind("<Button-3>", lambda e: opcjePrzycisk(8))
    przyciski_tekstowe[1][4][0].bind("<Button-3>", lambda e: opcjePrzycisk(9))
    przyciski_tekstowe[1][4][1].bind("<Button-3>", lambda e: opcjePrzycisk(10))
    przyciski_tekstowe[1][5][0].bind("<Button-3>", lambda e: opcjePrzycisk(11))
    przyciski_tekstowe[1][5][1].bind("<Button-3>", lambda e: opcjePrzycisk(12))
    przyciski_tekstowe[1][6][0].bind("<Button-3>", lambda e: opcjePrzycisk(13))
    przyciski_tekstowe[1][6][1].bind("<Button-3>", lambda e: opcjePrzycisk(14))
    przyciski_tekstowe[1][7][0].bind("<Button-3>", lambda e: opcjePrzycisk(15))
    przyciski_tekstowe[1][7][1].bind("<Button-3>", lambda e: opcjePrzycisk(16))

    return przyciski_tekstowe

def opcjePrzycisk(nr_przycisku):

    global aktulany_widok_przyciski
    print("opcja dla przycisku")
    window = tk.Tk()
    window.title(f'{aktulany_widok_przyciski}, przycisk nr: {nr_przycisku}')
    window.geometry('341x200')
    tekst_informacyjny = ttk.Label(window, text="Informacja wyswietlana", background='cyan', foreground="black",
                                   font=("Verdana", 9))
    tekst_informacyjny.grid(row=0, column=0)
    tekst_do_wyswietlania = ScrolledText(window, width=38, height=5, font=('Verdana', 9))
    tekst_do_wyswietlania.grid(row=1, column=0)
    tekst_informacyjny2 = ttk.Label(window, text=' Zdiecie ')
    tekst_informacyjny2.grid(row=2, column=0)
    zdiecie = ttk.Entry(window, width=42, font=('Verdana', 9))
    zdiecie.grid(row=3, column=0)
    przycisk_zapisz = tk.Button(window, text='Zapisz')
    przycisk_zapisz.grid(row=4, column=0)
    print(f"nr przycisku to :{nr_przycisku}")
    plik_nazwa = str(aktulany_widok_przyciski) + ".txt"
    print(f"bedzie otwarty plik o nazwie: {plik_nazwa}")
    plik_otwarty = open(f"pliki\{plik_nazwa}", 'r')
    nr = ""
    tekst_na_przycisk_linia1 = ""
    tekst_na_przycisk_linia2 = ""
    tekst_na_przycisk_linia3 = ""
    for i in range(nr_przycisku):
        nr = plik_otwarty.readline()
        nr = nr.rstrip("\n")
        print(f"mamywiec nr  z tekstu: {nr}")
        tekst_na_przycisk_linia1 = plik_otwarty.readline()
        tekst_na_przycisk_linia1 = tekst_na_przycisk_linia1.rstrip("\n")
        print(f"tekst zlinia1 to : {tekst_na_przycisk_linia1}")
        tekst_na_przycisk_linia2 = plik_otwarty.readline()
        tekst_na_przycisk_linia2 = tekst_na_przycisk_linia2.rstrip("\n")
        print(f"tekst zlinia1 to : {tekst_na_przycisk_linia2}")
        tekst_na_przycisk_linia3 = plik_otwarty.readline()
        tekst_na_przycisk_linia3 = tekst_na_przycisk_linia3.rstrip("\n")
        print(f"tekst zlinia1 to : {tekst_na_przycisk_linia3}")
        d = str(nr_przycisku)
        print(f"zmienna d z nr_przycisku ma nr: {d}")
        print(f"zmienna nr ma wartosc {nr}")
    tekst_do_wyswietlania.insert(1.0, tekst_na_przycisk_linia1 + '\n')
    tekst_do_wyswietlania.insert(2.0, tekst_na_przycisk_linia2 + '\n')
    tekst_do_wyswietlania.insert(3.0, tekst_na_przycisk_linia3 + '\n')
    global przyciski_tekstowe
    plik_otwarty.close()

    def zapisz_tekst_przycisk():
        def a():
            global aktulany_widok_przyciski
            plik_urzadzenie_tymczasowy = open(f"pliki\{aktulany_widok_przyciski} tymczasowy.txt", 'w')
            plik_otwarty = open(f"pliki\{plik_nazwa}", 'r')
            print(plik_nazwa)
            tekst_przycisk = [["" for i in range(4)] for j in range(16)]
            for j in range(16):
                for i in range(4):
                    tekst_przycisk[j][i] = plik_otwarty.readline()
                    tekst_przycisk[j][i] = tekst_przycisk[j][i].rstrip("\n")
                    if nr_przycisku == j+1 and i==0:
                        tekst_przycisk[j][i] = str(nr_przycisku)
                    if nr_przycisku == j+1 and i==1:
                        tekst_przycisk[j][i] = tekst_do_wyswietlania.get('1.0', '1.end')
                    if nr_przycisku == j+1 and i==2:
                        tekst_przycisk[j][i] = tekst_do_wyswietlania.get('2.0', '2.end')
                    if nr_przycisku == j+1 and i==3:
                        tekst_przycisk[j][i] = tekst_do_wyswietlania.get('3.0', '3.end')
                    plik_urzadzenie_tymczasowy.write(tekst_przycisk[j][i] + '\n')
                    print(tekst_przycisk[j][i])
            plik_urzadzenie_tymczasowy.close()
            plik_otwarty.close()
            os.remove(f"pliki\{plik_nazwa}")  # Usunięcie pliku np: Skaut 8.txt
            os.rename(f"pliki\{aktulany_widok_przyciski} tymczasowy.txt", f"pliki\{plik_nazwa}")  # Zmiana nazwy pliku tymczasowego.

            # ------------------ instrukcji to wyswietlania tekstu na przycisku ---------------------

            plik_przyciski = open(f"pliki\{aktulany_widok_przyciski}.txt", 'r')
            x = 0
            for i in range(8):
                for j in range(2):
                    x += 1
                    przyciski_tekstowe[0][i][j] = str(x)
                    nr = plik_przyciski.readline()
                    nr = nr.rstrip("\n")
                    print(f"mamywiec nr  z tekstu: {nr}")
                    linia1 = plik_przyciski.readline()
                    linia1 = linia1.rstrip("\n")
                    print(f"tekst zlinia1 to : {linia1}")
                    linia2 = plik_przyciski.readline()
                    linia2 = linia2.rstrip("\n")
                    print(f"tekst zlinia1 to : {linia2}")
                    linia3 = plik_przyciski.readline()
                    linia3 = linia3.rstrip("\n")
                    print(f"tekst zlinia1 to : {linia3}")
                    if linia1 == "" and linia2 == "" and linia3 == "":
                        przyciski_tekstowe[1][i][j].config(text=przyciski_tekstowe[0][i][j])
                    else:
                        przyciski_tekstowe[0][i][j] = linia1 + '\n' + linia2 + '\n' + linia3
                        przyciski_tekstowe[1][i][j].config(text=przyciski_tekstowe[0][i][j])
            plik_przyciski.close()

        return a

    przycisk_zapisz.config(command=zapisz_tekst_przycisk())

    window.mainloop()

def deletePrzyciskiTekstowe(przyciski_tekstowe):
    for i in range(8):
        for j in range(2):
            przyciski_tekstowe[1][i][j].grid_remove()

#------ okno ustawienia------

def oknoUstawienia():
    def a():
        root2 = Tk()
        okno_ustawienia = ttk.Notebook(root2)
        okno_ustawienia.pack()
        now = str(datetime.datetime.now())
        now =  now[0:10]
        rok_pobrany = now[0:3]
        print(rok_pobrany)


        #------------------------------------------zawartosc zakladki email---------------------------------------------
        #---------------------------------------------------------------------------------------------------------------

        # ---------------frame1-------------------
        frame1 = ttk.Frame(okno_ustawienia)
        okno_ustawienia.add(frame1, text='  email  ')
        #--Konfiguracja Serwera--
        tekst_informacyjny = ttk.Label(frame1, text='Konfiguracja serwera', font=('Verdana', 12)).grid(row=0, columnspan=2)
        tekst_linia_1 = ttk.Label(frame1, text=' Smtp_serwer: ').grid(row=1, column=0)
        pole_tekstowe_linia_1 = ttk.Entry(frame1, width='42', font=('Verdana', 9))
        pole_tekstowe_linia_1.grid(row=1, column=1)
        tekst_linia_2 = ttk.Label(frame1, text=' Port: ').grid(row=2, column=0)
        pole_tekstowe_linia_2 = ttk.Entry(frame1, width='42', font=('Verdana', 9))
        pole_tekstowe_linia_2.grid(row=2, column=1)
        tekst_linia_3 = ttk.Label(frame1, text=' Haslo: ').grid(row=3, column=0)
        pole_tekstowe_linia_3 = ttk.Entry(frame1, width='42', font=('Verdana', 9))
        pole_tekstowe_linia_3.grid(row=3, column=1)
        tekst_linia_4 = ttk.Label(frame1, text=' Nadawca: ').grid(row=4, column=0)
        pole_tekstowe_linia_4 = ttk.Entry(frame1, width='42', font=('Verdana', 9))
        pole_tekstowe_linia_4.grid(row=4, column=1)
        pusty_obszar = ttk.Label(frame1).grid(row=5)
        tekst_informacyjny2 = ttk.Label(frame1, text='Zawartosc i adresowanie wiadomosci', font=('Verdana', 12)).grid(row=6, columnspan=2)
        tekst_linia_5 = ttk.Label(frame1, text=' Odbiorca: ').grid(row=7, column=0)
        pole_tekstowe_linia_5 = ttk.Entry(frame1, width='42', font=('Verdana', 9))
        pole_tekstowe_linia_5.grid(row=7, column=1)
        tekst_linia_6 = ttk.Label(frame1, text=' Temat: ').grid(row=8, column=0)
        pole_tekstowe_linia_6 = ttk.Entry(frame1, width='42', font=('Verdana', 9))
        pole_tekstowe_linia_6.grid(row=8, column=1)
        tekst_linia_7 = ttk.Label(frame1, text=' Tresc: ').grid(row=9, column=0)
        pole_tekstowe_linia_7 = ScrolledText(frame1, width=40, height=5, font=('Verdana', 9))
        pole_tekstowe_linia_7.grid(row=9, column=1)
        pusty_obszar2 = ttk.Label(frame1).grid(row=10)
        przycisk = ttk.Button(frame1, text='Zapisz')
        przycisk.grid(row=11, columnspan=2)
        informacje = ttk.Label(frame1, text="\nW Temacie wiadomosci nalezy podac \ntresc + wartosc 202. Do wartosci \nzostanie dopisana automatycznie data. \n \nPrzyklad : Plik z raportem 202", font=('Verdana', 12)).grid(row=12 , columnspan=2)

        def Zapisz_dane_do_pliku_email():
            def a():
                polet_tekstowe_linia_1_nowe_dane = pole_tekstowe_linia_1.get() #smtp
                polet_tekstowe_linia_2_nowe_dane = pole_tekstowe_linia_2.get() #port
                polet_tekstowe_linia_3_nowe_dane = pole_tekstowe_linia_3.get() #haslo
                polet_tekstowe_linia_4_nowe_dane = pole_tekstowe_linia_4.get() #nadawca
                polet_tekstowe_linia_5_nowe_dane = pole_tekstowe_linia_5.get() #odbiorca
                polet_tekstowe_linia_6_nowe_dane = pole_tekstowe_linia_6.get() #temat

                #--!!!!!wpisuje tylko na date z roku 2023 - do poprawy
                rok = polet_tekstowe_linia_6_nowe_dane.find(rok_pobrany)
                print(rok)
                polet_tekstowe_linia_6_nowe_dane = polet_tekstowe_linia_6_nowe_dane[0: rok] + now
                print(polet_tekstowe_linia_6_nowe_dane)
                #tresc
                polet_tekstowe_linia_7_nowe_dane = pole_tekstowe_linia_7.get('1.0', '1.end')
                polet_tekstowe_linia_7b_nowe_dane = pole_tekstowe_linia_7.get('2.0', '2.end')
                polet_tekstowe_linia_7c_nowe_dane = pole_tekstowe_linia_7.get('3.0', '3.end')
                polet_tekstowe_linia_7d_nowe_dane = pole_tekstowe_linia_7.get('4.0', '4.end')
                polet_tekstowe_linia_7e_nowe_dane = pole_tekstowe_linia_7.get('5.0', '5.end')
                polet_tekstowe_linia_7f_nowe_dane = pole_tekstowe_linia_7.get('6.0', '6.end')
                polet_tekstowe_linia_7g_nowe_dane = pole_tekstowe_linia_7.get('7.0', '7.end')
                polet_tekstowe_linia_7h_nowe_dane = pole_tekstowe_linia_7.get('8.0', '8.end')
                polet_tekstowe_linia_7i_nowe_dane = pole_tekstowe_linia_7.get('9.0', '9.end')
                polet_tekstowe_linia_7j_nowe_dane = pole_tekstowe_linia_7.get('10.0', '10.end')
                plik_email_tymczasowy = open("pliki/plikiTekstowe/email-plik-tymczasowy.txt", 'w')
                plik_email_tymczasowy.write('Smtp_serwer:' + "\n")  # Zapisujemy zmodyfikowany rekord w pliku tymczasowym.
                plik_email_tymczasowy.write(polet_tekstowe_linia_1_nowe_dane + "\n")
                plik_email_tymczasowy.write('Port:' + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_2_nowe_dane + "\n")
                plik_email_tymczasowy.write('Haslo:' + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_3_nowe_dane + "\n")
                plik_email_tymczasowy.write('Nadawca:' + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_4_nowe_dane + "\n")
                plik_email_tymczasowy.write('Odbiorca:' + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_5_nowe_dane + "\n")
                plik_email_tymczasowy.write('Temat:' + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_6_nowe_dane + "\n")
                plik_email_tymczasowy.write('Tresc:' + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7b_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7c_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7d_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7e_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7f_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7g_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7h_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7i_nowe_dane + "\n")
                plik_email_tymczasowy.write(polet_tekstowe_linia_7j_nowe_dane + "\n")
                plik_email_tymczasowy.close()
                os.remove("pliki/plikiTekstowe/email.txt")  # Usunięcie pliku Pracownicy.txt.
                os.rename("pliki/plikiTekstowe/email-plik-tymczasowy.txt", "pliki/plikiTekstowe/email.txt")  # Zmiana nazwy pliku tymczasowego.

            return a

        przycisk.configure(command = Zapisz_dane_do_pliku_email())

        def Odczytaj_dane_z_pliku_email():
            plik_email = open("pliki/plikiTekstowe/email.txt", 'r')
            plik_email.readline()
            smtp_serwer = plik_email.readline()
            smtp_serwer = smtp_serwer.rstrip("\n")
            print(smtp_serwer)
            plik_email.readline()
            port = plik_email.readline()
            port = port.rstrip("\n")
            print(port)
            plik_email.readline()
            haslo = plik_email.readline()
            haslo = haslo.rstrip("\n")
            plik_email.readline()
            nadawca = plik_email.readline()
            nadawca = nadawca.rstrip("\n")
            plik_email.readline()
            odbiorca = plik_email.readline()
            odbiorca = odbiorca.rstrip("\n")
            plik_email.readline()
            temat = plik_email.readline()
            temat = temat.rstrip("\n")
            print(temat) # dziala tylko dla roku 2023 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if temat.find(rok_pobrany) != -1 :
                # --!!!!!wpisuje tylko na date z roku 2023 - do poprawy
                rok = temat.find(rok_pobrany)
                print(f"wyswietl rok : {rok}")
                temat = temat[0: rok] + now
            plik_email.readline()
            tresc = plik_email.readline()
            tresc = tresc.rstrip("\n")
            tresc_b = plik_email.readline()
            tresc_b = tresc_b.rstrip("\n")
            tresc_c = plik_email.readline()
            tresc_c = tresc_c.rstrip("\n")
            tresc_d = plik_email.readline()
            tresc_d = tresc_d.rstrip("\n")
            tresc_e = plik_email.readline()
            tresc_e = tresc_e.rstrip("\n")
            tresc_f = plik_email.readline()
            tresc_f = tresc_f.rstrip("\n")
            tresc_g = plik_email.readline()
            tresc_g = tresc_g.rstrip("\n")
            tresc_h = plik_email.readline()
            tresc_h = tresc_h.rstrip("\n")
            tresc_i = plik_email.readline()
            tresc_i = tresc_i.rstrip("\n")
            tresc_j = plik_email.readline()
            tresc_j = tresc_j.rstrip("\n")
            pole_tekstowe_linia_1.insert(0, smtp_serwer)
            pole_tekstowe_linia_2.insert(0, port)
            pole_tekstowe_linia_3.insert(0, haslo)
            pole_tekstowe_linia_4.insert(0, nadawca)
            pole_tekstowe_linia_5.insert(0, odbiorca)
            pole_tekstowe_linia_6.insert(0, temat)
            pole_tekstowe_linia_7.insert(1.0, tresc + '\n')
            pole_tekstowe_linia_7.insert(2.0, tresc_b + '\n')
            pole_tekstowe_linia_7.insert(3.0, tresc_c + '\n')
            pole_tekstowe_linia_7.insert(4.0, tresc_d + '\n')
            pole_tekstowe_linia_7.insert(5.0, tresc_e + '\n')
            pole_tekstowe_linia_7.insert(6.0, tresc_f + '\n')
            pole_tekstowe_linia_7.insert(7.0, tresc_g + '\n')
            pole_tekstowe_linia_7.insert(8.0, tresc_h + '\n')
            pole_tekstowe_linia_7.insert(9.0, tresc_i + '\n')
            pole_tekstowe_linia_7.insert(10.0, tresc_j + '\n')
            plik_email.close()
        Odczytaj_dane_z_pliku_email()



        # -----------------------------------zawartosc zakladki Przyciski ----------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # ---------------frame2-------------------
        frame2 = ttk.Frame(okno_ustawienia)
        okno_ustawienia.add(frame2, text='Przyciski')
        zakaldka_przyciski = [[ttk.Label(frame2) for i in range(30)], [ttk.Entry(frame2) for i in range(30)]]
        for i in range(30):
            zakaldka_przyciski[0][i].config(text=f"{i + 1}.", font=('Verdana', 9))
            zakaldka_przyciski[0][i].grid(row=i, column=0)
            zakaldka_przyciski[1][i].config(width='40', font=('Verdana', 9))
            zakaldka_przyciski[1][i].grid(row=i, column=1)
        przycisk_dodaj_elementy = ttk.Button(frame2, text="Zapisz")
        przycisk_dodaj_elementy.grid(row=30, column=1)

        # ------funkcja urzywana podczas klikniecia na przycisk Zapisz --------
        def dodanieDoListy():
            def b():
                #wpisane_nazwy_urzadzenia = "" #["" for i in range(30)]
                listaUrzadzeniaTymczasowa = open("pliki/plikiTekstowe/listaUrzadzeniaTymczasowa.txt", 'w')
                for i in range(30):
                    wpisane_nazwy_urzadzenia = zakaldka_przyciski[1][i].get()
                    listaUrzadzeniaTymczasowa.write(wpisane_nazwy_urzadzenia + '\n')
                    if os.path.exists(f'pliki/{wpisane_nazwy_urzadzenia}.txt'):
                        print(f"Plik o nazwie {wpisane_nazwy_urzadzenia} istnieje")
                    elif wpisane_nazwy_urzadzenia == "":
                        print("brak plikow do dodania")
                    else:
                        shutil.copyfile("pliki/plikiTekstowe/Szablon.txt", f"pliki/{wpisane_nazwy_urzadzenia}.txt")
                        print(f"Zostal utworzony plik o nazwie {wpisane_nazwy_urzadzenia}.txt")
                listaUrzadzeniaTymczasowa.close()
                os.remove("pliki/plikiTekstowe/UrzadzeniaLista.txt")  # Usunięcie pliku Pracownicy.txt.
                os.rename("pliki/plikiTekstowe/listaUrzadzeniaTymczasowa.txt", "pliki/plikiTekstowe/UrzadzeniaLista.txt")
                pierwszeUrzadzenie()
                lista_urzadzen.set(aktulany_widok_przyciski)
                comboboxOdswiez()
                global przyciski_tekstowe
                deletePrzyciskiTekstowe(przyciski_tekstowe)
                przyciski_tekstowe = przyciskiTekstowe(root, opcjePrzycisk)

            return b

        przycisk_dodaj_elementy.configure(command=dodanieDoListy())

        def odczytanieDaneUrzadeniaLista():
            lista = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
            x = 1
            licznik = 0
            while (x == 1):
                licznik += 1
                urzadzenie_z_lista = lista.readline()
                urzadzenie_z_lista = urzadzenie_z_lista.rstrip("\n")
                if urzadzenie_z_lista == "":
                    x = 0
                    print("wychodze z petli")
            print(f"wartosc licznika to {licznik - 1}")
            lista.close()
            lista = open("pliki/plikiTekstowe/UrzadzeniaLista.txt", 'r')
            lista_urzadzen_tablica = ["" for i in range(licznik - 1)]
            for i in range(licznik - 1):
                lista_urzadzen_tablica[i] = lista.readline()
                lista_urzadzen_tablica[i] = lista_urzadzen_tablica[i].rstrip("\n")
                print(lista_urzadzen_tablica[i])
                zakaldka_przyciski[1][i].insert(0, lista_urzadzen_tablica[i])
            lista.close()

        odczytanieDaneUrzadeniaLista()

        # ------------------------zawartosc zakladka Uzytkownik--------------------------------------------
        #--------------------------------------------------------------------------------------------------
        # ---------------frame3-------------------
        frame3 = ttk.Frame(okno_ustawienia)
        okno_ustawienia.add(frame3, text='Uzytkownik')
        tekst_nazwa_urzytkownika = ttk.Label(frame3, text=' Nazwa uzytkownika: ').grid(row=0, column=0)
        pole_tekstowe_nazwa_uzytkownika = ttk.Entry(frame3, width='42', font=('Verdana', 9))
        pole_tekstowe_nazwa_uzytkownika.grid(row=0, column=1)
        przycisk_zapisz_nazwa_uzytkownika = ttk.Button(frame3, text='Zapisz')
        przycisk_zapisz_nazwa_uzytkownika.grid(row=1, columnspan=2)

        def Zapisz_dane_do_pliku_uzytkownik():
            def a():
                nazwa_uzytkownik = pole_tekstowe_nazwa_uzytkownika.get()
                plik_uzytkownik_tymczasowy = open("pliki/plikiTekstowe/uzytkownikTymczasowy.txt", 'w')
                plik_uzytkownik_tymczasowy.write(nazwa_uzytkownik)  # Zapisujemy rekord w pliku tymczasowym.
                plik_uzytkownik_tymczasowy.close()
                os.remove("pliki/plikiTekstowe/uzytkownik.txt")  # Usunięcie pliku uzytkownik.txt.
                os.rename("pliki/plikiTekstowe/uzytkownikTymczasowy.txt", "pliki/plikiTekstowe/uzytkownik.txt")  # Zmiana nazwy pliku tymczasowego.

            return a

        przycisk_zapisz_nazwa_uzytkownika.configure(command = Zapisz_dane_do_pliku_uzytkownik())

        def Odczytaj_dane_z_pliku_uzytkownik():

            plik_uzytkownik = open("pliki/plikiTekstowe/uzytkownik.txt", 'r')
            nazawa_uzytkownika = plik_uzytkownik.readline()
            nazawa_uzytkownika = nazawa_uzytkownika.rstrip("\n")

            pole_tekstowe_nazwa_uzytkownika.insert(0, nazawa_uzytkownika)

            plik_uzytkownik.close()
        Odczytaj_dane_z_pliku_uzytkownik()

        # ------------------------zawartosc zakladka Dzwieki--------------------------------------------
        #-----------------------------------------------------------------------------------------------
        # ---------------frame4-------------------
        frame4 = ttk.Frame(okno_ustawienia)
        okno_ustawienia.add(frame4, text='Dzwieki')
        lista_dzwieki = [[ttk.Label(frame4) for i in range(12)], [ttk.Entry(frame4) for i in range(12)]]
        for i in range(12):
            lista_dzwieki[0][i].config(text=f"{7+i}:00", font=('Verdana', 9))
            lista_dzwieki[0][i].grid(row=i, column=0)
            lista_dzwieki[1][i].config(width='40', font=('Verdana', 9))
            lista_dzwieki[1][i].grid(row=i, column=1)
        przycisk_zapisz_dzwieki = ttk.Button(frame4, text="Zapisz")
        przycisk_zapisz_dzwieki.grid(row=12, column=1)

        # ------funkcja urzywana podczas klikniecia na przycisk Zapisz --------
        def dodanieDoListyDzwieki():
            def b():
                #wpisane_nazwy_dzwieki = ""#["" for i in range(30)] # lista pusta - 30 elementow
                listaDzwiekiTymczasowa = open("pliki/dzwieki/listaDzwiekiTymczasowa.txt", 'w')
                for i in range(12):
                    wpisane_nazwy_dzwieki = lista_dzwieki[1][i].get()
                    listaDzwiekiTymczasowa.write(wpisane_nazwy_dzwieki + '\n')
                    if os.path.exists(f'pliki/{wpisane_nazwy_dzwieki}'):
                        print(f"Plik o nazwie {wpisane_nazwy_dzwieki} istnieje")
                    elif wpisane_nazwy_dzwieki == "":
                        print("brak plikow dzwiekow do dodania")
                listaDzwiekiTymczasowa.close()
                os.remove("pliki/dzwieki/DzwiekiLista.txt")  # Usunięcie pliku Pracownicy.txt.
                os.rename("pliki/dzwieki/listaDzwiekiTymczasowa.txt", "pliki/dzwieki/DzwiekiLista.txt")

            return b

        przycisk_zapisz_dzwieki.configure(command=dodanieDoListyDzwieki())

        def odczytanieDzwiekiLista():
            lista = open("pliki/dzwieki/DzwiekiLista.txt", 'r')
            x = 1
            licznik = 0
            while (x == 1):
                licznik += 1
                dzwiek_z_lista = lista.readline()
                dzwiek_z_lista = dzwiek_z_lista.rstrip("\n")
                if dzwiek_z_lista == "":
                    x = 0
                    print("wychodze z petli")
            print(f"wartosc licznika to {licznik - 1}")
            lista.close()
            lista = open("pliki/dzwieki/DzwiekiLista.txt", 'r')
            lista_dzwieki_tablica = ["" for i in range(licznik - 1)]
            for i in range(licznik - 1):
                lista_dzwieki_tablica[i] = lista.readline()
                lista_dzwieki_tablica[i] = lista_dzwieki_tablica[i].rstrip("\n")
                print(lista_dzwieki_tablica[i])
                lista_dzwieki[1][i].insert(0, lista_dzwieki_tablica[i])

            lista.close()


        odczytanieDzwiekiLista()


        root2.mainloop()

    return a

if __name__=="__main__":

    pygame.mixer.init()
    pierwszeUrzadzenie()
    pobieranieZExel()
    root = okno()
    data = dataPobrana(root)
    czas = zegarPobrany(root)
    zapisz_do_exel = przyciskZapisDoExel(root)
    tabela_ramek = tabela(root)
    przyciski_tekstowe = przyciskiTekstowe(root, opcjePrzycisk) # funkcja jest w pliku przyciski.py
    wstawaineZExelDoTabeli()
    wyslij_email_z_exel = przyciskWyslijPlikExel(root)
    przycisk_zmien_widok_tbeli = przyciskWidokTabela(root)
    lista_urzadzen = boxListaUrzadzen(root)
    lista_urzadzen.set(aktulany_widok_przyciski)
    root.bind('<Control-Tab>', lambda e: shortcut('Get', tabela_ramek))
    root.bind('<Button-1>', lambda e: shortcut('Get', tabela_ramek))
    lista_urzadzen.bind("<<ComboboxSelected>>", callbackFunc)



    root.mainloop()