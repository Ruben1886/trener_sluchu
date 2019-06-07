import random

pitchList = [
        ["C3", 130.81],  # 0 C3 NUMBER OF ELEMENT IN THIS LIST
        ["C#3", 138.59],  # 1 C#3
        ["D3", 146.83],  # 2 D3
        ["D#3", 155.56],  # 3 D#3
        ["E3", 164.81],  # 4 E3
        ["F3", 174.61],  # 5 F3
        ["F#3", 185.00],  # 6 F#3
        ["G3", 196.00],  # 7 G3
        ["G#3", 207.65],  # 8 G#3
        ["A3", 220.00],  # 9 A3
        ["A#3", 233.08],  # 10 A#3
        ["B3", 246.94],  # 11 B3
        ["C4", 261.63],  # 12 C4
        ["C#4", 277.18],  # 13 C#4
        ["D4", 293.66],  # 14 D4
        ["D#4", 311.13],  # 15 D#4
        ["E3", 329.63],  # 16 E4
        ["F4", 349.23],  # 17 F4
        ["F#4", 369.99],  # 18 F#4
        ["G4", 392.00],  # 19 G4
        ["G#4", 415.30],  # 20 G#4
        ["A4", 440.00],  # 21 A4
        ["A#4", 466.16],  # 22 A#4
        ["B4", 493.88],  # 23 B4
        ["C5", 523.25],  # 24 C5
        ["C#5", 554.37],  # 25 C#5
        ["D5", 587.33],  # 26 D5
        ["D#5", 622.25],  # 27 D#5
        ["E5", 659.26],  # 28 E5
        ["F5", 698.46],  # 29 F5
        ["F#5", 739.99],  # 30 F#5
        ["G5", 783.99],  # 31 G5
        ["G#5", 830.61],  # 32 G#5
        ["A5", 880.00],  # 33 A5
        ["A#5", 932.33],  # 34 A#5
        ["B5", 987.77]  # 35 B5
    ]

randomNote = random.randint(12,23)

intervals = {
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


def answersGen(invervals, answersList):
        x = 0
        while x < 3:
                if x == 0:
                        correct = random.choice(list(invervals.items()))
                        answersList.append(correct[0])

                y = random.choice(list(intervals))

                if y not in answersList:
                        answersList.append(y)

                x = x + 1

        random.shuffle(answersList)
        return correct, answersList
