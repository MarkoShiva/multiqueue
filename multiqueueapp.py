import sys

from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtWidgets import QApplication, QMainWindow

# import uic
from ui_multiqueueapp import Ui_MainWindow

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
        dateMe = QtCore.QDate.currentDate()
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
        self.ui.priority.itemDoubleClicked.connect(self.editPriority)
        self.ui.urgent.itemDoubleClicked.connect(self.editUrgent)
        self.ui.dueDate.itemDoubleClicked.connect(self.editDueDate)
        # self.ui.priority.






    def editPriority(self):
        selectedItems = self.ui.priority.selectedItems()
        for item in selectedItems:
            item.setSelected(True)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.priority.editItem(item)
            curText = item.text()
            print(curText)














    def editUrgent(self):
        selectedItems = self.ui.urgent.selectedItems()
        for item in selectedItems:
            item.setSelected(True)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.urgent.editItem(item)



    def editDueDate(self):
        selectedItems = self.ui.dueDate.selectedItems()
        for item in selectedItems:
            item.setSelected(True)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.ui.dueDate.editItem(item)



    def saveEdited(self, text):
        query = "UPDATE urgent set priority = 1, task = '" + text \
                + "', date = datetime('now')" + " );"
        print(query)
        que = QSqlQuery(query)
        if que.exec_:
            print("Successful")
            self.db.commit()
    # ToDo add multiple views one for daily list one for a scrum view one for gantt chart agregated view one for calendar view add tracking
# Todo Refactor the code below so its not repetitive


    def save(self):
        text = self.ui.dateEdit.text() + " | " + self.ui.lineEdit.text()
        ls = self.ui.comboBox.currentIndex()
        if ls == 0:
            self.ui.urgent.addItem(text)
            self.addToDatabase("urgent", text)
        elif ls == 1:
            self.ui.priority.addItem(text)
            self.addToDatabase("priority", text)
        elif ls == 2:
            self.ui.dueDate.addItem(text)
            self.addToDatabase("dueDate", text)

        self.ui.lineEdit.clear()

    def addToDatabase(self, lst, txt=""):
        query = "Insert into " + lst + " (priority, task, date) VALUES " \
                                               "(1, '" + txt + "', datetime('now') " + " );"
        que = QSqlQuery(query)

        if que.exec_:
            print("Successful")
            self.db.commit()


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