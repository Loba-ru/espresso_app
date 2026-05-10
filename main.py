import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
