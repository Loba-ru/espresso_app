import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)
from PyQt6.uic import loadUi

from dialogs import AddEditCoffeeDialog


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)

        self.actionAdd.triggered.connect(self.add_record)
        self.actionEdit.triggered.connect(self.edit_record)

        self.tableWidget.setHorizontalHeaderLabels(
            [
                "ID",
                "Название сорта",
                "Степень обжарки",
                "Молотый/в зернах",
                "Описание вкуса",
                "Цена",
                "Объем упаковки",
            ]
        )

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT ID, name, roast, ground, taste, price, volume FROM Coffee"
        )
        rows = cursor.fetchall()
        connection.close()

        self.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

        self.tableWidget.resizeColumnsToContents()

    def add_record(self):
        """Добавление записи"""
        dialog = AddEditCoffeeDialog(self)
        if dialog.exec():
            self.load_data()

    def edit_record(self):
        """Редактирование записи"""
        current_row = self.tableWidget.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self, "Ошибка", "Выберите запись для редактирования."
            )
            return
        coffee_id = int(self.tableWidget.item(current_row, 0).text())
        dialog = AddEditCoffeeDialog(self, coffee_id)
        if dialog.exec():
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
