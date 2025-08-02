import pygame
import random
import math
import os.path
import pygame.time
# Inicjalizacja biblioteki Pygame

pygame.init()



# Ustawienia ekranu
szerokosc = 800 
wysokosc = 600
ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Forest Invaders")

# Tło
tlo = pygame.image.load("images/background.png").convert_alpha()
tlo = pygame.transform.scale(tlo, (800, 600))
# Gracz
gracz_img = pygame.image.load("images/player.png").convert_alpha()
gracz_x = szerokosc / 2 - 32
gracz_y = wysokosc - 64
gracz_x_change = 0

# Dźwięki
strzal_dzwiek = pygame.mixer.Sound("sound/shoot.mp3")
trafienie_dzwiek = pygame.mixer.Sound("sound/hit.wav")

# Wrogi
wrog_img = pygame.image.load("images/golem.png").convert_alpha()
wrog_x = []
wrog_y = []
wrog_x_change = []
wrog_y_change = []
liczba_wrogow = 6

for i in range(liczba_wrogow):
    wrog_x.append(random.randint(0, szerokosc - 64))
    wrog_y.append(random.randint(50, 150))
    wrog_x_change.append(1)
    wrog_y_change.append(40)

# Pocisk gracza
pocisk_img = pygame.image.load("images/arrow.png").convert_alpha()
pocisk_img = pygame.transform.scale(pocisk_img, (16,32))
pocisk_x = 0
pocisk_y = wysokosc - 64
pocisk_x_change = 0
pocisk_y_change = 10
pocisk_gotowy = True

# Pocisk wroga
wrog_pocisk_img = pygame.image.load("images/magicfire.png").convert_alpha()
wrog_pocisk_img = pygame.transform.scale(wrog_pocisk_img, (32,32))
wrog_pocisk_x = []
wrog_pocisk_y = []
wrog_pocisk_x_change = []
wrog_pocisk_y_change = []
liczba_wrog_pociskow = 10

for i in range(liczba_wrog_pociskow):
    wrog_pocisk_x.append(0)
    wrog_pocisk_y.append(16)
    wrog_pocisk_x_change.append(0)
    wrog_pocisk_y_change.append(1)

# Wynik
wynik = 0
czcionka = pygame.font.Font("freesansbold.ttf", 32)
tekst_x = 10
tekst_y = 10

# Życie
zycie = 3
zycie_czcionka = pygame.font.Font("freesansbold.ttf", 24)
zycie_x = szerokosc - 120
zycie_y = 10


#cooldown
cooldown = 1000  # Czas odstępu między strzałami (w milisekundach)
ostatni_strzal_czas = 0


# Top 10 wyników
top_10_wynikow = []

def zapisz_wynik(wynik):
    global top_10_wynikow
    # Odczytanie istniejących wyników
    top_10_wynikow = odczytaj_top_score()  
    # Dodanie nowego wyniku
    top_10_wynikow.append(wynik) 
    # Sortowanie w kolejności malejącej
    top_10_wynikow.sort(reverse=True)
    # Ograniczenie listy do 10 elementów
    if len(top_10_wynikow) > 10:
        top_10_wynikow = top_10_wynikow[:10]
    
    with open("top_score.txt", "w") as plik:
        plik.write("\n".join(str(w) for w in top_10_wynikow))

def odczytaj_top_score():
    try:
        with open("top_score.txt", "r") as plik:
            top_10_wynikow = [int(wynik) for wynik in plik.readlines()]
            return top_10_wynikow
    except FileNotFoundError:
        return []

         
  
def wyswietl_top_wyniki():
    global top_10_wynikow
    ekran.fill((0, 0, 0))
    ekran.blit(tlo, (0, 0))
    tekst_top = czcionka.render("Top 10 najlepszych wyników:", True, (255, 255, 255))
    ekran.blit(tekst_top, (szerokosc / 2 - 225, 50))

    top_10_wynikow = odczytaj_top_score()  # Przypisanie wartości zwracanej przez funkcję
    
    for i, wynik in enumerate(top_10_wynikow):
        tekst_wynik = czcionka.render(str(wynik), True, (255, 255, 255))
        ekran.blit(tekst_wynik, (szerokosc / 2 - 50, 100 + i * 30))
    pygame.display.update()
                
