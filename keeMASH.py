
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QTimer
import sqlite3
import datetime

choBD = sqlite3.connect('choinka_data.db')

app = QtWidgets.QApplication([])
ui = uic.loadUi("keeMASH.ui")
ui.setWindowTitle("keeMASH")

serial = QSerialPort()
serial.setBaudRate (115200)
portList = []
ports = QSerialPortInfo().availablePorts()

for port in ports:
    portList.append(port.portName())
ui.comboBox.addItems(portList)

def clear_cho_table():
    cursor = choBD.cursor()
    cursor.execute("DELETE FROM humidity")

    choBD.commit()
    cursor.close()

def get_cho():
    cursor = choBD.cursor()
    cursor.execute("SELECT * FROM humidity ORDER BY date DESC LIMIT 8")
    results = cursor.fetchall()
    cursor.close()
    return results

def update_choT():

    first_measurements = get_cho()
    display_text = ""
    for date, humidity in first_measurements:
        display_text += f"{date} choinka {humidity}\n"

    ui.choT.setText(display_text)

def add_choinka_db(x):
    choBD = sqlite3.connect('choinka_data.db')
    c = choBD.cursor()
    c.execute("INSERT INTO humidity (date, humidity_level) VALUES (?, ?)",
              (datetime.datetime.now().strftime("%m-%d %H:%M"), x))
    choBD.commit()
    choBD.close()

def onOpen():
    serial.setPortName(ui.comboBox.currentText())
    serial.open(QIODevice.ReadWrite)

def feedback():
    commands = [("garland_echo", 1900), ("red_led_echo", 1900), ("sens_echo", 1900), ("choinka", 1900), ("bedside_echo", 1900)]
    for i, (command, delay) in enumerate(commands):
        QTimer.singleShot(sum(item[1] for item in commands[:i+1]), lambda cmd=command: sendi(cmd))
    print("feeeeeeeeeeee")

def onClose():
    serial.close()
    #clear_cho_table()

def sendi (datic):
    serial.writeData(datic.encode('utf-8'))

def modBoxR_change(index):
    sendi(f'01_mode_{index}')

def set_col_ind (x, u, y):
    getattr(ui, x).setCurrentIndex(u)
    getattr(ui, x).setStyleSheet(f"background-color: {y}; color: white;")

def mod_change_fid(x):
    if x[:2] == '01':
        set_col_ind("modBoxR", int(x[-1]), "grey")

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
    if index <= 9:
        sendi(f'02_bri_{index}')
    else: sendi(f'02_bri_M')

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

    if data[0] == 'pimpa':
        ui.pumpB.setStyleSheet("background-color: green; color: white;")
    if data[0] == 'turbo1':
        ui.turbo1B.setStyleSheet("background-color: black; color: white;")

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
        ui.bedLB.setStyleSheet("background-color: green; color: white;")

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

    if data[0][:2] == '09':
        cho = data[0][2:]
        add_choinka_db(cho)
        update_choT()
        ui.choB.setStyleSheet("background-color: green; color: white;")

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
        if x == '1':
            ui.turbo1B.setStyleSheet("background-color: green; color: white;")
        else: ui.turbo1B.setStyleSheet("background-color: black; color: white;")



    mod_change_fid(data[0])
    bri_change_fid(data[0])


ui.modBoxR.activated.connect(modBoxR_change)
ui.briBoxR.activated.connect(briBoxR_change)

serial.readyRead.connect(onRead)

ui.upB.clicked.connect(feedback)

ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.bedLB.clicked.connect(lambda: sendi("bedside"))
ui.pushB.clicked.connect(lambda: sendi("garland"))
ui.redB.clicked.connect(lambda: sendi("power"))

ui.ppmB.clicked.connect(lambda: sendi("ppm_echo"))
ui.tempB.clicked.connect(lambda: sendi("temp_echo"))
ui.humiB.clicked.connect(lambda: sendi("humi_echo"))
ui.luxB.clicked.connect(lambda: sendi("lux_echo"))
ui.atmB.clicked.connect(lambda: sendi("atm_echo"))

ui.pumpB.clicked.connect(lambda: sendi("pomp"))
ui.turbo1B.clicked.connect(lambda: sendi("turbo1"))

ui.choB.clicked.connect(lambda: sendi("choinka"))

ui.speedBU.clicked.connect(lambda: sendi("redl_sp+"))
ui.speedBD.clicked.connect(lambda: sendi("redl_sp-"))

ui.spedE.returnPressed.connect(reti)
ui.sendL.returnPressed.connect(send2mash)

ui.show()
app.exec()
