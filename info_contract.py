from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class ContractInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Информация о договорах")
        self.init_ui()

    def init_ui(self):
        self.lbl_contract_id = QLabel("Номер договора:")
        self.edit_contract_id = QTextEdit()

        self.btn_get_info = QPushButton("Получить информацию")
        self.btn_get_info.clicked.connect(self.get_contract_info)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_contract_id)
        layout.addWidget(self.edit_contract_id)
        layout.addWidget(self.btn_get_info)

        self.setLayout(layout)

    def get_contract_info(self):
        contract_id = self.edit_contract_id.toPlainText()

        # Проверка наличия номера договора
        if not contract_id:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите номер договора!")
            return

        try:
            contract_id = int(contract_id)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Некорректный номер договора!")
            return

        # Подключение к базе данных
        conn = sqlite3.connect('lombard.db')
        cursor = conn.cursor()

        # Поиск договора по номеру
        cursor.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
        contract = cursor.fetchone()

        if not contract:
            QMessageBox.critical(self, "Ошибка", "Договор с таким номером не найден!")
            return

        client_id = contract[1]
        item_id = contract[2]
        estimated_value = contract[3]
        loan_amount = contract[4]
        commission = contract[5]
        return_date = contract[6]

        # Получение информации о клиенте
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        client = cursor.fetchone()
        client_info = f"Клиент: {client[1]} {client[2]} {client[3]}\nПаспортные данные: {client[4]}"

        # Получение информации о товаре
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        item_info = f"Описание товара: {item[1]}\nТекущая цена: {item[3]}"

        # Вывод информации о договоре
        contract_info = f"Номер договора: {contract_id}\n\n{client_info}\n\n{item_info}\n\n" \
                        f"Оцененная стоимость: {estimated_value}\nСумма займа: {loan_amount}\n" \
                        f"Комиссионные: {commission}\nСрок возврата: {return_date}"

        QMessageBox.information(self, "Информация о договоре", contract_info)

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContractInfoWindow()
    window.show()
    sys.exit(app.exec_())
