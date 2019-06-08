import random
from logic.pitchList import pitchList

def generate_inverals(randomNote):
        intervalsDict = {
                "Oktawa (w dół)": [pitchList[randomNote], pitchList[randomNote - 12]],
                "Septyma wielka (w dół)": [pitchList[randomNote], pitchList[randomNote - 11]],
                "Septyma mała (w dół)": [pitchList[randomNote], pitchList[randomNote - 10]],
                "Seksta wielka (w dół)": [pitchList[randomNote], pitchList[randomNote - 9]],
                "Seksta mala (w dół)": [pitchList[randomNote], pitchList[randomNote - 8]],
                "Kwinta czysta (w dół)": [pitchList[randomNote], pitchList[randomNote - 7]],
                "Tryton (w dół)": [pitchList[randomNote], pitchList[randomNote - 6]],
                "Kwarta czysta (w dół)": [pitchList[randomNote], pitchList[randomNote - 5]],
                "Tercja wielka (w dół) ": [pitchList[randomNote], pitchList[randomNote - 4]],
                "Tercja mała (w dół)": [pitchList[randomNote], pitchList[randomNote - 3]],
                "Sekunda wielka (w dół)": [pitchList[randomNote], pitchList[randomNote - 2]],
                "Sekunda mała (w dół)": [pitchList[randomNote], pitchList[randomNote - 1]],

                "Unison": [pitchList[randomNote], pitchList[randomNote]],

                "Sekunda mała (w góre)": [pitchList[randomNote], pitchList[randomNote + 1]],
                "Sekunda Wielka (w góre)": [pitchList[randomNote], pitchList[randomNote + 2]],
                "Tercja mała (w góre)": [pitchList[randomNote], pitchList[randomNote + 3]],
                "Tercja wielka (w góre)": [pitchList[randomNote], pitchList[randomNote + 4]],
                "Kwinta czysta (w góre)": [pitchList[randomNote], pitchList[randomNote + 5]],
                "Tryton (w góre)": [pitchList[randomNote], pitchList[randomNote + 6]],
                "Kwarta czysta (w góre)": [pitchList[randomNote], pitchList[randomNote + 7]],
                "Seksta mała (w góre)": [pitchList[randomNote], pitchList[randomNote + 8]],
                "Seksta wielka (w góre)": [pitchList[randomNote], pitchList[randomNote + 9]],
                "Septyma mała (w góre)": [pitchList[randomNote], pitchList[randomNote + 10]],
                "Septyma wielka (w góre)": [pitchList[randomNote], pitchList[randomNote + 11]],
                "Oktawa (w góre)": [pitchList[randomNote], pitchList[randomNote + 12]]
        }
        return intervalsDict

def answer_generator(intervals, answersList):
# FUNKCJA TWORZY LISTE CORRECT[] Z NAZWĄ INTERWAŁÓW, NAZWAMI NUT, CZĘSTOTLIWOSCIAMI
# TWORZY TEŻ LISTE CZTERECH !ODPOWIEDZI Z JEDNĄ POPRAWNĄ(CORRECT[0) A NASTĘPNIE JĄ PRZETASOWUJE
        x = 0
        while x < 3:
                if x == 0:
                        correct = random.choice(list(intervals.items()))
                        answersList.append(correct[0])
                y = random.choice(list(intervals))

                if y not in answersList:
                        answersList.append(y)
                        x += 1
                elif y in answersList and x != 0:
                        x -= 1

        random.shuffle(answersList)
        return correct, answersList