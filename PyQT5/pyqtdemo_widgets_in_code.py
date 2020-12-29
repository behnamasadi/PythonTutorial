import sys
print(sys.version)
import warnings
warnings.filterwarnings('ignore')


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QSlider
from PyQt5.QtCore import QSize, Qt, pyqtSlot,pyqtSignal 



class HelloWindow(QMainWindow):
    
    pushButtonClicked = pyqtSignal()
    valueUpdating = pyqtSignal(int)
    
    
    def pushButtonClicked(self):
        self.title.setText("PyQt updated!")
            
    def valueUpdating(self, value):
        self.title.setText(str(value))
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("Hello world") 

        self.title = QLabel("PyQt!", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter) 


        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(140, 200, 99, 27))#x,y, width, height
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Click Me!")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        
        self.slider = QtWidgets.QSlider(self)
        self.slider.setGeometry(QtCore.QRect(100, 20, 100, 30))
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)
        self.slider.setMaximum(100)
        self.slider.setMinimum(0)
        self.slider.setOrientation(Qt.Horizontal)
        
        self.slider.valueChanged.connect(self.valueUpdating)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )