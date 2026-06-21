from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "rpg_secret_key"


@app.route("/", methods=["GET", "POST"])
def home():
    postava = session.get("postava")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            meno = request.form["meno"]
            pohlavie = request.form["pohlavie"]

            vzacnost = random.choice(["Obyčajná", "Vzácna", "Epická", "Legendárna"])

            farba_vzacnosti = {
                "Obyčajná": "#ffffff",
                "Vzácna": "#00aaff",
                "Epická": "#cc00ff",
                "Legendárna": "#ff9900"
            }[vzacnost]

            level = random.randint(1, 50)
            sila = level + random.randint(20, 50)
            obratnost = level + random.randint(20, 50)
            inteligencia = level + random.randint(20, 50)

            trieda = random.choice(["Bojovník", "Mág", "Lukostrelec", "Assassin", "Alchymista"])

            if trieda == "Bojovník":
                sila += 20
            elif trieda == "Mág":
                inteligencia += 20
            elif trieda == "Lukostrelec":
                obratnost += 20
            elif trieda == "Assassin":
                obratnost += 15
                sila += 10
            elif trieda == "Alchymista":
                inteligencia += 10

            if level <= 10:
                hodnost = "Nováčik"
            elif level <= 20:
                hodnost = "Dobrodruh"
            elif level <= 30:
                hodnost = "Hrdina"
            elif level <= 40:
                hodnost = "Majster"
            else:
                hodnost = "Legenda"

            pribeh = f"{meno} je {vzacnost.lower()} postava. Pochádza z tajomného sveta, kde bojuje ako odvážny hrdina."

            postava = {
                "meno": meno,
                "pohlavie": pohlavie,
                "level": level,
                "hodnost": hodnost,
                "zlato": random.randint(50, 500),
                "xp": random.randint(0, 100),
                "vitazstva": 0,
                "hra_skoncila": False,
                "hp": random.randint(80, 150),
                "max_hp": 150,
                "rasa": random.choice(["Človek", "Elf", "Démon", "Anjel", "Kitsune"]),
                "trieda": trieda,
                "zbran": random.choice(["Meč", "Luk", "Magická palica", "Dýka", "Kniha kúziel"]),
                "vzacnost": vzacnost,
                "monster": None,
                "monster_hp": 0,
                "monster_utok": 0,
                "utok_hrdinu": 0,
                "obrana_hrdinu": 0,
                "vysledok_boja": None,
                "farba_vzacnosti": farba_vzacnosti,
                "sila": sila,
                "obratnost": obratnost,
                "inteligencia": inteligencia,
                "pribeh": pribeh,
                "inventar": random.sample([
                    "🧪 Liečivý elixír",
                    "💎 Magický kryštál",
                    "📜 Starý zvitok",
                    "🔑 Starý kľúč",
                    "🪙 Strieborná minca",
                    "🏹 Šíp",
                    "🛡️ Malý štít"
                ], 3),
                "obrazok": random.choice(["🧙", "🧝", "👸", "🐉", "⚔️", "👑"]),
                "monster": None,
                "monster_hp": 0,
                "monster_utok": 0,
                "vysledok_boja": None,
                "utok_hrdinu": 0,
                "obrana_hrdinu": 0
            }

        if action in ["attack", "defend", "heal", "run"] and postava:
            monster = postava.get("monster")

            if monster is None:
                monster = random.choice(["Goblin", "Ork", "Temný vlk", "Kostlivec", "Drak"])
            monster_hp = postava.get("monster_hp", 0)
            monster_utok = postava.get("monster_utok", 0)

            if monster_hp <= 0:
                monster_hp = random.randint(60, 130)
                monster_utok = random.randint(8, 25)

            utok_hrdinu = 0
            obrana_hrdinu = 0

            if action == "attack":
                utok_hrdinu = random.randint(10, 40) + postava["sila"] // 10

                if utok_hrdinu > monster_utok:
                    damage = utok_hrdinu - monster_utok
                    monster_hp -= damage

                    vysledok_boja = f"⚔️ Zasiahol si nepriateľa za {damage} HP"

                    if monster_hp <= 0:
                        vysledok_boja = "🏆 Nepriateľ porazený!"
                        postava["vitazstva"] = postava.get("vitazstva", 0) + 1

                        if postava["vitazstva"] >= 5:
                            vysledok_boja = "👑 Vyhral si celú hru!"
                            postava["hra_skoncila"] = True
                        postava["zlato"] += random.randint(20, 80)
                        postava["xp"] += random.randint(10, 30)

                        monster = None
                        monster_hp = 0
                        monster_utok = 0
                else:
                    vysledok_boja = "⚔️ Výmena úderov"
                    postava["hp"] -= random.randint(5, 15)

            if action == "defend":
                obrana_hrdinu = random.randint(20, 50)
                vysledok_boja = "🛡️ Obrana"
                postava["hp"] += random.randint(5, 15)

            if action == "heal":
                liecenie = random.randint(15, 40)
                postava["hp"] += liecenie
                if postava["hp"] > postava["max_hp"]:
                    postava["hp"] = postava["max_hp"]

                vysledok_boja = f"🧪 Liečenie +{liecenie} HP"

            if action == "run":
                vysledok_boja = "🏃 Útek"

            if postava["xp"] >= 100:
                postava["level"] += 1
                postava["xp"] -= 100

            if postava["hp"] < 0:
                postava["hp"] = 0
            if postava["hp"] <= 0:
                vysledok_boja = "💀 Hrdina zomrel!"
                postava["hra_skoncila"] = True

            postava["monster"] = monster
            postava["monster_hp"] = monster_hp
            postava["monster_utok"] = monster_utok
            postava["utok_hrdinu"] = utok_hrdinu
            postava["obrana_hrdinu"] = obrana_hrdinu
            postava["vysledok_boja"] = vysledok_boja

        session["postava"] = postava

    return render_template("index.html", postava=postava)


if __name__ == "__main__":
    app.run(debug=True)