import turtle
import random
import time

# ============================================================
#  ŰRHAJÓS KALAND 2.0
#  Újdonságok: nehézségi szint, pontszám, életek (HP),
#  színes ellenségek különböző képességekkel, 2 játékos mód,
#  végtelen pálya (egyre nehezebb lesz!)
# ============================================================

# 1. Képernyő (Az űr) beállítása
ablak = turtle.Screen()
ablak.bgcolor("black")
ablak.title("Űrhajós Kaland 2.0!")
ablak.setup(width=600, height=600)
ablak.tracer(0)  # Folyamatos animációhoz

# --- NEHÉZSÉGI SZINT KIVÁLASZTÁSA ---
# A textinput egy kis ablakot dob fel, amibe írni lehet
valasz = ablak.textinput("Nehézség", "Válassz nehézséget!\n1 = Könnyű\n2 = Közepes\n3 = Nehéz")
if valasz == "3":
    nehezseg = 3
elif valasz == "2":
    nehezseg = 2
else:
    nehezseg = 1  # Ha mást ír be (vagy semmit), könnyű lesz

# --- JÁTÉKOSOK SZÁMA ---
valasz2 = ablak.textinput("Játékosok", "Hány játékos? (1 vagy 2)")
if valasz2 == "2":
    ketjatekos = True
else:
    ketjatekos = False

# --- JÁTÉK BEÁLLÍTÁSAI (ezeken lehet csavargatni!) ---
alap_sebesseg = 1 + nehezseg          # Ennyivel mozognak a meteorok az elején
meteor_darab = 2 + nehezseg           # Ennyi meteor van egyszerre a képernyőn
eletek = 5 - nehezseg                 # Könnyű: 4 élet, Közepes: 3, Nehéz: 2
pontszam = 0
jatek_kezdete = time.time()           # Megjegyezzük, mikor indult a játék

# 2. Játékos (Űrhajó)
jatekos = turtle.Turtle()
jatekos.color("cyan")
jatekos.shape("triangle")
jatekos.penup()
jatekos.setheading(90)
jatekos.goto(-100 if ketjatekos else 0, -250)

# 2/b. Második játékos (csak ha ketten játszanak)
jatekos2 = turtle.Turtle()
jatekos2.color("lime")
jatekos2.shape("triangle")
jatekos2.penup()
jatekos2.setheading(90)
if ketjatekos:
    jatekos2.goto(100, -250)
else:
    jatekos2.hideturtle()
    jatekos2.goto(0, -1000)  # Jó messze eldugjuk, hogy ne zavarjon

# --- PONTSZÁM ÉS ÉLETEK KIÍRÁSA ---
# Ez a teknős nem játszik, csak szöveget ír a képernyő tetejére
tabla = turtle.Turtle()
tabla.color("white")
tabla.penup()
tabla.hideturtle()
tabla.goto(0, 260)

def tabla_frissit():
    tabla.clear()  # Letöröljük a régi szöveget
    szoveg = "Pont: {}   Élet: {}".format(pontszam, "♥" * eletek)
    tabla.write(szoveg, align="center", font=("Courier", 16, "bold"))

# ============================================================
#  ELLENSÉGEK - minden színnek más a képessége!
#
#  piros   = sima meteor, csak esik lefelé
#  orange  = GYORS! Kétszer olyan gyorsan esik
#  yellow  = GYÁVA: elfut oldalra a lézer elől
#  purple  = VADÁSZ: követi a játékost oldalra
#  green   = KEMÉNY: 2 lövés kell neki (kettéosztódik... na jó,
#            először csak összemegy, másodikra hal meg)
#  white   = LÖVÉSZ: néha visszalő rád!
# ============================================================

ellenseg_szinek = ["red", "red", "orange", "yellow", "purple", "green", "white"]
# (A "red" kétszer van benne, így az a leggyakoribb)

def uj_ellenseg_beallitas(e):
    """Egy ellenséget feltesz a képernyő tetejére, véletlen színnel."""
    szin = random.choice(ellenseg_szinek)
    e.color(szin)
    e.szin = szin              # Elmentjük a teknősbe, milyen színű
    e.hp = 2 if szin == "green" else 1  # A zöldnek 2 élete van!
    e.shapesize(1, 1)          # Normál méret (a sebzett zöld kisebb lesz)
    e.goto(random.randint(-280, 280), random.randint(250, 400))
    # (Néha a képernyő fölött indul, így nem egyszerre érnek le)

ellensegek = []  # Ebben a listában tároljuk az ÖSSZES ellenséget
for i in range(meteor_darab):
    e = turtle.Turtle()
    e.shape("circle")
    e.penup()
    uj_ellenseg_beallitas(e)
    ellensegek.append(e)

# --- ELLENSÉG LÉZEREI (a fehér ellenség lő velük) ---
gonosz_lezerek = []

def gonosz_lezer(x, y):
    """A fehér ellenség lelő egy piros lézert (x, y)-ból."""
    gl = turtle.Turtle()
    gl.color("red")
    gl.shape("square")
    gl.shapesize(stretch_wid=0.2, stretch_len=1)
    gl.penup()
    gl.setheading(270)  # Lefelé néz
    gl.goto(x, y)
    gonosz_lezerek.append(gl)

# 4. Játékosok lézerei
def lezer_keszit(szin):
    l = turtle.Turtle()
    l.color(szin)
    l.shape("square")
    l.shapesize(stretch_wid=0.2, stretch_len=1)
    l.penup()
    l.setheading(90)
    l.hideturtle()
    l.allapot = "kesz"  # "kesz" = lőhetünk, "lo" = repül
    return l

