# -*- coding: utf-8 -*-

import random
import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *


def check(s, ans):
    bulls = 0
    cows = 0

    for i in range(4):
        bulls += (s[i] == ans[i])

    for i in range(4):
        for j in range(4):
            cows += (s[i] == ans[j])

    cows -= bulls

    return bulls, cows


# ------------------------------------------------------------------------------


class ReverseGame(QObject):
    r_incorrect_value = Signal()
    r_incorrect_input = Signal()
    r_question = Signal()
    r_win = Signal()

    def start_over(self):

        self.status = 'Playing'
        self.m = []
        for n in range(1000, 9999):
            s = str(n)
            correct = True
            for i in range(4):
                for j in range(i + 1, 4):
                    if s[i] == s[j]:
                        correct = False
            if correct:
                self.m.append(s)

        self.m_full = self.m.copy()
        self.value = '1234'

    def __init__(self):

        QObject.__init__(self)
        self.start_over()

    def process_result(self, bulls, cows):

        if bulls + cows > 4:

            self.r_incorrect_input.emit()

        else:

            number = self.value

            m = []
            for ans in self.m:
                if check(number, ans) == (bulls, cows):
                    m.append(ans)
            self.m = m.copy()

            if len(m) == 0:
                self.status = 'Error'
                self.r_incorrect_value.emit()
            elif bulls == 4:
                self.status = 'Won'
                self.r_win.emit()
            else:
                number = ''
                if len(m) <= 1000:
                    min_max_left = 10000
                    for n in m:
                        d = dict()
                        for number2 in m:
                            res = check(number2, n)
                            if res not in d:
                                d[res] = 1
                            else:
                                d[res] += 1
                        max_left = 0
                        for key in d:
                            max_left = max(max_left, d[key])
                        if max_left < min_max_left:
                            min_max_left = max_left
                            number = n
                else:
                    ind = random.randint(0, len(m))
                    number = m[ind]

                self.value = number

                if reverse_game.status == 'Playing':
                    self.r_question.emit()

                # ------------------------------------------------------------------------------


def check_correctness(a):
    if not a.isdigit():
        return False

    if len(a) != 4:
        return False

    if a[0] == '0':
        return False

    for i in range(4):
        for j in range(i + 1, 4):
            if a[i] == a[j]:
                return False
    return True


# ------------------------------------------------------------------------------


class Game(QObject):
    incorrect_value = Signal(str)
    result = Signal(tuple)
    win = Signal()

    def set_data(self):
        a = ''
        while not check_correctness(a):
            a = str(random.randint(1000, 9999))
        self.data = a

        self.last_checked_value = ''
        self.tries = 0

    def __init__(self):

        QObject.__init__(self)

        self.data = ''
        self.value = ''
        self.last_checked_value = ''
        self.tries = 0

    def set_value(self, value):
        self.value = value

    def check_value(self):
        if not check_correctness(self.value):
            self.result.emit((self.value, None))
        else:

            if self.value != self.last_checked_value:
                self.tries += 1
                self.last_checked_value = self.value

            oxes = 0
            cows = 0
            for i in range(4):
                oxes += (self.data[i] == self.value[i])

            for i in range(4):
                for j in range(4):
                    cows += (self.data[i] == self.value[j])

            cows -= oxes
            if oxes == 4:
                self.win.emit()
            else:
                self.result.emit((oxes, cows))


# ------------------------------------------------------------------------------


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Быки и коровы')
window.resize(1000, 1000)

line = QLineEdit(window)
line.setGeometry(10, 210, 200, 50)

label = QLabel("", window)
label.setGeometry(10, 300, 400, 200)

sendButton = QPushButton("Угадать", window)
sendButton.setGeometry(220, 210, 150, 50)

stopButton = QPushButton("Сдаться", window)
stopButton.setGeometry(380, 210, 150, 50)

tableButton = QPushButton("Таблица результатов", window)
tableButton.setGeometry(10, 10, 300, 50)

label_r = QLabel("", window)
label_r.setGeometry(10, 10, 1000, 100)

bulls = QSpinBox(window)
bulls.setMaximum(4)
bulls.setWindowTitle("bulls")
bulls.setGeometry(10, 120, 100, 50)

cows = QSpinBox(window)
cows.setMaximum(4)
cows.setWindowTitle("cows")
cows.setGeometry(120, 120, 100, 50)

send_r = QPushButton("Отправить", window)
send_r.setGeometry(230, 120, 150, 50)

new_game_button = QPushButton("Новая игра", window)
new_game_button.setGeometry(10, 210, 200, 50)

start_label = QLabel("Выберите режим игры", window)
start_label.setGeometry(10, 10, 300, 100)

mode1_button = QPushButton("Хочу угадывать", window)
mode1_button.setGeometry(10, 120, 300, 50)

mode2_button = QPushButton("Хочу загадывать", window)
mode2_button.setGeometry(320, 120, 300, 50)

# ------------------------------------------------------------------------------


game = Game()
reverse_game = ReverseGame()

try:
    results = open("results_table.txt", "r+")
except FileNotFoundError:
    results = open("results_table.txt", "x+")
results.close()


# ------------------------------------------------------------------------------


