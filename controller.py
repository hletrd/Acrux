import serial
import serial.tools.list_ports

from PyQt5.QtWidgets import * #QApplication, QWidget, QPushButton, QLineEdit, QListView
from PyQt5.QtGui import * #QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import *

import sqlite3

import sys, argparse, pkgutil, os.path

#from flask import Flask

def log(description):
	print(description)

v='0.2.2'

txt = {
	'inpserial': '시리얼 포트',
	'title': 'Acrux ' + v,
	'connect': '연결',
	'message': '메시지',
	'quit': '종료하시겠습니까?',
	'catsearch': '카탈로그 검색',
	'selectslew': '선택한 대상으로 GOTO',
	'stopslew': '적도의 정지',
	'mountra': '적도의 적경',
	'mountdec': '적도의 적위',
	'objectname': '대상 이름',
	'objectra': '대상 적경',
	'objectdec': '대상 적위',
	'constellation': '별자리',
	'commonname': '다른 이름',
	'type': '종류',
	'magnitude': '등급',
	'connected': '연결됨',
	'nc': '연결 안 됨',
	'status': '상태',
	'connectfailed': '연결 실패',
	'speed': '속도',
	'nightmodeon': '야간 모드 켜기',
	'nightmodeoff': '야간 모드 끄기',
	'sync': '선택한 대상에 Sync',
	'park': 'Park',
	'warning': '경고',
	'belowhorizon': '대상이 지평선 아래에 있습니다.',
	'notsynced': 'Sync를 해야 GOTO를 사용할 수 있습니다.',
	'by': 'ACRUX ' + v + ' by HLETRD',
	'star': '별',
	'galaxy': '은하',
	'opencluster': '산개성단',
	'globularcluster': '구상성단',
	'nebula': '성운',
	'join': ' 및 ',
	'galaxycloud': '은하수',
	'planetarynebula': '행성상 성운',
	'asterism': '성군',
	'darknebula': '암흑 성운',
	'customslew': '직접 입력한 좌표로 GOTO',
	'ra': '적경',
	'dec': '적위',
	'h': '시',
	'm': '분',
	's': '초',
	'd': '도',
	'slew': '입력한 좌표로 GOTO',

	'And': '안드로메다자리',
	'Ant': '공기펌프자리',
	'Aps': '극락조자리',
	'Aqr': '물병자리',
	'Aql': '독수리자리',
	'Ara': '제단자리',
	'Ari': '양자리',
	'Aur': '마차부자리',
	'Boo': '목동자리',
	'Cae': '조각칼자리',
	'Cam': '기린자리',
	'Cnc': '게자리',
	'CVn': '사냥개자리',
	'CMa': '큰개자리',
	'CMi': '작은개자리',
	'Cap': '염소자리',
	'Car': '용골자리',
	'Cas': '카시오페이아자리',
	'Cen': '센타우루스자리',
	'Cep': '세페우스자리',
	'Cet': '고래자리',
	'Cha': '카멜레온자리',
	'Cir': '컴퍼스자리',
	'Col': '비둘기자리',
	'Com': '머리털자리',
	'CrA': '남쪽왕관자리',
	'CrB': '북쪽왕관자리',
	'Crv': '까마귀자리',
	'Crt': '컵자리',
	'Cru': '남십자자리',
	'Cyg': '백조자리',
	'Del': '돌고래자리',
	'Dor': '황새치자리',
	'Dra': '용자리',
	'Equ': '조랑말자리',
	'Eri': '에리다누스자리',
	'For': '화로자리',
	'Gem': '쌍둥이자리',
	'Gru': '두루미자리',
	'Her': '헤르쿨레스자리',
	'Hor': '시계자리',
	'Hya': '바다뱀자리',
	'Hyi': '물뱀자리',
	'Ind': '인디언자리',
	'Lac': '도마뱀자리',
	'Leo': '사자자리',
	'LMi': '작은사자자리',
	'Lep': '토끼자리',
	'Lib': '천칭자리',
	'Lup': '이리자리',
	'Lyn': '살쾡이자리',
	'Lyr': '거문고자리',
	'Men': '테이블산자리',
	'Mic': '현미경자리',
	'Mon': '외뿔소자리',
	'Mus': '파리자리',
	'Nor': '직각자자리',
	'Oct': '팔분의자리',
	'Oph': '뱀주인자리',
	'Ori': '오리온자리',
	'Pav': '공작자리',
	'Peg': '페가수스자리',
	'Per': '페르세우스자리',
	'Phe': '불사조자리',
	'Pic': '화가자리',
	'Psc': '물고기자리',
	'PsA': '남쪽물고기자리',
	'Pup': '고물자리',
	'Pyx': '나침반자리',
	'Ret': '그물자리',
	'Sge': '화살자리',
	'Sgr': '궁수자리',
	'Sco': '전갈자리',
	'Scl': '조각가자리',
	'Sct': '방패자리',
	'Ser': '뱀자리',
	'Sex': '육분의자리',
	'Tau': '황소자리',
	'Tel': '망원경자리',
	'Tri': '삼각형자리',
	'TrA': '남쪽삼각형자리',
	'Tuc': '큰부리새자리',
	'UMa': '큰곰자리',
	'UMi': '작은곰자리',
	'Vel': '돛자리',
	'Vir': '처녀자리',
	'Vol': '날치자리',
	'Vul': '여우자리'
	
	
}

