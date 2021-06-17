from __future__ import print_function
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread,QTimer
import capture
import cnn_model
import recognise


class Window (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Language Detector")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('logo.png'))
        # self.mainMenu = QMenuBar()
        self.setStyleSheet("""
               QMenuBar {
                   background-color: rgb(49,49,49);
                   color: rgb(255,255,255);
                   border: 1px solid #000;
               }

               QMenuBar::item {
                   background-color: rgb(49,49,49);
                   color: rgb(255,255,255);
               }

               QMenuBar::item::selected {
                   background-color: rgb(30,30,30);
               }

               QMenu {
                   background-color: rgb(49,49,49);
                   color: rgb(255,255,255);
                   border: 1px solid #000;           
               }

               QMenu::item::selected {
                   background-color: rgb(30,30,30);
               }
           """)
        self.init_ui()
        self.show()
        self.h_low, self.h_high, self.s_low, self.s_high, self.v_low, self.v_high = 0, 0, 0, 0, 0, 0

    # To Create the widgets we need
    def init_ui(self):
        # Train model button
        trainBtn = QPushButton("Train The Model")
        trainBtn.setStyleSheet("color: white; font-size: 16px; background-color: #2b5b84;" "border-radius: 10px; padding: 10px; text-align: center; ")
        trainBtn.clicked.connect(self.train)

        # Detect Gesture button
        detectBtn = QPushButton("Detect Gesture")
        detectBtn.setStyleSheet("color: white; font-size: 16px; background-color: #2b5b84;" "border-radius: 10px; padding: 10px; text-align: center; ")
        detectBtn.clicked.connect(self.detect)

        # Create New Sign button
        createBtn = QPushButton('Create New Sign')
        createBtn.clicked.connect(self.addSign)
        createBtn.setStyleSheet("QPushButton::pressed""{""background-color : white;""}")
        createBtn.setStyleSheet("color: white; font-size: 16px; background-color: #2b5b84; border-radius: 10px;"" padding: 10px; text-align: center;")

        # Capture button
        captureBtn = QPushButton("Capture")
        captureBtn.setStyleSheet("color: white; font-size: 16px; background-color: #2b5b84;" "border-radius: 10px; padding: 10px; text-align: center; ")
        captureBtn.clicked.connect(self.capture)

        # Create a model training info Label
        self.label3 = QLabel()
        self.label3.setStyleSheet("color:#2b5b84 ; font-size: 16px; border-radius: 10px; padding:"" 10px; text-align: center;")
        self.label3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create an Information Label
        self.label2 =QLabel()
        self.label2.setStyleSheet("color:#2b5b84 ; font-size: 12px; border-radius: 10px; padding:"" 10px; text-align: center;")
        self.label2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label2.setText("Press (Detect) button to start detecting a well-known character or (Create New Sign) button to create a new gesture, To Exit Press ESC")

        # Create a gesture Label
        self.label1 = QLabel()
        self.label1.setStyleSheet("color:#2b5b84 ; font-size: 12px; border-radius: 10px; padding:"" 10px; text-align: center;")
        self.label1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.label1.setText("Enter gesture name: ")

        # Create textbox
        self.textbox = QLineEdit(self)

        # Create a spacer item for the Hbox
        spacer =QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

###########################################################################
        # Create HSV sliders
        # low H
        hbox1 = QHBoxLayout()
        hbox1.setContentsMargins(0, 0, 0, 0)
        self.left_label1 = QLabel('Low H', self)
        self.right_label1 = QLabel('0', self)
        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setRange(0, 255)
        self.sld1.valueChanged.connect(self.slide)
        hbox1.addItem(spacer)
        hbox1.addWidget(self.left_label1)
        hbox1.addWidget(self.sld1)
        hbox1.addWidget(self.right_label1)
        hbox1.addItem(spacer)

        # high H
        hbox2 = QHBoxLayout()
        hbox2.setContentsMargins(0, 0, 0, 0)
        self.left_label2 = QLabel('High H', self)
        self.right_label2 = QLabel('0', self)
        self.sld2 = QSlider(Qt.Horizontal, self)
        self.sld2.setRange(0, 255)
        self.sld2.valueChanged.connect(self.slide)
        hbox2.addItem(spacer)
        hbox2.addWidget(self.left_label2)
        hbox2.addWidget(self.sld2)
        hbox2.addWidget(self.right_label2)
        hbox2.addItem(spacer)

        # low S
        hbox3 = QHBoxLayout()
        hbox3.setContentsMargins(0, 0, 0, 0)
        self.left_label3 = QLabel('Low S', self)
        self.right_label3 = QLabel('0', self)
        self.sld3 = QSlider(Qt.Horizontal, self)
        self.sld3.setRange(0, 255)
        self.sld3.valueChanged.connect(self.slide)
        hbox3.addItem(spacer)
        hbox3.addWidget(self.left_label3)
        hbox3.addWidget(self.sld3)
        hbox3.addWidget(self.right_label3)
        hbox3.addItem(spacer)

        # high S
        hbox4 = QHBoxLayout()
        hbox4.setContentsMargins(0, 0, 0, 0)
        self.left_label4 = QLabel('High S', self)
        self.right_label4 = QLabel('0', self)
        self.sld4 = QSlider(Qt.Horizontal, self)
        self.sld4.setRange(0, 255)
        self.sld4.valueChanged.connect(self.slide)
        hbox4.addItem(spacer)
        hbox4.addWidget(self.left_label4)
        hbox4.addWidget(self.sld4)
        hbox4.addWidget(self.right_label4)
        hbox4.addItem(spacer)

        # low V
        hbox5 = QHBoxLayout()
        hbox5.setContentsMargins(0, 0, 0, 0)
        self.left_label5 = QLabel('Low V', self)
        self.right_label5 = QLabel('0', self)
        self.sld5 = QSlider(Qt.Horizontal, self)
        self.sld5.setRange(0, 255)
        self.sld5.valueChanged.connect(self.slide)
        hbox5.addItem(spacer)
        hbox5.addWidget(self.left_label5)
        hbox5.addWidget(self.sld5)
        hbox5.addWidget(self.right_label5)
        hbox5.addItem(spacer)

        # high V
        hbox6 = QHBoxLayout()
        hbox6.setContentsMargins(0, 0, 0, 0)
        self.left_label6 = QLabel('High V', self)
        self.right_label6 = QLabel('0', self)
        self.sld6 = QSlider(Qt.Horizontal, self)
        self.sld6.setRange(0, 255)
        self.sld6.valueChanged.connect(self.slide)
        hbox6.addItem(spacer)
        hbox6.addWidget(self.left_label6)
        hbox6.addWidget(self.sld6)
        hbox6.addWidget(self.right_label6)
        hbox6.addItem(spacer)
############################################################################

        # create hbox for capture
        hbox7 = QHBoxLayout()
        hbox7.setContentsMargins(0, 0, 0, 0)
        hbox7.addItem(spacer)
        hbox7.addWidget(self.label1)
        hbox7.addWidget(self.textbox)
        hbox7.addWidget(captureBtn)
        hbox7.addItem(spacer)

        # Create vbox layout ( will be the main layout including the hbox layout)
        vboxlayout = QVBoxLayout()
        vboxlayout.addLayout(hbox1)
        vboxlayout.addLayout(hbox2)
        vboxlayout.addLayout(hbox3)
        vboxlayout.addLayout(hbox4)
        vboxlayout.addLayout(hbox5)
        vboxlayout.addLayout(hbox6)
        vboxlayout.addWidget(self.label2)
        vboxlayout.addWidget(trainBtn)
        vboxlayout.addWidget(detectBtn)
        vboxlayout.addWidget(createBtn)
        vboxlayout.addLayout(hbox7)
        vboxlayout.addWidget(self.label3)

        # Set the layout to your window
        self.setLayout(vboxlayout)

    # On changing slider value this method is executed
    def slide(self):
        h_low = str(self.sld1.value())
        h_high = str(self.sld2.value())
        s_low = str(self.sld3.value())
        s_high = str(self.sld4.value())
        v_low = str(self.sld5.value())
        v_high = str(self.sld6.value())

        self.right_label1.setText(h_low)
        self.right_label2.setText(h_high)
        self.right_label3.setText(s_low)
        self.right_label4.setText(s_high)
        self.right_label5.setText(v_low)
        self.right_label6.setText(v_high)

        file = open('hsv_values.txt', 'w')
        file.write(h_low + ' ' + h_high + ' ' + s_low + ' ' + s_high + ' ' + v_low + ' ' + v_high)
        file.close()

    # On clicking Train The Model button this method is executed
    def train(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("model is training..........")
        msgBox.setWindowTitle("Training info")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.label3.setText("model is training........")

        cnn_model.train()
        self.label3.setText("model has completed the training.")

    # On clicking Detect button this method is executed
    def detect(self):
        recognise.recognise()

    # On clicking Capture button this method is executed
    def capture(self):
        ges_name = self.textbox.text()
        capture.create(ges_name)

    # On clicking Create New Sign button this method is executed
    def addSign(self):
        ges_name = self.textbox.text()
        capture.create(ges_name)


# Initiate the application
app = QApplication(sys.argv)
app.setStyle("Fusion")
window = Window()
sys.exit(app.exec_())
