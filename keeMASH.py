from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QTimer, QTime, pyqtSignal
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox
import sqlite3
import datetime


app = QtWidgets.QApplication([])
ui = uic.loadUi("keeMASH.ui")
ui.setWindowTitle("keeMASH")

msg = QMessageBox()
msg.setIcon(QMessageBox.Information)
msg.setText("яїчка готові")
msg.setWindowTitle("яйовар")
msg.setStandardButtons(QMessageBox.Ok)

serial = QSerialPort()
serial.setBaudRate (115200)
portList = []
ports = QSerialPortInfo().availablePorts()

for port in ports:
    portList.append(port.portName())
ui.comboBox.addItems(portList)

def onOpen():
    serial.setPortName(ui.comboBox.currentText())
    serial.open(QIODevice.ReadWrite)

def feedback():
    commands = [("garland_echo", 1300), ("red_led_echo", 1300), ("sens_echo", 1300), ("choinka", 1300), ("bedside_echo", 1300), ("echo_turb", 1300), ("lamech", 1300)]
    for i, (command, delay) in enumerate(commands):
        QTimer.singleShot(sum(item[1] for item in commands[:i+1]), lambda cmd=command: sendi(cmd))
    print("feeeeeeeeeeee")

def onClose():
    serial.close()

def sendi (datic):
    serial.writeData(datic.encode('utf-8'))
def set_col_ind (x, u, y):
    getattr(ui, x).setCurrentIndex(u)
    getattr(ui, x).setStyleSheet(f"background-color: {y}; color: white;")

def turboBox_change(index):
    sendi(f'14{index}')
def modBoxR_change(index):
    sendi(f'01_mode_{index}')
def colorBox_change(index):
    sendi(f'18{index}')
def watLBox_change(index):
    if index <= 9:
        sendi(f'19{index}')
    else: sendi(f'19M')
def briBoxR_change(index):
    if index <= 9:
        sendi(f'02_bri_{index}')
    else: sendi(f'02_bri_M')
def mod_change_fid(x):
    if x[:2] == '01':
        set_col_ind("modBoxR", int(x[-1]), "grey")

def mod_colorBox_fid(x):
    if x[:2] == '21':
        set_col_ind("colorBox", int(x[-1]), "grey")

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

def watLBox_change_fid(x):
    match x:
        case "200": set_col_ind("watLBox", 0, "grey")
        case "2026": set_col_ind("watLBox", 1, "grey")
        case "2051": set_col_ind("watLBox", 2, "grey")
        case "2077": set_col_ind("watLBox", 3, "grey")
        case "20102": set_col_ind("watLBox", 4, "grey")
        case "20128": set_col_ind("watLBox", 5, "grey")
        case "20153": set_col_ind("watLBox", 6, "grey")
        case "20179": set_col_ind ("watLBox", 7, "grey")
        case "20204": set_col_ind ("watLBox", 8, "grey")
        case "20230": set_col_ind ("watLBox", 9, "grey")
        case "20255": set_col_ind ("watLBox", 10, "grey")

def reti():                                # тут можуть бути баги
    txt = "05" + ui.spedE.text()
    ui.spedE.clear()
    sendi(txt)
def send2mash():                                # тут можуть бути баги
    sendi(ui.sendL.text())
    ui.sendL.clear()

