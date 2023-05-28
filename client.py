from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация клиента")
        self.init_ui()

    def init_ui(self):
        self.lbl_last_name = QLabel("Фамилия:")
        self.edit_last_name = QLineEdit()

        self.lbl_first_name = QLabel("Имя:")
        self.edit_first_name = QLineEdit()

        self.lbl_patronymic = QLabel("Отчество:")
        self.edit_patronymic = QLineEdit()

        self.lbl_passport = QLabel("Паспортные данные:")
        self.edit_passport = QLineEdit()

        self.btn_register = QPushButton("Зарегистрировать")
        self.btn_register.clicked.connect(self.register_client)

        self.btn_exit = QPushButton("Завершить")
        self.btn_exit.clicked.connect(self.exit_program)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_last_name)
        layout.addWidget(self.edit_last_name)
        layout.addWidget(self.lbl_first_name)
        layout.addWidget(self.edit_first_name)
        layout.addWidget(self.lbl_patronymic)
        layout.addWidget(self.edit_patronymic)
        layout.addWidget(self.lbl_passport)
        layout.addWidget(self.edit_passport)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    def validate_name(self, name):
        if not name.isalpha():
            return False
        if not name.istitle():
            return False
        return True

    def validate_passport(self, passport):
        if not passport.isdigit() or len(passport) > 11:
            return False
        return True

    def register_client(self):
        last_name = self.edit_last_name.text()
        first_name = self.edit_first_name.text()
        patronymic = self.edit_patronymic.text()
        passport = self.edit_passport.text()

        # Проверка корректности фамилии
        if not self.validate_name(last_name):
            QMessageBox.critical(self, "Ошибка", "Некорректная фамилия!")
            return

        # Проверка корректности имени
        if not self.validate_name(first_name):
            QMessageBox.critical(self, "Ошибка", "Некорректное имя!")
            return

        # Проверка корректности отчества
        if not self.validate_name(patronymic):
            QMessageBox.critical(self, "Ошибка", "Некорректное отчество!")
            return

        # Проверка корректности паспортных данных
        if not self.validate_passport(passport):
            QMessageBox.critical(self, "Ошибка", "Некорректные паспортные данные!")
            return

        # Подключение к базе данных
        conn = sqlite3.connect('lombard.db')
        cursor = conn.cursor()

        # Создание таблицы "Клиенты", если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           last_name TEXT,
                           first_name TEXT,
                           patronymic TEXT,
                           passport TEXT)''')

        # Добавление нового клиента в базу данных
        cursor.execute("INSERT INTO clients (last_name, first_name, patronymic, passport) VALUES (?, ?, ?, ?)",
                       (last_name, first_name, patronymic, passport))

        # Сохранение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Клиент зарегистрирован!")

        # Очистка полей ввода после регистрации
        self.edit_last_name.clear()
        self.edit_first_name.clear()
        self.edit_patronymic.clear()
        self.edit_passport.clear()

    def exit_program(self):
        # Завершение программы
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())
