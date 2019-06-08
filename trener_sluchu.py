#IMPORTOWANIE BIBLIOTEK
import random
from logic import pitchList, intervalsDict, chordsList
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
    wysokoscStatPopr = db.Column(db.Integer, nullable=False, default=0)
    wysokoscStatBled = db.Column(db.Integer, nullable=False, default=0)
    interwalyStatPopr = db.Column(db.Integer, nullable=False, default=0)
    interwalyStatBled = db.Column(db.Integer, nullable=False, default=0)
    akordyStatPopr = db.Column(db.Integer, nullable=False, default=0)
    akordyStatBled = db.Column(db.Integer, nullable=False, default=0)

    #FUNKCJA WYSWIETLAJĄCA TABELE
    def __repr__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.id, self.login, self.haslo,
                                                self.wysokoscStatPopr, self.wysokoscStatBled, self.interwalyStatPopr,
                                                self.interwalyStatBled, self.akordyStatPopr, self.akordyStatBled)

@app.route('/', methods=['GET', 'POST'])
def start():
    #INICJOWANIE SESJI
    if session:
        pass
    else:
        session['uid'] = random.randint(0, 1000)
        session['username'] = None

    if request.get_json() is not None:
        session['sprawdzenie'] = None  #USTAWIENIE ODPOWIEDZI SERWERA NA NONE ABY NIE ZOSTAWALA PO DZIALANIACH UZYTKOWNIKA
        #WYBÓR TRYBU GRY
        if request.get_json().get('game_mode') is not None:
            session['game_mode'] = request.get_json().get('game_mode')
            #MECHANIZM ODGRYWANIA DŹWIEKÓW DLA ODPOWIEDNICH TRYBOW GRY
            if session['game_mode'] == 'wysokosc':
                session['dzwiekA'], session['dzwiekB'] = pitchList.pitch_generator(random.randint(0, 35), random.randint(0, 35))
                session['odpowiedzi'] = ['Nizej', 'Rowny', 'Wyzej']

            if session['game_mode'] == 'interwaly':
                session['odpowiedzi'] = []  # USTAWIENIE PUSTEJ LISTY Z ODPOWIEDZIAMI
                correctAnswer, session['odpowiedzi'] = intervalsDict.answer_generator(intervalsDict.generate_inverals(random.randint(12, 23)), session['odpowiedzi'])
                session['dzwiekA'], session['dzwiekB'] = correctAnswer[1][0][1], correctAnswer[1][1][1]#[nazwa interwalu][nazwy nut][czestotliwosci]
                session['poprawnyInterwal'] = correctAnswer[0]

            if session['game_mode'] == 'akordy':
                session['akord'] = chordsList.chord_generator(random.randint(0, 16))
                session['odpowiedzi'] = ['mollowy', 'Durowy']

        #MECHANIZM SPRAWDZANIA ODPOWIEDZI I EDYCJI STATYSTYK W BAZIE DANYCH
        if request.get_json().get('response') is not None:
            #DLA WYSOKOSCI
            if session['game_mode'] == 'wysokosc':
                if ((session['dzwiekA'] < session['dzwiekB'] and request.get_json().get('response') == 'Wyzej') or
                            (session['dzwiekA'] == session['dzwiekB'] and request.get_json().get('response') == 'Rowny') or
                            (session['dzwiekA'] > session['dzwiekB'] and request.get_json().get('response') == 'Nizej')):
                        session['sprawdzenie'] = 'Dobrze!'
                        #POWTORZENIE MECHANIZMU TWORZENIA DZWIEKOW
                        session['dzwiekA'], session['dzwiekB'] = pitchList.pitch_generator(random.randint(0, 35), random.randint(0, 35))
                else:
                        session['sprawdzenie'] = 'Źle!'
                #EDYCJA STATYSTYK
                if session['username'] is not None:
                    if session['sprawdzenie'] == 'Dobrze!': session['wysokoscStatPopr'] += 1
                    elif session['sprawdzenie'] == 'Źle!': session['wysokoscStatBled'] += 1
                    db.session.commit()
            #DLA INTERWALOW
            if session['game_mode'] == 'interwaly':
                if session['poprawnyInterwal'] == request.get_json().get('response'):
                    session['sprawdzenie'] = 'Dobrze!'
                    #POWTORZENIE MECHANIZMU TWORZENIA DZWIEKOW
                    session['odpowiedzi'] = []
                    correctAnswer, session['odpowiedzi'] = intervalsDict.answer_generator(intervalsDict.generate_inverals(random.randint(12, 23)), session['odpowiedzi'])
                    session['dzwiekA'], session['dzwiekB'] = correctAnswer[1][0][1], correctAnswer[1][1][1] #[nazwa interwalu][nazwy nut][czestotliwosci]
                    session['poprawnyInterwal'] = correctAnswer[0]
                else:
                    session['sprawdzenie'] = 'Źle!'
                #EDYCJA STATYSTYK
                if session['username'] is not None:
                    if session['sprawdzenie'] == 'Dobrze!': session['interwalyStatPopr'] += 1
                    elif session['sprawdzenie'] == 'Źle!': session['interwalyStatBled'] += 1
                    db.session.commit()
            #DLA AKORDOW
            if session['game_mode'] == 'akordy':
                if (request.get_json().get('response') == 'mollowy' and (session['akord'].strip()[-1] == 'm')) or (
                        request.get_json().get('response') == 'Durowy' and (session['akord'].strip()[-1] != 'm')):
                    session['sprawdzenie'] = 'Dobrze!'
                    session['akord'] = chordsList.chord_generator(random.randint(0, 16))
                else:
                    session['sprawdzenie'] = 'Źle!'
                #EDYCJA STATYSTYK
                if session['username'] is not None:
                    if session['sprawdzenie'] == 'Dobrze!': session['akordyStatPopr'] += 1
                    elif session['sprawdzenie'] == 'Źle!': session['akordyStatBled'] += 1
                    db.session.commit()
        #RESETOWANIE STATYSTYK
        if request.get_json().get('reset') is not None:
            if session['game_mode'] == 'wysokosc': session['wysokoscStatPopr']  = session['wysokoscStatBled'] = 0
            elif session['game_mode'] == 'interwaly': session['interwalyStatPopr'] = session['interwalyStatBled'] = 0
            elif session['game_mode'] == 'akordy':    session['akordyStatPopr'] = session['akordyStatBled'] = 0
            db.session.commit()
        #MECHANIZM WYLOGOWYWANIA
        if request.get_json().get('logout') is not None:
                session.clear()
    return render_template("home.jinja2")

