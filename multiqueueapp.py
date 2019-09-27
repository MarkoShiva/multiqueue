from PySide2.QtWidgets import QApplication, QMainWindow
import sys
import json

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
        self.que = QSqlQuery("CREATE Table priority (id integer, task varchar(256));")
        if self.que.exec_:
            print("Executed successful.")

    # ToDo add multiple views one for daily list one for a scrum view one for gantt chart agregated view one for calendar view add tracking



# ToDo rewrite app in MVC mode.
    def save(self):
        date = self.ui.dateEdit.text()
        txt = self.ui.lineEdit.text()
        ls = self.ui.comboBox.currentIndex()
        if ls == 0:
            text = date + " | " + self.ui.lineEdit.text()
            self.ui.priority.addItem(text)
            que = QSqlQuery("Insert into priority task=" + text + ";")
            if que.exec_:
                print("Successful")
        elif ls == 1:
            self.ui.noPriority.addItem(date + " | " + self.ui.lineEdit.text())
        elif ls == 2:
            self.ui.dated.addItem(date + " | " + self.ui.lineEdit.text())
        else:
            pass
        self.ui.lineEdit.clear()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Multi Schedule Application")
    window.show()


    sys.exit(app.exec_())