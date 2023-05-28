from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class ItemOwnershipWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Переход товара в собственность ломбарда")
        self.init_ui()

    def init_ui(self):
        self.lbl_contract_id = QLabel("Номер договора:")
        self.edit_contract_id = QLineEdit()

        self.btn_transfer_ownership = QPushButton("Переход товара в собственность ломбарда")
        self.btn_transfer_ownership.clicked.connect(self.transfer_ownership)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_contract_id)
        layout.addWidget(self.edit_contract_id)
        layout.addWidget(self.btn_transfer_ownership)

        self.setLayout(layout)

    def transfer_ownership(self):
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

        return_date = contract[10]

        # Проверка срока возврата денег
        if not return_date:
            QMessageBox.warning(self, "Предупреждение", "Срок возврата денег еще не прошел!")
            return

        # Обновление статуса товара
        cursor.execute("UPDATE items SET status = ? WHERE id = ?", ("собственность ломбарда", contract[6]))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Товар перешел в собственность ломбарда!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemOwnershipWindow()
    window.show()
    sys.exit(app.exec_())