def wyswietl_wynik(x, y):
    wynik_render = czcionka.render("Wynik: " + str(wynik), True, (255, 255, 255))
    ekran.blit(wynik_render, (x, y))

def wyswietl_zycie(x, y):
    zycie_render = zycie_czcionka.render("Życie: " + str(zycie), True, (255, 255, 255))
    ekran.blit(zycie_render, (x, y))

def gracz(x, y):
    ekran.blit(gracz_img, (x, y))

def wrog(x, y):
    ekran.blit(wrog_img, (x, y))

def strzal_pocisku(x, y):
    global pocisk_gotowy
    pocisk_gotowy = False
    ekran.blit(pocisk_img, (x + 16, y + 10))
    strzal_dzwiek.play()

def strzal_wrog_pocisku(x, y):
    for i in range(liczba_wrog_pociskow):
        if not wrog_pocisk_y[i] < wysokosc:
            wrog_pocisk_x[i] = x + 16
            wrog_pocisk_y[i] = y + 10
            break

def kolizja(wrog_x, wrog_y, pocisk_x, pocisk_y):
    odleglosc = math.sqrt(math.pow(wrog_x - pocisk_x, 2) + math.pow(wrog_y - pocisk_y, 2))
    if odleglosc < 27:
        return True
    else:
        return False

def kolizja_gracz_wrog(wrog_x, wrog_y, gracz_x, gracz_y):
    odleglosc = math.sqrt(math.pow(wrog_x - gracz_x, 2) + math.pow(wrog_y - gracz_y, 2))
    if odleglosc < 32:
        return True
    else:
        return False

def resetuj_gre():
    global gracz_x, gracz_y, wynik, zycie, pocisk_gotowy, ostatni_strzal_czas
   
    gracz_x = szerokosc / 2 - 32
    gracz_y = wysokosc - 64
    wynik = 0
    zycie = 3
    pocisk_gotowy = True
    ostatni_strzal_czas = 0

    for i in range(liczba_wrogow):
        wrog_x[i] = random.randint(0, szerokosc - 64)
        wrog_y[i] = random.randint(50, 150)
        wrog_x_change[i] = 1
        wrog_y_change[i] = 40
        
