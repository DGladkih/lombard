from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class ItemValuationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оценка стоимости товара")
        self.init_ui()

    def init_ui(self):
        self.lbl_item_name = QLabel("Наименование товара:")
        self.edit_item_name = QLineEdit()

        self.lbl_item_description = QLabel("Описание товара:")
        self.edit_item_description = QLineEdit()

        self.lbl_market_value = QLabel("Рыночная стоимость:")
        self.edit_market_value = QLineEdit()

        self.btn_evaluate = QPushButton("Оценить")
        self.btn_evaluate.clicked.connect(self.evaluate_item)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_item_name)
        layout.addWidget(self.edit_item_name)
        layout.addWidget(self.lbl_item_description)
        layout.addWidget(self.edit_item_description)
        layout.addWidget(self.lbl_market_value)
        layout.addWidget(self.edit_market_value)
        layout.addWidget(self.btn_evaluate)

        self.setLayout(layout)

    def evaluate_item(self):
        item_name = self.edit_item_name.text()
        item_description = self.edit_item_description.text()
        market_value = self.edit_market_value.text()

        # Проверка наличия введенных данных
        if not item_name or not item_description or not market_value:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните все поля!")
            return

        try:
            market_value = float(market_value)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Некорректная рыночная стоимость!")
            return

        # Подключение к базе данных
        conn = sqlite3.connect('lombard.db')
        cursor = conn.cursor()

        # Создание таблицы "Товары", если она не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS items
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT,
                           description TEXT,
                           market_value REAL)''')

        # Добавление оценки товара в базу данных
        cursor.execute("INSERT INTO items (name, description, market_value) VALUES (?, ?, ?)",
                       (item_name, item_description, market_value))

        # Сохранение изменений и закрытие соединения с базой данных
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Оценка стоимости товара сохранена!")

        # Очистка полей ввода после оценки товара
        self.edit_item_name.clear()
        self.edit_item_description.clear()
        self.edit_market_value.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemValuationWindow()
    window.show()
    sys.exit(app.exec_())
