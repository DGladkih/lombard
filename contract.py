from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class AgreementFormWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оформление договора")
        self.init_ui()

    def init_ui(self):
        self.lbl_full_name = QLabel("ФИО клиента:")
        self.edit_full_name = QLineEdit()

        self.lbl_item_value = QLabel("Оцененная стоимость товара:")
        self.edit_item_value = QLineEdit()

        self.lbl_loan_amount = QLabel("Сумма займа:")
        self.edit_loan_amount = QLineEdit()

        self.lbl_commission = QLabel("Комиссионные:")
        self.edit_commission = QLineEdit()

        self.lbl_return_date = QLabel("Срок возврата:")
        self.edit_return_date = QLineEdit()

        self.btn_create_agreement = QPushButton("Оформить договор")
        self.btn_create_agreement.clicked.connect(self.create_agreement)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_full_name)
        layout.addWidget(self.edit_full_name)
        layout.addWidget(self.lbl_item_value)
        layout.addWidget(self.edit_item_value)
        layout.addWidget(self.lbl_loan_amount)
        layout.addWidget(self.edit_loan_amount)
        layout.addWidget(self.lbl_commission)
        layout.addWidget(self.edit_commission)
        layout.addWidget(self.lbl_return_date)
        layout.addWidget(self.edit_return_date)
        layout.addWidget(self.btn_create_agreement)

        self.setLayout(layout)

    def create_agreement(self):
        full_name = self.edit_full_name.text()
        item_value = self.edit_item_value.text()
        loan_amount = self.edit_loan_amount.text()
        commission = self.edit_commission.text()
        return_date = self.edit_return_date.text()

        # Проверка наличия введенных данных
        if not full_name or not item_value or not loan_amount or not commission or not return_date:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните все поля!")
            return

        # Создание соединения с базой данных
        conn = sqlite3.connect("lombard.db")
        cursor = conn.cursor()

        # Создание таблицы договоров, если она не существует
        cursor.execute("CREATE TABLE IF NOT EXISTS agreements (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "full_name TEXT, item_value REAL, loan_amount REAL, commission REAL, return_date TEXT)")

        # Вставка данных договора в таблицу
        cursor.execute("INSERT INTO agreements (full_name, item_value, loan_amount, commission, return_date) "
                       "VALUES (?, ?, ?, ?, ?)", (full_name, item_value, loan_amount, commission, return_date))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Договор успешно оформлен!")

        # Очистка полей формы
        self.edit_full_name.clear()
        self.edit_item_value.clear()
        self.edit_loan_amount.clear()
        self.edit_commission.clear()
        self.edit_return_date.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgreementFormWindow()
    window.show()
    sys.exit(app.exec_())
