from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from create_map import QueryMap, MapIterator
from query_incidents import QueryDF


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.EndDateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.EndDateEdit.setGeometry(QtCore.QRect(250, 470, 91, 31))
        self.EndDateEdit.setObjectName("dateEdit_2")
        self.EndDateEdit.setDisplayFormat("MM/yyyy")
        self.QueryPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.QueryPushButton.setGeometry(QtCore.QRect(250, 510, 88, 27))
        self.QueryPushButton.setObjectName("pushButton_3")
        self.NextPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.NextPushButton.setGeometry(QtCore.QRect(530, 520, 41, 21))
        self.NextPushButton.setObjectName("pushButton")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(
            self.centralwidget)
        self.webEngineView.setGeometry(QtCore.QRect(0, 10, 791, 361))
        self.webEngineView.setMinimumSize(QtCore.QSize(791, 361))
        self.webEngineView.setMaximumSize(QtCore.QSize(791, 361))
        self.webEngineView.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.webEngineView.setLayoutDirection(QtCore.Qt.LayoutDirectionAuto)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.StartDateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.StartDateEdit.setGeometry(QtCore.QRect(250, 430, 91, 31))
        self.StartDateEdit.setObjectName("plainTextEdit")
        self.StartDateEdit.setDisplayFormat("MM/yyyy")
        self.incidents_label = QtWidgets.QLabel(self.centralwidget)
        self.incidents_label.setGeometry(QtCore.QRect(390, 450, 81, 19))
        self.incidents_label.setObjectName("label_4")
        self.incidents_desc_label = QtWidgets.QLabel(self.centralwidget)
        self.incidents_desc_label.setGeometry(QtCore.QRect(480, 450, 81, 29))
        self.incidents_desc_label.setObjectName("plainTextEdit_4")
        self.incidents_desc_label.setStyleSheet(
            "background-color: white; border: 1px solid black;")
        self.nb_label = QtWidgets.QLabel(self.centralwidget)
        self.nb_label.setGeometry(QtCore.QRect(430, 480, 41, 19))
        self.nb_label.setObjectName("label_5")
        self.month_desc_label = QtWidgets.QLabel(self.centralwidget)
        self.month_desc_label.setGeometry(QtCore.QRect(480, 415, 81, 31))
        self.month_desc_label.setObjectName("month label")
        self.month_desc_label.setStyleSheet(
            "background-color: white; border: 1px solid black;")
        self.month_label = QtWidgets.QLabel(self.centralwidget)
        self.month_label.setGeometry(QtCore.QRect(440, 420, 31, 19))
        self.month_label.setObjectName("label_3")
        self.end_date_label = QtWidgets.QLabel(self.centralwidget)
        self.end_date_label.setGeometry(QtCore.QRect(160, 480, 81, 19))
        self.end_date_label.setObjectName("label_2")
        self.nb_ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.nb_ComboBox.setGeometry(QtCore.QRect(480, 480, 240, 31))
        self.nb_ComboBox.setObjectName("plainTextEdit_5")
        self.BackPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.BackPushButton.setGeometry(QtCore.QRect(480, 520, 41, 21))
        self.BackPushButton.setObjectName("pushButton_2")
        self.start_date_label = QtWidgets.QLabel(self.centralwidget)
        self.start_date_label.setGeometry(QtCore.QRect(160, 430, 81, 19))
        self.start_date_label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.QueryPushButton.setText(_translate("MainWindow", "Consultar"))
        self.NextPushButton.setText(_translate("MainWindow", ">>"))
        self.incidents_label.setText(_translate("MainWindow", "# incidentes"))
        self.nb_label.setText(_translate("MainWindow", "Barrio"))
        self.month_label.setText(_translate("MainWindow", "Mes"))
        self.end_date_label.setText(_translate("MainWindow", "Fecha final"))
        self.BackPushButton.setText(_translate("MainWindow", "<<"))
        self.start_date_label.setText(
            _translate("MainWindow", "Fecha inicial"))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.map_iterator = None
        self._show_map()
        self._init_nb_ComboBox()
        self.ui.StartDateEdit.setMinimumDate(QDate(2015, 1, 1))
        self.ui.EndDateEdit.setMinimumDate(QDate(2015, 1, 1))
        self.ui.QueryPushButton.clicked.connect(
            self._show_marks_by_neighborhood_date)
        self.ui.BackPushButton.setDisabled(True)
        self.ui.NextPushButton.setDisabled(True)

        self.ui.NextPushButton.clicked.connect(self._show_marks_next_date)
        self.ui.BackPushButton.clicked.connect(self._show_marks_back_date)

    def _init_nb_ComboBox(self):
        query_df = QueryDF('incidents.csv')
        nb_list = query_df.get_neighborhood_list()

        self.ui.nb_ComboBox.addItems(nb_list)

    def _show_map(self):
        self.map = QueryMap('incidents.csv')
        data = self.map.show_map()
        self.ui.webEngineView.setHtml(data.getvalue().decode())

    def _update_map(self, data, date, num_inc: int):
        if num_inc > 0:
            date = date.strftime("%m-%Y")
            self.ui.month_desc_label.setText(str(date))
        elif num_inc == 0:
            self.ui.month_desc_label.setText("")

        self.ui.webEngineView.setHtml(data.getvalue().decode())
        self.ui.incidents_desc_label.setText(str(num_inc))

    def _show_marks_by_neighborhood(self):
        nbh_name = self.ui.nb_ComboBox.toPlainText()
        data, num_inc = self.map.show_marks_by_neighborhood(nbh_name)
        self.ui.webEngineView.setHtml(data.getvalue().decode())
        self.ui.incidents_desc_label.setText(str(num_inc))
        self.ui.NextPushButton.setDisabled(False)

    def _show_marks_by_neighborhood_date(self):
        nbh_name = str(self.ui.nb_ComboBox.currentText())
        start_date = self.ui.StartDateEdit.date().toPyDate()
        end_date = self.ui.EndDateEdit.date().toPyDate()

        # Get map iterator for move between registers
        self.map_iterator = self.map.show_marks_by_neighborhood_and_date_range(
            nbh_name, start_date, end_date)

        # Show the first register
        data, num_inc, date = self.map_iterator.show_reg()

        # Disable back and next buttons by default
        self.ui.BackPushButton.setDisabled(True)
        self.ui.NextPushButton.setDisabled(True)

        # Get number of registers
        num_regs = self.map_iterator.get_num_regs()

        # Only disable back and next buttons if there are more than one register
        if num_regs > 1:
            self.ui.NextPushButton.setDisabled(False)

        self._update_map(data, date, num_inc)

    def _show_marks_next_date(self):
        if self.map_iterator:
            data, num_inc, date, end = self.map_iterator.show_next_reg()

            if end:
                self.ui.NextPushButton.setDisabled(True)

            self.ui.BackPushButton.setDisabled(False)

            self._update_map(data, date, num_inc)

    def _show_marks_back_date(self):
        if self.map_iterator:
            data, num_inc, date, end = self.map_iterator.show_back_reg()

            if end:
                self.ui.BackPushButton.setDisabled(True)

            self.ui.NextPushButton.setDisabled(False)

            self._update_map(data, date, num_inc)


if __name__ == "__main__":
    app = QtWidgets.QApplication(["NY Incidents Map"])

    mainWindow = QtWidgets.QMainWindow()
    window = MainWindow()
    window.setWindowTitle("NY Incidents Map")
    window.show()

    sys.exit(app.exec())