#REJESTRACJA
@app.route("/register", methods=["GET", "POST"])
def reg():
    error = None
    if request.method == "POST":
        uname = request.form['uname']
        passw = request.form['passw']
        passwConf = request.form["passwConf"]

        #ZABEZPIECZENIA
        if passw == passwConf:
            if (uname == '') or (passw == ''):
                    error = "Musisz wypełnić wszystkie pola!"
            elif len(uname) >= 20 or len(passw) >= 20:
                    error = "Zbyt długi login lub hasło (musi być krótsze niż 20 znaków)!"
            elif len(uname) < 4 or len(passw) < 4:
                    error = "Zbyt krótki login lub hasło (minimum 4 znaki)!"
            else:   #REJESTRACJA POMYŚLNA
                    if Uzytkownik.query.filter_by(login=uname).first() is not None:
                        error = "Login jest już zajęty!"
                    else:#TWORZENIE ZMIENNYCH SESYJNYCH POBIERAJACYCH WARTOSCI Z BAZY DANYCH
                        db.session.add(Uzytkownik(login=uname, haslo=passw))
                        db.session.commit()
                        session['username'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().login
                        session['wysokoscStatPopr'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().wysokoscStatPopr
                        session['wysokoscStatBled'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().wysokoscStatBled
                        session['interwalyStatPopr'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().interwalyStatPopr
                        session['interwalyStatBled'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().interwalyStatBled
                        session['akordyStatPopr'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().akordyStatPopr
                        session['akordyStatBled'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().akordyStatBled
                        return redirect(url_for("start"))
        else:
            error = "Hasła się nie zgadzają"
    return render_template("register.jinja2", error=error)

#LOGOWANIE
@app.route("/login", methods=["GET", "POST"])
def log():
    error = None
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        #TWORZENIE ZMIENNYCH SESYJNYCH POBRANIERAJACYCH WARTOSCI Z BAZY DANYCH
        if Uzytkownik.query.filter_by(login=uname, haslo=passw).first() is not None:
            session['username'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().login
            session['wysokoscStatPopr'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().wysokoscStatPopr
            session['wysokoscStatBled'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().wysokoscStatBled
            session['interwalyStatPopr'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().interwalyStatPopr
            session['interwalyStatBled'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().interwalyStatBled
            session['akordyStatPopr'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().akordyStatPopr
            session['akordyStatBled'] = Uzytkownik.query.filter(Uzytkownik.login == uname).first().akordyStatBled
            return redirect(url_for("start"))

        #ZABEZPIECZENIA
        elif Uzytkownik.query.filter_by(login=uname, haslo=passw).first() is None:
            if Uzytkownik.query.filter_by(login=uname, haslo=passw).first() is not None:
                error = "Błędne hasło"
            else:
                error = "Nie ma takiego użytkownika!"
    return render_template("login.jinja2", error=error)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=55101)