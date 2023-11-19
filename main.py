import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_table()

    def load_table(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        table = cur.execute(f'''SELECT * FROM cofes''').fetchall()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах"
                                                       , "описание вкуса", "цена", "объем упаковки"])

        for row in table:
            a, b, c, d, f, g, h = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(a)))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(str(b)))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(c)))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(d)))
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(f)))
            self.tableWidget.setItem(row_position, 5, QTableWidgetItem(str(g)))
            self.tableWidget.setItem(row_position, 6, QTableWidgetItem(str(h)))

        con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