'''if not os.path.isfile('dso.db'):
	dso_db = pkgutil.get_data('data', 'dso.db')
	f = open('dso.db', 'w')
	f.write(dso_db)
	star_db = pkgutil.get_data('data', 'star.db')
	f = open('star.db', 'w')
	f.write(star_db)'''

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

print(sys._MEIPASS)

try:
	db = resource_path('dso.db')
	dbc = sqlite3.connect(db, check_same_thread=False)
	dbc.text_factory = str
	c = dbc.cursor()

	db_star = resource_path('star.db')
	dbc_star = sqlite3.connect(db_star, check_same_thread=False)
	dbc_star.text_factory = str
	c_star = dbc_star.cursor()
except:
	import time
	time.sleep(30)

ser = serial.Serial()
ser.baudrate = 9600
ser.timeout = 0.1
refreshinterval = 100

objdata = []
selectedobj = None

def getDSOName(dso):
	if dso[1] != '':
		return dso[7] + ' ' + str(dso[8]) + ' (' + dso[1] + ')'
	else:
		return dso[7] + ' ' + str(dso[8])

def convRA(RA):
	RAH = int(RA)
	RAM = int((RA-RAH)*60)
	RAS = int(round(((RA-RAH)*60-RAM)*60))
	return [RAH, RAM, RAS]

def convDEC(DEC):
	sign = 1 if abs(DEC) == DEC else -1
	dectmp = abs(DEC)
	DECD = int(dectmp)
	DECM = int((dectmp-DECD)*60)
	DECS = int(round(((dectmp-DECD)*60-DECM)*60))
	return [sign, DECD, DECM, DECS]

def serialwrite(window_main, data):
	global ser
	print(data)
	try:
		ser.write(data.encode())
	except:
		print("Serial Error")
		if window_main != None:
			window_main.status = False

def flushserial():
	global ser 
	ser.reset_input_buffer()

def serialread(length):
	global ser
	try:
		data = ser.read(length).decode('utf-8')
		print('"' + data + '"')
		return data
	except:
		#if length == 9:
		#	return '04:54:23#'
		#else:
		#	return "-32*34'23#"
		pass

def makestatus(status):
	return '<b>' + txt['status'] + ' </b>' + status

def gettype(typetext):
	if typetext == 'Gxy':
		return txt['galaxy']
	elif typetext == 'OC':
		return txt['opencluster']
	elif typetext == 'GC':
		return txt['globularcluster']
	elif typetext == 'Neb':
		return txt['nebula']
	elif typetext == 'GxyCld':
		return txt['galaxycloud']
	elif typetext == 'PN':
		return txt['planetarynebula']
	elif typetext == 'Ast':
		return txt['asterism']
	elif typetext == 'DN':
		return txt['darknebula']
	elif '+' in typetext:
		return gettype(typetext.split('+')[0]) + txt['join'] + gettype(typetext.split('+')[1])
	else:
		return typetext

