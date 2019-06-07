#IMPORTOWANIE BIBLIOTEK
import random
from logic import pitchList, intervalList, chordList
from flask import Flask, session, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

#KONFIGURACJA APLIKACJI
app = Flask(__name__)
app.config['SECRET_KEY'] = '195ca1ceb0d831fe4d0140d7d3d0935b'

#KONFIGURACJA BAZY DANYCH SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#GŁÓWNA TABELA Z UŻYTKOWNIKAMI I STATYSTYKAMI
class Uzytkownik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    haslo = db.Column(db.String(20), nullable=False)
    wysokoscStat = db.Column(db.Integer, nullable=False, default=0)
    interwalyStat = db.Column(db.Integer, nullable=False, default=0)
    akordyStat = db.Column(db.Integer, nullable=False, default=0)

    #FUNKCJA WYSWIETLAJĄCA TABELE
    def __repr__(self):
        return '%s %s %s %s %s' % (self.login, self.haslo, self.wysokoscStat, self.interwalyStat, self.akordyStat)

@app.route('/', methods=['GET', 'POST'])
def start():
    if session:
        pass
    else:
        session['uid'] = random.randint(0,1000)
        session['username'] = None

    if request.get_json() is not None:
        #WYBÓR TRYBU GRY
        if request.get_json().get('game_mode') is not None:
            session['game_mode'] = request.get_json().get('game_mode')

            #MECHANIZM ODGRYWANIA DŹWIEKÓW
            if session['game_mode'] == 'wysokosc':
                    session['dzwiekA'], session['dzwiekB'] = pitchList.pitch_generator(random.randint(0, 35), random.randint(0, 35))
                    session['odpowiedzi'] = ['Nizej', 'Unison', 'Wyzej']

            if session['game_mode'] == 'akordy':
                session['akord'] = chordList.chord_generator(random.randint(0, 16))
                session['odpowiedzi'] = ['mollowy', 'Durowy']

            if session['game_mode'] == 'interwaly':
                pass

        #MECHANIZM SPRAWDZANIA ODPOWIEDZI
        if request.get_json().get('response') is not None:
                if session['game_mode'] == 'wysokosc':
                    if ((session['dzwiekA'] < session['dzwiekB'] and request.get_json().get('response') == 'Wyzej') or
                        (session['dzwiekA'] == session['dzwiekB'] and request.get_json().get('response') == 'Unison') or
                        (session['dzwiekA'] > session['dzwiekB'] and request.get_json().get('response') == 'Nizej')):

                            session['sprawdzenie'] = 'Dobrze!'
                            session['dzwiekA'], session['dzwiekB'] = pitchList.pitch_generator(random.randint(0, 35),
                                                                                               random.randint(0, 35))
                    else:
                            session['sprawdzenie'] = 'Źle!'

                    if session['username'] is not None:
                        if session['sprawdzenie'] == 'Dobrze!': session['wysokoscStat'] += 1
                        elif session['sprawdzenie'] == 'Źle': session['wysokoscStat'] -= 1
                        db.session.commit()

                if session['game_mode'] == 'interwaly':
                    pass

                if session['game_mode'] == 'akordy':
                    if (request.get_json().get('response') == 'mollowy' and (session['akord'].strip()[-1] == 'm')) or (
                        request.get_json().get('response')== 'Durowy' and (session['akord'].strip()[-1] != 'm')):

                            session['sprawdzenie'] = 'Dobrze!'
                            session['akord'] = chordList.chord_generator(random.randint(0, 16))
                    else:
                            session['sprawdzenie'] = 'Źle!'

                    if session['username'] is not None:
                        if session['sprawdzenie'] == 'Dobrze!': session['akordyStat'] += 1
                        elif session['sprawdzenie'] == 'Źle': session['akordyStat'] -= 1
                        db.session.commit()

        #RESETOWANIE STATYSTYK
        if request.get_json().get('reset') is not None:
            if session['game_mode'] == 'wysokosc': session['wysokoscStat'] = 0
            elif session['game_mode'] == 'interwaly': session['interwalyStat'] = 0
            elif session['game_mode'] == 'akordy':    session['akordyStat'] = 0
            db.session.commit()

        #MECHANIZM WYLOGOWYWANIA
        if request.get_json().get('logout') is not None:
                session.clear()


    #MECHANIZM SPRAWDZANIA ODPOWIEDZI I EDYCJI STATYSTYK

    return render_template("home.jinja2")

#REJESTRACJA
@app.route("/register", methods=["GET", "POST"])
def reg():
    error = None
    if request.method == "POST":
        uname = request.form['uname']
        passw = request.form['passw']

        if (uname == '') or (passw == ''):
                error = "Musisz wypełnić wszystkie pola!"
        elif len(uname) >= 20 or len(passw) >= 20:
                error = "Zbyt długi login lub hasło (musi być krótsze niż 20 znaków)!"
        elif len(uname) < 4 or len(passw) < 4:
                error = "Zbyt krótki login lub hasło (minimum 4 znaki)!"
        else:
                if Uzytkownik.query.filter_by(login=uname).first() is not None:
                    error = "Login jest już zajęty!"
                else:
                    db.session.add(Uzytkownik(login=uname, haslo=passw))
                    db.session.commit()
                    session['username'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().login
                    session['wysokoscStat'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().wysokoscStat
                    session['interwalyStat'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().interwalyStat
                    session['akordyStat'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().akordyStat
                    return redirect(url_for("start"))
    return render_template("register.jinja2", error=error)

#LOGOWANIE
@app.route("/login", methods=["GET", "POST"])
def log():
    error = None
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        if Uzytkownik.query.filter_by(login=uname, haslo=passw).first() is not None:
            session['username'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().login
            session['wysokoscStat'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().wysokoscStat
            session['interwalyStat'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().interwalyStat
            session['akordyStat'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().akordyStat
            return redirect(url_for("start"))

        elif Uzytkownik.query.filter_by(login=uname, haslo=passw).first() is None:
            if Uzytkownik.query.filter_by(login=uname, haslo=passw).first() is not None:
                error = "Błędne hasło"
            else:
                error = "Nie ma takiego użytkownika"
    return render_template("login.jinja2", error=error)

if __name__ == '__main__':
    app.run()
    #app.run(debug=False, host='0.0.0.0', port=55101)