def show_table():
    f = open("results_table.txt", "r")
    s = f.read()
    f.close()

    msgBox = QMessageBox()
    msgBox.setText("Таблица лучших результатов:\n" + s)
    msgBox.exec()


def show_result(t):
    if t[1] is not None:

        oxes, cows = int(t[0]), int(t[1])

        oxes_name = 'бык'
        if oxes == 0:
            oxes_name += 'ов'
        elif oxes > 1:
            oxes_name += 'a'

        cows_name = 'коров'
        if cows == 1:
            cows_name += 'а'
        elif cows > 1:
            cows_name += 'ы'

        label.setText(str(oxes) + ' ' + oxes_name + ' и ' + str(cows) + ' ' + cows_name)

    else:
        label.setText('Некорректное значение')


def show_win():
    sendButton.setDisabled(True)
    stopButton.setText('Новая игра')
    label.setText('Победа!\nКоличество попыток: ' + str(game.tries))
    add_to_table()


def show_loose():
    sendButton.setDisabled(True)
    stopButton.setText('Новая игра')
    label.setText('Игра окончена.\nКоличество попыток: ' + str(game.tries) + '\nЗагаданное число: ' + str(
        game.data) + '\nВы были близки!')


def stop_button_pressed():
    if stopButton.text() == 'Сдаться':
        show_loose()
    else:
        start_game()


def add_to_table():
    global game
    global label

    result = game.tries

    f = open("results_table.txt", "r")
    m = f.readlines()
    f.close()

    for i in range(len(m)):
        ind = m[i].rfind(' ')
        name = m[i][: ind]
        res = int(m[i][ind + 1:])
        m[i] = (name, res)

    if len(m) < 5 or result < m[-1][1]:
        msgBox = QMessageBox()
        msgBox.setText("Вот это игра! Введите свое имя, чтобы попасть в таблицу результатов")
        msgBox.exec()
        name, status = QInputDialog.getText(None, "", "Введите свое имя")

        if status:
            m.append((name, result))
            m.sort(key=lambda n: n[1])
            if len(m) > 5:
                m.pop()

            s = ''
            for name, res in m:
                s += name + ' ' + str(res) + '\n'

            f = open("results_table.txt", "w")
            f.write(s)
            f.close()

            msgBox.setText("Таблица лучших результатов:\n" + s)
            msgBox.exec()


def send_button_pressed():
    global game
    if stopButton.text() == 'Сдаться':
        game.check_value()


# ------------------------------------------------------------------------------


def r_ask_question():
    global reverse_game
    label_r.setText("Сколько быков и коров в числе " + reverse_game.value + "?")


def r_process_results():
    global reverse_game
    global bulls
    global cows

    reverse_game.process_result(bulls.value(), cows.value())


def r_show_win():
    global reverse_game
    send_r.setDisabled(True)
    label_r.setText("Ура! Загаданное число - " + reverse_game.value)


def r_incorrect_value():
    global reverse_game
    send_r.setDisabled(True)
    bulls.setValue(0)
    cows.setValue(0)
    label_r.setText("Ваши ответы противоречивы!")


def r_incorrect_input():
    global reverse_game
    s = label_r.text()
    label_r.setText(s + '\n' + 'Введенные данные некорректны. Попробуйте еще раз')


# ------------------------------------------------------------------------------


def new_game():
    start_label.close()
    mode1_button.close()
    mode2_button.close()

    line.show()
    sendButton.show()
    stopButton.show()
    tableButton.show()
    label.show()

    global game
    stopButton.setText('Сдаться')
    sendButton.setEnabled(True)
    label.setText('')
    line.setText('')
    game.set_data()
    print(game.data)


def new_reverse_game():
    start_label.close()
    mode1_button.close()
    mode2_button.close()

    label_r.show()
    bulls.show()
    bulls.setValue(0)
    cows.show()
    cows.setValue(0)
    send_r.show()
    send_r.setEnabled(True)
    new_game_button.show()

    global reverse_game
    reverse_game.start_over()
    r_ask_question()


def start_game():
    line.close()
    sendButton.close()
    stopButton.close()
    tableButton.close()
    label.close()
    label_r.close()
    new_game_button.close()
    bulls.close()
    cows.close()
    send_r.close()

    start_label.show()
    mode1_button.show()
    mode2_button.show()


# ------------------------------------------------------------------------------


line.textChanged.connect(game.set_value)

sendButton.clicked.connect(send_button_pressed)
stopButton.clicked.connect(stop_button_pressed)
tableButton.clicked.connect(show_table)

game.result.connect(show_result)
game.win.connect(show_win)

reverse_game.r_question.connect(r_ask_question)
reverse_game.r_win.connect(r_show_win)
reverse_game.r_incorrect_value.connect(r_incorrect_value)
reverse_game.r_incorrect_input.connect(r_incorrect_input)

send_r.clicked.connect(r_process_results)
new_game_button.clicked.connect(start_game)

mode1_button.clicked.connect(new_game)
mode2_button.clicked.connect(new_reverse_game)

# ------------------------------------------------------------------------------


start_game()

# ------------------------------------------------------------------------------


window.show()
app.exec_()
