from PySide2.QtWidgets import QApplication, QMainWindow
import sys
import datetime

# import uic
from ui_multiqueueapp import Ui_MainWindow
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2 import QtCore
qt_creator_file = "multiqueueapp.ui"
# Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit.setMinimumDate(QtCore.QDate.currentDate())
        self.ui.dateEdit.setMaximumDate(QtCore.QDate(8181, 12, 31))

        self.ui.AddBtn.clicked.connect(self.save)

        self.ui.lineEdit.returnPressed.connect(self.save)
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("store")
        self.db.open()
        self.que = QSqlQuery("CREATE Table urgent (priority integer, "
                             "task varchar(256), date datetime);")
        if self.que.exec_:
            print("Executed successful.")
        self.que = QSqlQuery("CREATE Table priority (priority integer, "
                             "task varchar(256), date datetime);")
        if self.que.exec_:
            print("Executed successful.")
        self.que = QSqlQuery("CREATE Table dueDate (priority integer, "
                             "task varchar(256), date datetime);")
        if self.que.exec_:
            print("Executed successful.")
        self.load()

    # ToDo add multiple views one for daily list one for a scrum view one for gantt chart agregated view one for calendar view add tracking

# ToDo rewrite app in MVC mode.
    def save(self):
        date = self.ui.dateEdit.text()
        # cur = datetime.datetime.now()
        txt = self.ui.lineEdit.text()
        ls = self.ui.comboBox.currentIndex()
        if ls == 0:
            text = date + " | " + self.ui.lineEdit.text()
            self.ui.urgent.addItem(text)
            query = "Insert into urgent (priority, task, date) VALUES " \
                    "(1, '" + text + "', datetime('now') " + " );"
            print(query)
            que = QSqlQuery(query)


            if que.exec_:
                print("Successful")
                self.db.commit()
        elif ls == 1:
            text = date + " | " + self.ui.lineEdit.text()
            self.ui.priority.addItem(text)
            query = "Insert into priority (priority, task, date) VALUES " \
                    "(1, '" + text + "', datetime('now') " + " );"
            que = QSqlQuery(query)
            if que.exec_:
                print("Successful")
                self.db.commit()
        elif ls == 2:
            text = date + " | " + self.ui.lineEdit.text()
            self.ui.dueDate.addItem(text)
            query = "Insert into dueDate (priority, task, date) VALUES " \
                    "(1, '" + text + "', datetime('now') " + " );"
            que = QSqlQuery(query)
            if que.exec_:
                print("Successful")
                self.db.commit()
        else:
            pass
        self.ui.lineEdit.clear()

    def load(self):
        query = QSqlQuery()
        query.exec_("SELECT task from priority;")
        while query.next():
            print(query.value(0))
            self.ui.priority.addItem(query.value(0))
        query = QSqlQuery()
        query.exec_("SELECT task from urgent;")
        while query.next():
            print(query.value(0))
            self.ui.urgent.addItem(query.value(0))
        query = QSqlQuery()
        query.exec_("SELECT task from dueDate;")
        while query.next():
            print(query.value(0))
            self.ui.dueDate.addItem(query.value(0))

#

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Multi Schedule Application")
    window.show()


    sys.exit(app.exec_())