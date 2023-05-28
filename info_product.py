from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class ItemInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о товаре")
        self.init_ui()

    def init_ui(self):
        self.lbl_item_id = QLabel("Номер товара:")
        self.edit_item_id = QLineEdit()

        self.lbl_description = QLabel("Описание:")
        self.edit_description = QTextEdit()
        self.edit_description.setReadOnly(True)

        self.lbl_current_price = QLabel("Текущая цена:")
        self.edit_current_price = QLineEdit()
        self.edit_current_price.setReadOnly(True)

        self.btn_get_info = QPushButton("Получить информацию")
        self.btn_get_info.clicked.connect(self.get_item_info)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_item_id)
        layout.addWidget(self.edit_item_id)
        layout.addWidget(self.lbl_description)
        layout.addWidget(self.edit_description)
        layout.addWidget(self.lbl_current_price)
        layout.addWidget(self.edit_current_price)
        layout.addWidget(self.btn_get_info)

        self.setLayout(layout)

    def get_item_info(self):
        item_id = self.edit_item_id.text()

        # Проверка наличия номера товара
        if not item_id:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите номер товара!")
            return

        try:
            item_id = int(item_id)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Некорректный номер товара!")
            return

        # Подключение к базе данных
        try:
            conn = sqlite3.connect('lombard.db')
            cursor = conn.cursor()

            # Поиск товара по номеру
            cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
            item = cursor.fetchone()

            if not item:
                QMessageBox.critical(self, "Ошибка", "Товар с таким номером не найден!")
                return

            description = item[1]
            current_price = item[3]

            # Получение истории изменений цены товара
            cursor.execute("SELECT price FROM item_prices WHERE item_id = ? ORDER BY id ASC", (item_id,))
            price_history = cursor.fetchall()

            # Заполнение полей формы информацией о товаре
            self.edit_description.setText(description)
            self.edit_current_price.setText(str(current_price))

            # Вывод истории изменений цены товара
            if price_history:
                price_history_text = "История изменений цены:\n"
                for price in price_history:
                    price_history_text += str(price[0]) + "\n"
                QMessageBox.information(self, "История изменений цены", price_history_text)
            else:
                QMessageBox.information(self, "История изменений цены", "Нет доступной информации")

            # Сохранение изменений и закрытие соединения
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Произошла ошибка базы данных: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemInfoWindow()
    window.show()
    sys.exit(app.exec_())