def getconst(sym):
	return sym[:3] + ' (' + txt[sym[:3]] + ')'

def slew(RA, DEC):
	DEC = convDEC(DEC)
	sign = "-" if DEC[0] < 0 else "+"
	for i in range(1, 4):
		if DEC[i] < 10:
			DEC[i] = '0' + str(DEC[i])
		else:
			DEC[i] = str(DEC[i])

	RA = convRA(RA)
	for i in range(0, 3):
		if RA[i] < 10:
			RA[i] = '0' + str(RA[i])
		else:
			RA[i] = str(RA[i])
	serialwrite(None, ':Sd' + sign + DEC[1] + '*' + DEC[2] + ':' + DEC[3] + '#')
	result = serialread(1)
	serialwrite(None, ':Sr' + RA[0] + ':' + RA[1] + ':' + RA[2] + '#')
	result = serialread(1)
	serialwrite(None, ':MS#')
	result = serialread(1)
	return result



class DInputCoor(QDialog):
	def __init__(self, parent=None):
		super(DInputCoor, self).__init__(parent)
		self.layoutMain = QVBoxLayout(self)

		global MountRA, MountDEC
		RA = convRA(MountRA)
		DEC = convDEC(MountDEC)

		self.layout1 = QHBoxLayout(self)
		self.labelRA = QLabel(self)
		self.labelRA.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelRA.setText('<b>' + txt['ra'] + '</b>')
		self.layout1.addWidget(self.labelRA)
		self.layout1.addSpacing(10)

		self.inpRAh = QLineEdit(self)
		self.inpRAh.setText(str(RA[0]))
		self.inpRAh.setValidator(QIntValidator(0, 24))
		self.layout1.addWidget(self.inpRAh)

		self.labelRA = QLabel(self)
		self.labelRA.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelRA.setText(txt['h'])
		self.layout1.addWidget(self.labelRA)
		self.layout1.addSpacing(10)


		self.inpRAm = QLineEdit(self)
		self.inpRAm.setText(str(RA[1]))
		self.inpRAm.setValidator(QIntValidator(0, 60))
		self.layout1.addWidget(self.inpRAm)

		self.labelRA = QLabel(self)
		self.labelRA.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelRA.setText(txt['m'])
		self.layout1.addWidget(self.labelRA)
		self.layout1.addSpacing(10)


		self.inpRAs = QLineEdit(self)
		self.inpRAs.setText(str(RA[2]))
		self.inpRAs.setValidator(QIntValidator(0, 60))
		self.layout1.addWidget(self.inpRAs)

		self.labelRA = QLabel(self)
		self.labelRA.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelRA.setText(txt['s'])
		self.layout1.addWidget(self.labelRA)
		self.layout1.addSpacing(10)




		self.layoutMain.addLayout(self.layout1)
		self.layoutMain.addSpacing(10)

		self.layout2 = QHBoxLayout(self)
		self.labelDEC = QLabel(self)
		self.labelDEC.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelDEC.setText('<b>' + txt['dec'] + '</b>')
		self.layout2.addWidget(self.labelDEC)
		self.layout2.addSpacing(10)

		DEC[0] = '-' if DEC[0] == -1 else ''

		self.inpDECd = QLineEdit(self)
		self.inpDECd.setText(str(DEC[1]))
		self.inpDECd.setValidator(QIntValidator(-90, 90))
		self.layout2.addWidget(self.inpDECd)

		self.labelDEC = QLabel(self)
		self.labelDEC.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelDEC.setText(txt['d'])
		self.layout2.addWidget(self.labelDEC)
		self.layout2.addSpacing(10)


		self.inpDECm = QLineEdit(self)
		self.inpDECm.setText(str(DEC[2]))
		self.inpDECm.setValidator(QIntValidator(0, 60))
		self.layout2.addWidget(self.inpDECm)

		self.labelDEC = QLabel(self)
		self.labelDEC.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelDEC.setText(txt['m'])
		self.layout2.addWidget(self.labelDEC)
		self.layout2.addSpacing(10)


		self.inpDECs = QLineEdit(self)
		self.inpDECs.setText(str(DEC[3]))
		self.inpDECs.setValidator(QIntValidator(0, 60))
		self.layout2.addWidget(self.inpDECs)

		self.labelDEC = QLabel(self)
		self.labelDEC.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelDEC.setText(txt['s'])
		self.layout2.addWidget(self.labelDEC)
		self.layout2.addSpacing(10)


		self.layoutMain.addLayout(self.layout2)

		self.btnSlew = QPushButton(txt['slew'], self)
		self.btnSlew.clicked.connect(self.click_btnSlew)
		self.layoutMain.addWidget(self.btnSlew)


		self.setLayout(self.layoutMain)
		self.setFixedSize(300, 150)

	def click_btnSlew(self, parent=None):
		RAh = int(self.inpRAh.text())
		RAm = int(self.inpRAm.text())
		RAs = int(self.inpRAs.text())

		DECd = int(self.inpDECd.text())
		DECm = int(self.inpDECm.text())
		DECs = int(self.inpDECs.text())

		RA = RAh + RAm / 60. + RAs / 60. / 60.
		DEC = DECd + DECm / 60. + DECs / 60. / 60. 
		
		slew(RA, DEC)
		self.close()





