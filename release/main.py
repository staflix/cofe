import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog
from main_ui import Ui_MainWindow
from addEditCoffeeForm_ui import Ui_Dialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.add_btn.clicked.connect(self.add_coffee)
        self.ui.redact_btn.clicked.connect(self.redact_coffee)
        self.load_table()

    def load_table(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        con = sqlite3.connect("D:/gh4/data/coffee.sqlite")
        cur = con.cursor()
        table = cur.execute('''SELECT * FROM cofes''').fetchall()

        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах",
                                                       "описание вкуса", "цена", "объем упаковки"])

        for row in table:
            a, b, c, d, f, g, h = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)

            self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(a)))
            self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(str(b)))
            self.ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(c)))
            self.ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(d)))
            self.ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(f)))
            self.ui.tableWidget.setItem(row_position, 5, QTableWidgetItem(str(g)))
            self.ui.tableWidget.setItem(row_position, 6, QTableWidgetItem(str(h)))

        con.close()

    def add_coffee(self):
        dialog = MyDialogWidget(False)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            self.load_table()

    def redact_coffee(self):
        row = self.ui.tableWidget.currentRow()
        key = self.ui.tableWidget.item(row, 0).text()
        a = self.ui.tableWidget.item(row, 1).text()
        b = self.ui.tableWidget.item(row, 2).text()
        c = self.ui.tableWidget.item(row, 3).text()
        d = self.ui.tableWidget.item(row, 4).text()
        e = self.ui.tableWidget.item(row, 5).text()
        f = self.ui.tableWidget.item(row, 6).text()

        dialog = MyDialogWidget(key, True, a, b, c, d, e, f)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            self.load_table()


class MyDialogWidget(QDialog):
    def __init__(self, ids, is_edit=False, a='', b='', c='', d='', e='', f=''):
        self.key = ids
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        if not is_edit:
            self.ui.ok_btn.clicked.connect(self.add)
        else:
            self.ui.ok_btn.clicked.connect(self.redact)
            self.ui.a.setText(a)
            self.ui.b.setText(b)
            self.ui.c.setText(c)
            self.ui.d.setText(d)
            self.ui.e.setText(e)
            self.ui.f.setText(f)

    def add(self):
        a = self.ui.a.text()
        b = self.ui.b.text()
        c = self.ui.c.text()
        d = self.ui.d.text()
        e = self.ui.e.text()
        f = self.ui.f.text()

        con = sqlite3.connect("D:/gh4/data/coffee.sqlite")
        cur = con.cursor()
        cur.execute('''INSERT INTO cofes("название сорта", "степень обжарки", "молотый/в зернах", 
                                        "описание вкуса", "цена", "объем упаковки")
                                        VALUES (?, ?, ?, ?, ?, ?)''', (a, b, c, d, e, f))
        con.commit()
        con.close()

        self.accept()

    def redact(self):
        a = self.ui.a.text()
        b = self.ui.b.text()
        c = self.ui.c.text()
        d = self.ui.d.text()
        e = self.ui.e.text()
        f = self.ui.f.text()

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
