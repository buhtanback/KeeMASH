
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
#import time
import threading


app = QtWidgets.QApplication([])
ui = uic.loadUi("keeMASH.ui")
ui.setWindowTitle("keeMASH")

serial = QSerialPort()
serial.setBaudRate (9600)
portList = []
ports = QSerialPortInfo().availablePorts()

for port in ports:
    portList.append(port.portName())
ui.comboBox.addItems(portList)

def onOpen():
    serial.setPortName(ui.comboBox.currentText())
    serial.open(QIODevice.ReadWrite)
    # feedback()

def feedback():
    commands = [("garland_echo", 100), ("red_led_echo", 1000)]
    for i, (command, delay) in enumerate(commands):
        QTimer.singleShot(sum(item[1] for item in commands[:i+1]), lambda cmd=command: sendi(cmd))
    print("feeeeeeeeeeee")

# def feedback():
#     QTimer.singleShot(100, lambda: sendi("garland_echo"))
#     QTimer.singleShot(1000, lambda: sendi("red_led_echo"))
#     print("feeeeeeeeeeee")

def onClose():
    serial.close()

def sendi (datic):
    serial.writeData(datic.encode('utf-8'))

def modBoxR_change(index):
    print("Selected index modBoxR:", index)
    match index :
        case 0 : sendi("01_mode_0")
        case 1 : sendi("01_mode_1")
        case 2 : sendi("01_mode_2")
        case 3 : sendi("01_mode_3")
        case 4 : sendi("01_mode_4")
        case 5 : sendi("01_mode_5")
        case 6 : sendi("01_mode_6")
        case 7 : sendi("01_mode_7")
        case 8 : sendi("01_mode_8")
        case 9 : sendi("01_mode_9")
def set_col_ind (x, u, y):
    getattr(ui, x).setCurrentIndex(u)
    getattr(ui, x).setStyleSheet(f"background-color: {y}; color: white;")
def mod_change_fid(x):
    match x:
        case "01_mode_0": set_col_ind("modBoxR", 0, "grey")
        case "01_mode_1": set_col_ind("modBoxR", 1, "grey")
        case "01_mode_2": set_col_ind("modBoxR", 2, "grey")
        case "01_mode_3": set_col_ind("modBoxR", 3, "grey")
        case "01_mode_4": set_col_ind("modBoxR", 4, "grey")
        case "01_mode_5": set_col_ind("modBoxR", 5, "grey")
        case "01_mode_6": set_col_ind("modBoxR", 6, "grey")
        case "01_mode_7": set_col_ind ("modBoxR", 7, "grey")
        case "01_mode_8": set_col_ind ("modBoxR", 8, "grey")
        case "01_mode_9": set_col_ind ("modBoxR", 9, "grey")

def bri_change_fid(x):
    match x:
        case "020": set_col_ind("briBoxR", 0, "grey")
        case "0226": set_col_ind("briBoxR", 1, "grey")
        case "0251": set_col_ind("briBoxR", 2, "grey")
        case "0277": set_col_ind("briBoxR", 3, "grey")
        case "02102": set_col_ind("briBoxR", 4, "grey")
        case "02128": set_col_ind("briBoxR", 5, "grey")
        case "02153": set_col_ind("briBoxR", 6, "grey")
        case "02179": set_col_ind ("briBoxR", 7, "grey")
        case "02204": set_col_ind ("briBoxR", 8, "grey")
        case "02230": set_col_ind ("briBoxR", 9, "grey")
        case "02255": set_col_ind ("briBoxR", 10, "grey")

def briBoxR_change(index):
    print("Selected index briBoxR:", index)
    match index :
        case 0 : sendi("02_bri_0")
        case 1 : sendi("02_bri_1")
        case 2 : sendi("02_bri_2")
        case 3 : sendi("02_bri_3")
        case 4 : sendi("02_bri_4")
        case 5 : sendi("02_bri_5")
        case 6 : sendi("02_bri_6")
        case 7 : sendi("02_bri_7")
        case 8 : sendi("02_bri_8")
        case 9 : sendi("02_bri_9")
        case 10 : sendi("02_bri_M")

def onRead():
    rx = serial.readLine()
    rxs = str (rx, "utf-8").strip()
    data = rxs.split(",")
    print(data)

    if data[0] == 'hello':
        ui.openB.setStyleSheet("background-color: green; color: white;")

    if data[0] == 'garland_on':
        ui.pushB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'garland_off':
        ui.pushB.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'redled_on':
        ui.redB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'redled_off':
        ui.redB.setStyleSheet("background-color: black; color: white;")

    mod_change_fid(data[0])
    bri_change_fid(data[0])


        #if len(data) == 3:
            #if data[2] != '_' :
                #ui.modBoxR.setCurrentIndex(int(data[2]))
                #ui.modBoxR.setStyleSheet("background-color: grey; color: white;")

        #if len(data) == 4:
            #print("0000000000000000")
            #if data[3] != '_' :
                #print("dedthdthdhtedherbdf")
                #if data[3] == 'M' :
                    #ui.briBoxR.setCurrentIndex(10)
                    #ui.briBoxR.setStyleSheet("background-color: grey; color: white;")

        #if len(data) >= 4:
        #    print("dedthdthdhtedherbdf")
            #if int(data[2]) >= 0 and int(data[2]) <= 9:
                #ui.modBoxR.setCurrentIndex(int(data[2]))
                #ui.modBoxR.setStyleSheet("background-color: grey; color: white;")



ui.modBoxR.activated.connect(modBoxR_change)
ui.briBoxR.activated.connect(briBoxR_change)

serial.readyRead.connect(onRead)

ui.upB.clicked.connect(feedback)

ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)
ui.pushB.clicked.connect(lambda: sendi("garland"))
ui.redB.clicked.connect(lambda: sendi("power"))

ui.speedBU.clicked.connect(lambda: sendi("red_led_speed+"))
ui.speedBD.clicked.connect(lambda: sendi("red_led_speed-"))


ui.show()
app.exec()