class WMain(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		'''self.inpSerial = QLineEdit(self)
		self.inpSerial.setPlaceholderText(txt['inpserial'])
		self.inpSerial.resize(100, 20)
		self.inpSerial.move(15, 15)'''

		serlist = serial.tools.list_ports.comports()
		serlist_cmb = []

		for i in serlist:
			serlist_cmb.append(i[0])

		self.layoutMain = QVBoxLayout(self)


		self.layout1 = QHBoxLayout(self)

		self.cmbSerial = QComboBox(self)
		self.cmbSerial.addItems(serlist_cmb)
		self.cmbSerial.resize(150, 20)
		#self.cmbSerial.move(15, 15)
		self.cmbSerial.setCurrentIndex(0)

		self.layout1.addWidget(self.cmbSerial)


		self.btnSerial = QPushButton(txt['connect'], self)
		self.btnSerial.resize(70, 20)
		#self.btnSerial.move(125, 15)
		self.btnSerial.clicked.connect(self.click_btnSerial)

		self.layout1.addWidget(self.btnSerial)


		self.layout1.addSpacing(10)


		self.labelStatus = QLabel(self)
		self.labelStatus.resize(300, 20)
		self.labelStatus.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelStatus.setText(makestatus(txt['nc']))

		self.layout1.addWidget(self.labelStatus)

		self.layoutMain.addLayout(self.layout1)
		self.layoutMain.addSpacing(10)



		#self.layout2 = QGridLayout(self)

		self.layoutV1 = QVBoxLayout(self)

		self.inpCat = QLineEdit(self)
		self.inpCat.setPlaceholderText(txt['catsearch'])
		self.inpCat.resize(120, 20)
		#self.inpCat.move(15, 60)
		self.inpCat.textChanged.connect(self.searchCat)

		self.layoutV1.addWidget(self.inpCat)

		self.listCat = QListView(self)
		self.listCat.resize(120, 110)
		#self.listCat.move(15, 85)
		self.listCat.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.searchCat()

		self.layoutV1.addWidget(self.listCat)
		#self.layout2.addLayout(self.layoutV1, 0, 0, 1, 2)
		self.layoutMain.addLayout(self.layoutV1)

		#self.layout2.setSpacing(5)

		self.layoutV2 = QVBoxLayout(self)

		self.labelCat = QLabel(self)
		self.labelCat.setFixedSize(300, 120)
		#self.labelCat.move(150, 60)
		self.labelCat.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelCat.setText(
			"<b>" + txt['objectname'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A<br />" +
			"<b>" + txt['objectra'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A<br />" +
			"<b>" + txt['objectdec'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A<br />" +
			"<b>" + txt['constellation'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A<br />" +
			"<b>" + txt['magnitude'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A<br />" +
			"<b>" + txt['magnitude'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A<br />" +
			"<b>" + txt['type'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>N/A"
			)

		self.layoutV2.addWidget(self.labelCat)
		#self.layout2.addLayout(self.layoutV2, 0, 2, 1, 3)
		#self.layout2.setColumnMinimumWidth(2, 160)
		self.layoutMain.addLayout(self.layoutV2)



		self.layoutMain.addSpacing(10)



		self.btnSync = QPushButton(txt['sync'], self)
		self.btnSync.resize(200, 40)
		#self.btnSync.move(150, 190)
		self.btnSync.clicked.connect(self.click_btnSync)
		self.layoutMain.addWidget(self.btnSync)

		self.btnSlew = QPushButton(txt['selectslew'], self)
		self.btnSlew.resize(200, 40)
		#self.btnSlew.move(70, 245)
		self.btnSlew.clicked.connect(self.click_btnSlew)
		self.layoutMain.addWidget(self.btnSlew)

		self.btnCustomSlew = QPushButton(txt['customslew'], self)
		self.btnCustomSlew.resize(200, 40)
		#self.btnSlew.move(70, 245)
		self.btnCustomSlew.clicked.connect(self.click_btnCustomSlew)
		self.layoutMain.addWidget(self.btnCustomSlew)

		self.btnStopSlew = QPushButton(txt['stopslew'], self)
		self.btnStopSlew.resize(200, 40)
		#self.btnStopSlew.move(70, 285)
		self.btnStopSlew.clicked.connect(self.click_btnStopSlew)
		self.layoutMain.addWidget(self.btnStopSlew)



		self.layoutMain.addSpacing(10)



		self.labelMount = QLabel(self)
		self.labelMount.resize(300, 100)
		#self.labelMount.move(20, 330)
		self.labelMount.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.layoutMain.addWidget(self.labelMount)

		#self.layoutMain.addSpacing(10)

		self.timerMount = QTimer(self)
		self.timerMount.timeout.connect(self.runTimerMount)
		self.timerMount.start(refreshinterval)

		font = QFont()
		font.setPointSize(18)



		self.layoutKeys = QGridLayout()
		self.layoutKeys.setSpacing(10)
		self.layoutKeys.setColumnMinimumWidth(0, 50)
		self.layoutKeys.setColumnMinimumWidth(4, 50)



		self.btnMoveUp = QPushButton('▲', self)
		self.btnMoveUp.resize(70, 50)
		#self.btnMoveUp.move(135, 380)
		self.btnMoveUp.clicked.connect(self.click_btnMoveUp)
		self.btnMoveUp.setFont(font)
		self.layoutKeys.addWidget(self.btnMoveUp, 0, 2, 2, 1)
		
		self.btnMoveDown = QPushButton('▼', self)
		self.btnMoveDown.resize(70, 50)
		#self.btnMoveDown.move(135, 440)
		self.btnMoveDown.clicked.connect(self.click_btnMoveDown)
		self.btnMoveDown.setFont(font)
		self.layoutKeys.addWidget(self.btnMoveDown, 2, 2, 2, 1)
		
		self.btnMoveLeft = QPushButton('◀', self)
		self.btnMoveLeft.resize(70, 50)
		#self.btnMoveLeft.move(50, 410)
		self.btnMoveLeft.clicked.connect(self.click_btnMoveLeft)
		self.btnMoveLeft.setFont(font)
		self.layoutKeys.addWidget(self.btnMoveLeft, 1, 1, 2, 1)
		
		self.btnMoveRight = QPushButton('▶', self)
		self.btnMoveRight.resize(70, 50)
		#self.btnMoveRight.move(220, 410)
		self.btnMoveRight.clicked.connect(self.click_btnMoveRight)
		self.btnMoveRight.setFont(font)
		self.layoutKeys.addWidget(self.btnMoveRight, 1, 3, 2, 1)

		#for i in range(1,3):
		#	self.layoutKeys.setRowMinimumHeight(i, 60)
		self.layoutMain.addLayout(self.layoutKeys)


		self.layoutMain.addSpacing(10)

		self.layout3 = QHBoxLayout()

		self.labelSpeed = QLabel(self)
		self.labelSpeed.resize(100, 20)
		#self.labelSpeed.move(215, 380)
		self.labelSpeed.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelSpeed.setText('<b>' + txt['speed'] + '</b>')
		self.layout3.addWidget(self.labelSpeed)

		self.layout3.addSpacing(5)

		self.cmbSpeed = QComboBox(self)
		self.cmbSpeed.addItems(["Stop", "Guide", "Center", "Find", "Slew"])
		self.cmbSpeed.currentIndexChanged.connect(self.changeSpeed)
		self.cmbSpeed.resize(85, 25)
		#self.cmbSpeed.move(240, 375)
		self.cmbSpeed.setCurrentIndex(4)
		self.layout3.addWidget(self.cmbSpeed)


		self.layout3.addSpacing(30)


		#self.layoutMain.addSpacing(10)
		self.btnNightMode = QPushButton(txt['nightmodeon'], self)
		self.btnNightMode.resize(100, 40)
		#self.btnNightMode.move(20, 480)
		self.btnNightMode.clicked.connect(self.setNightMode)
		self.nightmode = False
		self.layout3.addWidget(self.btnNightMode)

		#self.layoutMain.addWidget(self.btnNightMode)
		self.layoutMain.addLayout(self.layout3)



		self.labelBy = QLabel(self)
		self.labelBy.resize(300, 20)
		self.labelBy.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		self.labelBy.setText(txt['by'])
		self.layoutMain.addWidget(self.labelBy)



		#self.btnPark = QPushButton(txt['park'], self)
		#self.btnPark.resize(100, 25)
		#self.btnPark.move(230, 480)
		#self.btnPark.clicked.connect(self.click_btnPark)

		
		self.moving = [0, 0, 0, 0]

		self.MountRA = 0.
		self.MountDEC = 0.
		self.toggleTimer = 1
		self.status = False
		self.synced = False

		self.setFixedSize(340, 700)
		self.setWindowTitle(txt['title'])
		self.setStyle(QStyleFactory.create('Fusion'))
		self.setLayout(self.layoutMain)

		self.setStyleSheet('color: black;')
		self.show()

	def warn(self, message):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText(message)
		msg.setWindowTitle(txt['warning'])
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
		print('warning')

	def closeEvent(self, event):
		result = QMessageBox.question(self, txt['message'], txt['quit'], QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

		if result == QMessageBox.Yes:
			event.accept()
			app.exit(0)
		else:
			event.ignore()

	def click_btnSerial(self):
		global ser
		try:
			#ser.port = self.inpSerial.text()
			ser.port = self.cmbSerial.currentText()
			print(self.cmbSerial.currentText())
			ser.open()
			self.status = True
			self.labelStatus.setText(makestatus(txt['connected']))
			serialwrite(self, ':RS#')
		except:
			self.status = False
			self.labelStatus.setText(makestatus(txt['connectfailed']))
		serialwrite(self, ':Sr00:00:00#')
		result = serialread(1)
		#serialwrite(self, ':U#')

	def searchCat(self):
		global c
		c.execute("SELECT * FROM DSO WHERE catalogue || cid LIKE ? OR REPLACE(name, ' ', '') LIKE ? ORDER BY catalogue, cid", ('%' + self.inpCat.text().replace(' ', '') + '%', '%' + self.inpCat.text().replace(' ', '') + '%'))
		#print(c.fetchall())
		global objdata
		objdata = c.fetchall()

		global c_star
		c_star.execute("SELECT * FROM star WHERE name LIKE ? ORDER BY name", ('%' + self.inpCat.text().replace(' ', '') + '%',))
		objdata += c_star.fetchall()

		model = QStandardItemModel(self.listCat)
		for i in objdata:
			if len(i) == 7: #star
				item = QStandardItem(i[1])
				model.appendRow(item)
			else:
				item = QStandardItem(getDSOName(i))
				model.appendRow(item)

		self.listCat.setModel(model)
		self.listCat.selectionModel().selectionChanged.connect(self.selectCat)


	def selectCat(self, selected):
		global objdata, selectedobj
		selected = selected.indexes()[0].data()
		for i in objdata:
			if len(i) == 7: #star
				if i[1] == selected:
					selectedobj = i
					RA = convRA(selectedobj[2])
					DEC = convDEC(selectedobj[3])
					RA = str(RA[0]) + "h " + str(RA[1]) + "m " + str(RA[2]) + "s"
					DEC = ("-" if DEC[0] < 0 else "") + str(DEC[1]) + "° " + str(DEC[2]) + "m " + str(DEC[3]) + "s"

					self.labelCat.setText(
						"<b>" + txt['objectname'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + selected  + "<br />" +
						"<b>" + txt['objectra'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + RA + "<br />" +
						"<b>" + txt['objectdec'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + DEC + "<br />" +
						"<b>" + txt['commonname'] + "&emsp;&nbsp;&nbsp;&nbsp;</b><br />" +
						"<b>" + txt['constellation'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + getconst(i[4]) + "<br />" +
						"<b>" + txt['magnitude'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + str(i[5]) + "<br />" +
						"<b>" + txt['type'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + txt['star']
						)
					break
			elif getDSOName(i) == selected:
				selectedobj = i
				RA = convRA(selectedobj[2])
				DEC = convDEC(selectedobj[3])
				RA = str(RA[0]) + "h " + str(RA[1]) + "m " + str(RA[2]) + "s"
				DEC = ("-" if DEC[0] < 0 else "") + str(DEC[1]) + "° " + str(DEC[2]) + "m " + str(DEC[3]) + "s"

				self.labelCat.setText(
					"<b>" + txt['objectname'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + selected  + "<br />" +
					"<b>" + txt['objectra'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + RA + "<br />" +
					"<b>" + txt['objectdec'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + DEC + "<br />" +
					"<b>" + txt['commonname'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + i[1] + "<br />" +
					"<b>" + txt['constellation'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + getconst(i[5]) + "<br />" +
					"<b>" + txt['magnitude'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + str(i[6]) + "<br />" +
					"<b>" + txt['type'] + "&emsp;&nbsp;&nbsp;&nbsp;</b>" + gettype(i[4])
					)
				break


	def Mmove(self, direction):
		global moving
		if direction == 0:
			if self.moving[direction] == 0:
				serialwrite(self, ':Mn#')
				self.btnMoveUp.setText('■')
				self.moving[direction] = 1
			else:
				serialwrite(self, ':Qn#')
				self.btnMoveUp.setText('▲')
				self.moving[direction] = 0
		elif direction == 1:
			if self.moving[direction] == 0:
				serialwrite(self, ':Ms#')
				self.btnMoveDown.setText('■')
				self.moving[direction] = 1
			else:
				serialwrite(self, ':Qs#')
				self.btnMoveDown.setText('▼')
				self.moving[direction] = 0
		elif direction == 2:
			if self.moving[direction] == 0:
				serialwrite(self, ':Mw#')
				self.btnMoveLeft.setText('■')
				self.moving[direction] = 1
			else:
				serialwrite(self, ':Qw#')
				self.btnMoveLeft.setText('◀')
				self.moving[direction] = 0
		elif direction == 3:
			if self.moving[direction] == 0:
				serialwrite(self, ':Me#')
				self.btnMoveRight.setText('■')
				self.moving[direction] = 1
			else:
				serialwrite(self, ':Qe#')
				self.btnMoveRight.setText('▶')
				self.moving[direction] = 0

	def click_btnSlew(self):
		if self.synced == False:
			self.warn(txt['notsynced'])
			return
		if selectedobj != None:

			result = slew(selectedobj[2], selectedobj[3])

			if result == '0':
				pass
			elif result == '1':
				self.warn(txt['belowhorizon'])
			elif result == '2':
				pass

	def click_btnStopSlew(self):
		serialwrite(self, ':Q#')
		serialwrite(self, ':RC#')

	def click_btnCustomSlew(self):
		global MountRA, MountDEC
		MountRA = self.MountRA
		MountDEC = self.MountDEC
		self.dialog = DInputCoor()
		self.dialog.show()

	def runTimerMount(self):
		try:
			if self.status == True and self.toggleTimer == -1:
				serialwrite(self, ':GR#')
				RAtmp = serialread(9)
				if RAtmp[-1] != '#':
					raise IndexError
				RAtmp = RAtmp.split(':')
				RAtmp[2] = RAtmp[2].replace('#', '')
				self.MountRA = int(RAtmp[0]) + int(RAtmp[1]) / 60. + int(RAtmp[2]) / 60. / 60.
			elif self.status == True:
				serialwrite(self, ':GD#')
				DECtmp = serialread(10)
				if DECtmp[-1] != '#':
					raise IndexError
				DECsign = -1 if DECtmp[0] == "-" else 1
				DECD = int(DECtmp[1:3])
				DECM = int(DECtmp[4:6])
				DECS = int(DECtmp[7:9])
				self.MountDEC = (int(DECD) + int(DECM) / 60. + int(DECS) / 60. / 60.) * DECsign
		except (IndexError, ValueError) as e:
			flushserial()
			pass
		self.toggleTimer *= -1

		RA = convRA(self.MountRA)
		DEC = convDEC(self.MountDEC)

		RA = str(RA[0]) + "h " + str(RA[1]) + "m " + str(RA[2]) + "s"
		DEC = ("-" if DEC[0] < 0 else "") + str(DEC[1]) + "° " + str(DEC[2]) + "m " + str(DEC[3]) + "s"

		self.labelMount.setText(
			"<b>" + txt['mountra'] + " </b>" + RA + "<br />"
			"<b>" + txt['mountdec'] + " </b>" + DEC + "<br />"
			)

	def click_btnMoveUp(self):
		self.Mmove(0)

	def click_btnMoveDown(self):
		self.Mmove(1)

	def click_btnMoveLeft(self):
		self.Mmove(2)

	def click_btnMoveRight(self):
		self.Mmove(3)

	def changeSpeed(self, item):
		if item == 1:
			serialwrite(self, ':RG#')
		elif item == 2:
			serialwrite(self, ':RC#')
		elif item == 3:
			serialwrite(self, ':RM#')
		elif item == 4:
			serialwrite(self, ':RS#')
		elif item == 0:
			serialwrite(self, ':Q#')

	def setNightMode(self):
		if self.nightmode == True:
			self.nightmode = False
			self.setStyleSheet('color: black;') #giving nothing may show strange theme on macOS
			self.btnNightMode.setText(txt['nightmodeon'])
		else:
			self.nightmode = True
			self.setStyleSheet('background-color: red;')
			self.btnNightMode.setText(txt['nightmodeoff'])

	def click_btnSync(self):
		if selectedobj != None:
			DEC = convDEC(selectedobj[3])
			sign = "-" if DEC[0] < 0 else "+"
			for i in range(1, 4):
				if DEC[i] < 10:
					DEC[i] = '0' + str(DEC[i])
				else:
					DEC[i] = str(DEC[i])

			RA = convRA(selectedobj[2])
			for i in range(0, 3):
				if RA[i] < 10:
					RA[i] = '0' + str(RA[i])
				else:
					RA[i] = str(RA[i])
			serialwrite(self, ':Sd' + sign + DEC[1] + '*' + DEC[2] + ':' + DEC[3] + '#')
			serialwrite(self, ':Sr' + RA[0] + ':' + RA[1] + ':' + RA[2] + '#')
			serialwrite(self, ':CM#')
			self.synced = True

	#TODO: after supporting local time, location
	#def click_btnPark(self):
	#	pass




if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = WMain()
	sys.exit(app.exec_())