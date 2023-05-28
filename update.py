from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class PriceUpdateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменение цены товара")
        self.init_ui()

    def init_ui(self):
        self.lbl_item_id = QLabel("Номер товара:")
        self.edit_item_id = QLineEdit()

        self.lbl_new_price = QLabel("Новая цена:")
        self.edit_new_price = QLineEdit()

        self.btn_update_price = QPushButton("Обновить цену")
        self.btn_update_price.clicked.connect(self.update_price)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_item_id)
        layout.addWidget(self.edit_item_id)
        layout.addWidget(self.lbl_new_price)
        layout.addWidget(self.edit_new_price)
        layout.addWidget(self.btn_update_price)

        self.setLayout(layout)

    def update_price(self):
        item_id = self.edit_item_id.text()
        new_price = self.edit_new_price.text()

        # Проверка наличия номера товара и новой цены
        if not item_id or not new_price:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите номер товара и новую цену!")
            return

        try:
            item_id = int(item_id)
            new_price = float(new_price)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Некорректный номер товара или новая цена!")
            return

        # Подключение к базе данных
        conn = sqlite3.connect('lombard.db')
        cursor = conn.cursor()

        # Поиск товара по номеру
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()

        if not item:
            QMessageBox.critical(self, "Ошибка", "Товар с таким номером не найден!")
            return

        # Обновление цены товара
        cursor.execute("UPDATE items SET price = ? WHERE id = ?", (new_price, item_id))

        # Сохранение всех возможных значений цены для товара
        cursor.execute("INSERT INTO item_prices (item_id, price) VALUES (?, ?)", (item_id, new_price))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Цена товара успешно обновлена!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PriceUpdateWindow()
    window.show()
    sys.exit(app.exec_())