def start_gry():
    global gra_aktywna, wynik, zycie

    while not gra_aktywna:
        ekran.fill((0, 0, 0))
        ekran.blit(tlo, (0, 0))
        tekst_start = czcionka.render("Naciśnij SPACJĘ, aby rozpocząć grę", True, (255, 255, 255))
        ekran.blit(tekst_start, (szerokosc / 2 - 250, wysokosc / 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gra_aktywna = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gra_aktywna = True
                    wynik = 0
                    zycie = 3
                    for i in range(liczba_wrogow):
                        wrog_x[i] = random.randint(0, szerokosc - 64)
                        wrog_y[i] = random.randint(50, 150)
                    
        pygame.display.update()

def koniec_gry():
    global gra_aktywna

    while gra_aktywna:
        ekran.fill((0, 0, 0))
        ekran.blit(tlo, (0, 0))
        tekst_koniec = czcionka.render("Koniec gry! Twój wynik: " + str(wynik), True, (255, 255, 255))
        tekst_reset = czcionka.render("Naciśnij SPACJA, aby zacząć grę od nowa.", True, (255, 255, 255))
        tekst_escape = czcionka.render("Naciśnij ESC, aby zakończyć.", True, (255, 255, 255))
        tekst_topscore = czcionka.render("Naciśnij X, aby zobaczyć top wyników.", True, (255, 255, 255))
        ekran.blit(tekst_koniec, (szerokosc / 2.5 - 250, wysokosc / 5))
        ekran.blit(tekst_reset, (szerokosc / 2.5 - 250, wysokosc / 3.5 + 50))
        ekran.blit(tekst_escape, (szerokosc / 2.5 -250, wysokosc / 2 + 100))
        ekran.blit(tekst_topscore, (szerokosc / 2.5 -250, wysokosc / 2 + 150))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gra_aktywna = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gra_aktywna = False
                    
                #nie dziala restart
                if event.key == pygame.K_SPACE:
                    resetuj_gre()
                    return
                    
                #Lista wyników
                if event.key == pygame.K_x:
                    pokazuj_top_wyniki = not pokazuj_top_wyniki  # Odwrócenie wartości flagi
                    if pokazuj_top_wyniki:
                        wyswietl_top_wyniki()
                        pygame.time.delay(1000)   
        pokazuj_top_wyniki = False  
         
        pygame.display.update()
# Pętla gry
gra_aktywna = False

start_gry()
clock = pygame.time.Clock()
FPS = 60  # Maksymalna liczba klatek na sekundę
while gra_aktywna:
    ekran.fill((0, 0, 0))
    ekran.blit(tlo, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_aktywna = False
        
        # Ruch gracza
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gracz_x_change = -2
            if event.key == pygame.K_RIGHT:
                gracz_x_change = 2

            # Strzał gracza
            if event.key == pygame.K_SPACE:
                if pocisk_gotowy:
                    pocisk_x = gracz_x
                    strzal_pocisku(pocisk_x, pocisk_y)
            # Wyłączenie gry
            if event.key == pygame.K_ESCAPE:
                gra_aktywna = False
            # Resetowanie gry
            if event.key == pygame.K_r:
                resetuj_gre()
                   
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                gracz_x_change = 0

    
    czas = clock.tick(FPS) / 7.0  # Czas od ostatniej aktualizacji w sekundach
  
    # Przeliczenie prędkości gracza zgodnie z czasem
    gracz_x += gracz_x_change * czas

    # Ograniczenia planszy dla gracza
    if gracz_x < 0:
        gracz_x = 0
    elif gracz_x > szerokosc - 64:
        gracz_x = szerokosc - 64

    # Ruch wrogów
    for i in range(liczba_wrogow):
        # Koniec gry - kolizja wrog-gracz
        if wrog_y[i] > wysokosc - 100:
            zapisz_wynik(wynik)
            koniec_gry()
            break
        
        #Trudność gry (Przeciwnicy się ruszają! wartość 0 sprawi że nie będą się ruszać)
        wrog_x[i] += wrog_x_change[i]

        # Ograniczenia planszy dla wroga
        if wrog_x[i] <= 0:
            wrog_x_change[i] = 4
            wrog_y[i] += wrog_y_change[i]
        elif wrog_x[i] >= szerokosc - 64:
            wrog_x_change[i] = -4
            wrog_y[i] += wrog_y_change[i]

        # Kolizja pocisku z wrogiem
        if kolizja(wrog_x[i], wrog_y[i], pocisk_x, pocisk_y):
            trafienie_dzwiek.play()
            pocisk_y = wysokosc - 64
            pocisk_gotowy = True
            wynik += 1
            wrog_x[i] = random.randint(0, szerokosc - 64)
            wrog_y[i] = random.randint(50, 150)

        wrog(wrog_x[i], wrog_y[i])

 
        # Strzał wroga + cooldown   
        czas_teraz = pygame.time.get_ticks()
        if random.randint(0, 100) < 50 and czas_teraz - ostatni_strzal_czas > cooldown:
            strzal_wrog_pocisku(wrog_x[i], wrog_y[i])
            ostatni_strzal_czas = czas_teraz  # Zapisz aktualny czas jako czas ostatniego strzału
        # Ruch wrogiego pocisku
        for j in range(liczba_wrog_pociskow):
            wrog_pocisk_y[j] += wrog_pocisk_y_change[j]
        
            # Kolizja wrogiego pocisku z graczem
            if kolizja_gracz_wrog(wrog_pocisk_x[j], wrog_pocisk_y[j], gracz_x, gracz_y):
                trafienie_dzwiek.play()
                wrog_pocisk_y[j] = wysokosc
                zycie -= 1

            # Wyświetlanie wrogiego pocisku
            ekran.blit(wrog_pocisk_img, (wrog_pocisk_x[j], wrog_pocisk_y[j]))

    # Ruch pocisku
    if pocisk_y <= 0:
        pocisk_y = wysokosc - 64
        pocisk_gotowy = True

    if not pocisk_gotowy:
        strzal_pocisku(pocisk_x, pocisk_y)
        pocisk_y -= pocisk_y_change

    gracz(gracz_x, gracz_y)
    wyswietl_wynik(tekst_x, tekst_y)
    wyswietl_zycie(zycie_x, zycie_y)
    
    # Sprawdzenie warunku końca gry
    if zycie <= 0:
        zapisz_wynik(wynik)
        koniec_gry()
        
    pygame.display.update()