def onRead():
    rx = serial.readLine()
    rxs = str (rx, "utf-8").strip()
    data = rxs.split(",")
    print(data)

    if data[0] == 'hello':
        ui.openB.setStyleSheet("background-color: green; color: white;")
        feedback()

    if data[0] == 'jajo_on':
        msg.exec_()

    if data[0] == 'pimpa':
        ui.pumpB.setStyleSheet("background-color: green; color: white;")
    #if data[0] == 'turbo1':
        #ui.turbo1B.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'garland_on':
        ui.pushB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'garland_off':
        ui.pushB.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'redled_on':
        ui.redB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'redled_off':
        ui.redB.setStyleSheet("background-color: black; color: white;")

    if data[0] == 'bedside_on':
        ui.bedLB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'bedside_off':
        ui.bedLB.setStyleSheet("background-color: black; color: white;")

    if data[0][:2] == '03':
        spF = data[0][2:]
        ui.lcdSp.display(spF)

    if data[0][:2] == '04':
        ppm = data[0][2:]
        ui.lcdPpm.display(ppm)
        ui.ppmB.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '05':
        temp = data[0][2:]
        ui.lcdTemp.display(temp)
        ui.tempB.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '06':
        humi = data[0][2:]
        ui.lcdHumi.display(humi)
        ui.humiB.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '07':
        lux = data[0][2:]
        ui.lcdLux.setDigitCount(7)
        ui.lcdLux.display(lux)
        ui.luxB.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '08':
        atm = data[0][2:]
        ui.lcdAtm.setDigitCount(6)
        ui.lcdAtm.display(atm)
        ui.atmB.setStyleSheet("background-color: green; color: white;")

    #if data[0][:2] == '09':
        #cho = data[0][2:]
        #add_choinka_db(cho)
        #update_choT()
        #ui.choB.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '10':
        pm1 = data[0][2:]
        ui.lcdpm1.display(pm1)
        ui.pm1B.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '11':
        pm2 = data[0][2:]
        ui.lcdpm2.display(pm2)
        ui.pm2B.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '12':
        pm10 = data[0][2:]
        ui.lcdpm10.display(pm10)
        ui.pm10B.setStyleSheet("background-color: green; color: white;")

    if data[0][:2] == '13':
        x = data[0][2:]
        if x == '1':
            ui.pumpB.setStyleSheet("background-color: green; color: white;")
        else: ui.pumpB.setStyleSheet("background-color: black; color: white;")

    if data[0][:2] == '14':
        x = data[0][2:]
        if x == '0':
            ui.turboBox.setStyleSheet("background-color: black; color: white;")
        else: ui.turboBox.setStyleSheet("background-color: grey; color: white;")

    if data[0][:2] == '16':
        x = data[0][2:]
        if x == '1':
            ui.flowB.setStyleSheet("background-color: green; color: white;")
        else: ui.flowB.setStyleSheet("background-color: black; color: white;")

    if data[0][:2] == '17':
        x = data[0][2:]
        if x == '1':
            ui.ionB.setStyleSheet("background-color: green; color: white;")
        else: ui.ionB.setStyleSheet("background-color: black; color: white;")

    if data[0][:2] == '15':
        ui.huB.setStyleSheet("background-color: green; color: white;")

        if data[0][2:3] == '0':
            ui.turboBox.setStyleSheet("background-color: black; color: white;")
            ui.turboBox.setCurrentIndex(0)
        elif data[0][2:3] == '1':
            ui.turboBox.setCurrentIndex(1)
            ui.turboBox.setStyleSheet("background-color: grey; color: white;")
        elif data[0][2:3] == '2':
            ui.turboBox.setCurrentIndex(2)
            ui.turboBox.setStyleSheet("background-color: grey; color: white;")
        else:
            ui.turboBox.setCurrentIndex(3)
            ui.turboBox.setStyleSheet("background-color: grey; color: white;")

        if data[0][3:4] == '0':
            ui.pumpB.setStyleSheet("background-color: green; color: white;")
        else: ui.pumpB.setStyleSheet("background-color: black; color: white;")

        if data[0][4:5] == '0':
            ui.flowB.setStyleSheet("background-color: green; color: white;")
        else: ui.flowB.setStyleSheet("background-color: black; color: white;")

        if data[0][5:6] == '0':
            ui.ionB.setStyleSheet("background-color: green; color: white;")
        else: ui.ionB.setStyleSheet("background-color: black; color: white;")

    if data[0][:2] == 'La':
        x = data[0][2:]
        if x == '1':
            ui.lamB.setStyleSheet("background-color: green; color: white;")
        else: ui.lamB.setStyleSheet("background-color: black; color: white;")

    watLBox_change_fid(data[0])
    mod_colorBox_fid(data[0])

    mod_change_fid(data[0])
    bri_change_fid(data[0])
#///////////////////////////////////////////////
def checkEvent_1():
    if ui.checkEvent_1.isChecked():
        print("Чекбокс встановлено")
    else:
        print("Чекбокс скасовано")
