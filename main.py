import sqlite3
from pathlib import PurePath
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDesktopWidget
)


_DB_FILENAME = r'data\coffee.sqlite'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('./ui/main.ui', self)
        db_filename = str(PurePath(__file__).parent.joinpath(_DB_FILENAME))
        self.statusbar.showMessage(db_filename)
        self.db_load(db_filename)

    def center_window(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

    def db_load(self, db_filename):
        if not(db_filename):
            return

        headers = ()
        coffees = ()
        with sqlite3.connect(db_filename) as con:
            cur = con.cursor()
            coffees = cur.execute(
                f"""
                SELECT
                    Coffee.Id as "Идентификатор",
                    Coffee.GradeName as "Название",
                    Roast.Name as "Обжарка",
                    Type.Name as "Тип",
                    Coffee.Price as "Цена, руб.",
                    Coffee.Packing as "Вес, гр",
                    Coffee.Description as "Описание"
                FROM Coffee
                INNER JOIN Roast ON Roast.Id = Coffee.RoastId
                INNER JOIN Type ON Type.Id = Coffee.TypeId
                ORDER BY Coffee.GradeName
                """).fetchall()

            headers = tuple(desc[0] for desc in cur.description)

        self.table.setColumnCount(len(headers) - 1)
        self.table.setHorizontalHeaderLabels(headers[1:])
        self.table.setRowCount(0)

        if coffees:
            for row, coffee in enumerate(coffees):
                self.table.setRowCount(self.table.rowCount() + 1)
                for col, coffee_property in enumerate(coffee[1:]):
                    item = QtWidgets.QTableWidgetItem(str(coffee_property))
                    item.setData(QtCore.Qt.UserRole, coffee[0])
                    self.table.setItem(row, col, item)

        # self.table.resizeColumnsToContents()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.center_window()
    win.show()
    sys.exit(app.exec_())