lezer = lezer_keszit("yellow")
lezer2 = lezer_keszit("lime")
lezer_sebesseg = 7

# --- MOZGÁS FÜGGVÉNYEK ---

def balra():
    if jatekos.xcor() > -280:
        jatekos.setx(jatekos.xcor() - 20)

def jobbra():
    if jatekos.xcor() < 280:
        jatekos.setx(jatekos.xcor() + 20)

def loves():
    if lezer.allapot == "kesz":
        lezer.allapot = "lo"
        lezer.goto(jatekos.xcor(), jatekos.ycor() + 10)
        lezer.showturtle()

def balra2():
    if jatekos2.xcor() > -280:
        jatekos2.setx(jatekos2.xcor() - 20)

def jobbra2():
    if jatekos2.xcor() < 280:
        jatekos2.setx(jatekos2.xcor() + 20)

def loves2():
    if lezer2.allapot == "kesz":
        lezer2.allapot = "lo"
        lezer2.goto(jatekos2.xcor(), jatekos2.ycor() + 10)
        lezer2.showturtle()

# --- IRÁNYÍTÁS BEÁLLÍTÁSA ---
ablak.listen()
ablak.onkeypress(balra, "Left")
ablak.onkeypress(jobbra, "Right")
ablak.onkeypress(loves, "space")
if ketjatekos:
    ablak.onkeypress(balra2, "a")
    ablak.onkeypress(jobbra2, "d")
    ablak.onkeypress(loves2, "w")

tabla_frissit()

# ============================================================
#  FŐ JÁTÉKCIKLUS
# ============================================================
while True:
    try:
        ablak.update()
        time.sleep(0.01)

        # --- VÉGTELEN PÁLYA: minél tovább élsz, annál gyorsabb! ---
        # Minden eltelt 15 másodperc után +1 sebesség
        eltelt_ido = time.time() - jatek_kezdete
        sebesseg = alap_sebesseg + int(eltelt_ido / 15)

        # --- MINDEN ELLENSÉG MOZGATÁSA ---
        for e in ellensegek:

            # 1. lépés: lefelé esés (a narancssárga kétszer gyorsabb!)
            if e.szin == "orange":
                e.sety(e.ycor() - sebesseg * 2)
            else:
                e.sety(e.ycor() - sebesseg)

            # 2. lépés: különleges képességek
            if e.szin == "yellow":
                # A GYÁVA elfut a legközelebbi lézer elől
                if lezer.allapot == "lo" and abs(lezer.xcor() - e.xcor()) < 60:
                    if lezer.xcor() < e.xcor():
                        e.setx(e.xcor() + 2)  # Lézer balra van -> fuss jobbra
                    else:
                        e.setx(e.xcor() - 2)

            if e.szin == "purple":
                # A VADÁSZ lassan a játékos felé sodródik
                if jatekos.xcor() < e.xcor():
                    e.setx(e.xcor() - 1)
                else:
                    e.setx(e.xcor() + 1)

            if e.szin == "white":
                # A LÖVÉSZ néha (kb. 200-ból 1 körben) lő egyet
                if random.randint(1, 200) == 1:
                    gonosz_lezer(e.xcor(), e.ycor() - 15)

            # 3. lépés: ha leért az aljára, új ellenség jön fentről
            if e.ycor() < -290:
                uj_ellenseg_beallitas(e)

            # 4. lépés: ütközés a játékosokkal -> életvesztés
            if jatekos.distance(e) < 25 or (ketjatekos and jatekos2.distance(e) < 25):
                eletek -= 1
                tabla_frissit()
                uj_ellenseg_beallitas(e)

        # --- JÁTÉKOS LÉZEREK MOZGATÁSA ---
        for l in [lezer, lezer2]:
            if l.allapot == "lo":
                l.sety(l.ycor() + lezer_sebesseg)
                if l.ycor() > 290:
                    l.hideturtle()
                    l.allapot = "kesz"

            # Eltalált-e valamit ez a lézer?
            if l.allapot == "lo":
                for e in ellensegek:
                    if l.distance(e) < 20:
                        l.hideturtle()
                        l.allapot = "kesz"
                        e.hp -= 1
                        if e.hp <= 0:
                            pontszam += 10
                            uj_ellenseg_beallitas(e)
                        else:
                            # A zöld túlélte az első lövést: összemegy
                            pontszam += 5
                            e.shapesize(0.6, 0.6)
                        tabla_frissit()
                        break  # Egy lézer csak egy ellenséget találhat el

        # --- GONOSZ LÉZEREK MOZGATÁSA ---
        for gl in gonosz_lezerek[:]:  # A [:] másolat, mert közben törlünk
            gl.sety(gl.ycor() - 5)

            eltalalt = (jatekos.distance(gl) < 20 or
                        (ketjatekos and jatekos2.distance(gl) < 20))
            if eltalalt:
                eletek -= 1
                tabla_frissit()

            if eltalalt or gl.ycor() < -290:
                gl.hideturtle()
                gonosz_lezerek.remove(gl)

        # --- JÁTÉK VÉGE? ---
        if eletek <= 0:
            tabla.goto(0, 0)
            tabla.write("JÁTÉK VÉGE!  Pont: {}".format(pontszam),
                        align="center", font=("Courier", 24, "bold"))
            ablak.update()
            print("Vége a játéknak! Pontszám:", pontszam,
                  "- Túlélt idő:", int(eltelt_ido), "másodperc")
            time.sleep(3)
            break

    except (turtle.Terminator, Exception):
        print("Játék bezárva!")
        break
