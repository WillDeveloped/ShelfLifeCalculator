from PyQt5 import QtCore, QtGui, QtWidgets
import datetime


def send_error(obj, message, where):
    #Takes an error message, where it came from, and sends it to the class error handler.
    output = where + " " + message
    Ui_MainWindow.send_error(obj, output)

def split_date(obj, date, what):
    date = date.replace("-", "/")   #If user uses - instead of / for the date
    date = date.upper()             #If user inputs q, changes it to Q

    if len(date) < 8 and date.find('Q') == -1:
        #If the date doesn't have enough characters, returns -1 for all values
        return -1, -1, -1
        

    if date.find('Q') > -1:
        if date.split('Q')[0] == '1': #1st quarter ends March 31st
            d = 31
            m = 3
        if date.split('Q')[0] == '2': #2nd quarter ends June 30th
            d = 30
            m = 6   
        if date.split('Q')[0] == '3': #3rd quarter ends September 30th
            d = 30
            m = 9   
        if date.split('Q')[0] == '4': #4th quarter ends December 31st
            d = 31
            m = 12
        if int(date.split('Q')[0]) > 4: #Any value other than the above 4 will result in an error
            d = 0
            m = 0
        y = date.split('Q')[1]

    else:
        m = int(date.split('/')[0]) #format is mm/dd/yyyy. before first / is the month
        d = int(date.split('/')[1]) #After the first slash, before the 2nd is the day
        y = int(date.split('/')[2]) #Everything after is a the year
    

    #Date validation
    if d <= 0 or d > 31:
        send_error(obj, 'Day has error. should be bigger than 0, less than 31, is' + str(d), what)
        return -1, -1, -1
    
    elif m <= 0 or m > 12:
        send_error(obj, 'Month has error. should be bigger than 0, less than 12, is' + str(m), what)
        return -1, -1, -1

    elif len(str(y)) < 4 or len(str(y)) > 4:
        send_error(obj, 'Year has error. should be bigger than 3 digits, less than 5', what )
        return -1, -1, -1

    else:
        return d, m, y
        
    
#This function takes in the year, month, date and shelf life, and returns how much shelf life is remaining, or if it is expired
def Shelflife_Remaining(cureYear, cureMonth, cureDay, life_in_months):
    today = datetime.date.today()
    cureDate = datetime.date(cureYear, cureMonth, cureDay)
    exp_date = datetime.timedelta(days = life_in_months*30.4166666666666)
    days_remaining = (cureDate + exp_date) - today
    response = round(days_remaining.days / exp_date.days * 100, 2)

    if response > 0:
        return str(response) + "% as of today"
    else:
        return "Expired"

#This function takes in the date the material was made, how much shelf life it has, when the part should ship, and returns how much shelf life
#it will have when it ships. 
def When_Shipped(cureYear, cureMonth, cureDay, life_in_months, shipYear, shipMonth, shipDay):
    if shipYear == -1:
        return ""
    shipDate = datetime.date(shipYear, shipMonth, shipDay)
    cureDate = datetime.date(cureYear, cureMonth, cureDay)
    exp_date = datetime.timedelta(days = life_in_months*30.4166666666666)
    days_remaining = (cureDate + exp_date) - shipDate
    shipDateString = str(shipMonth) + "-" + str(shipDay) + "-" + str(shipYear)
    response = round(days_remaining.days / exp_date.days * 100, 2)
    
    if response > 0:
        return str(response) + "% when shipped"
    else:
        return "Expired"
    



class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(329, 263)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 120, 75, 41))
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_click)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 20, 121, 16))
        self.label_2.setObjectName("label_2")

        #Cure Date input 
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 113, 20))
        self.lineEdit.setObjectName("lineEdit")

        #Shipdate input
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 40, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")

        #Shelf life input
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 111, 16))
        self.label_3.setObjectName("label_3")
        self.shelfLifeSet = QtWidgets.QLabel(self.centralwidget)
        self.shelfLifeSet.setGeometry(QtCore.QRect(160, 170, 101, 16))
        self.shelfLifeSet.setObjectName("shelfLifeSet")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 190, 121, 16))
        self.label_4.setObjectName("label_4")
        self.shipppedShelfLife = QtWidgets.QLabel(self.centralwidget)
        self.shipppedShelfLife.setGeometry(QtCore.QRect(160, 190, 130, 16))
        self.shipppedShelfLife.setObjectName("shipppedShelfLife")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 90, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(120, 140, 150, 16))
        self.label_6.setObjectName("label_6")
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 70, 101, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 329, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #this function operates inside the class, and sets the text in the error bar to inform user what the issue is
    def send_error(self, message):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("MainWindow", message))
        

    #This function connects the calculate button to the input boxes. 
    def on_click(self):
        cureDate = self.lineEdit.text()
        shipDate = self.lineEdit_2.text()
        shelfLife = self.lineEdit_3.text()
        
        cd, cm, cy = split_date(self, cureDate, 'Cure Date')
        sd, sm, sy = split_date(self, shipDate, 'Ship Date')
        

        if shelfLife == '':
            send_error(self, 'Cannot be blank', 'Shelf Life')
            shelfLife = 0
        else:
            shelfLife = int(shelfLife)

        if shelfLife < 0:
            send_error(self, 'Cannot be negative', 'Shelf Life')
        
        if shelfLife > 0 and cy != -1:
            x = Shelflife_Remaining(cy, cm, cd, shelfLife)
            _translate = QtCore.QCoreApplication.translate
            self.shelfLifeSet.setText(_translate("MainWindow", x))
            y = When_Shipped(cy, cm, cd, shelfLife, sy, sm, sd)
            self.shipppedShelfLife.setText(_translate("MainWindow", y))

    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Shelf Life Calculator v1.0"))
        self.pushButton.setText(_translate("MainWindow", "Calculate"))    
        self.label.setText(_translate("MainWindow", "Cure Date (mm/dd/yyyy)"))
        self.label_2.setText(_translate("MainWindow", "Ship Date (mm/dd/yyyy)"))
        self.label_3.setText(_translate("MainWindow", "  Shelf Life Remaining:"))
        self.shelfLifeSet.setText(_translate("MainWindow", ""))
        self.label_4.setText(_translate("MainWindow", "Shelf Life when shipped:"))
        self.shipppedShelfLife.setText(_translate("MainWindow", ""))
        self.label_5.setText(_translate("MainWindow", "Shelf Life in months"))
        self.label_6.setText(_translate("MainWindow", ""))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
