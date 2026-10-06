import turtle
import random
import time  # <-- ÚJ: Ezt be kell importálni az időzítéshez!

# 1. Képernyő (Az űr) beállítása
ablak = turtle.Screen()
ablak.bgcolor("black")
ablak.title("Űrhajós Kaland!")
ablak.setup(width=600, height=600)
ablak.tracer(0) # Folyamatos animációhoz

# 2. Játékos (Űrhajó)
jatekos = turtle.Turtle()
jatekos.color("cyan")
jatekos.shape("triangle")
jatekos.penup() # Ne húzzon vonalat
jatekos.setheading(90) # Felfelé néz
jatekos.goto(0, -250)

# 3. Ellenség (Meteor)
ellenseg = turtle.Turtle()
ellenseg.color("red")
ellenseg.shape("circle")
ellenseg.penup()
ellenseg.goto(0, 250)
ellenseg_sebesseg = 3

# 4. Lézer
lezer = turtle.Turtle()
lezer.color("yellow")
lezer.shape("square")
lezer.shapesize(stretch_wid=0.2, stretch_len=1) # Kicsi csíkká alakítjuk
lezer.penup()
lezer.setheading(90)
lezer.hideturtle() # Kezdetben el van rejtve
lezer_allapot = "kesz" # A lézer állapota ("kesz" = lőhetünk, "lo" = repül)
lezer_sebesseg = 7

# --- MOZGÁS FÜGGVÉNYEK ---

def balra():
    x = jatekos.xcor()
    if x > -280: # Ne menjen le a képernyőről
        x -= 20
    jatekos.setx(x)

def jobbra():
    x = jatekos.xcor()
    if x < 280:
        x += 20
    jatekos.setx(x)

def loves():
    global lezer_allapot
    # Csak akkor lőhetünk, ha a lézer épp nem repül
    if lezer_allapot == "kesz":
        lezer_allapot = "lo"
        # A lézer a játékos orrához ugrik
        lezer.goto(jatekos.xcor(), jatekos.ycor() + 10)
        lezer.showturtle()

# --- IRÁNYÍTÁS BEÁLLÍTÁSA ---
ablak.listen() # Figyeljük a billentyűzetet
ablak.onkeypress(balra, "Left")
ablak.onkeypress(jobbra, "Right")
ablak.onkeypress(loves, "space")

# --- FŐ JÁTÉKCIKLUS ---
while True:
    try:
        ablak.update() # Képernyő frissítése minden körben
        
        time.sleep(0.01) # <-- ÚJ: Ez a sor lassítja le a játékot normális sebességre (10ms szünet)

        # Meteor mozgatása lefelé
        y = ellenseg.ycor()
        y -= ellenseg_sebesseg
        ellenseg.sety(y)

        # Ha a meteor leér az aljára, újraindul fentről
        if ellenseg.ycor() < -290:
            x = random.randint(-280, 280) # Véletlenszerű X koordináta
            ellenseg.goto(x, 250)

        # Lézer mozgatása felfelé
        if lezer_allapot == "lo":
            y = lezer.ycor()
            y += lezer_sebesseg
            lezer.sety(y)

        # Ha a lézer kimegy a képernyőről felül
        if lezer.ycor() > 290:
            lezer.hideturtle()
            lezer_allapot = "kesz" # Újra lőhetünk

        # ÜTKÖZÉS: Eltalálta a lézer a meteort?
        if lezer.distance(ellenseg) < 20:
            lezer.hideturtle()
            lezer_allapot = "kesz" # Lézer újra töltve
            # Meteor robban (visszaugrik a tetejére)
            x = random.randint(-280, 280)
            ellenseg.goto(x, 250)
            
        # --- ÚJ RÉSZ: ÜTKÖZÉS A JÁTÉKOS ÉS A METEOR KÖZÖTT ---
        if jatekos.distance(ellenseg) < 20:
            print("Vége a játéknak! A meteor eltalálta az űrhajót.")
            break # Ezzel megszakítjuk a végtelen ciklust, és a játék leáll.
            
    except Exception:
        # Ha a játékos bezárja az ablakot, a ciklus leáll hibaüzenet nélkül
        print("Játék bezárva!")
        break