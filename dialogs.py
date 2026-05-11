import sqlite3
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi


class AddEditCoffeeDialog(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        loadUi("addEditCoffeeForm.ui", self)

        self.coffee_id = coffee_id

        self.saveButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.reject)

        if self.coffee_id:
            self.setWindowTitle("Редактирование записи")
            self.load_data_for_edit()
        else:
            self.setWindowTitle("Добавление записи")

    def load_data_for_edit(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT name, roast, ground, taste, price, volume
            FROM Coffee WHERE ID = ?
            """,
            (self.coffee_id,),
        )
        row = cursor.fetchone()
        connection.close()

        if row:
            name, roast, ground, taste, price, volume = row
            self.nameEdit.setText(name)
            self.roastCombo.setCurrentText(roast)
            self.groundCombo.setCurrentText(ground)
            self.tasteEdit.setText(taste)
            self.priceSpinBox.setValue(price)  # float
            self.volumeSpinBox.setValue(volume)  # int

    def save_data(self):
        name = self.nameEdit.text().strip()
        roast = self.roastCombo.currentText()
        ground = self.groundCombo.currentText()
        taste = self.tasteEdit.text().strip()
        price = self.priceSpinBox.value()
        volume = self.volumeSpinBox.value()

        if not name:
            QMessageBox.warning(
                self, "Ошибка", "Название сорта не может быть пустым."
            )
            return

        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        if self.coffee_id is None:
            cursor.execute(
                """
                INSERT INTO Coffee (name, roast, ground, taste, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, roast, ground, taste, price, volume),
            )
        else:
            cursor.execute(
                """
                UPDATE Coffee
                SET name = ?, roast = ?, ground = ?, taste = ?, price = ?, volume = ?
                WHERE ID = ?
                """,
                (name, roast, ground, taste, price, volume, self.coffee_id),
            )
        connection.commit()
        connection.close()
        self.accept()
