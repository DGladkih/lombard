from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class MoneyIssueWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выдача денег и хранение товара")
        self.init_ui()

    def init_ui(self):
        self.lbl_contract_id = QLabel("Номер договора:")
        self.edit_contract_id = QLineEdit()

        self.btn_issue_money = QPushButton("Выдать деньги")
        self.btn_issue_money.clicked.connect(self.issue_money)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_contract_id)
        layout.addWidget(self.edit_contract_id)
        layout.addWidget(self.btn_issue_money)

        self.setLayout(layout)

    def issue_money(self):
        contract_id = self.edit_contract_id.text()

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

        # Обновление статуса товара
        cursor.execute("UPDATE items SET status = ? WHERE id = ?", ("залоговый", contract[6]))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Деньги выданы клиенту и товар остался в ломбарде!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoneyIssueWindow()
    window.show()
    sys.exit(app.exec_())
