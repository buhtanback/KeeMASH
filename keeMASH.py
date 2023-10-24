
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice


app = QtWidgets.QApplication([])
ui = uic.loadUi("keeMASH.ui")
ui.setWindowTitle("keeMASH")

serial = QSerialPort()
serial.setBaudRate(9600)
portList = []
ports = QSerialPortInfo().availablePorts()

for port in ports:
    portList.append(port.portName())
ui.comboBox.addItems(portList)

def onOpen(): # ok
    serial.setPortName(ui.comboBox.currentText())
    serial.open(QIODevice.ReadWrite)
    sendi("garland_echo")
    sendi("red_led_echo")

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

#def mod_change_fid(value: str):
#    match value:
#        case "": sendi("")
#        case "": sendi("")
#        case "02255": sendi("")



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

    #mod_change_fid(data[0])


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

ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)
ui.pushB.clicked.connect(lambda: sendi("garland"))
ui.redB.clicked.connect(lambda: sendi("power"))

ui.speedBU.clicked.connect(lambda: sendi("red_led_speed+"))
ui.speedBD.clicked.connect(lambda: sendi("red_led_speed-"))


ui.show()
app.exec()
