from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sqlite3
import sys


class LoanCalculationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчет суммы займа и комиссионных")
        self.init_ui()

    def init_ui(self):
        self.lbl_item_value = QLabel("Оцененная стоимость товара:")
        self.edit_item_value = QLineEdit()

        self.lbl_loan_amount = QLabel("Сумма займа:")
        self.edit_loan_amount = QLineEdit()

        self.lbl_commission = QLabel("Комиссионные:")
        self.edit_commission = QLineEdit()

        self.btn_calculate = QPushButton("Рассчитать")
        self.btn_calculate.clicked.connect(self.calculate_loan)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_item_value)
        layout.addWidget(self.edit_item_value)
        layout.addWidget(self.lbl_loan_amount)
        layout.addWidget(self.edit_loan_amount)
        layout.addWidget(self.lbl_commission)
        layout.addWidget(self.edit_commission)
        layout.addWidget(self.btn_calculate)

        self.setLayout(layout)

    def calculate_loan(self):
        item_value = self.edit_item_value.text()

        # Проверка наличия введенной стоимости товара
        if not item_value:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите оцененную стоимость товара!")
            return

        try:
            item_value = float(item_value)
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Некорректная оцененная стоимость товара!")
            return

        # Расчет суммы займа и комиссионных
        loan_amount = item_value * 0.8
        commission = item_value * 0.05

        # Округление до двух знаков после запятой
        loan_amount = round(loan_amount, 2)
        commission = round(commission, 2)

        # Вывод результатов на экран
        self.edit_loan_amount.setText(str(loan_amount))
        self.edit_commission.setText(str(commission))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoanCalculationWindow()
    window.show()
    sys.exit(app.exec_())
