import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.add_btn.clicked.connect(self.add_coffee)
        self.redact_btn.clicked.connect(self.redact_coffee)
        self.load_table()

    def load_table(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        table = cur.execute('''SELECT * FROM cofes''').fetchall()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах",
                                                    "описание вкуса", "цена", "объем упаковки"])

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

        con.close()

    def add_coffee(self):
        dialog = MyDialogWidget(False)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.load_table()

    def redact_coffee(self):
        row = self.tableWidget.currentRow()
        key = self.tableWidget.item(row, 0).text()
        a = self.tableWidget.item(row, 1).text()
        b = self.tableWidget.item(row, 2).text()
        c = self.tableWidget.item(row, 3).text()
        d = self.tableWidget.item(row, 4).text()
        e = self.tableWidget.item(row, 5).text()
        f = self.tableWidget.item(row, 6).text()

        dialog = MyDialogWidget(key, True, a, b, c, d, e, f)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            self.load_table()


class MyDialogWidget(QDialog):
    def __init__(self, ids, is_edit=False, a='', b='', c='', d='', e='', f=''):
        self.key = ids
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        if not is_edit:
            self.ok_btn.clicked.connect(self.add)
        else:
            self.ok_btn.clicked.connect(self.redact)
            self.a.setText(a)
            self.b.setText(b)
            self.c.setText(c)
            self.d.setText(d)
            self.e.setText(e)
            self.f.setText(f)

    def add(self):
        a = self.a.text()
        b = self.b.text()
        c = self.c.text()
        d = self.d.text()
        e = self.e.text()
        f = self.f.text()

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        cur.execute('''INSERT INTO cofes("название сорта", "степень обжарки", "молотый/в зернах", 
                                        "описание вкуса", "цена", "объем упаковки")
                                        VALUES (?, ?, ?, ?, ?, ?)''', (a, b, c, d, e, f))
        con.commit()
        con.close()

        self.accept()

    def redact(self):
        a = self.a.text()
        b = self.b.text()
        c = self.c.text()
        d = self.d.text()
        e = self.e.text()
        f = self.f.text()

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()

        cur.execute('''UPDATE cofes
                       SET "название сорта" = ?,
                           "степень обжарки" = ?,
                           "молотый/в зернах" = ?,
                           "описание вкуса" = ?,
                           "цена" = ?,
                           "объем упаковки" = ?
                       WHERE "ID" = ?''', (str(a), str(b), str(c), str(d), str(e), str(f), str(self.key)))

        con.commit()
        con.close()

        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
