import turtle
import time

# ============================================================
#  PONG
#  Két ütő, egy labda, aki 10 pontig ér el, az nyer!
#  Bal oldali ütőt Te irányítod (W = fel, S = le)
#  Jobb oldali ütőt a GÉP irányítja (követi a labdát)
# ============================================================

# 1. Képernyő beállítása
ablak = turtle.Screen()
ablak.bgcolor("black")
ablak.title("Pong!")
ablak.setup(width=700, height=500)
ablak.tracer(0)  # Folyamatos animációhoz kell


# 2. Bal oldali ütő (Te irányítod)
bal_uto = turtle.Turtle()
bal_uto.speed(0)
bal_uto.shape("square")
bal_uto.color("cyan")
bal_uto.shapesize(stretch_wid=3, stretch_len=0.5)  # Hosszú, keskeny ütő
bal_uto.penup()
bal_uto.goto(-300, 0)


# 3. Jobb oldali ütő (a gép irányítja)
jobb_uto = turtle.Turtle()
jobb_uto.speed(0)
jobb_uto.shape("square")
jobb_uto.color("orange")
jobb_uto.shapesize(stretch_wid=3, stretch_len=0.5)
jobb_uto.penup()
jobb_uto.goto(300, 0)


# 4. Labda
labda = turtle.Turtle()
labda.speed(0)
labda.shape("circle")
labda.color("white")
labda.penup()
labda.goto(0, 0)

# A labda ennyit mozog vízszintesen és függőlegesen minden körben
labda_dx = 3
labda_dy = 3


# 5. Pontszámok kiírása
pontok = turtle.Turtle()
pontok.speed(0)
pontok.color("white")
pontok.penup()
pontok.hideturtle()
pontok.goto(0, 210)

bal_pont = 0
jobb_pont = 0


def pontok_frissit():
    pontok.clear()
    szoveg = "{}   :   {}".format(bal_pont, jobb_pont)
    pontok.write(szoveg, align="center", font=("Courier", 24, "normal"))


pontok_frissit()


# ============================================================
#  IRÁNYÍTÁS - a Te ütőd
# ============================================================

def bal_fel():
    # Ha még nem ért a tábla tetejéig, mehet feljebb
    if bal_uto.ycor() < 200:
        bal_uto.sety(bal_uto.ycor() + 20)


def bal_le():
    # Ha még nem ért a tábla aljáig, mehet lejjebb
    if bal_uto.ycor() > -200:
        bal_uto.sety(bal_uto.ycor() - 20)


ablak.listen()
ablak.onkeypress(bal_fel, "w")
ablak.onkeypress(bal_le, "s")


# ============================================================
#  FŐ JÁTÉKCIKLUS
# ============================================================
while True:

    ablak.update()
    time.sleep(0.015)  # Ez fékezi le a játékot - enélkül gyors gépen követhetetlen lenne

    # --- LABDA MOZGATÁSA ---
    labda.setx(labda.xcor() + labda_dx)
    labda.sety(labda.ycor() + labda_dy)

    # --- ÜTKÖZÉS A FELSŐ ÉS ALSÓ FALLAL ---
    # Ha eléri a tábla tetejét vagy alját, visszapattan (megfordul dy)
    if labda.ycor() > 240:
        labda.sety(240)
        labda_dy *= -1

    if labda.ycor() < -240:
        labda.sety(-240)
        labda_dy *= -1

    # --- HA VALAKI GÓLT KAPOTT ---
    # Ha a labda kimegy a jobb oldalon -> Te szerzel pontot
    if labda.xcor() > 350:
        labda.goto(0, 0)
        labda_dx *= -1
        bal_pont += 1
        pontok_frissit()

    # Ha a labda kimegy a bal oldalon -> a gép szerez pontot
    if labda.xcor() < -350:
        labda.goto(0, 0)
        labda_dx *= -1
        jobb_pont += 1
        pontok_frissit()

    # --- ÜTKÖZÉS AZ ÜTŐKKEL ---
    # A distance() megmondja, milyen messze van egymástól két teknős.
    # Ha ez kicsi, akkor "összeértek", tehát eltalálta az ütőt.

    if labda.distance(bal_uto) < 50 and labda.xcor() < -280:
        labda.setx(-280)  # Ne ragadjon bele az ütőbe
        labda_dx *= -1

    if labda.distance(jobb_uto) < 50 and labda.xcor() > 280:
        labda.setx(280)
        labda_dx *= -1

    # --- EGYSZERŰ "MESTERSÉGES INTELLIGENCIA" ---
    # A gép ütője egyszerűen követi a labda magasságát.
    # Ha a labda feljebb van, mint az ütő -> ütő megy fel.
    # Ha lejjebb van -> ütő megy le.
    # (Ha ugyanolyan sebességgel követné, sosem hibázna,
    #  ezért csak lassan, kicsit "esetlenül" mozog - így van esélyed nyerni!)

    # Csak akkor mozogjon, ha nem lépné túl a pálya szélét
    if jobb_uto.ycor() < labda.ycor() and jobb_uto.ycor() < 200:
        jobb_uto.sety(jobb_uto.ycor() + 2)

    if jobb_uto.ycor() > labda.ycor() and jobb_uto.ycor() > -200:
        jobb_uto.sety(jobb_uto.ycor() - 2)

    # --- JÁTÉK VÉGE, HA VALAKI ELÉRTE A 10 PONTOT ---
    if bal_pont == 10 or jobb_pont == 10:
        pontok.goto(0, 0)
        if bal_pont == 10:
            pontok.write("NYERTÉL!", align="center", font=("Courier", 30, "bold"))
        else:
            pontok.write("A GÉP NYERT!", align="center", font=("Courier", 30, "bold"))
        break