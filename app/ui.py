import math
import os
import sympy
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QAction, QHBoxLayout
from PyQt5.QtGui import QFontDatabase,QIcon
from PyQt5.QtCore import QFile, QTextStream, QThread, pyqtSignal
from .approximation import adaptive_simpsons


class CalculationThread(QThread):
    res_r = pyqtSignal(float)
    err = pyqtSignal(str)
    
    def __init__(self, func_str, a, b, e):
        super().__init__()
        self.func_str = func_str
        self.a = a
        self.b = b
        self.e = e
        self._is_running = True
    
    def run(self):
        try:
            if not self._is_running:
                return
            x = sympy.symbols('x')
            expr = sympy.sympify(self.func_str)
            f = sympy.lambdify(x, expr)
            result = adaptive_simpsons(f, self.a, self.b, self.e,100)
            if self._is_running:
                self.res_r.emit(result)
        except Exception as e:
            self.err.emit(str(e))
    def stop(self):
        self._is_running = False







class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приближённое вычисление определённых интегралов")


        #mainwindow
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setFixedSize(800,800)

        #менюшка
        self.menu_bar = self.menuBar()
        self.programs_menu = self.menu_bar.addMenu('Настройки')
        self.program1_action = QAction('Вычисление определённых интегралов', self)
        self.program2_action = QAction('Справка', self)
        self.program2_action.triggered.connect(self.show_help)
        self.programs_menu.addAction(self.program1_action)
        self.programs_menu.addAction(self.program2_action)




        #компарь
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        #лейблы и эдиторы
        self.func_label = QLabel("Введите функцию для интегрирования")
        self.func_input = QLineEdit()

        self.a_label = QLabel("Нижняя граница интегрирования a:")
        self.a_input = QLineEdit()

        self.b_label = QLabel("Верхняя граница интегрирования b:")
        self.b_input = QLineEdit()

        self.e_label = QLabel("Точность вычисления e:")
        self.e_input = QLineEdit()
        self.e_input.setText("0.001")
        

        #кнопки
        self.calc_button = QPushButton("Вычислить")
        self.calc_button.clicked.connect(self.calc)
        self.calc_button.move(300, 250)
        self.calc_button.resize(200, 40)
        button_layout.addWidget(self.calc_button)
  

        self.open_button = QPushButton('Открыть файл', self)
        self.open_button.move(300, 300)
        self.open_button.resize(200, 40)
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        self.clear_button = QPushButton('Очистить файл', self)
        self.clear_button.move(300, 350)
        self.clear_button.resize(200, 40)
        self.clear_button.clicked.connect(self.clear_file)
        button_layout.addWidget(self.clear_button)

        #результат
        self.result_label = QLabel("Результат интегрирования:")

        
        layout.addWidget(self.func_label)
        layout.addWidget(self.func_input)
        layout.addWidget(self.a_label)
        layout.addWidget(self.a_input)
        layout.addWidget(self.b_label)
        layout.addWidget(self.b_input)
        layout.addWidget(self.e_label)
        layout.addWidget(self.e_input)
        layout.addWidget(self.result_label)

        self.central_widget.setLayout(layout)

        #стили
        font_id = QFontDatabase.addApplicationFont("resources/fonts/Oswald.ttf")
        icon_calc = QIcon("resources/icons/icon1.svg")
        icon_open = QIcon("resources/icons/icon_open.svg")
        icon_del = QIcon("resources/icons/icon_del.svg")
        self.calc_button.setIcon(icon_calc)
        self.open_button.setIcon(icon_open)
        self.clear_button.setIcon(icon_del)
        self.load_styles()
        
    def show_help(self):
        help_message = QMessageBox()
        help_message.setWindowTitle('Справка')
        help_text = """
        <h3>Правила ввода функций:</h3>
        <ul>
        <li><b>Операторы:</b> +, -, *, /, ^ для возведения в степень.</li>
        <li><b>Переменная интегрирования:</b> Интегрирование идёт по переменной x!</li>
        <li><b>Функции:</b> поддерживаются стандартные математические функции:
            <ul>
                <li>sin(x), cos(x), tan(x)</li>
                <li>sinh(x), cosh(x), tanh(x)</li>
                <li>asin(x), acos(x), atan(x)</li>
                <li>asin(x), acos(x), atan(x), asinh(x), acosh(x)</li>
                <li>log(x), exp(x), log10(x),log2(x)</li>
                <li>sqrt(x) — квадратный корень</li>
                <li>abs(x) — модуль числа</li>
                <li> 
            </ul>
        </li>
        <li><b>Пример:</b> Ввод функции <i>sin(x) + log(x)^2</i></li>
        </ul>
        """
        help_message.setTextFormat(1) 
        help_message.setText(help_text)
        help_message.exec_()        

    def load_styles(self):
        file = QFile("resources/styles.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()

    def calc(self):
        try:
            self.result_label.setText(f"Ожидайте! Программа ведёт вычисления")
            func_str = self.func_input.text()
            if not func_str.strip():
                raise ValueError("Функция не может быть пустой.")
            x = sympy.symbols('x')
            expr = sympy.sympify(func_str)
            f = sympy.lambdify(x, expr)
            a = sympy.sympify(self.a_input.text())
            b = sympy.sympify(self.b_input.text())
            a, b = float(a), float(b)
            e = float(self.e_input.text())
            if (a==None or b == None):
                raise ValueError("Границы интегрирования не могут быть пустыми.")
            self.calc_thread = CalculationThread(func_str, a, b, e)
            self.calc_thread.res_r.connect(self.on_result)
            self.calc_thread.err.connect(self.on_error)
            self.calc_thread.start()
        except ValueError as ve:
            QMessageBox.critical(self, "Ошибка", f"Неверные числовые данные: {ve}")
        except Exception as error:
            QMessageBox.critical(self, "Ошибка", f"Неверные входные данные: {error}")
    def on_result(self, result):
        self.result_label.setText(f"Результат интегрирования: {result}")
        if self.calc_thread:
            self.calc_thread.stop()
            self.calc_thread.wait()

    def on_error(self, error):
        QMessageBox.critical(self, "Ошибка", f"Ошибка при вычислении: {error}")
        if self.calc_thread:
            self.calc_thread.stop()
            self.calc_thread.wait()

    def open_file(self):
        try:
            os.startfile('resources\logs.txt')
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось открыть файл: {e}')
    

    def clear_file(self):
        try:
            with open('resources\logs.txt', 'w') as file:
                file.write('')
            QMessageBox.information(self, 'Успешно', 'Лог файл очищен.')
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'Не удалось очистить файл: {e}')




