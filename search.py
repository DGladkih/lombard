from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск")
        self.init_ui()

    def init_ui(self):
        self.lbl_search_client = QLabel("Поиск по ФИО клиента:")
        self.edit_search_client = QLineEdit()

        self.lbl_search_item = QLabel("Поиск по имени товара:")
        self.edit_search_item = QLineEdit()

        self.btn_search = QPushButton("Поиск")
        self.btn_search.clicked.connect(self.search)

        self.lbl_result = QLabel("Результат поиска:")
        self.edit_result = QTextEdit()
        self.edit_result.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_search_client)
        layout.addWidget(self.edit_search_client)
        layout.addWidget(self.lbl_search_item)
        layout.addWidget(self.edit_search_item)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.lbl_result)
        layout.addWidget(self.edit_result)

        self.setLayout(layout)

    def search(self):
        search_client = self.edit_search_client.text()
        search_item = self.edit_search_item.text()

        # Подключение к базе данных
        conn = sqlite3.connect('lombard.db')
        cursor = conn.cursor()

        # Поиск по ФИО клиента
        if search_client:
            cursor.execute("SELECT * FROM clients WHERE last_name= ?", (search_client,))
            clients = cursor.fetchall()

            if clients:
                result = "Результаты поиска по ФИО клиента:\n"
                for client in clients:
                    result += f"Клиент: {client[1]} {client[2]} {client[3]}\nПаспортные данные: {client[4]}\n\n"
                self.edit_result.setText(result)
            else:
                self.edit_result.setText("Нет результатов поиска по ФИО клиента.")

        # Поиск по имени товара
        if search_item:
            cursor.execute("SELECT * FROM items WHERE name = ?", (search_item,))
            items = cursor.fetchall()

            if items:
                result = "Результаты поиска по имени товара:\n"
                for item in items:
                    result += f"Описание товара: {item[1]}\nТекущая цена: {item[3]}\n\n"
                self.edit_result.append(result)
            else:
                self.edit_result.append("Нет результатов поиска по имени товара.")

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec_())
