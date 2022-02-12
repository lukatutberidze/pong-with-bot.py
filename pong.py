from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import random
import threading
from pynput.keyboard import Key, Listener
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sys

class Ui_MainWindow(QObject):
    update_required = QtCore.pyqtSignal()
    msg = QtCore.pyqtSignal()
    def __init__(self):
            super().__init__()
            self.update_required.connect(self.update)
            self.msg.connect(self.news)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 650)
        MainWindow.setStyleSheet("background-color: rgb(17, 17, 17);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.p1 = QtWidgets.QLabel(self.centralwidget)
        self.p1.setGeometry(QtCore.QRect(20, 250, 20, 100))
        self.p1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.p1.setText("")
        self.p1.setObjectName("p1")
        self.p2 = QtWidgets.QLabel(self.centralwidget)
        self.p2.setGeometry(QtCore.QRect(960, 250, 20, 100))
        self.p2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.p2.setText("")
        self.p2.setObjectName("p2")
        self.ball = QtWidgets.QLabel(self.centralwidget)
        self.ball.setGeometry(QtCore.QRect(0,0, 15, 15))
        self.ball.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ball.setText("")
        self.ball.setObjectName("ball")
        self.wall = QtWidgets.QLabel(self.centralwidget)
        self.wall.setGeometry(QtCore.QRect(500, 0, 20, 621))
        self.wall.setStyleSheet("background-color: rgb(136, 136, 136);")
        self.wall.setText("")
        self.wall.setObjectName("wall")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(460, 0, 21, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(540, 0, 21, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setup()
            
    def setup(self):
        self.done=False
        self.start=1
        self.x,self.y=960, 250
        self.bx,self.by=20,250
        self.dx,self.dy=1,1
        self.sc1=0
        self.sc2=0
        t1=threading.Thread(target=self.move)
        t1.start()
        self.kickoff()
        t2=threading.Thread(target=self.bupdate)
        t2.start()

    def news(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        st='Congrats! you beat the machine. :)' if self.sc2==5 else 'Tough luck, try again.. :('
        self.sc2=0
        self.sc1=0
        msgBox.setText(st)
        msgBox.setWindowTitle("Game Over!")
        msgBox.addButton('Ok', QMessageBox.YesRole)
        self.kickoff()
        returnValue = msgBox.exec()
        MainWindow.close()
        exit()


    def kickoff(self):
        if max([self.sc1,self.sc2])==5:
            self.msg.emit()
        self.label.setText(str(self.sc1))
        self.label_2.setText(str(self.sc2))
        self.balx,self.baly=310,random.randint(150,300)
        self.dx=13
        self.dy=random.randint(5,9)*random.choice([1,-1])
    
    def bupdate(self):
        while True:
            if self.by<self.baly and self.by+100<self.baly:
                self.by+=8
            elif self.by>self.baly and self.by+100>self.baly:
                self.by-=8
            self.update_required.emit()

            if self.baly>=635:
                self.dy=-self.dy
            elif self.baly<=0:
                self.dy=-self.dy
            elif self.baly in range(self.y,self.y+100) and self.balx in range(self.x-20,self.x+1):
                x=(abs(self.y-self.baly)-50)
                self.dx=-self.dx
                p=abs(x)
                n=1 if x>0 else -1
                if p<=5:
                    self.dy=0
                elif p<=10:
                    self.dy=2*n
                elif p<=20:
                    self.dy=5*n
                elif p<=30:
                    self.dy=8*n
                elif p<=40:
                    self.dy=10*n
                else:
                    self.dy=12*n

            elif self.baly in range(self.by,self.by+100) and self.balx<=self.bx: 
                x=(abs(self.by-self.baly)-50)
                self.dx=-self.dx
                p=abs(x)
                n=1 if x>0 else -1
                if p<=5:
                    self.dy=0
                elif p<=10:
                    self.dy=2*n
                elif p<=20:
                    self.dy=5*n
                elif p<=30:
                    self.dy=8*n
                elif p<=40:
                    self.dy=10*n
                else:
                    self.dy=12*n
            
            elif self.balx<10 or self.balx>1000:
                self.start=-self.start
                if self.balx>1000:
                    self.sc1+=1
                elif self.balx<0:
                    self.sc2+=1
                self.kickoff()
                
            time.sleep(0.016)
            self.balx+=self.dx
            self.baly+=self.dy
        

    def update(self):
        self.ball.setGeometry(self.balx,self.baly, 16,16)
        if self.y<=0:
            self.y=0
        elif self.y>=530:
            self.y=530

        if self.by<=0:
            self.by=0
        elif self.by>=530:
            self.by=530
        self.p2.setGeometry(self.x,self.y, 21, 101)
        self.p1.setGeometry(self.bx,self.by, 21, 101)


    def move(self):
        def on_press(key):
            check_key(key)
        def check_key(key):
            if key!=Key.up and key!=Key.down:
                None
            elif key==Key.up: 
                for i in range(30):
                    self.y-=1
                    self.update_required.emit()
            elif key==key.down:
                for i in range(30):
                    self.y+=1
                    self.update_required.emit()
                
        with Listener(on_press=on_press) as listener:listener.join()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pong by luka tutberidze"))
        self.label.setText(_translate("MainWindow", "0"))
        self.label_2.setText(_translate("MainWindow", "0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())