def checkEvent_2():
    if ui.checkEvent_2.isChecked():
        print("Чекбокс встановлено")
    else:
        print("Чекбокс скасовано")
def readT1():
    time = ui.timeEvent_1.time()
    #print("Час1:", time.toString("hh:mm:ss"))
def readT2():
    time = ui.timeEvent_2.time()
    #print("Час2:", time.toString("hh:mm:ss"))
def saveT1():
    saved_text = ui.lineEvent_1.text()
    sendi( saved_text)
    readT1()
def saveT2():
    saved_text = ui.lineEvent_2.text()
    sendi( saved_text)
    readT2()

def updox_change(s):
    if s == QtCore.Qt.Checked:
        print("Чекбокс 'updox' встановлено")

    else:
        print("Чекбокс 'updox' скасовано")

#/////////////////////////////////////////////////////

class TimerWidget(QtWidgets.QWidget):
    timer1_timeout = QtCore.pyqtSignal()
    timer2_timeout = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.timer1 = QtCore.QTimer(self)
        self.timer1.timeout.connect(self.timer1_timeout.emit)

        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.timer2_timeout.emit)

        ui.timeEvent_1.timeChanged.connect(self.set_timer1)
        ui.timeEvent_2.timeChanged.connect(self.set_timer2)

        self.timer1_timeout.connect(saveT1)
        self.timer2_timeout.connect(saveT2)

        ui.checkEvent_1.stateChanged.connect(self.toggle_timer1)
        ui.checkEvent_2.stateChanged.connect(self.toggle_timer2)

    def set_timer1(self):
        if ui.checkEvent_1.isChecked():
            time = ui.timeEvent_1.time()
            self.timer1.setSingleShot(True)
            self.timer1.setInterval(QTime.currentTime().msecsTo(time))
            self.timer1.start()

    def set_timer2(self):
        if ui.checkEvent_2.isChecked():
            time = ui.timeEvent_2.time()
            self.timer2.setSingleShot(True)
            self.timer2.setInterval(QTime.currentTime().msecsTo(time))
            self.timer2.start()

    def toggle_timer1(self, state):
        if state == QtCore.Qt.Checked:
            self.set_timer1()
        else:
            self.timer1.stop()

    def toggle_timer2(self, state):
        if state == QtCore.Qt.Checked:
            self.set_timer2()
        else:
            self.timer2.stop()


timer_widget = TimerWidget()

###############
ui.colorBox.activated.connect(colorBox_change)
ui.watLBox.activated.connect(watLBox_change)

ui.modBoxR.activated.connect(modBoxR_change)
ui.briBoxR.activated.connect(briBoxR_change)

ui.turboBox.activated.connect(turboBox_change)

serial.readyRead.connect(onRead)

ui.upB.clicked.connect(feedback)

ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.updox.stateChanged.connect(updox_change)

ui.bedLB.clicked.connect(lambda: sendi("bedside"))
ui.pushB.clicked.connect(lambda: sendi("garland"))
ui.redB.clicked.connect(lambda: sendi("power"))
ui.lamB.clicked.connect(lambda: sendi("lam"))

ui.ppmB.clicked.connect(lambda: sendi("ppm_echo"))
ui.tempB.clicked.connect(lambda: sendi("temp_echo"))
ui.humiB.clicked.connect(lambda: sendi("humi_echo"))
ui.luxB.clicked.connect(lambda: sendi("lux_echo"))
ui.atmB.clicked.connect(lambda: sendi("atm_echo"))

ui.pumpB.clicked.connect(lambda: sendi("pomp"))
ui.flowB.clicked.connect(lambda: sendi("flow"))
ui.ionB.clicked.connect(lambda: sendi("ion"))
ui.huB.clicked.connect(lambda: sendi("huOn"))


ui.jajoB.clicked.connect(lambda: sendi("jajo"))

ui.speedBU.clicked.connect(lambda: sendi("redl_sp+"))
ui.speedBD.clicked.connect(lambda: sendi("redl_sp-"))

ui.spedE.returnPressed.connect(reti)
ui.sendL.returnPressed.connect(send2mash)

ui.show()
app.exec()