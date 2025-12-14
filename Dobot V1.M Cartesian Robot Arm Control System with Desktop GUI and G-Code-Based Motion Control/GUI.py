from PyQt5 import QtWidgets, QtCore, QtGui, sip 
from PyQt5.QtGui import QFont, QColor, QDesktopServices
from PyQt5.QtCore import QTimer, QEvent, Qt, QUrl
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QTextEdit, QInputDialog, QDialog, QVBoxLayout, QHBoxLayout, QListWidget
import sys
import time
import asyncio
import threading
import re
import ctypes
from ctypes import wintypes

# === 🎯 PERBAIKAN IMPORT: TAMBAHKAN QSplashScreen DAN QProgressBar ===
from PyQt5.QtWidgets import QSplashScreen, QProgressBar, QLabel
from PyQt5.QtGui import QPixmap, QPainter

# Load DLL untuk API Windows
dwmapi = ctypes.WinDLL('dwmapi')

# === 🎯 DEFINISIKAN KONSTANTA YANG DIPERLUKAN ===
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_CAPTION_COLOR = 35

# === 🎯 BUAT CLASS LOADING SCREEN ===
class LoadingScreen(QSplashScreen):
    def __init__(self):
        # Buat QPixmap untuk background
        pixmap = QPixmap(600, 400)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap)
        
        self.setWindowTitle("DOBOT ROBOT CON - Loading")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # Widget untuk loading content
        self.loading_widget = QWidget(self)
        self.loading_widget.setGeometry(0, 0, 600, 400)
        self.loading_widget.setStyleSheet("background-color: #0F172B; border-radius: 30px;")
        
        layout = QVBoxLayout(self.loading_widget)
        
        # Logo/Title
        self.title_label = QLabel("DOBOT ROBOT CONTROL SYSTEM")
        self.title_label.setStyleSheet("color: #4F39F6; font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Loading text
        self.label = QLabel("Initializing DOBOT ROBOT Control System...")
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin: 10px;")
        self.label.setAlignment(Qt.AlignCenter)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFormat("")
        self.progress.setMaximum(100)
        self.progress.setMinimum(0)
        self.progress.setValue(0)
        self.progress.setFixedHeight(25)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4F39F6;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-weight: bold;
                background-color: #1D293D;
            }
            QProgressBar::chunk {
                background-color: #4F39F6;
                border-radius: 8px;
            }
        """)
        
        # Progress percentage
        self.percent_label = QLabel("0%")
        self.percent_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.percent_label.setAlignment(Qt.AlignCenter)

        # <<< KODE BARU: CREDIT LABEL DITAMBAHKAN DI SINI >>>
        self.credit_label = QLabel("Kelompok 2_32, 49, 60 - PSM 2025")
        self.credit_label.setStyleSheet("color: #D4CDFF; font-size: 12px;") # Warna yang lebih soft
        self.credit_label.setAlignment(Qt.AlignCenter)
        # <<< AKHIR KODE BARU >>>
        
        # Add widgets to layout
        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.addWidget(self.percent_label)
        layout.addStretch()

        # <<< KODE BARU: CREDIT LABEL DITAMBAHKAN KE LAYOUT >>>
        layout.addWidget(self.credit_label)
        # <<< AKHIR KODE BARU >>>
        
    def update_progress(self, value, text=""):
        self.progress.setValue(value)
        self.percent_label.setText(f"{value}%")
        if text:
            self.label.setText(text)
        QApplication.processEvents()


class Ui_DOBOTROBOT_V1(QtWidgets.QWidget):
    def setupUi(self, DOBOTROBOT_V1):
        _translate = QtCore.QCoreApplication.translate
        DOBOTROBOT_V1.setObjectName("DOBOTROBOT_V1")
        DOBOTROBOT_V1.resize(1427, 904)
        DOBOTROBOT_V1.setWindowIcon(QtGui.QIcon("D:\Me\Akademik\Teknik Mekatronika\Mata Kuliah\Semester 5\Pemrograman Sistem Mekatronik\DOBOT ROBOT\DOBOTROBOT.ico"))
        DOBOTROBOT_V1.setAnimated(True)
        DOBOTROBOT_V1.setTabShape(QtWidgets.QTabWidget.Rounded)

        # Konten utama
        self.centralwidget = QtWidgets.QWidget(DOBOTROBOT_V1)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {\n"
                                         "    background-color: #0F172B;\n"
                                         "}\n"
                                         "")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Set warna title bar sesuai tema sistem
        self.set_title_bar_color(DOBOTROBOT_V1)

        self.frame_header = QtWidgets.QFrame(self.centralwidget)
        self.frame_header.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header.setLineWidth(1)
        self.frame_header.setObjectName("frame_portUSB")
        self.layout_Header = QtWidgets.QHBoxLayout(self.frame_header)
        self.layout_Header.setContentsMargins(0, 0, 0, 0)
        self.layout_Header.setSpacing(10)
        self.layout_Header.setObjectName("horizontalLayout")
        # self.line = QtWidgets.QFrame(self.frame_header)
        # self.line.setFrameShape(QtWidgets.QFrame.VLine)
        # self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line.setObjectName("line")
        # self.layout_Header.addWidget(self.line)
        self.pushButton_start = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_start.setEnabled(True)
        self.pushButton_start.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setStyleSheet("QPushButton {\n"
                                           "    background-color: #009966; /* Warna latar belakang tombol */\n"
                                           "    max-width: 90px; \n"
                                           "    min-width: 90px; \n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #009966; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding:5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #06D38F; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #06D38F; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #077D56; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #077D56; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #077D56; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    max-width: 90px; \n"
                                           "    min-width: 90px; \n"
                                           "    color: #B0CFB2; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #077D56; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
        self.pushButton_start.setObjectName("pushButton_start")
        self.layout_Header.addWidget(self.pushButton_start)
        self.pushButton_pause = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_pause.setStyleSheet("QPushButton {\n"
"  background-color: #E17100; /* Warna latar belakang tombol */\n"
"  max-width: 90px; \n" 
"  min-width: 90px; \n"
"  color: #FFFFFF; /* Warna teks */\n"
"  border: 2px solid #E17100; /* Warna border */\n"
"  border-radius: 6px; /* Sudut tombol yang melengkung */\n"
"  padding: 5px; /* Padding di dalam tombol */\n"
"  font-size: 18px; /* Ukuran font */\n"
"  font-weight: bold; /* Ketebalan font */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: #FFA54A; /* Warna latar belakang saat hover */\n"
"  border: 2px solid #FFA54A; /* Warna border saat hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: #A35607; /* Warna latar belakang saat ditekan */\n"
"  border: 2px solid #A35607; /* Warna border saat ditekan */\n"
"  color: #FFFFFF; /* Warna teks saat ditekan */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  background-color: #A35607; /* Warna latar belakang saat tombol dinonaktifkan */\n"
"  max-width: 90px; \n"      # <<< PASTIKAN BARIS INI DITAMBAH
"  min-width: 90px; \n"      # <<< PASTIKAN BARIS INI DITAMBAH
"  color: #F3A24F; /* Warna teks saat tombol dinonaktifkan */\n"
"  border: 2px solid #A35607; /* Warna border saat tombol dinonaktifkan */\n"
"}")
        self.pushButton_pause.setObjectName("pushButton_pause")
        self.layout_Header.addWidget(self.pushButton_pause)
        self.pushButton_stop = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_stop.setEnabled(True)
        self.pushButton_stop.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.setStyleSheet("QPushButton {\n"
                                           "    background-color: #EC003F; /* Warna latar belakang tombol */\n"
                                           "    max-width: 90px; \n"
                                           "    min-width: 90px; \n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #EC003F; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding: 5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #FF3269; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #FF3269; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #A70530; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #A70530; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #A70530; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    color: #FF638D; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #A70530; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.layout_Header.addWidget(self.pushButton_stop)

        # <<< START KODE BARU: Tombol Single Run >>>
        self.pushButton_single_run = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_single_run.setEnabled(True)
        self.pushButton_single_run.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_single_run.setFont(font)
        # Menggunakan style yang sama agar konsisten
        self.pushButton_single_run.setStyleSheet(self.pushButton_stop.styleSheet()) 
        self.pushButton_single_run.setObjectName("pushButton_single_run")
        self.layout_Header.addWidget(self.pushButton_single_run)
        # <<< AKHIR KODE BARU >>>

        self.pushButton_single_run.setStyleSheet("QPushButton {\n"
                                           "    background-color: #49CEC3; /* Warna latar belakang tombol */\n"
                                           "    max-width: 120px; \n"
                                           "    min-width: 120px; \n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #49CEC3; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding:5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #5DF2E5; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #5DF2E5; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #138B81; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #138B81; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #138B81; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    color: #13CFC0; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #138B81; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
# -----------------------------------------------------------



# -----------------------------------------------------------
        
        self.pushButton_single_run.setObjectName("pushButton_single_run")
        self.layout_Header.addWidget(self.pushButton_single_run)
        # <<< AKHIR KODE PERBAIKAN >>>

        self.pushButton_save_as = QtWidgets.QPushButton(self.frame_header) #Save dibagian atas
        self.pushButton_save_as.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save_as.setFont(font)
        self.pushButton_save_as.setStyleSheet("QPushButton {\n"
                                              "    background-color: #155DFC; /* Warna latar belakang tombol */\n"
                                              "    max-width: 90px; \n"
                                              "    min-width: 90px; \n"
                                                "    color: #FFFFFF; /* Warna teks */\n"
                                                "    border: 2px solid #155DFC; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #4A82FD; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #4A82FD; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #4A82FD; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #4A82FD; /* Warna border saat ditekan */\n"
                                                "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n")
        self.pushButton_save_as.setObjectName("pushButton_save_as")
        self.layout_Header.addWidget(self.pushButton_save_as)
        self.label_port_usb = QtWidgets.QLabel(self.frame_header)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_port_usb.setFont(font)
        self.label_port_usb.setStyleSheet("QLabel#label_port_usb {\n"
                                          "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                          "}\n"
                                          "")
        self.label_port_usb.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_port_usb.setObjectName("label_port_usb")
        self.layout_Header.addWidget(self.label_port_usb)
        self.pushButton_connect = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_connect.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setStyleSheet("QPushButton {\n"
                                                "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.layout_Header.addWidget(self.pushButton_connect)
        self.lineEdit_com = QtWidgets.QLineEdit(self.frame_header)
        self.lineEdit_com.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_com.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lineEdit_com.setFont(font)
        self.lineEdit_com.setStyleSheet("QLineEdit {\n"
                                        "    background-color: #3B4252; /* Warna latar belakang */\n"
                                        "    color: #FFFFFF; /* Warna teks */\n"
                                        "    border: 2px solid #3B4252; /* Warna border */\n"
                                        "    border-radius: 8px; /* Sudut melengkung */\n"
                                        "    font-size: 18px; /* Ukuran font */\n"
                                        "    padding: 6px; /* Padding dalam */\n"
                                        "    selection-background-color: #001C38; /* Warna latar belakang saat teks diseleksi */\n"
                                        "    selection-color: #FFFFFF; /* Warna teks saat diseleksi */\n"
                                        "}\n"
                                        "\n"
                                        "/* Efek hover */\n"
                                        "QLineEdit:hover {\n"
                                        "    border: 2px solid #3B4252; /* Border lebih terang saat hover */\n"
                                        "}\n"
                                        "\n"
                                        "/* Efek saat LineEdit aktif (focus) */\n"
                                        "QLineEdit:focus {\n"
                                        "    border: 2px solid #434C5E; /* Warna lebih cerah saat aktif */\n"
                                        "    background-color: #434C5E; /* Latar belakang sedikit lebih terang */\n"
                                        "}\n"
                                        "")
        self.lineEdit_com.setMaxLength(10)
        self.lineEdit_com.setFrame(False)
        self.lineEdit_com.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_com.setCursorPosition(3)
        self.lineEdit_com.setDragEnabled(False)
        self.lineEdit_com.setReadOnly(False)
        self.lineEdit_com.setObjectName("lineEdit_com")
        self.layout_Header.addWidget(self.lineEdit_com)

        # --- KOTAK BAUDRATE (QComboBox) ---
        self.comboBox_baudrate = QtWidgets.QComboBox(self.frame_header)
        self.comboBox_baudrate.setMinimumSize(QtCore.QSize(0, 33))
        self.comboBox_baudrate.setMaximumSize(QtCore.QSize(150, 16777215)) # Tetapkan lebar max
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.comboBox_baudrate.setFont(font)
        self.comboBox_baudrate.setStyleSheet("QComboBox {\n"
"    background-color: #3B4252;\n"
"    color: #FFFFFF;\n"
"    border: 2px solid #3B4252;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"    font-size: 18px;\n"
"}\n"
"QComboBox:focus { border: 2px solid #434C5E; }\n"
# --- KODE QSS UNTUK DITAMBAHKAN ---

"QComboBox QAbstractItemView {\n"
"    border: 1px solid #4C566A; /* Border list dropdown */\n"
"    background-color: #2E3440; /* Warna Latar Belakang list item */\n"
"    color: #ECEFF4; /* Warna Teks Item normal (Putih/Abu Muda) */\n"
"    selection-background-color: #4F39F6; /* Warna Latar Belakang Item yang Dipilih (Ungu) */\n"
"    selection-color: #FFFFFF; /* Warna Teks Item yang Dipilih */\n"
"    outline: 0px; /* Menghilangkan border biru saat fokus */\n"
"}\n"

# --- AKHIR KODE QSS UNTUK DITAMBAHKAN ---
"QComboBox::drop-down { border-left-width: 1px; border-left-color: #4C566A; border-left-style: solid; }\n"
"QComboBox::down-arrow {\n"
"    image: url(resources/Arrow.png);\n" 
"    width: 14px;  /* <<< TAMBAHKAN INI >>> */\n"
"    height: 14px; /* <<< TAMBAHKAN INI >>> */\n"
"}\n") # Asumsi Anda memiliki ikon panah

        # Tambahkan item baud rate
        self.comboBox_baudrate.addItem("115200") # Pilihan default
        self.comboBox_baudrate.addItem("9600")
        self.comboBox_baudrate.addItem("57600")
        self.comboBox_baudrate.addItem("250000") # Pilihan baud rate umum lainnya
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.layout_Header.addWidget(self.comboBox_baudrate)
        # ----------------------------------------------------

        self.label_status = QtWidgets.QLabel(self.frame_header)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_status.setFont(font)
        self.label_status.setStyleSheet("QLabel#label_status {\n"
                                        "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                        "}\n"
                                        "QLabel#label_status:disabled {\n"
                                        "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                        "}\n"
                                        "")
        self.label_status.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_status.setObjectName("label_status")
        self.label_status.hide()
        # self.layout_Header.addWidget(self.label_status)
        self.pushButton_calibration = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_calibration.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_calibration.setFont(font)
        self.pushButton_calibration.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #4F39F6; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #4F39F6; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #7967FF; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #7967FF; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #1601B8; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #1601B8; /* Warna border saat ditekan */\n"
                                                  "    color: #7563FF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_calibration.setObjectName("pushButton_calibration")
        self.layout_Header.addWidget(self.pushButton_calibration)
        # spacer_kanan = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.layout_Header.addItem(spacer_kanan)
        self.gridLayout.addWidget(self.frame_header, 0, 0, 1, 1)
        self.layout_Header.insertStretch(5, 100)
        self.frame_bawahutama = QtWidgets.QFrame(self.centralwidget)
        self.frame_bawahutama.setEnabled(True)
        self.frame_bawahutama.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_bawahutama.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bawahutama.setObjectName("frame_bawah")
        self.layout_BawahUtama = QtWidgets.QHBoxLayout(self.frame_bawahutama)
        self.layout_BawahUtama.setStretch(0, 1)
        self.layout_BawahUtama.setStretch(1, 0)
        self.layout_BawahUtama.setStretch(2, 4)
        self.layout_BawahUtama.setObjectName("horizontalLayout_2")
        self.listWidget_save = QtWidgets.QListWidget(self.frame_bawahutama)
        self.listWidget_save.setEnabled(True)
        self.listWidget_save.setMinimumSize(QtCore.QSize(0, 0))
        # self.listWidget_save.setMaximumSize(QtCore.QSize(400, 16777215))
        self.listWidget_save.setSizeIncrement(QtCore.QSize(0, 0))
        self.listWidget_save.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.listWidget_save.setFont(font)
        self.listWidget_save.setMouseTracking(False)
        self.listWidget_save.setTabletTracking(False)
        self.listWidget_save.setAcceptDrops(False)
        self.listWidget_save.setAutoFillBackground(False)
        self.listWidget_save.setStyleSheet("""
QListWidget {
    background-color: #1D293D; /* Warna latar belakang */
    border: 2px solid #1D293D; /* Warna border */
    border-radius: 12px; /* Sudut melengkung */
    color: #FFFFFF; /* Warna teks putih */
    font-size: 14px; /* Ukuran font */
    padding: 5px; /* Padding di dalam list */
}

QListWidget::item {
    background-color: #2A3E5F   ; /* Warna latar belakang item */
    border-radius: 6px; /* Sudut melengkung untuk item */
    padding: 0px; /* Padding di dalam item */
    margin: 1px; /* Jarak antar item */
}

QListWidget::item:hover {
    background-color: #2A3850; /* Warna latar belakang saat hover */
    color: #FFFFFF; /* Warna teks saat hover */
}

QListWidget::item:selected {
    background-color: #4F39F6; /* Warna latar belakang saat dipilih */
    color: #FFFFFF; /* Warna teks saat dipilih */
}

QListWidget:disabled {
    background-color: #3B4252; /* Warna latar belakang saat dinonaktifkan */
    color: #7F8C9A; /* Warna teks saat dinonaktifkan */
    border: 2px solid #3B4252; /* Warna border saat dinonaktifkan */
}

QListWidget::item:disabled {
    background-color: #2E3440; /* Warna latar belakang item saat dinonaktifkan */
    color: #5C677D; /* Warna teks item saat dinonaktifkan */
}

/* Scrollbar vertikal */
QScrollBar:vertical {
    background-color: #3B4252; /* Warna latar belakang scrollbar */
    width: 12px; /* Lebar scrollbar */
    margin: 0px; /* Margin scrollbar */
    border-radius: 6px; /* Sudut melengkung scrollbar */
}

QScrollBar::handle:vertical {
    background-color: #4C566A; /* Warna handle scrollbar */
    border-radius: 6px; /* Sudut melengkung handle */
}

QScrollBar::handle:vertical:hover {
    background-color: #5E6A77; /* Warna handle saat hover */
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: none; /* Menghilangkan tombol tambahan di scrollbar */
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none; /* Menghilangkan latar belakang tambahan di scrollbar */
}

/* Scrollbar horizontal */
QScrollBar:horizontal {
    background-color: #3B4252; /* Warna latar belakang scrollbar horizontal */
    height: 12px; /* Tinggi scrollbar horizontal */
    border-radius: 6px; /* Sudut melengkung scrollbar horizontal */
}

QScrollBar::handle:horizontal {
    background-color: #4C566A; /* Warna handle scrollbar horizontal */
    border-radius: 6px; /* Sudut melengkung handle horizontal */
}

QScrollBar::handle:horizontal:hover {
    background-color: #5E6A77; /* Warna handle saat hover horizontal */
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    background: none; /* Menghilangkan tombol tambahan di scrollbar horizontal */
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none; /* Menghilangkan latar belakang tambahan di scrollbar horizontal */
}
""")


        self.listWidget_save.setTabKeyNavigation(False)
        self.listWidget_save.setDragEnabled(True)
        self.listWidget_save.setDragDropOverwriteMode(False)
        self.listWidget_save.setAlternatingRowColors(False)
        self.listWidget_save.setProperty("isWrapping", False)
        self.listWidget_save.setUniformItemSizes(False)
        self.listWidget_save.setWordWrap(False)
        self.listWidget_save.setSelectionRectVisible(False)
        self.listWidget_save.setObjectName("listWidget_save")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_save.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_save.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_save.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_save.addItem(item)
        # --- KODE BARU: MEMBUAT WADAH VERTIKAL UNTUK LIST PROGRAM ---

        # 1. Buat Container Vertikal baru khusus List Program
        self.frame_list_container = QtWidgets.QFrame(self.frame_bawahutama)
        self.frame_list_container.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.layout_list_vertical = QtWidgets.QVBoxLayout(self.frame_list_container)
        self.layout_list_vertical.setContentsMargins(0, 0, 0, 0)
        self.layout_list_vertical.setSpacing(5)

        # 2. Tambahkan Label Judul Baru "SERIAL PROGRAM"
        self.label_list_title = QtWidgets.QLabel(self.frame_list_container)
        self.label_list_title.setText(_translate("DOBOTROBOT_V1", "SERIAL PROGRAM"))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_list_title.setFont(font)
        # --- KODE YANG HARUS DIGANTI UNTUK self.label_list_title ---
        self.label_list_title.setStyleSheet("QLabel {\n"
        "    color: #FFFFFF; \n"
        "}\n"
        "QLabel:disabled {\n"
        "    color: #5C677D; /* Memastikan teks tetap putih cerah walau panel dinonaktifkan */\n"
        "}")
        # ----------------------------------------------------
        self.label_list_title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout_list_vertical.addWidget(self.label_list_title)

        # 3. Pindahkan List Widget ke Layout Vertikal Baru
        self.layout_list_vertical.addWidget(self.listWidget_save) 

        # --- AKHIR KODE WADAH BARU ---

        # Anda harus memasukkan wadah baru ini ke layout utama:
        self.layout_BawahUtama.addWidget(self.frame_list_container)
        self.frame_ProgramKontrol = QtWidgets.QFrame(self.frame_bawahutama)
        self.frame_ProgramKontrol.setMaximumSize(QtCore.QSize(250, 16777215)) 
        self.frame_ProgramKontrol.setEnabled(True)
        self.frame_ProgramKontrol.setMinimumSize(QtCore.QSize(220, 0))
        self.frame_ProgramKontrol.setMaximumSize(QtCore.QSize(250, 16777215)) # Lebar max 250px
        self.frame_ProgramKontrol.setEnabled(True)
        self.frame_ProgramKontrol.setMinimumSize(QtCore.QSize(220, 0)) # Lebar minimum (agar tombol muat)
        self.frame_ProgramKontrol.setMaximumSize(QtCore.QSize(250, 16777215)) # Lebar maksimum (agar tidak melar)
        self.frame_ProgramKontrol.setEnabled(True)
        self.frame_ProgramKontrol.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_ProgramKontrol.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ProgramKontrol.setObjectName("frame_3")
        self.layout_ProgramKontrol = QtWidgets.QVBoxLayout(self.frame_ProgramKontrol)
        self.layout_ProgramKontrol.setObjectName("verticalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("QLabel#label_8 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_8:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter) #Open Program
        self.label_8.setObjectName("label_8")
        self.layout_ProgramKontrol.addWidget(self.label_8)
        self.pushButton_edit = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_edit.setFont(font)
        self.pushButton_edit.setStyleSheet("QPushButton {\n"
                                            "   background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        self.pushButton_edit.setObjectName("pushButton_edit") #Dibawahnya Open Program
        self.layout_ProgramKontrol.addWidget(self.pushButton_edit)
        self.pushButton_next = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_next.setFont(font)
        self.pushButton_next.setStyleSheet("QPushButton {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #1D293D; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding: 5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
        self.pushButton_next.setObjectName("pushButton_next")
        self.layout_ProgramKontrol.addWidget(self.pushButton_next)
        self.pushButton_new = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_new.setFont(font)
        self.pushButton_new.setStyleSheet("QPushButton {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #1D293D; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding: 5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
        self.pushButton_new.setObjectName("pushButton_new")
        self.layout_ProgramKontrol.addWidget(self.pushButton_new)
        self.pushButton_delete = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setStyleSheet("QPushButton {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #1D293D; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding: 5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.layout_ProgramKontrol.addWidget(self.pushButton_delete)
        self.pushButton_clear = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_clear.setFont(font)
        self.pushButton_clear.setStyleSheet("QPushButton {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                           "    color: #FFFFFF; /* Warna teks */\n"
                                           "    border: 2px solid #1D293D; /* Warna border */\n"
                                           "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                           "    padding: 5px; /* Padding di dalam tombol */\n"
                                           "    font-size: 18px; /* Ukuran font */\n"
                                           "    font-weight: bold; /* Ketebalan font */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                           "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                           "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                           "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {\n"
                                           "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                           "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                           "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                           "}")
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.layout_ProgramKontrol.addWidget(self.pushButton_clear)
        self.pushButton_up = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_up.setFont(font)
        self.pushButton_up.setStyleSheet("QPushButton {\n"
                                        "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                        "    color: #FFFFFF; /* Warna teks */\n"
                                        "    border: 2px solid #1D293D; /* Warna border */\n"
                                        "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                        "    padding: 5px; /* Padding di dalam tombol */\n"
                                        "    font-size: 18px; /* Ukuran font */\n"
                                        "    font-weight: bold; /* Ketebalan font */\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                        "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed {\n"
                                        "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                        "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                        "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:disabled {\n"
                                        "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                        "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                        "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                        "}")
        self.pushButton_up.setObjectName("pushButton_up")
        self.layout_ProgramKontrol.addWidget(self.pushButton_up)
        self.pushButton_down = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_down.setFont(font)
        self.pushButton_down.setStyleSheet("QPushButton {\n"
                                          "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        self.pushButton_down.setObjectName("pushButton_down")
        self.layout_ProgramKontrol.addWidget(self.pushButton_down)
        self.label_9 = QtWidgets.QLabel(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("QLabel#label_9 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_9:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)

        # --- Penempatan Tombol Gripper 01 (Perbaikan) ---
        self.pushButton_gripper_01 = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_gripper_01.setFont(font)
        self.pushButton_gripper_01.setStyleSheet(self.pushButton_up.styleSheet())
        self.pushButton_gripper_01.setObjectName("pushButton_gripper_01")
        # Gunakan layout yang benar: self.layout_ProgramKontrol
        self.layout_ProgramKontrol.addWidget(self.pushButton_gripper_01)
        # ------------------------------------------------

        self.label_9.setObjectName("label_9")
        self.layout_ProgramKontrol.addWidget(self.label_9)
        self.pushButton_gripper_vacum = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_gripper_vacum.setFont(font)
        self.pushButton_gripper_vacum.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_gripper_vacum.setObjectName("pushButton_gripper_vacum")
        self.layout_ProgramKontrol.addWidget(self.pushButton_gripper_vacum)
        self.pushButton_gripper_servo = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_gripper_servo.setFont(font)
        self.pushButton_gripper_servo.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_gripper_servo.setObjectName("pushButton_gripper_servo")
        self.layout_ProgramKontrol.addWidget(self.pushButton_gripper_servo) #Save servo
        self.pushButton_save_servo = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save_servo.setFont(font)
        self.pushButton_save_servo.setStyleSheet("QPushButton {\n"
                                                 "    background-color: #E78F36; /* Warna latar belakang tombol */\n"
                                                 "    color: #FFFFFF; /* Warna teks */\n"
                                                 "    border: 2px solid #E78F36; /* Warna border */\n"
                                                 "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                 "    padding: 5px; /* Padding di dalam tombol */\n"
                                                 "    font-size: 18px; /* Ukuran font */\n"
                                                 "    font-weight: bold; /* Ketebalan font */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover {\n"
                                                 "    background-color: #F4A351; /* Warna latar belakang saat hover */\n"
                                                 "    border: 2px solid #F4A351; /* Warna border saat hover */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:pressed {\n"
                                                 "    background-color: #F4A351; /* Warna latar belakang saat ditekan */\n"
                                                 "    border: 2px solid #F4A351; /* Warna border saat ditekan */\n"
                                                 "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:disabled {\n"
                                                 "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                 "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                 "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                 "}")
        self.pushButton_save_servo.setObjectName("pushButton_save_servo")
        self.layout_ProgramKontrol.addWidget(self.pushButton_save_servo)
        self.label_10 = QtWidgets.QLabel(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("QLabel#label_10 {\n"
                                    "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                    "}\n"
                                    "QLabel#label_10:disabled {\n"
                                    "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                    "}\n"
                                    "")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.layout_ProgramKontrol.addWidget(self.label_10)
        self.pushButton_LG1 = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_LG1.setFont(font)
        self.pushButton_LG1.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_LG1.setObjectName("pushButton_LG1")
        self.layout_ProgramKontrol.addWidget(self.pushButton_LG1)
        self.pushButton_LG2 = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_LG2.setFont(font)
        self.pushButton_LG2.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_LG2.setObjectName("pushButton_LG2")
        self.layout_ProgramKontrol.addWidget(self.pushButton_LG2)
        self.pushButton_LG3 = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_LG3.setFont(font)
        self.pushButton_LG3.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_LG3.setObjectName("pushButton_LG3")
        self.layout_ProgramKontrol.addWidget(self.pushButton_LG3)
        self.pushButton_save_LG = QtWidgets.QPushButton(self.frame_ProgramKontrol)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save_LG.setFont(font)
        self.pushButton_save_LG.setStyleSheet("QPushButton {\n"
                                              "    background-color: #E78F36; /* Warna latar belakang tombol */\n"
                                                 "    color: #FFFFFF; /* Warna teks */\n"
                                                 "    border: 2px solid #E78F36; /* Warna border */\n"
                                                 "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                 "    padding: 5px; /* Padding di dalam tombol */\n"
                                                 "    font-size: 18px; /* Ukuran font */\n"
                                                 "    font-weight: bold; /* Ketebalan font */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover {\n"
                                                 "    background-color: #F4A351; /* Warna latar belakang saat hover */\n"
                                                 "    border: 2px solid #F4A351; /* Warna border saat hover */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:pressed {\n"
                                                 "    background-color: #F4A351; /* Warna latar belakang saat ditekan */\n"
                                                 "    border: 2px solid #F4A351; /* Warna border saat ditekan */\n"
                                                 "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:disabled {\n"
                                                 "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                 "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                 "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                 "}")
        self.pushButton_save_LG.setObjectName("pushButton_save_LG")
        self.layout_ProgramKontrol.addWidget(self.pushButton_save_LG)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_ProgramKontrol.addItem(spacerItem)
        self.layout_BawahUtama.addWidget(self.frame_ProgramKontrol)
        self.frame_2 = QtWidgets.QFrame(self.frame_bawahutama)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("QLabel#label_12 {\n"
                                    "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                    "}\n"
                                    "QLabel#label_12:disabled {\n"
                                    "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                    "}\n"
                                    "")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.pushButton_cek_posisi = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_cek_posisi.setFont(font)
        self.pushButton_cek_posisi.setStyleSheet("QPushButton {\n"
                                                 "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                "    color: #FFFFFF; /* Warna teks */\n"
                                                "    border: 2px solid #1D293D; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                                "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
        self.pushButton_cek_posisi.setObjectName("pushButton_cek_posisi")
        self.verticalLayout.addWidget(self.pushButton_cek_posisi)
        self.pushButton_endstop = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_endstop.setFont(font)
        self.pushButton_endstop.setStyleSheet("QPushButton {\n"
                                              "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        self.pushButton_endstop.setObjectName("pushButton_endstop")
        self.verticalLayout.addWidget(self.pushButton_endstop)
        self.pushButton_motor_ONOFF = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_motor_ONOFF.setFont(font)
        self.pushButton_motor_ONOFF.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #1D293D; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
        self.pushButton_motor_ONOFF.setObjectName("pushButton_motor_ONOFF")
        self.verticalLayout.addWidget(self.pushButton_motor_ONOFF)
        self.pushButton_fan = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_fan.setFont(font)
        self.pushButton_fan.setStyleSheet("QPushButton {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #366DE6; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #366DE6; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:checked {\n"
                                            "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                            "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                            "    color: #FFFFFF; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:checked:hover {\n"
                                            "    background-color: #366DE6; /* Warna latar belakang saat tombol checked dan hover */\n"
                                            "    border: 2px solid #366DE6; /* Warna border saat tombol checked dan hover */\n"
                                            "    color: #FFFFFF; /* Warna teks saat tombol checked dan hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        self.pushButton_fan.setObjectName("pushButton_fan")
        self.verticalLayout.addWidget(self.pushButton_fan)
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("QLabel#label_11 {\n"
                                    "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                    "}\n"
                                    "QLabel#label_11:disabled {\n"
                                    "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                    "}\n"
                                    "")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.pushButton_S1 = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_S1.setFont(font)
        self.pushButton_S1.setStyleSheet("QPushButton {\n"
                                         "    background-color: #4F39F6; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #4F39F6; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 18px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:disabled {\n"
                                         "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                         "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                         "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                         "}")
        self.pushButton_S1.setObjectName("pushButton_S1")
        self.verticalLayout.addWidget(self.pushButton_S1)
        self.pushButton_S2 = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_S2.setFont(font)
        self.pushButton_S2.setStyleSheet("QPushButton {\n"
                                         "    background-color: #4F39F6; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #4F39F6; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 18px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:disabled {\n"
                                         "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                         "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                         "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                         "}")
        self.pushButton_S2.setObjectName("pushButton_S2")
        self.verticalLayout.addWidget(self.pushButton_S2)
        self.pushButton_S3 = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_S3.setFont(font)
        self.pushButton_S3.setStyleSheet("QPushButton {\n"
                                         "    background-color: #4F39F6; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #4F39F6; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 18px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:disabled {\n"
                                         "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                         "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                         "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                         "}")
        self.pushButton_S3.setObjectName("pushButton_S3")
        self.verticalLayout.addWidget(self.pushButton_S3)
        self.pushButton_save_sensor = QtWidgets.QPushButton(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save_sensor.setFont(font)
        self.pushButton_save_sensor.setStyleSheet("QPushButton {\n"
                                                    "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                    "    color: #ECEFF4; /* Warna teks */\n"
                                                    "    border: 2px solid #1B5E20; /* Warna border */\n"
                                                    "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                    "    padding: 5px; /* Padding di dalam tombol */\n"
                                                    "    font-size: 18px; /* Ukuran font */\n"
                                                    "    font-weight: bold; /* Ketebalan font */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QPushButton:hover {\n"
                                                    "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                    "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QPushButton:pressed {\n"
                                                    "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                    "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                    "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QPushButton:disabled {\n"
                                                    "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                    "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                    "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                    "}")
        self.pushButton_save_sensor.setObjectName("pushButton_save_sensor")
        self.verticalLayout.addWidget(self.pushButton_save_sensor)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel#label_3 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_3:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.pushButton_info = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_info.setStyleSheet("QPushButton {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        # self.pushButton_info dibuat di sini (baris 1083-1084)
        self.pushButton_info.setObjectName("pushButton_info")
        self.verticalLayout.addWidget(self.pushButton_info) # Menambahkan TUTORIAL

        # --- Bagian Sisipan Tombol CREDIT di bawah TUTORIAL ---
        self.pushButton_credit = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_credit.setStyleSheet(self.pushButton_info.styleSheet())
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_credit.setFont(font)
        self.pushButton_credit.setObjectName("pushButton_credit")
        
        # 1. TAMBAHKAN TOMBOL CREDIT KE LAYOUT VERTICAL
        self.verticalLayout.addWidget(self.pushButton_credit) 
        # --- AKHIR SISIPAN TOMBOL CREDIT ---

        # 2. SEKARANG BARU TAMBAHKAN SPACER 
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1) 
        
        # Sisa kode di bawahnya...
        self.layout_BawahUtama.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(self.frame_bawahutama)
        self.frame_4.setEnabled(True)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(9, 9, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_KontrolAxis = QtWidgets.QFrame(self.frame_5)
        self.frame_KontrolAxis.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_KontrolAxis.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_KontrolAxis.setObjectName("frame_12")
        self.layout_Header_7 = QtWidgets.QHBoxLayout(self.frame_KontrolAxis)
        self.layout_Header_7.setContentsMargins(0, 0, 0, 0)
        self.layout_Header_7.setObjectName("horizontalLayout_7")
        self.frame = QtWidgets.QFrame(self.frame_KontrolAxis)
        self.frame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layout_KontrolAxis = QtWidgets.QVBoxLayout(self.frame)
        self.layout_KontrolAxis.setObjectName("verticalLayout_4")
        self.frame_X = QtWidgets.QFrame(self.frame)
        self.frame_X.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_X.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_X.setObjectName("frame_X")
        self.layout_Header_3 = QtWidgets.QHBoxLayout(self.frame_X)
        self.layout_Header_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame_X)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel#label {\n"
                                 "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                 "}\n"
                                 "QLabel#label:disabled {\n"
                                 "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                 "}\n"
                                 "")
        self.label.setObjectName("label")
        self.layout_Header_3.addWidget(self.label)
        self.horizontalSlider_X = QtWidgets.QSlider(self.frame_X)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.horizontalSlider_X.setFont(font)
        self.horizontalSlider_X.setAutoFillBackground(False)
        self.horizontalSlider_X.setStyleSheet("QSlider#horizontalSlider_X {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider */\n"
                                              "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                              "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::groove:horizontal {\n"
                                              "    border: 1px solid #0F172B; /* Border untuk jalur slider */\n"
                                              "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                              "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                              "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::handle:horizontal {\n"
                                              "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                              "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                              "    width: 25px; /* Lebar handle lebih besar */\n"
                                                "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::sub-page:horizontal {\n"
                                              "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::add-page:horizontal {\n"
                                              "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "/* Warna saat dinonaktifkan (disabled) */\n"
                                              "QSlider#horizontalSlider_X:disabled {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::groove:horizontal:disabled {\n"
                                              "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                              "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::handle:horizontal:disabled {\n"
                                              "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                              "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::sub-page:horizontal:disabled {\n"
                                              "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_X::add-page:horizontal:disabled {\n"
                                              "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                              "}")
        self.horizontalSlider_X.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_X.setInvertedAppearance(False)
        self.horizontalSlider_X.setInvertedControls(False)
        self.horizontalSlider_X.setObjectName("horizontalSlider_X")
        self.layout_Header_3.addWidget(self.horizontalSlider_X)
        self.doubleSpinBox_X = QtWidgets.QDoubleSpinBox(self.frame_X)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBox_X.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_X.setSizePolicy(sizePolicy)
        self.doubleSpinBox_X.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox_X.setFont(font)
        self.doubleSpinBox_X.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #1D293D; /* Warna latar belakang */
                                            color: #FFFFFF; /* Warna teks */
                                            border: 2px solid #1D293D; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2A3850;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #2A3850;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_X.setWrapping(False)
        self.doubleSpinBox_X.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_X.setProperty("showGroupSeparator", False)
        self.doubleSpinBox_X.setMinimum(0.0)
        self.doubleSpinBox_X.setObjectName("doubleSpinBox_X")
        self.layout_Header_3.addWidget(self.doubleSpinBox_X)
        self.layout_KontrolAxis.addWidget(self.frame_X)
        self.frame_Y = QtWidgets.QFrame(self.frame)
        self.frame_Y.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Y.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Y.setObjectName("frame_Y")
        self.layout_Header_4 = QtWidgets.QHBoxLayout(self.frame_Y)
        self.layout_Header_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_Y)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel#label_2 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_2:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_2.setObjectName("label_2")
        self.layout_Header_4.addWidget(self.label_2)
        self.horizontalSlider_Y = QtWidgets.QSlider(self.frame_Y)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.horizontalSlider_Y.setFont(font)
        self.horizontalSlider_Y.setStyleSheet("QSlider#horizontalSlider_Y {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider */\n"
                                              "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                              "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::groove:horizontal {\n"
                                              "    border: 1px solid 0F172B; /* Border untuk jalur slider */\n"
                                              "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                              "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                              "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::handle:horizontal {\n"
                                              "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                              "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                              "    width: 25px; /* Lebar handle lebih besar */\n"
                                                "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::sub-page:horizontal {\n"
                                              "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::add-page:horizontal {\n"
                                              "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "/* Warna saat dinonaktifkan (disabled) */\n"
                                              "QSlider#horizontalSlider_Y:disabled {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::groove:horizontal:disabled {\n"
                                              "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                              "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::handle:horizontal:disabled {\n"
                                              "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                              "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::sub-page:horizontal:disabled {\n"
                                              "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Y::add-page:horizontal:disabled {\n"
                                              "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                              "}")
        self.horizontalSlider_Y.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Y.setObjectName("horizontalSlider_Y")
        self.layout_Header_4.addWidget(self.horizontalSlider_Y)
        self.doubleSpinBox_Y = QtWidgets.QDoubleSpinBox(self.frame_Y)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBox_Y.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Y.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Y.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox_Y.setFont(font)
        self.doubleSpinBox_Y.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #3B4252; /* Warna latar belakang */
                                            color: #D8DEE9; /* Warna teks */
                                            border: 2px solid #1B5E20; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2E3440;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #81A1C1;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_Y.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_Y.setObjectName("doubleSpinBox_Y")
        self.layout_Header_4.addWidget(self.doubleSpinBox_Y)
        self.layout_KontrolAxis.addWidget(self.frame_Y)
        self.frame_Z = QtWidgets.QFrame(self.frame)
        self.frame_Z.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Z.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Z.setObjectName("frame_Z")
        self.layout_Header_5 = QtWidgets.QHBoxLayout(self.frame_Z)
        self.layout_Header_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame_Z)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel#label_4 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_4:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.layout_Header_5.addWidget(self.label_4)
        self.horizontalSlider_Z = QtWidgets.QSlider(self.frame_Z)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.horizontalSlider_Z.setFont(font)
        self.horizontalSlider_Z.setStyleSheet("QSlider#horizontalSlider_Z {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider */\n"
                                              "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                              "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::groove:horizontal {\n"
                                              "    border: 1px solid 0F172B; /* Border untuk jalur slider */\n"
                                              "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                              "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                              "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::handle:horizontal {\n"
                                              "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                              "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                              "    width: 25px; /* Lebar handle lebih besar */\n"
                                                "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::sub-page:horizontal {\n"
                                              "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::add-page:horizontal {\n"
                                              "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "/* Warna saat dinonaktifkan (disabled) */\n"
                                              "QSlider#horizontalSlider_Z:disabled {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::groove:horizontal:disabled {\n"
                                              "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                              "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::handle:horizontal:disabled {\n"
                                              "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                              "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::sub-page:horizontal:disabled {\n"
                                              "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_Z::add-page:horizontal:disabled {\n"
                                              "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                              "}")
        self.horizontalSlider_Z.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Z.setObjectName("horizontalSlider_Z")
        self.layout_Header_5.addWidget(self.horizontalSlider_Z)
        self.doubleSpinBox_Z = QtWidgets.QDoubleSpinBox(self.frame_Z)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBox_Z.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_Z.setSizePolicy(sizePolicy)
        self.doubleSpinBox_Z.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox_Z.setFont(font)
        self.doubleSpinBox_Z.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #3B4252; /* Warna latar belakang */
                                            color: #D8DEE9; /* Warna teks */
                                            border: 2px solid #1B5E20; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2E3440;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #81A1C1;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_Z.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_Z.setObjectName("doubleSpinBox_Z")
        self.layout_Header_5.addWidget(self.doubleSpinBox_Z)
        self.layout_KontrolAxis.addWidget(self.frame_Z)
        self.frame_E = QtWidgets.QFrame(self.frame)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.frame_E.setFont(font)
        self.frame_E.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_E.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_E.setObjectName("frame_E")
        self.layout_Header_6 = QtWidgets.QHBoxLayout(self.frame_E)
        self.layout_Header_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.frame_E)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("QLabel#label_5 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_5:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_5.setObjectName("label_5")
        self.layout_Header_6.addWidget(self.label_5)
        self.horizontalSlider_E = QtWidgets.QSlider(self.frame_E)
        self.horizontalSlider_E.setStyleSheet("QSlider#horizontalSlider_E {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider */\n"
                                              "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                              "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::groove:horizontal {\n"
                                              "    border: 1px solid 0F172B; /* Border untuk jalur slider */\n"
                                              "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                              "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                              "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::handle:horizontal {\n"
                                              "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                              "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                              "    width: 25px; /* Lebar handle lebih besar */\n"
                                                "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::sub-page:horizontal {\n"
                                              "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::add-page:horizontal {\n"
                                              "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                              "    border-radius: 8px; /* Sudut melengkung */\n"
                                              "}\n"
                                              "\n"
                                              "/* Warna saat dinonaktifkan (disabled) */\n"
                                              "QSlider#horizontalSlider_E:disabled {\n"
                                              "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::groove:horizontal:disabled {\n"
                                              "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                              "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::handle:horizontal:disabled {\n"
                                              "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                              "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::sub-page:horizontal:disabled {\n"
                                              "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                              "}\n"
                                              "\n"
                                              "QSlider#horizontalSlider_E::add-page:horizontal:disabled {\n"
                                              "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                              "}")
        self.horizontalSlider_E.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_E.setObjectName("horizontalSlider_E")
        self.layout_Header_6.addWidget(self.horizontalSlider_E)
        self.doubleSpinBox_E = QtWidgets.QDoubleSpinBox(self.frame_E)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBox_E.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_E.setSizePolicy(sizePolicy)
        self.doubleSpinBox_E.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox_E.setFont(font)
        self.doubleSpinBox_E.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #3B4252; /* Warna latar belakang */
                                            color: #D8DEE9; /* Warna teks */
                                            border: 2px solid #1B5E20; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2E3440;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #81A1C1;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_E.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_E.setObjectName("doubleSpinBox_E")
        self.layout_Header_6.addWidget(self.doubleSpinBox_E)
        self.layout_KontrolAxis.addWidget(self.frame_E)
        self.frame_speed = QtWidgets.QFrame(self.frame)
        self.frame_speed.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_speed.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_speed.setObjectName("frame_speed")
        self.layout_Header_8 = QtWidgets.QHBoxLayout(self.frame_speed)
        self.layout_Header_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.frame_speed)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("QLabel#label_6 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_6:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_6.setObjectName("label_6")
        self.layout_Header_8.addWidget(self.label_6)
        self.horizontalSlider_speed = QtWidgets.QSlider(self.frame_speed)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.horizontalSlider_speed.setFont(font)
        self.horizontalSlider_speed.setStyleSheet("QSlider#horizontalSlider_speed {\n"
                                                    "    background-color: #0F172B; /* Latar belakang slider */\n"
                                                    "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                                    "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::groove:horizontal {\n"
                                                    "    border: 1px solid 0F172B; /* Border untuk jalur slider */\n"
                                                    "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                                    "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                                    "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::handle:horizontal {\n"
                                                    "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                                    "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                                    "    width: 25px; /* Lebar handle lebih besar */\n"
                                                        "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                        "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                        "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::sub-page:horizontal {\n"
                                                    "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                                    "    border-radius: 8px; /* Sudut melengkung */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::add-page:horizontal {\n"
                                                    "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                                    "    border-radius: 8px; /* Sudut melengkung */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* Warna saat dinonaktifkan (disabled) */\n"
                                                    "QSlider#horizontalSlider_speed:disabled {\n"
                                                    "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::groove:horizontal:disabled {\n"
                                                    "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                                    "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::handle:horizontal:disabled {\n"
                                                    "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                                    "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::sub-page:horizontal:disabled {\n"
                                                    "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QSlider#horizontalSlider_speed::add-page:horizontal:disabled {\n"
                                                    "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                                    "}")
        self.horizontalSlider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_speed.setObjectName("horizontalSlider_speed")
        self.layout_Header_8.addWidget(self.horizontalSlider_speed)
        self.doubleSpinBox_speed = QtWidgets.QDoubleSpinBox(self.frame_speed)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBox_speed.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_speed.setSizePolicy(sizePolicy)
        self.doubleSpinBox_speed.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox_speed.setFont(font)
        self.doubleSpinBox_speed.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #3B4252; /* Warna latar belakang */
                                            color: #D8DEE9; /* Warna teks */
                                            border: 2px solid #1B5E20; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2E3440;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #81A1C1;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_speed.setObjectName("doubleSpinBox_speed")
        self.layout_Header_8.addWidget(self.doubleSpinBox_speed)
        self.layout_KontrolAxis.addWidget(self.frame_speed)
        self.frame_gripper = QtWidgets.QFrame(self.frame)
        self.frame_gripper.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_gripper.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_gripper.setObjectName("frame_gripper")
        self.layout_Header_9 = QtWidgets.QHBoxLayout(self.frame_gripper)
        self.layout_Header_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.frame_gripper)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("QLabel#label_7 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_7:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_7.setObjectName("label_7")
        self.layout_Header_9.addWidget(self.label_7)
        self.horizontalSlider_gripper_servo = QtWidgets.QSlider(
            self.frame_gripper)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.horizontalSlider_gripper_servo.setFont(font)
        self.horizontalSlider_gripper_servo.setStyleSheet("QSlider#horizontalSlider_gripper_servo {\n"
                                                            "    background-color: #0F172B; /* Latar belakang slider */\n"
                                                            "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                                            "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::groove:horizontal {\n"
                                                            "    border: 1px solid 0F172B; /* Border untuk jalur slider */\n"
                                                            "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                                            "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                                            "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::handle:horizontal {\n"
                                                            "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                                            "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                                            "    width: 25px; /* Lebar handle lebih besar */\n"
                                                                "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                                "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                                "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::sub-page:horizontal {\n"
                                                            "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                                            "    border-radius: 8px; /* Sudut melengkung */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::add-page:horizontal {\n"
                                                            "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                                            "    border-radius: 8px; /* Sudut melengkung */\n"
                                                            "}\n"
                                                            "\n"
                                                            "/* Warna saat dinonaktifkan (disabled) */\n"
                                                            "QSlider#horizontalSlider_gripper_servo:disabled {\n"
                                                            "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::groove:horizontal:disabled {\n"
                                                            "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                                            "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::handle:horizontal:disabled {\n"
                                                            "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                                            "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::sub-page:horizontal:disabled {\n"
                                                            "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servo::add-page:horizontal:disabled {\n"
                                                            "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                                            "}")
        self.horizontalSlider_gripper_servo.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_gripper_servo.setObjectName("horizontalSlider_gripper_servo")
        self.layout_Header_9.addWidget(self.horizontalSlider_gripper_servo)
        self.doubleSpinBox_gripper_servo = QtWidgets.QDoubleSpinBox(self.frame_gripper)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_gripper_servo.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_gripper_servo.setSizePolicy(sizePolicy)
        self.doubleSpinBox_gripper_servo.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.doubleSpinBox_gripper_servo.setFont(font)
        self.doubleSpinBox_gripper_servo.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #3B4252; /* Warna latar belakang */
                                            color: #D8DEE9; /* Warna teks */
                                            border: 2px solid #1B5E20; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2E3440;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #81A1C1;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_gripper_servo.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_gripper_servo.setObjectName("doubleSpinBox_gripper_servo")
        self.layout_Header_9.addWidget(self.doubleSpinBox_gripper_servo)


        self.label_13 = QtWidgets.QLabel(self.frame_gripper)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("QLabel#label_13 {\n"
                                   "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                   "}\n"
                                   "QLabel#label_13:disabled {\n"
                                   "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                   "}\n"
                                   "")
        self.label_13.setObjectName("label_13")
        self.layout_Header_9.addWidget(self.label_13)
        self.horizontalSlider_gripper_servoB = QtWidgets.QSlider(self.frame_gripper)
        self.horizontalSlider_gripper_servoB.setMaximumSize(QtCore.QSize(250, 16777215))
        self.horizontalSlider_gripper_servoB.setStyleSheet("QSlider#horizontalSlider_gripper_servoB {\n"
                                                            "    background-color: #0F172B; /* Latar belakang slider */\n"
                                                            "    border-radius: 12px; /* Membuat sudut melengkung pada slider */\n"
                                                            "    height: 30px; /* Menambah tinggi keseluruhan slider untuk membuatnya lebih tebal */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::groove:horizontal {\n"
                                                            "    border: 1px solid 0F172B; /* Border untuk jalur slider */\n"
                                                            "    background: #0F172B; /* Latar belakang jalur slider */\n"
                                                            "    height: 15px; /* Membuat jalur slider lebih tebal */\n"
                                                            "    border-radius: 8px; /* Sudut melengkung pada jalur */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::handle:horizontal {\n"
                                                            "    background: #FFFFFF; /* Warna handle (knob) */\n"
                                                            "    border: 2px solid #4A36DE; /* Border di sekitar handle */\n"
                                                            "    width: 25px; /* Lebar handle lebih besar */\n"
                                                                "    height: 15px; /* Tinggi handle lebih besar */\n"
                                                                "    border-radius: 12.5px; /* Sudut melengkung pada handle untuk membuatnya bulat */\n"
                                                                "    margin: -6px 0; /* Membuat handle lebih besar dari jalur */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::sub-page:horizontal {\n"
                                                            "    background: #4F39F6; /* Warna bagian yang sudah terisi */\n"
                                                            "    border-radius: 8px; /* Sudut melengkung */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::add-page:horizontal {\n"
                                                            "    background: #D4CDFF; /* Warna bagian yang belum terisi */\n"
                                                            "    border-radius: 8px; /* Sudut melengkung */\n"
                                                            "}\n"
                                                            "\n"
                                                            "/* Warna saat dinonaktifkan (disabled) */\n"
                                                            "QSlider#horizontalSlider_gripper_servoB:disabled {\n"
                                                            "    background-color: #0F172B; /* Latar belakang slider yang lebih gelap */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::groove:horizontal:disabled {\n"
                                                            "    background: #6D6D6D; /* Warna groove abu-abu saat dinonaktifkan */\n"
                                                            "    border: 1px solid #808080; /* Border groove lebih cerah */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::handle:horizontal:disabled {\n"
                                                            "    background: #A0A0A0; /* Warna handle abu-abu */\n"
                                                            "    border: 2px solid #888888; /* Border handle abu-abu */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::sub-page:horizontal:disabled {\n"
                                                            "    background: #808080; /* Warna bagian yang sudah terisi saat dinonaktifkan */\n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider#horizontalSlider_gripper_servoB::add-page:horizontal:disabled {\n"
                                                            "    background: #C0C0C0; /* Warna bagian yang belum terisi saat dinonaktifkan */\n"
                                                            "}")
        self.horizontalSlider_gripper_servoB.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_gripper_servoB.setObjectName("horizontalSlider_gripper_servoB")
        self.layout_Header_9.addWidget(self.horizontalSlider_gripper_servoB)
        self.doubleSpinBox_gripper_servoB = QtWidgets.QDoubleSpinBox(self.frame_gripper)
        self.doubleSpinBox_gripper_servoB.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #3B4252; /* Warna latar belakang */
                                            color: #D8DEE9; /* Warna teks */
                                            border: 2px solid #1B5E20; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #81A1C1;
                                            selection-color: #2E3440;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #81A1C1;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #88C0D0;
                                            background-color: #434C5E;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox_gripper_servoB.setObjectName("doubleSpinBox_gripper_servoB")
        self.layout_Header_9.addWidget(self.doubleSpinBox_gripper_servoB)
        self.pushButton_save_servo_seld = QtWidgets.QPushButton(self.frame_gripper)
        self.pushButton_save_servo_seld.setStyleSheet("QPushButton {\n"
                                                        "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                        "    color: #ECEFF4; /* Warna teks */\n"
                                                        "    border: 2px solid #1B5E20; /* Warna border */\n"
                                                        "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                        "    padding: 5px; /* Padding di dalam tombol */\n"
                                                        "    font-size: 18px; /* Ukuran font */\n"
                                                        "    font-weight: bold; /* Ketebalan font */\n"
                                                        "}\n"
                                                        "\n"
                                                        "QPushButton:hover {\n"
                                                        "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                        "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                        "}\n"
                                                        "\n"
                                                        "QPushButton:pressed {\n"
                                                        "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                        "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                        "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                        "}\n"
                                                        "\n"
                                                        "QPushButton:disabled {\n"
                                                        "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                        "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                        "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                        "}")
        self.pushButton_save_servo_seld.setObjectName("pushButton_save_servo_seld")
        self.layout_Header_9.addWidget(self.pushButton_save_servo_seld)

        self.layout_KontrolAxis.addWidget(self.frame_gripper)
        self.frame_button = QtWidgets.QFrame(self.frame)
        self.frame_button.setEnabled(True)
        self.frame_button.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_button.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_button.setObjectName("frame_button")
        self.layout_Header_10 = QtWidgets.QHBoxLayout(self.frame_button)
        self.layout_Header_10.setObjectName("horizontalLayout_10")
        self.pushButton_save_move = QtWidgets.QPushButton(self.frame_button)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save_move.setFont(font)
        self.pushButton_save_move.setStyleSheet("QPushButton {\n"
                                                "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                                "    color: #FFFFFF; /* Warna teks */\n"
                                                "    border: 2px solid #1D293D; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                                "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
        self.pushButton_save_move.setObjectName("pushButton_save_move")
        self.layout_Header_10.addWidget(self.pushButton_save_move)
        self.pushButton_LG4 = QtWidgets.QPushButton(self.frame_button)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_LG4.setFont(font)
        self.pushButton_LG4.setStyleSheet("QPushButton {\n"
                                          "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        self.pushButton_LG4.setObjectName("pushButton_LG4")
        self.layout_Header_10.addWidget(self.pushButton_LG4)
        
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.frame_button)

        self.doubleSpinBox.setStyleSheet("""
                                        QDoubleSpinBox {
                                            background-color: #1D293D; /* Warna latar belakang */
                                            color: #FFFFFF; /* Warna teks */
                                            border: 2px solid #1D293D; /* Warna border */
                                            border-radius: 4px; /* Sudut melengkung dikurangi */
                                            font-size: 18px; /* Ukuran font lebih kecil */
                                            font-weight: bold;
                                            padding: 2px 4px; /* Padding dalam dikurangi */
                                            selection-background-color: #4F39F6;
                                            selection-color: #FFFFFF;
                                            min-height: 25px; /* Tinggi minimal */
                                            min-width: 60px;  /* Lebar minimal */
                                        }

                                        /* Efek hover */
                                        QDoubleSpinBox:hover {
                                            border: 2px solid #27344A;
                                        }

                                        /* Efek saat aktif (focus) */
                                        QDoubleSpinBox:focus {
                                            border: 2px solid #27344A;
                                            background-color: #27344A;
                                        }

                                        /* Saat dinonaktifkan */
                                        QDoubleSpinBox:disabled {
                                            background-color: #3B4252;
                                            color: #7F8C9A;
                                            border: 2px solid #3B4252;
                                        }

                                        /* Gaya tombol panah saat ditekan */
                                        QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed {
                                            background-color: #4C566A;
                                        }
                                    
                                        /* Menyesuaikan ukuran tombol panah */
                                        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                                            width: 30px;  /* Lebar tombol panah */
                                            height: 14px; /* Tinggi tombol panah */  
                                        }
                                    """)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.layout_Header_10.addWidget(self.doubleSpinBox)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setProperty("value", 1)




        self.pushButton_home = QtWidgets.QPushButton(self.frame_button)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_home.setFont(font)
        self.pushButton_home.setStyleSheet("QPushButton {\n"
                                           "    background-color: #1D293D; /* Warna latar belakang tombol */\n"
                                            "    color: #FFFFFF; /* Warna teks */\n"
                                            "    border: 2px solid #1D293D; /* Warna border */\n"
                                            "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                            "    padding: 5px; /* Padding di dalam tombol */\n"
                                            "    font-size: 18px; /* Ukuran font */\n"
                                            "    font-weight: bold; /* Ketebalan font */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: #2A3850; /* Warna latar belakang saat hover */\n"
                                            "    border: 2px solid #2A3850; /* Warna border saat hover */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "    background-color: #1D293D; /* Warna latar belakang saat ditekan */\n"
                                            "    border: 2px solid #1D293D; /* Warna border saat ditekan */\n"
                                            "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:disabled {\n"
                                            "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                            "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                            "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                            "}")
        self.pushButton_home.setObjectName("pushButton_home")
        self.layout_Header_10.addWidget(self.pushButton_home)
        self.layout_KontrolAxis.addWidget(self.frame_button)
        self.layout_Header_7.addWidget(self.frame)
        self.verticalLayout_3.addWidget(self.frame_KontrolAxis)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.frame_MonitorInput = QtWidgets.QFrame(self.frame_4)
        self.frame_MonitorInput.setEnabled(True)
        self.frame_MonitorInput.setMaximumSize(QtCore.QSize(16777215, 400))
        self.frame_MonitorInput.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_MonitorInput.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_MonitorInput.setObjectName("frame_output_input")
        self.layout_Header_13 = QtWidgets.QHBoxLayout(
            self.frame_MonitorInput)
        self.layout_Header_13.setContentsMargins(0, 0, 0, 0)
        self.layout_Header_13.setObjectName("horizontalLayout_13")
        self.frame_6 = QtWidgets.QFrame(self.frame_MonitorInput)
        self.frame_6.setEnabled(True)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        # --- KODE BARU UNTUK LABEL SERIAL MONITOR ---
        self.label_serial_monitor = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_serial_monitor.setFont(font)
        self.label_serial_monitor.setStyleSheet("""
        QLabel {
            color: #FFFFFF; /* Warna Abu-abu (Soft/Disable Look) */
        }
        QLabel:disabled {
            color: #5C677D; /* Warna teks item saat dinonaktifkan (Jauh lebih abu-abu) */
        }
        """)
        self.label_serial_monitor.setAlignment(QtCore.Qt.AlignCenter)
        self.label_serial_monitor.setObjectName("label_serial_monitor")
        self.verticalLayout_5.addWidget(self.label_serial_monitor)
        # --- AKHIR KODE BARU ---
        self.textEdit_vew = QtWidgets.QTextEdit(self.frame_6)
        self.textEdit_vew.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.textEdit_vew.setFont(font)
        self.textEdit_vew.setStyleSheet("QTextEdit {\n"
                                        "    background-color: #1D293D; /* Warna latar belakang utama */\n"
                                        "    color: #877AE7; /* Warna teks */\n"
                                        "    border: 2px solid #1D293D; /* Border dengan warna gelap */\n"
                                        "    border-radius: 12px; /* Sudut melengkung */\n"
                                        "    font-size: 14px; /* Ukuran font */\n"
                                        "    padding: 8px; /* Padding dalam */\n"
                                        "    selection-background-color: #4F39F6; /* Warna latar belakang saat teks diseleksi */\n"
                                        "    selection-color: #FFFFFF; /* Warna teks saat diseleksi */\n"
                                        "}\n"
                                        "\n"
                                        "/* Scrollbar Vertikal */\n"
                                        "QScrollBar:vertical {\n"
                                        "    background: #3B4252; /* Warna latar belakang scrollbar */\n"
                                        "    width: 12px; /* Lebar scrollbar */\n"
                                        "    border-radius: 6px;\n"
                                        "}\n"
                                        "\n"
                                        "/* Handle (bagian yang bisa digerakkan) */\n"
                                        "QScrollBar::handle:vertical {\n"
                                        "    background: #4C566A; /* Warna handle */\n"
                                        "    border-radius: 6px;\n"
                                        "    min-height: 20px;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::handle:vertical:hover {\n"
                                        "    background: #81A1C1; /* Warna handle saat hover */\n"
                                        "}\n"
                                        "\n"
                                        "/* Tombol atas & bawah di scrollbar */\n"
                                        "QScrollBar::add-line:vertical,\n"
                                        "QScrollBar::sub-line:vertical {\n"
                                        "    background: none;\n"
                                        "}\n"
                                        "\n"
                                        "/* Latar belakang area kosong di scrollbar */\n"
                                        "QScrollBar::add-page:vertical,\n"
                                        "QScrollBar::sub-page:vertical {\n"
                                        "    background: none;\n"
                                        "}\n"
                                        "\n"
                                        "/* Scrollbar Horizontal */\n"
                                        "QScrollBar:horizontal {\n"
                                        "    background: #3B4252;\n"
                                        "    height: 12px;\n"
                                        "    border-radius: 6px;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::handle:horizontal {\n"
                                        "    background: #4C566A;\n"
                                        "    border-radius: 6px;\n"
                                        "    min-width: 20px;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::handle:horizontal:hover {\n"
                                        "    background: #81A1C1;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::add-line:horizontal,\n"
                                        "QScrollBar::sub-line:horizontal {\n"
                                        "    background: none;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::add-page:horizontal,\n"
                                        "QScrollBar::sub-page:horizontal {\n"
                                        "    background: none;\n"
                                        "}\n"
                                        "\n"
                                        "QTextEdit:disabled {\n"
                                        "    background-color: #3B4252; /* Warna latar belakang saat dinonaktifkan */\n"
                                        "    color: #7F8C9A; /* Warna teks saat dinonaktifkan */\n"
                                        "    border: 2px solid #3B4252; /* Warna border saat dinonaktifkan */\n"
                                        "}\n"
                                        "\n"
                                        "QTextEdit::item:disabled {\n"
                                        "    background-color: #2E3440; /* Warna latar belakang item saat dinonaktifkan */\n"
                                        "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                        "}\n"
                                        "")
        self.textEdit_vew.setLineWrapColumnOrWidth(0)
        self.textEdit_vew.setReadOnly(True)
        self.textEdit_vew.setPlaceholderText("")
        self.textEdit_vew.setObjectName("textEdit_vew")
        self.verticalLayout_5.addWidget(self.textEdit_vew)
        # ... (setelah self.verticalLayout_5.addWidget(self.label_serial_monitor) dan self.verticalLayout_5.addWidget(self.textEdit_vew) )
        
        # --- KODE BARU: DEKLARASI DAN PENEMPATAN TOMBOL CLEAR MONITOR (DIANTARA MONITOR DAN INPUT) ---
        self.pushButton_clear_monitor = QtWidgets.QPushButton(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_clear_monitor.setFont(font)
        self.pushButton_clear_monitor.setStyleSheet("QPushButton {\n"
                                                 "    background-color: #E78F36; /* Warna latar belakang tombol */\n"
                                                "    color: #FFFFFF; /* Warna teks */\n"
                                                "    border: 2px solid #E78F36; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #F4A351; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #F4A351; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #E78F36; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #E78F36; /* Warna border saat ditekan */\n"
                                                "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
        self.pushButton_clear_monitor.setObjectName("pushButton_clear_monitor")
        
        # PENTING: Tambahkan tombol ini SEBELUM frame input manual (self.frame_7)
        self.verticalLayout_5.addWidget(self.pushButton_clear_monitor)
        # --- AKHIR KODE BARU ---
        
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        # ... (Sisa kode untuk self.frame_7, lineEdit, dan tombol save input)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 115))
        self.frame_7.setSizeIncrement(QtCore.QSize(0, 0))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.layout_BawahUtama0 = QtWidgets.QHBoxLayout(self.frame_7)
        self.layout_BawahUtama0.setObjectName("horizontalLayout_20")
        self.label_24 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("QLabel#label_24 {\n"
                                    "    color: #FFFFFF; /* Mengubah warna teks menjadi putih */\n"
                                    "}\n"
                                    "QLabel#label_24:disabled {\n"
                                    "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                    "}\n"
                                    "")
        self.label_24.setObjectName("label_24")
        self.layout_BawahUtama0.addWidget(self.label_24)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_7)
        self.lineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 33))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        self.lineEdit.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1) #Kotak perintah
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "    background-color: #1D293D; /* Warna latar belakang */\n"
                                    "    color: #FFFFFF; /* Warna teks */\n"
                                    "    border: 2px solid #1D293D; /* Warna border */\n"
                                    "    border-radius: 7px; /* Sudut melengkung */\n"
                                    "    font-size: 15px; /* Ukuran font */\n"
                                    "    padding: 6px; /* Padding dalam */\n"
                                    "    selection-background-color: #4F39F6; /* Warna latar belakang saat teks diseleksi */\n"
                                    "    selection-color: #FFFFFF; /* Warna teks saat diseleksi */\n"
                                    "}\n"
                                    "\n"
                                    "/* Efek hover */\n"
                                    "QLineEdit:hover {\n"
                                    "    border: 2px solid #27344A; /* Border lebih terang saat hover */\n"
                                    "}\n"
                                    "\n"
                                    "/* Efek saat LineEdit aktif (focus) */\n"
                                    "QLineEdit:focus {\n"
                                    "    border: 2px solid #27344A; /* Warna lebih cerah saat aktif */\n"
                                    "    background-color: #27344A; /* Latar belakang sedikit lebih terang */\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit:disabled {\n"
                                    "    background-color: #3B4252; /* Warna latar belakang saat dinonaktifkan */\n"
                                    "    color: #7F8C9A; /* Warna teks saat dinonaktifkan */\n"
                                    "    border: 2px solid #3B4252; /* Warna border saat dinonaktifkan */\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit::item:disabled {\n"
                                    "    background-color: #2E3440; /* Warna latar belakang item saat dinonaktifkan */\n"
                                    "    color: #5C677D; /* Warna teks item saat dinonaktifkan */\n"
                                    "}\n"
                                    "")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setFrame(True)
        self.lineEdit.setObjectName("lineEdit")
        self.layout_BawahUtama0.addWidget(self.lineEdit) #Save paling bawah
        self.pushButton_save_manual = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_save_manual.setMinimumSize(QtCore.QSize(200, 33))
        self.pushButton_save_manual.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_save_manual.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton_save_manual.setStyleSheet("QPushButton {\n"
                                                 "    background-color: #E78F36; /* Warna latar belakang tombol */\n"
                                                "    color: #FFFFFF; /* Warna teks */\n"
                                                "    border: 2px solid #E78F36; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #F4A351; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #F4A351; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #E78F36; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #E78F36; /* Warna border saat ditekan */\n"
                                                "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
        self.pushButton_save_manual.setObjectName("pushButton_save_manual")
        self.layout_BawahUtama0.addWidget(self.pushButton_save_manual)
        self.verticalLayout_5.addWidget(self.frame_7)
        self.layout_Header_13.addWidget(self.frame_6)
        self.verticalLayout_2.addWidget(self.frame_MonitorInput)
        self.layout_BawahUtama.addWidget(self.frame_4)
        self.gridLayout.addWidget(self.frame_bawahutama, 1, 0, 1, 1)
        DOBOTROBOT_V1.setCentralWidget(self.centralwidget)

        self.retranslateUi(DOBOTROBOT_V1)
        QtCore.QMetaObject.connectSlotsByName(DOBOTROBOT_V1)

    def retranslateUi(self, DOBOTROBOT_V1):
        _translate = QtCore.QCoreApplication.translate
        DOBOTROBOT_V1.setWindowTitle(_translate(
            "DOBOTROBOT_V1", "GUI DOBOT - PSM 2025"))
        self.pushButton_start.setText(_translate("DOBOTROBOT_V1", "START"))
        self.pushButton_pause.setText(_translate("DOBOTROBOT_V1", "PAUSE"))
        self.pushButton_stop.setText(_translate("DOBOTROBOT_V1", "STOP"))
        self.pushButton_single_run.setText(_translate("DOBOTROBOT_V1", "SINGLE RUN"))
        self.pushButton_save_as.setText(
            _translate("DOBOTROBOT_V1", "SAVE"))
        self.label_port_usb.setText(_translate("DOBOTROBOT_V1", "PORT USB"))
        self.pushButton_connect.setText(
            _translate("DOBOTROBOT_V1", "CONNECT"))
        self.lineEdit_com.setText(_translate("DOBOTROBOT_V1", "COM"))
        self.label_status.setText(_translate("DOBOTROBOT_V1", "STATUS"))
        self.pushButton_calibration.setText(
            _translate("DOBOTROBOT_V1", "CALIBRATION"))
        __sortingEnabled = self.listWidget_save.isSortingEnabled()
        self.listWidget_save.setSortingEnabled(False)
        item = self.listWidget_save.item(0)
        item.setText(_translate("DOBOTROBOT_V1", "G0 X0 Y100 Z2 F200"))
        item = self.listWidget_save.item(1)
        item.setText(_translate("DOBOTROBOT_V1", "G0 X0 Y100 Z222 F200"))
        item = self.listWidget_save.item(2)
        item.setText(_translate("DOBOTROBOT_V1", "G0 X0 Y100 Z2 F200"))
        item = self.listWidget_save.item(3)
        item.setText(_translate("DOBOTROBOT_V1", "G0 X0 Y100 Z2 F200"))
        self.listWidget_save.setSortingEnabled(__sortingEnabled)
        self.label_8.setText(_translate("DOBOTROBOT_V1", "MAIN CONTROL"))
        self.pushButton_edit.setText(_translate("DOBOTROBOT_V1", "OPEN PROGRAM"))
        self.pushButton_next.setText(_translate("DOBOTROBOT_V1", "EDIT"))
        self.pushButton_new.setText(_translate("DOBOTROBOT_V1", "NEW"))
        self.pushButton_delete.setText(_translate("DOBOTROBOT_V1", "DELETE"))
        self.pushButton_clear.setText(_translate("DOBOTROBOT_V1", "CLEAR"))
        self.pushButton_up.setText(_translate("DOBOTROBOT_V1", "UP"))
        self.pushButton_down.setText(_translate("DOBOTROBOT_V1", "DOWN"))
        self.pushButton_gripper_01.setText(_translate("DOBOTROBOT_V1", "GRIPPER 01"))
        self.label_9.setText(_translate("DOBOTROBOT_V1", "GRIPPER"))
        self.pushButton_gripper_vacum.setText(_translate("DOBOTROBOT_V1", "VACUM OFF"))
        self.pushButton_gripper_servo.setText(_translate("DOBOTROBOT_V1", "SERVO OFF"))
        self.pushButton_save_servo.setText(_translate("DOBOTROBOT_V1", "SAVE"))
        self.label_10.setText(_translate("DOBOTROBOT_V1", "OUTPUT"))
        self.pushButton_LG1.setText(_translate("DOBOTROBOT_V1", "LG1 OFF"))
        self.pushButton_LG2.setText(_translate("DOBOTROBOT_V1", "LG2 OFF"))
        self.pushButton_LG3.setText(_translate("DOBOTROBOT_V1", "LG3 OFF"))
        self.pushButton_save_LG.setText(_translate("DOBOTROBOT_V1", "SAVE"))
        self.label_12.setText(_translate("DOBOTROBOT_V1", "CEK NOV"))
        self.pushButton_cek_posisi.setText(_translate("DOBOTROBOT_V1", "CEK POSISI"))
        self.pushButton_endstop.setText(_translate("DOBOTROBOT_V1", "CEK ENDSTOP"))
        self.pushButton_motor_ONOFF.setText(_translate("DOBOTROBOT_V1", "MOTOR OFF"))
        self.pushButton_fan.setText(_translate("DOBOTROBOT_V1", "FAN OFF"))
        self.label_11.setText(_translate("DOBOTROBOT_V1", "INPUT"))
        self.pushButton_S1.setText(_translate("DOBOTROBOT_V1", "SENSOR 1"))
        self.pushButton_S2.setText(_translate("DOBOTROBOT_V1", "SENSOR 2"))
        self.pushButton_S3.setText(_translate("DOBOTROBOT_V1", "SENSOR 3"))
        self.pushButton_save_sensor.setText(_translate("DOBOTROBOT_V1", "SAVE")) #masukan nama di sisni
        self.label_3.setText(_translate("DOBOTROBOT_V1", "INFO"))
        self.pushButton_info.setText(_translate("DOBOTROBOT_V1", "TUTORIAL"))
        self.pushButton_credit.setText(_translate("DOBOTROBOT_V1", "CREDIT"))
        self.label.setText(_translate("DOBOTROBOT_V1", "X"))
        self.label_2.setText(_translate("DOBOTROBOT_V1", "Y"))
        self.label_4.setText(_translate("DOBOTROBOT_V1", "Z"))
        self.label_5.setText(_translate("DOBOTROBOT_V1", "E"))
        self.label_6.setText(_translate("DOBOTROBOT_V1", "F"))
        self.label_7.setText(_translate("DOBOTROBOT_V1", "A"))
        self.label_13.setText(_translate("DOBOTROBOT_V1", "GRIPER"))
        self.pushButton_save_servo_seld.setText(_translate("DOBOTROBOT_V1", "SAVE"))
        self.pushButton_save_move.setText(_translate("DOBOTROBOT_V1", "SAVE MOVE"))
        self.pushButton_LG4.setText(_translate("DOBOTROBOT_V1", "SAVE DELAY"))
        self.pushButton_home.setText(_translate("DOBOTROBOT_V1", "GO HOME"))
        self.textEdit_vew.setHtml(_translate("DOBOTROBOT_V1", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14px; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">DOBOTROBOT_V1</span></p></body></html>"))
        self.label_24.setText(_translate("DOBOTROBOT_V1", "INPUT"))
        self.lineEdit.setPlaceholderText(_translate(
            "DOBOTROBOT_V1", "Kirim Perintah Manual Contoh G28"))
        self.pushButton_save_manual.setText(_translate("DOBOTROBOT_V1", "SAVE"))
        self.label_serial_monitor.setText(_translate("DOBOTROBOT_V1", "SERIAL MONITOR"))
        self.pushButton_clear_monitor.setText(_translate("DOBOTROBOT_V1", "CLEAR MONITOR"))
# =============================================================================================        
        
        
        
        
        
        
# =============================================================================================
# ----------------------------------------------------------------------------------------------
        self.sensor_status = {'S1': False, 'S2': False, 'S3': False}
# ----------------------------------------------------------------------------------------------
        self.listWidget_save.itemSelectionChanged.connect(self.update_spinboxes_from_selected_item)
# ----------------------------------------------------------------------------------------------       
        self.listWidget_save.itemDoubleClicked.connect(self.edit_item2)  # Event double-click
# ----------------------------------------------------------------------------------------------
        # Pasang event filter
        self.listWidget_save.viewport().installEventFilter(self)
# ----------------------------------------------------------------------------------------------
        self.listWidget_save.clear()
# ----------------------------------------------------------------------------------------------
        self.blink_timer = QTimer()  # Timer untuk kedipan border
        self.blink_timer.timeout.connect(self.toggle_border_color)
        self.blink_state = False  # Status kedipan (ON/OFF)
# ----------------------------------------------------------------------------------------------
        self.blink_timer_calibrasi = QTimer()
        self.blink_timer_calibrasi.timeout.connect(self.toggle_border_color_calibrasi)
        self.blink_state_kalibrasi = False
# ----------------------------------------------------------------------------------------------
        self.blink_timer_move = QTimer()
        self.blink_timer_move.timeout.connect(self.toggle_border_color_move)
        self.blink_state_move = False
# ----------------------------------------------------------------------------------------------
        self.blink_timer_move_servo = QTimer()
        self.blink_timer_move_servo.timeout.connect(self.toggle_border_color_move_servo)
        self.blink_state_move_servo = False
# ----------------------------------deteksi_port_com--------------------------------------------
        self.last_detected_ports = []  # Simpan status terakhir
        self.first_run = True  # Flag untuk deteksi pertama kali
        self.timer_deteksi_port_com = QTimer()
        self.timer_deteksi_port_com.timeout.connect(self.deteksi_port_com)
        self.timer_deteksi_port_com.start(1000)  # Cek setiap 1.5 detik
# ----------------------------------variabel----------------------------------------------------
        self.tanda_kalibrasi = False  # Inisialisasi status kalibrasi di constructor
        self.status_rail_on_off = False
        self.tanda_motor = False
        self.serial_buffer = ""  # Buffer untuk menyimpan data sementara
        self.baris = []  # List untuk menyimpan baris G-code dari listWidget_save
        self.current_line_index = 0  # Posisi baris saat ini dalam pengiriman
        self.ok_received = False  # Flag untuk menerima balasan 'ok'
        self.stop_sending = False  # Flag untuk menghentikan pengiriman
        self.pause_sending = False  # Flag untuk mode pause
        self.is_looping_mode = False # True = Loop, False = Single Run
# ---------------------------------------Output-------------------------------------------------
        self.pushButton_LG1.setCheckable(True)
        self.pushButton_LG1.clicked.connect(self.fungsi_pushButton_LG1)
# ----------------------------------------------------------------------------------------------
        self.pushButton_LG2.setCheckable(True)
        self.pushButton_LG2.clicked.connect(self.fungsi_pushButton_LG2)
# ----------------------------------------------------------------------------------------------
        self.pushButton_LG3.setCheckable(True)
        self.pushButton_LG3.clicked.connect(self.fungsi_pushButton_LG3)
# ----------------------------------------------------------------------------------------------
        self.pushButton_save_LG.setCheckable(False)
        self.pushButton_save_LG.clicked.connect(self.fungsi_pushButton_save_LG)
# ----------------------------------------------------------------------------------------------  
        self.pushButton_home.setCheckable(False)
        self.pushButton_home.clicked.connect(self.fungsi_pushButton_home)      
# ---------------------------------------gripper------------------------------------------------
        self.pushButton_gripper_servo.setCheckable(True)
        self.pushButton_gripper_servo.clicked.connect(self.fungsi_pushButton_gripper_servo)
# ----------------------------------------------------------------------------------------------
        self.pushButton_gripper_vacum.setCheckable(True)
        self.pushButton_gripper_vacum.clicked.connect(self.fungsi_pushButton_gripper_vacum)
# ----------------------------------------------------------------------------------------------
        self.pushButton_save_servo.setCheckable(False)
        self.pushButton_save_servo.clicked.connect(self.fungsi_pushButton_save_servo)
# ----------------------------------------------------------------------------------------------
        self.pushButton_delete.setCheckable(False)
        self.pushButton_delete.clicked.connect(self.fungsi_pushButton_delete)
# ----------------------------------------------------------------------------------------------
        self.pushButton_up.setCheckable(False)
        self.pushButton_up.clicked.connect(self.fungsi_pushButton_up)
# ----------------------------------------------------------------------------------------------
        self.pushButton_down.setCheckable(False)
        self.pushButton_down.clicked.connect(self.fungsi_pushButton_down)
# ----------------------------------------------------------------------------------------------
        # Di bagian retranslateUi:
        self.pushButton_gripper_01.setCheckable(True)
        self.pushButton_gripper_01.clicked.connect(self.fungsi_pushButton_gripper_01_toggle)
# -----------------------------
        self.pushButton_calibration.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.pushButton_single_run.setEnabled(False)
        self.pushButton_pause.setEnabled(False)
        self.pushButton_stop.setEnabled(False)
        self.frame_bawahutama.setEnabled(False)
        self.tutup_tombol_slide_dan_spinbox()

        self.pushButton_gripper_servo.setEnabled(False)
        self.pushButton_save_sensor.setEnabled(False)
        self.pushButton_next.setEnabled(False)
# ----------------------------------------------------------------------------------------------
        self.pushButton_info.setCheckable(False)
        self.pushButton_info.clicked.connect(self.fungsi_pushButton_info)
# ----------------------------------------------------------------------------------------------
        self.pushButton_edit.setCheckable(False)
        self.pushButton_edit.clicked.connect(self.load_h_file_to_list) # open Program
# ----------------------------------------------------------------------------------------------
        self.pushButton_save_as.setCheckable(False)
        self.pushButton_save_as.clicked.connect(self.fungsi_pushButton_save_as)
# ----------------------------------------------------------------------------------------------
        self.pushButton_save_move.setCheckable(False)
        self.pushButton_save_move.clicked.connect(self.fungsi_pushButton_save_move)
# ----------------------------------------------------------------------------------------------
        self.pushButton_save_servo_seld.setCheckable(False)
        self.pushButton_save_servo_seld.clicked.connect(self.fungsi_pushButton_save_move_servo)
# ----------------------------------------------------------------------------------------------
        self.pushButton_clear.setCheckable(False)
        self.pushButton_clear.clicked.connect(self.fungsi_pushButton_clear)
# ----------------------------------------------------------------------------------------------
        self.pushButton_start.setCheckable(False)
        self.pushButton_start.clicked.connect(self.fungsi_pushButton_start)
# ----------------------------------------------------------------------------------------------
        
        # <<< START KODE BARU: Hubungkan Tombol Single Run >>>
        self.pushButton_single_run.setCheckable(False)
        self.pushButton_single_run.clicked.connect(self.fungsi_pushButton_single_run)
        # <<< AKHIR KODE BARU >>>
        
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
        self.pushButton_pause.setCheckable(False)
        self.pushButton_pause.clicked.connect(self.fungsi_pushButton_pause)
# ----------------------------------------------------------------------------------------------
        self.pushButton_stop.setCheckable(False)
        self.pushButton_stop.clicked.connect(self.fungsi_pushButton_stop)
# ----------------------------------------------------------------------------------------------
        self.pushButton_cek_posisi.setCheckable(False)
        self.pushButton_cek_posisi.clicked.connect(self.fungsi_pushButton_cek_posisi)
# ----------------------------------------------------------------------------------------------
        self.pushButton_connect.setCheckable(True)  # harus ada ini
        self.pushButton_connect.clicked.connect(self.fungsi_pushButton_connect)
# ----------------------------------------------------------------------------------------------
        self.pushButton_calibration.setCheckable(False)
        self.pushButton_calibration.clicked.connect(self.fungsi_pushButton_calibration)
# ----------------------------------------------------------------------------------------------
        self.pushButton_save_manual.setCheckable(False)
        self.pushButton_save_manual.clicked.connect(self.fungsi_pushButton_save_manual)
# ----------------------------------------------------------------------------------------------
        self.lineEdit.returnPressed.connect(self.send_serial_data_input_manual)
# ----------------------------------------------------------------------------------------------
        self.pushButton_motor_ONOFF.setCheckable(True)  # harus ada ini
        self.pushButton_motor_ONOFF.clicked.connect(self.fungsi_pushButton_motor_ONOFF)
# ----------------------------------------------------------------------------------------------
        self.pushButton_fan.setCheckable(True)  # harus ada ini
        self.pushButton_fan.clicked.connect(self.fungsi_pushButton_fan)
# ----------------------------------------------------------------------------------------------
        self.pushButton_LG4.setCheckable(False)
        self.pushButton_LG4.clicked.connect(self.fungsi_pushButton_tunggu)
# ----------------------------------------------------------------------------------------------
        self.pushButton_new.setCheckable(False)
        self.pushButton_new.clicked.connect(self.fungsi_pushButton_new)
        self.pushButton_credit.clicked.connect(self.fungsi_pushButton_credit)
# ----------------------------------------------------------------------------------------------
# --- KODE BARU: MENGHUBUNGKAN TOMBOL CLEAR MONITOR ---
        self.pushButton_clear_monitor.setCheckable(False)
        self.pushButton_clear_monitor.clicked.connect(self.fungsi_pushButton_clear_monitor)
        # ----------------------------------------------------
        self.doubleSpinBox_X.setDecimals(2)
        self.doubleSpinBox_X.setMinimum(-350)
        self.doubleSpinBox_X.setMaximum(350)
        self.doubleSpinBox_X.setProperty("value", 0)
        self.doubleSpinBox_X.valueChanged.connect(lambda value: self.horizontalSlider_X.setValue(int(value)))
        self.horizontalSlider_X.setMinimum(-350)
        self.horizontalSlider_X.setMaximum(350)
        self.horizontalSlider_X.setProperty("value", 0)
        self.horizontalSlider_X.valueChanged.connect(self.doubleSpinBox_X.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_X.setValue(self.horizontalSlider_X.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_X.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_X.editingFinished.connect(self.send_gcode_command)
# ----------------------------------------------------------------------------------------------
        self.doubleSpinBox_Y.setDecimals(2)
        self.doubleSpinBox_Y.setMinimum(0)
        self.doubleSpinBox_Y.setMaximum(500)
        self.doubleSpinBox_Y.setProperty("value", 0)
        self.doubleSpinBox_Y.valueChanged.connect(lambda value: self.horizontalSlider_Y.setValue(int(value)))
        self.horizontalSlider_Y.setMinimum(0)
        self.horizontalSlider_Y.setMaximum(500)
        self.horizontalSlider_Y.setProperty("value", 0)
        self.horizontalSlider_Y.valueChanged.connect(self.doubleSpinBox_Y.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_Y.setValue(self.horizontalSlider_Y.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_Y.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_Y.editingFinished.connect(self.send_gcode_command)
# ----------------------------------------------------------------------------------------------
        self.doubleSpinBox_Z.setDecimals(2)
        self.doubleSpinBox_Z.setMinimum(-200)
        self.doubleSpinBox_Z.setMaximum(200)
        self.doubleSpinBox_Z.setProperty("value", 0)
        self.doubleSpinBox_Z.valueChanged.connect(lambda value: self.horizontalSlider_Z.setValue(int(value)))
        self.horizontalSlider_Z.setMinimum(-200)
        self.horizontalSlider_Z.setMaximum(200)
        self.horizontalSlider_Z.setProperty("value", 0)
        self.horizontalSlider_Z.valueChanged.connect(self.doubleSpinBox_Z.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_Z.setValue(self.horizontalSlider_Z.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_Z.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_Z.editingFinished.connect(self.send_gcode_command)
# ----------------------------------------------------------------------------------------------
        self.doubleSpinBox_E.setDecimals(2)
        self.doubleSpinBox_E.setMinimum(0)
        self.doubleSpinBox_E.setMaximum(355)
        self.doubleSpinBox_E.setProperty("value", 0)
        self.doubleSpinBox_E.valueChanged.connect(lambda value: self.horizontalSlider_E.setValue(int(value)))
        self.horizontalSlider_E.setMinimum(0)
        self.horizontalSlider_E.setMaximum(355)
        self.horizontalSlider_E.setProperty("value", 0)
        self.horizontalSlider_E.valueChanged.connect(self.doubleSpinBox_E.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_E.setValue(self.horizontalSlider_E.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_E.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_E.editingFinished.connect(self.send_gcode_command)
# ----------------------------------------------------------------------------------------------
        self.doubleSpinBox_speed.setDecimals(2)
        self.doubleSpinBox_speed.setMinimum(0)
        self.doubleSpinBox_speed.setMaximum(500)
        self.doubleSpinBox_speed.setProperty("value", 0)
        self.doubleSpinBox_speed.valueChanged.connect(lambda value: self.horizontalSlider_speed.setValue(int(value)))
        self.horizontalSlider_speed.setMinimum(0)
        self.horizontalSlider_speed.setMaximum(500)
        self.horizontalSlider_speed.setProperty("value", 0)
        self.horizontalSlider_speed.valueChanged.connect(self.doubleSpinBox_speed.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_speed.setValue(self.horizontalSlider_speed.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_speed.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_speed.editingFinished.connect(self.send_gcode_command)
# ----------------------------------------------------------------------------------------------
        self.doubleSpinBox_gripper_servo.setDecimals(2)
        self.doubleSpinBox_gripper_servo.setMinimum(0)
        self.doubleSpinBox_gripper_servo.setMaximum(180)
        self.doubleSpinBox_gripper_servo.setProperty("value", 90)
        self.doubleSpinBox_gripper_servo.valueChanged.connect(lambda value: self.horizontalSlider_gripper_servo.setValue(int(value)))
        self.horizontalSlider_gripper_servo.setMinimum(0)
        self.horizontalSlider_gripper_servo.setMaximum(180)
        self.horizontalSlider_gripper_servo.setProperty("value", 90)
        self.horizontalSlider_gripper_servo.valueChanged.connect(self.doubleSpinBox_gripper_servo.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move_servo.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_gripper_servo.setValue(self.horizontalSlider_gripper_servo.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command_servo()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_gripper_servo.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_gripper_servo.editingFinished.connect(self.send_gcode_command_servo)
# ----------------------------------------------------------------------------------------------
        self.doubleSpinBox_gripper_servoB.setDecimals(2)
        self.doubleSpinBox_gripper_servoB.setMinimum(10)
        self.doubleSpinBox_gripper_servoB.setMaximum(50)
        self.doubleSpinBox_gripper_servoB.setProperty("value", 30)
        self.doubleSpinBox_gripper_servoB.valueChanged.connect(lambda value: self.horizontalSlider_gripper_servoB.setValue(int(value)))
        self.horizontalSlider_gripper_servoB.setMinimum(10)
        self.horizontalSlider_gripper_servoB.setMaximum(50)
        self.horizontalSlider_gripper_servoB.setProperty("value", 30)
        self.horizontalSlider_gripper_servoB.valueChanged.connect(self.doubleSpinBox_gripper_servoB.setValue)

        def update_doubleSpinBox_and_send_gcode():
            self.blink_timer_move_servo.start(300)
            # Update nilai doubleSpinBox_Z berdasarkan nilai slider yang terakhir
            self.doubleSpinBox_gripper_servoB.setValue(self.horizontalSlider_gripper_servoB.value())
            # Kirim G-code setelah nilai di-update
            self.send_gcode_command_servo()
        # Menghubungkan sliderReleased dengan update dan pengiriman G-code
        self.horizontalSlider_gripper_servoB.sliderReleased.connect(update_doubleSpinBox_and_send_gcode)
        # Kirim G-code saat editing pada doubleSpinBox_Z selesai (setelah pengguna mengetik dan selesai)
        self.doubleSpinBox_gripper_servoB.editingFinished.connect(self.send_gcode_command_servo)
# ----------------------------------------------------------------------------------------------
    def set_title_bar_color(self, window):
        # Ambil handle window
        hwnd = window.winId().__int__()

        # Set warna title bar sesuai tema sistem
        value = ctypes.c_int(1)  # 1 untuk dark mode, 0 untuk light mode
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_connect(self):
        print("Tombol connect:", self.pushButton_connect.isChecked())
        self.port = self.lineEdit_com.text()

        # >>> BARIS INI DIBUAT LEBIH ROBUST DENGAN .strip() <<<
        self.port = self.lineEdit_com.text().strip() 

        # --- BLOK PEMERIKSAAN PORT BARU (DIGANTI) ---
        if not self.port or self.port.upper() == "COM":
            # --- KODE BARU UNTUK DISISIPKAN DI SINI ---
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning) # Ikon di BODY (segitiga kuning)
            msg.setWindowTitle("Koneksi Gagal")
            msg.setText("Silakan masukkan atau pilih Port USB yang valid.")

            # Mengatur ikon di Title Bar dengan path kustom Anda
            msg.setWindowIcon(QtGui.QIcon("D:\\Me\\Akademik\\Teknik Mekatronika\\Mata Kuliah\\Semester 5\\Pemrograman Sistem Mekatronik\\DOBOT ROBOT\\LOGO\\DOBOT_ROBOT.png")) 

            msg.exec_() # Menampilkan kotak pesan
            # --- AKHIR KODE BARU ---

        if self.pushButton_connect.isChecked():
            try:
                baud_rate_str = self.comboBox_baudrate.currentText()
                selected_baud = int(baud_rate_str) # Konversi ke integer
                self.serial = QSerialPort(self.port)
                self.serial.setBaudRate(selected_baud)
                # Connect the readyRed signal
                self.serial.readyRead.connect(self.read_serial)
                if not self.serial.open(QtCore.QIODevice.ReadWrite):
                    raise Exception("Gagal membuka port serial")
                # Menampilkan pesan sambungan berhasil
                self.update_view(f"Tersambung ke: {self.port}")
                self.pushButton_connect.setText("DISCONNECT")
                self.frame_bawahutama.setEnabled(True)
                self.listWidget_save.clearSelection()

                self.blink_timer.stop()  # Hentikan kedipan
                self.warna_defult_lineEdit_com()

                self.tanda_kalibrasi = False

                # Nonaktifkan DTR untuk mereset Arduino
                self.serial.setDataTerminalReady(False)
                time.sleep(0.1)  # Tunggu sedikit waktu untuk mereset Arduino
                self.serial.setDataTerminalReady(True)   # Aktifkan DTR kembali
                # Tunggu lebih lama untuk memberi kesempatan Arduino mengirimkan data
                time.sleep(0.1)

                # ✅ Jalankan pengecekan "READY CALIBRATION" dengan QTimer
                self.start_ready_calibration_check(timeout=5000)  # Timeout 10 detik

            except Exception as e:
                print(f"Error opening serial port: {e}")
                self.update_view(
                    f"Error opening serial port: {e} Pastikan serial tidak terbuka di aplikasi lain")
                self.pushButton_connect.setChecked(False)  # Reset kondisi tombol jika gagal
                self.serial = None  # Reset objek serial jika gagal

        else:
            self.stop_sending = True

            self.pushButton_save_servo.setEnabled(True)
            self.pushButton_save_LG.setEnabled(True)
            #self.pushButton_save_sensor.setEnabled(True)
            self.pushButton_save_move.setEnabled(True)
            self.pushButton_save_manual.setEnabled(True)
            self.pushButton_LG4.setEnabled(True)
            self.pushButton_edit.setEnabled(True)
            #self.pushButton_next.setEnabled(True)
            self.pushButton_new.setEnabled(True)
            self.pushButton_delete.setEnabled(True)
            self.pushButton_clear.setEnabled(True)
            self.pushButton_up.setEnabled(True)
            self.pushButton_down.setEnabled(True)
            self.pushButton_home.setEnabled(True)
            self.pushButton_save_servo_seld.setEnabled(True)
            
            if self.tanda_kalibrasi and self.tanda_motor:
                gcode_command = 'G0 X0,00 Y156,00 Z44,00 F0,00\r\n'
                self.serial.write(gcode_command.encode())
                self.serial.flush()
                print(gcode_command)
                self.textEdit_vew.append(gcode_command)

                self.ok_received = False
                self.timer_kaliber = QTimer(self)
                self.timer_kaliber.timeout.connect(self.check_ok_received_kalibrasi)
                self.timer_kaliber.start(100)  # Cek setiap 100ms

            else:
                if hasattr(self, 'serial') and self.serial is not None and self.serial.isOpen():
                    # Menampilkan pesan penutupan port
                    self.update_view(f"Port {self.port} DITUTUP.")
                    self.pushButton_connect.setText("CONNECT")
                    self.label_status.setText(":(")
                    self.pushButton_calibration.setEnabled(False)
                    self.frame_bawahutama.setEnabled(False)
                    self.pushButton_start.setEnabled(False)
                    self.pushButton_pause.setEnabled(False)
                    self.pushButton_stop.setEnabled(False)
                    self.tutup_tombol_slide_dan_spinbox()

                    self.blink_timer.start(500)  # Mulai kedipan setiap 500ms
                    self.blink_timer_calibrasi.stop()

                    self.pushButton_motor_ONOFF.setChecked(False)
                    self.pushButton_fan.setChecked(False)
                    self.pushButton_motor_ONOFF.setText("MOTOR OFF")
                    self.pushButton_fan.setText("FAN OFF")

                    self.pushButton_gripper_servo.setChecked(False)
                    self.pushButton_gripper_servo.setText("SERVO OFF")
                    self.pushButton_gripper_vacum.setChecked(False)
                    self.pushButton_gripper_vacum.setText("VACUM OFF")
                    self.pushButton_LG1.setChecked(False)
                    self.pushButton_LG1.setText("LG1 OFF")
                    self.pushButton_LG2.setChecked(False)
                    self.pushButton_LG2.setText("LG2 OFF")
                    self.pushButton_LG3.setChecked(False)
                    self.pushButton_LG3.setText("LG3 OFF")

                # Tunggu sebentar sebelum menutup koneksi
                # Delay 100ms agar perintah diproses
                QtCore.QThread.msleep(200)

                # Menutup koneksi serial secara langsung
                self.serial.close()
                self.serial = None  # Hapus referensi agar tidak ada masalah saat koneksi ulang
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_clear_monitor(self):
        """Mengosongkan (Clear) semua teks di area log serial (textEdit_vew)."""
        self.textEdit_vew.clear()
        print("Serial Monitor Cleared.")
# ----------------------------------------------------------------------------------------------

    def check_ok_received_kalibrasi(self):
        """ Memeriksa apakah balasan OK sudah diterima. """
        if self.ok_received:
            self.timer_kaliber.stop()  # Hentikan timer setelah berhasil
            self.tutup_koneksi_serial()

    def tutup_koneksi_serial(self):
        self.update_view("Kipas Off dalam 30 detik")
        gcode_command = 'M18\r'
        self.serial.write(gcode_command.encode())
        self.serial.flush()  # Pastikan data dikirim sebelum ditutup
        print(gcode_command)
        self.textEdit_vew.append(gcode_command)
        self.pushButton_fan.setChecked(False)
        self.pushButton_fan.setText("FAN OFF")

        self.pushButton_LG1.setChecked(False)
        self.pushButton_LG1.setText("LG1 OFF")
        self.pushButton_LG2.setChecked(False)
        self.pushButton_LG2.setText("LG2 OFF")
        self.pushButton_LG3.setChecked(False)
        self.pushButton_LG3.setText("LG3 OFF")

        self.fungsi_pushButton_LG1()
        self.fungsi_pushButton_LG2()
        self.fungsi_pushButton_LG3()

        if hasattr(self, 'serial') and self.serial is not None and self.serial.isOpen():
            # Menampilkan pesan penutupan port
            self.update_view(f"PORT {self.port} ditutup.")
            self.pushButton_connect.setText("CONNECT")
            self.label_status.setText(":(")
            self.pushButton_calibration.setEnabled(False)
            self.frame_bawahutama.setEnabled(False)
            self.pushButton_start.setEnabled(False)
            self.pushButton_pause.setEnabled(False)
            self.pushButton_stop.setEnabled(False)
            self.tutup_tombol_slide_dan_spinbox()

            self.blink_timer.start(500)  # Mulai kedipan setiap 500ms
            self.blink_timer_calibrasi.stop()

            self.pushButton_motor_ONOFF.setChecked(False)
            self.pushButton_fan.setChecked(False)
            self.pushButton_motor_ONOFF.setText("MOTOR OFF")
            self.pushButton_fan.setText("FAN OFF")

            self.pushButton_gripper_servo.setChecked(False)
            self.pushButton_gripper_servo.setText("SERVO OFF")
            self.pushButton_gripper_vacum.setChecked(False)
            self.pushButton_gripper_vacum.setText("VACUM OFF")
            

        QtCore.QThread.msleep(200)  # Delay 100ms agar perintah diproses

        # Menutup koneksi serial secara langsung
        self.serial.close()
        self.serial = None  # Hapus referensi agar tidak ada masalah saat koneksi ulang
# ----------------------------------------------------------------------------------------------
    def update_view(self, text):
        # Update QTextEdit with new text
        self.textEdit_vew.append(text)
# ----------------------------------------------------------------------------------------------
    def read_serial(self):
        if self.serial.bytesAvailable():
            try:
                # Baca semua data yang tersedia di buffer
                data = self.serial.readAll().data().decode('utf-8', errors='ignore')

                # Tambahkan data ke buffer sementara
                self.serial_buffer += data

                # Cek jika ada newline (akhir dari satu pesan lengkap)
                if "\n" in self.serial_buffer:
                    # Pisahkan data berdasarkan newline
                    lines = self.serial_buffer.split("\n")
                    # Simpan sisa data yang belum lengkap
                    self.serial_buffer = lines[-1]

                    for line in lines[:-1]:  # Proses semua baris yang sudah lengkap
                        line = line.strip()
                        print("Data lengkap dari serial:", line)
                        self.textEdit_vew.append(line)  # Tampilkan di UI

                        # ✅ Cek jika data mengandung "CURRENT POSITION:"
                        if "CURRENT POSITION:" in line:
                            self.parse_current_position(line)  # Panggil fungsi parsing

                        elif "SETUP GRIPPER SERVO" in line:
                            self.parse_current_position_servo(line)

                        # ✅ Cek kondisi "homing complete"
                        elif "HOMING COMPLETE" in line:

                            # Pastikan tanda_kalibrasi dan tanda_motor diatur dengan benar
                            self.tanda_kalibrasi = True
                            self.tanda_motor = True

                            self.pushButton_start.setEnabled(True)
                            self.pushButton_single_run.setEnabled(True)
                            self.pushButton_pause.setEnabled(True)
                            self.pushButton_stop.setEnabled(True)

                            self.pushButton_motor_ONOFF.setChecked(True)
                            self.pushButton_fan.setChecked(True)
                            self.pushButton_motor_ONOFF.setText("MOTOR ON")
                            self.pushButton_fan.setText("FAN ON")

                            self.label_status.setText("DONE")
                            self.buka_tombol_slide_dan_spinbox()
                            self.fungsi_pushButton_cek_posisi()
                            self.homing_timer.stop()
                            self.blink_timer_calibrasi.stop()
                            self.pushButton_calibration.setEnabled(True)
                            self.update_pushButton_calibration()


                        elif "ok" in line.lower():
                            self.ok_received = True

                        elif "stop" in line.lower():
                            self.stop_sending = True

                        elif "S1 ON" in line:
                            self.S1_ON()
                            self.pushButton_S1.setText("S1 ON")

                        elif "S1 OFF" in line:
                            self.S1_OFF()  
                            self.pushButton_S1.setText("S1 OFF")

                        elif "S2 ON" in line:
                            self.S2_ON()
                            self.pushButton_S2.setText("S2 ON")

                        elif "S2 OFF" in line:
                            self.S2_OFF()  
                            self.pushButton_S2.setText("S2 OFF") 

                        elif "S3 ON" in line:
                            self.S3_ON()
                            self.pushButton_S3.setText("S3 ON")

                        elif "S3 OFF" in line:
                            self.S3_OFF()  
                            self.pushButton_S3.setText("S3 OFF")             

                        elif "RAIL OFF" in line:
                            self.status_rail_on_off = False

                        elif "RAIL ON" in line:
                            self.status_rail_on_off = True

                        # ✅ Tambahkan pengecekan untuk "READY CALIBRATION"
                        elif "READY CALIBRATION" in line:
                            self.ready_calibration_detected = True  # Set flag jika ditemukan    
                            self.calibration_timer.stop()  # Hentikan pengecekan
                            self.label_status.setText("ROBOT READY")
                            self.pushButton_calibration.setEnabled(True)  # Aktifkan tombol kalibrasi
                            self.blink_timer_calibrasi.start(500)

            except Exception as e:
                print(f"Error reading serial data: {e}")
# ----------------------------------------------------------------------------------------------
    def deteksi_port_com(self):
        ports = QSerialPortInfo.availablePorts()
        ch340_ports = [port.portName()
                       for port in ports if "CH340" in port.description()]

        # Hanya update jika ada perubahan
        if ch340_ports != self.last_detected_ports:
            self.last_detected_ports = ch340_ports

            if ch340_ports:
                # Gabungkan list jadi string
                detected_ports = ", ".join(ch340_ports)
                self.update_view(f"PORT ROBOT TERDETEKSI DI {detected_ports}")
                self.lineEdit_com.setText(detected_ports)  # Set ke lineEdit
                self.label_status.setText("")
                self.blink_timer.start(500)  # Mulai kedipan setiap 500ms
                self.first_run = False  # Setelah menampilkan pesan, ubah flag agar tidak muncul lagi

            else:
                self.update_view("Robot tidak terdeteksi, silahkan hubungkan robot ke perangkat ini")
                self.lineEdit_com.setText("COM")  # Set default ke "COM"
                self.blink_timer.stop()  # Hentikan kedipan
                self.warna_defult_lineEdit_com()  # Kembali ke warna default

                self.pushButton_connect.setText("CONNECT")
                self.label_status.setText("")
                self.pushButton_calibration.setEnabled(False)
                self.frame_bawahutama.setEnabled(False)
                self.pushButton_start.setEnabled(False)
                self.pushButton_pause.setEnabled(False)
                self.pushButton_stop.setEnabled(False)
                self.tutup_tombol_slide_dan_spinbox()

                self.pushButton_connect.setChecked(False)
                self.pushButton_motor_ONOFF.setChecked(False)
                self.pushButton_fan.setChecked(False)
                self.pushButton_motor_ONOFF.setText("MOTOR OFF")
                self.pushButton_fan.setText("FAN OFF")

                self.pushButton_gripper_servo.setChecked(False)
                self.pushButton_gripper_servo.setText("SERVO OFF")
                self.pushButton_gripper_vacum.setChecked(False)
                self.pushButton_gripper_vacum.setText("VACUM OFF")
                self.pushButton_LG1.setChecked(False)
                self.pushButton_LG1.setText("LG1 OFF")
                self.pushButton_LG2.setChecked(False)
                self.pushButton_LG2.setText("LG2 OFF")
                self.pushButton_LG3.setChecked(False)
                self.pushButton_LG3.setText("LG3 OFF")


                self.pushButton_save_servo.setEnabled(True)
                self.pushButton_save_LG.setEnabled(True)
                #self.pushButton_save_sensor.setEnabled(True)
                self.pushButton_save_move.setEnabled(True)
                self.pushButton_save_manual.setEnabled(True)
                self.pushButton_LG4.setEnabled(True)
                self.pushButton_edit.setEnabled(True)
                #self.pushButton_next.setEnabled(True)
                self.pushButton_new.setEnabled(True)
                self.pushButton_delete.setEnabled(True)
                self.pushButton_clear.setEnabled(True)
                self.pushButton_up.setEnabled(True)
                self.pushButton_down.setEnabled(True)
                self.pushButton_home.setEnabled(True)
                self.pushButton_save_servo_seld.setEnabled(True)

        # Tampilkan pesan sekali saat pertama kali program berjalan dan tidak ada perangkat
        if self.first_run and not ch340_ports:
            self.update_view(
                "Robot tidak terdeteksi, silahkan hubungkan robot ke perangkat ini")
            self.first_run = False  # Setelah menampilkan pesan, ubah flag agar tidak muncul lagi

# ----------------------------------------------------------------------------------------------
    def toggle_border_color(self):
        if self.blink_state:
            self.pushButton_connect.setStyleSheet("QPushButton {\n"
                                                     "    background-color: #155DFC; /* Warna latar belakang tombol */\n"
                                                     "    color: #FFFFFF; /* Warna teks */\n"
                                                     "    border: 2px solid #155DFC; /* Warna border */\n"
                                                     "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                     "    padding: 5px; /* Padding di dalam tombol */\n"
                                                     "    font-size: 18px; /* Ukuran font */\n"
                                                     "    font-weight: bold; /* Ketebalan font */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #366DE6; /* Warna latar belakang saat hover */\n"
                                                     "    border: 2px solid #366DE6; /* Warna border saat hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #155DFC; /* Warna latar belakang saat ditekan */\n"
                                                     "    border: 2px solid #155DFC; /* Warna border saat ditekan */\n"
                                                     "    color: #FFFFFF; /* Warna teks saat ditekan */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked {\n"
                                                     "    background-color: #155DFC; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                     "    border: 2px solid #155DFC; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:disabled {\n"
                                                     "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                     "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                     "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                     "}")
        else:
            self.pushButton_connect.setStyleSheet("QPushButton {\n"
                                                     "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                     "    color: #ECEFF4; /* Warna teks */\n"
                                                     "    border: 2px solid #FFC107; /* Warna border */\n"
                                                     "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                     "    padding: 5px; /* Padding di dalam tombol */\n"
                                                     "    font-size: 18px; /* Ukuran font */\n"
                                                     "    font-weight: bold; /* Ketebalan font */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                     "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                     "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:disabled {\n"
                                                     "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                     "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                     "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                     "}")
        self.blink_state = not self.blink_state  # Toggle state
# ----------------------------------------------------------------------------------------------
    def toggle_border_color_calibrasi(self):
        if self.blink_state_kalibrasi:
            self.pushButton_calibration.setStyleSheet("QPushButton {\n"
                                                      "    background-color: #4F39F6; /* Warna latar belakang tombol */\n"
                                                      "    color: #FFFFFF; /* Warna teks */\n"
                                                      "    border: 2px solid #4F39F6; /* Warna border */\n"
                                                      "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                      "    padding: 5px; /* Padding di dalam tombol */\n"
                                                      "    font-size: 18px; /* Ukuran font */\n"
                                                      "    font-weight: bold; /* Ketebalan font */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:hover {\n"
                                                      "    background-color: #7967FF; /* Warna latar belakang saat hover */\n"
                                                      "    border: 2px solid #7967FF; /* Warna border saat hover */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:pressed {\n"
                                                      "    background-color: #1601B8; /* Warna latar belakang saat ditekan */\n"
                                                      "    border: 2px solid #1601B8; /* Warna border saat ditekan */\n"
                                                      "    color: #7563FF; /* Warna teks saat ditekan */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:checked {\n"
                                                      "    background-color: #5A00D7; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                      "    border: 2px solid #5A00D7; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                      "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:checked:hover {\n"
                                                      "    background-color: #A361FF; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                      "    border: 2px solid #A361FF; /* Warna border saat tombol checked dan hover */\n"
                                                      "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:disabled {\n"
                                                      "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                      "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                      "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                      "}")
        else:
            self.pushButton_calibration.setStyleSheet("QPushButton {\n"
                                                      "    background-color: #622DAD; /* Warna latar belakang tombol */\n"
                                                      "    color: #FFFFFF; /* Warna teks */\n"
                                                      "    border: 2px solid #622DAD; /* Warna border */\n"
                                                      "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                      "    padding: 5px; /* Padding di dalam tombol */\n"
                                                      "    font-size: 18px; /* Ukuran font */\n"
                                                      "    font-weight: bold; /* Ketebalan font */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:hover {\n"
                                                      "    background-color: #7967FF; /* Warna latar belakang saat hover */\n"
                                                      "    border: 2px solid #7967FF; /* Warna border saat hover */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:pressed {\n"
                                                      "    background-color: #4C2187; /* Warna latar belakang saat ditekan */\n"
                                                      "    border: 2px solid #4C2187; /* Warna border saat ditekan */\n"
                                                      "    color: #9763DF; /* Warna teks saat ditekan */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:checked {\n"
                                                      "    background-color: #4F39F6; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                      "    border: 2px solid #4F39F6; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                      "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:checked:hover {\n"
                                                      "    background-color: #7967FF; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                      "    border: 2px solid #7967FF; /* Warna border saat tombol checked dan hover */\n"
                                                      "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:disabled {\n"
                                                      "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                      "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                      "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                      "}")
        self.blink_state_kalibrasi = not self.blink_state_kalibrasi  # Toggle state
# ----------------------------------------------------------------------------------------------
    def warna_defult_lineEdit_com(self):
        self.pushButton_connect.setStyleSheet("QPushButton {\n"
                                                 "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                 "    color: #ECEFF4; /* Warna teks */\n"
                                                 "    border: 2px solid #1B5E20; /* Warna border */\n"
                                                 "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                 "    padding: 5px; /* Padding di dalam tombol */\n"
                                                 "    font-size: 18px; /* Ukuran font */\n"
                                                 "    font-weight: bold; /* Ketebalan font */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover {\n"
                                                 "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                 "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:pressed {\n"
                                                 "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                 "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                 "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:checked {\n"
                                                 "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                 "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                 "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:checked:hover {\n"
                                                 "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                 "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                 "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:disabled {\n"
                                                 "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                 "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                 "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                 "}")
# ----------------------------------------------------------------------------------------------
    def update_button_save_move(self):
        self.pushButton_save_move.setStyleSheet("QPushButton {\n"
                                                "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                "    color: #ECEFF4; /* Warna teks */\n"
                                                "    border: 2px solid #FFC107; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:checked {\n"
                                                "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:checked:hover {\n"
                                                "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
# ----------------------------------------------------------------------------------------------
    def toggle_border_color_move(self):
        if self.blink_state_move:
            self.pushButton_save_move.setStyleSheet("QPushButton {\n"
                                                     "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                     "    color: #ECEFF4; /* Warna teks */\n"
                                                     "    border: 2px solid #1B5E20; /* Warna border */\n"
                                                     "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                     "    padding: 5px; /* Padding di dalam tombol */\n"
                                                     "    font-size: 18px; /* Ukuran font */\n"
                                                     "    font-weight: bold; /* Ketebalan font */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                     "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                     "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:disabled {\n"
                                                     "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                     "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                     "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                     "}")
        else:
            self.pushButton_save_move.setStyleSheet("QPushButton {\n"
                                                     "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                     "    color: #ECEFF4; /* Warna teks */\n"
                                                     "    border: 2px solid #FFC107; /* Warna border */\n"
                                                     "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                     "    padding: 5px; /* Padding di dalam tombol */\n"
                                                     "    font-size: 18px; /* Ukuran font */\n"
                                                     "    font-weight: bold; /* Ketebalan font */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                     "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                     "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:disabled {\n"
                                                     "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                     "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                     "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                     "}")
        self.blink_state_move = not self.blink_state_move  # Toggle state    
# ----------------------------------------------------------------------------------------------
    def toggle_border_color_move_servo(self):
        if self.blink_state_move_servo:
            self.pushButton_save_servo_seld.setStyleSheet("QPushButton {\n"
                                                     "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                     "    color: #ECEFF4; /* Warna teks */\n"
                                                     "    border: 2px solid #1B5E20; /* Warna border */\n"
                                                     "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                     "    padding: 5px; /* Padding di dalam tombol */\n"
                                                     "    font-size: 18px; /* Ukuran font */\n"
                                                     "    font-weight: bold; /* Ketebalan font */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                     "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                     "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:disabled {\n"
                                                     "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                     "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                     "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                     "}")
        else:
            self.pushButton_save_servo_seld.setStyleSheet("QPushButton {\n"
                                                     "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                     "    color: #ECEFF4; /* Warna teks */\n"
                                                     "    border: 2px solid #FFC107; /* Warna border */\n"
                                                     "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                     "    padding: 5px; /* Padding di dalam tombol */\n"
                                                     "    font-size: 18px; /* Ukuran font */\n"
                                                     "    font-weight: bold; /* Ketebalan font */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                     "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked {\n"
                                                     "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                     "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:checked:hover {\n"
                                                     "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                     "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                     "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:disabled {\n"
                                                     "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                     "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                     "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                     "}")
        self.blink_state_move_servo = not self.blink_state_move_servo  # Toggle state    
# ----------------------------------------------------------------------------------------------
    def update_button_save_move_servo(self):
        self.pushButton_save_servo_seld.setStyleSheet("QPushButton {\n"
                                                "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                "    color: #ECEFF4; /* Warna teks */\n"
                                                "    border: 2px solid #FFC107; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:checked {\n"
                                                "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:checked:hover {\n"
                                                "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
# ----------------------------------------------------------------------------------------------
    def update_pushButton_calibration(self):
        self.pushButton_calibration.setStyleSheet("QPushButton {\n"
                                                  "    background-color: #5100C0; /* Warna latar belakang tombol */\n"
                                                  "    color: #FFFFFF; /* Warna teks */\n"
                                                  "    border: 2px solid #5100C0; /* Warna border */\n"
                                                  "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                  "    padding: 5px; /* Padding di dalam tombol */\n"
                                                  "    font-size: 18px; /* Ukuran font */\n"
                                                  "    font-weight: bold; /* Ketebalan font */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                  "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                  "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                  "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked {\n"
                                                  "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                  "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                  "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:checked:hover {\n"
                                                  "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                  "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                  "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:disabled {\n"
                                                  "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                  "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                  "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                  "}")
# ----------------------------------------------------------------------------------------------
    def update_pushButton_pause_merah(self):
        self.pushButton_pause.setStyleSheet("QPushButton {\n"
                                                "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                                "    color: #ECEFF4; /* Warna teks */\n"
                                                "    border: 2px solid #BF616A; /* Warna border */\n"
                                                "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                                "    padding: 5px; /* Padding di dalam tombol */\n"
                                                "    font-size: 18px; /* Ukuran font */\n"
                                                "    font-weight: bold; /* Ketebalan font */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "    background-color: #4C566A; /* Warna latar belakang saat hover */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "    background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
                                                "    color: #2E3440; /* Warna teks saat ditekan */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:checked {\n"
                                                "    background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
                                                "    border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
                                                "    color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:checked:hover {\n"
                                                "    background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
                                                "    border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
                                                "    color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:disabled {\n"
                                                "    background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
                                                "    color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
                                                "    border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
                                                "}")
# ----------------------------------------------------------------------------------------------
    def update_pushButton_pause_defult(self):
        """Mengatur style tombol PAUSE ke kondisi non-aktif standar (termasuk lebar)."""
        self.pushButton_pause.setStyleSheet("QPushButton {\n"
"  background-color: #2E3440; /* Warna latar belakang tombol */\n"
"  color: #ECEFF4; /* Warna teks */\n"
"  border: 2px solid #1B5E20; /* Warna border */\n"
"  border-radius: 6px; /* Sudut tombol yang melengkung */\n"
"  padding: 5px; /* Padding di dalam tombol */\n"
"  font-size: 18px; /* Ukuran font */\n"
"  font-weight: bold; /* Ketebalan font */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: #4C566A; /* Warna latar belakang saat hover */\n"
"  border: 2px solid #81A1C1; /* Warna border saat hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: #81A1C1; /* Warna latar belakang saat ditekan */\n"
"  border: 2px solid #81A1C1; /* Warna border saat ditekan */\n"
"  color: #2E3440; /* Warna teks saat ditekan */\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"  background-color: #81A1C1; /* Warna latar belakang saat tombol dalam keadaan aktif (checked) */\n"
"  border: 2px solid #88C0D0; /* Warna border saat tombol dalam keadaan aktif */\n"
"  color: #2E3440; /* Warna teks saat tombol dalam keadaan aktif */\n"
"}\n"
"\n"
"QPushButton:checked:hover {\n"
"  background-color: #4C566A; /* Warna latar belakang saat tombol checked dan hover */\n"
"  border: 2px solid #81A1C1; /* Warna border saat tombol checked dan hover */\n"
"  color: #2E3440; /* Warna teks saat tombol checked dan hover */\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  background-color: #3B4252; /* Warna latar belakang saat tombol dinonaktifkan */\n"
"  max-width: 90px; \n"       # <<< PASTIKAN BATASAN LEBAR DITAMBAH
"  min-width: 90px; \n"       # <<< PASTIKAN BATASAN LEBAR DITAMBAH
"  color: #7F8C9A; /* Warna teks saat tombol dinonaktifkan */\n"
"  border: 2px solid #3B4252; /* Warna border saat tombol dinonaktifkan */\n"
"}")
# ----------------------------------------------------------------------------------------------
    def send_gcode_command(self):
        # Mendapatkan nilai dari elemen GUI seperti doubleSpinBox_X, doubleSpinBox_Y, dll.
        x_value = self.doubleSpinBox_X.text()
        y_value = self.doubleSpinBox_Y.text()
        z_value = self.doubleSpinBox_Z.text()
        e_value = self.doubleSpinBox_E.text()
        f_value = self.doubleSpinBox_speed.text()
        # Membuat gcode_command
        gcode_command = f'G0 X{x_value} Y{y_value} Z{z_value} E{e_value} F{f_value}\r'

        self.serial.write(gcode_command.encode())
# ----------------------------------------------------------------------------------------------
    def send_gcode_command_servo(self):
        a_value = self.doubleSpinBox_gripper_servo.text()
        b_value = self.doubleSpinBox_gripper_servoB.text()
        # Membuat gcode_command
        gcode_command = f'G100 A{a_value} B{b_value}\r'

        self.serial.write(gcode_command.encode())
# ----------------------------------------------------------------------------------------------
    def send_gcode_command_pilih(self):
        # Mendapatkan nilai dari elemen GUI seperti doubleSpinBox_X, doubleSpinBox_Y, dll.
        x_value = self.doubleSpinBox_X.text()
        y_value = self.doubleSpinBox_Y.text()
        z_value = self.doubleSpinBox_Z.text()
        e_value = self.doubleSpinBox_E.text()
        # Membuat gcode_command
        gcode_command = f'G0 X{x_value} Y{y_value} Z{z_value} E{e_value}\r'

        self.serial.write(gcode_command.encode())
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_info(self):
        url = QUrl("https://drive.google.com/drive/folders/1FGs8Us85VPs0KTkP4ELsLuuvs37jpCe0?usp=sharing")  # Ganti dengan link yang diinginkan
        QDesktopServices.openUrl(url)  # Membuka link di browser default
# ----------------------------------------------------------------------------------------------
# --- SISIPKAN KODE FUNGSI BARU DI SINI ---
    def fungsi_pushButton_credit(self):
        """Menampilkan jendela pop-up dengan informasi kredit."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information) 
        msg.setWindowTitle("Credit")
        
        # Menggunakan string multi-baris dengan \n
        credit_text = (
            "Created by Kelompok 2 - Teknik Mekatronika B - Angkatan 2023\n"
            "Proyek Pemrograman Sistem Mekatronika - Tahun Ajaran 2025\n\n"
            " 1. Galang Shoddiqul Amin     - 4123600032\n"
            " 2. Brian Andi Pratama        - 4123600049\n"
            " 3. Mohammad Khalid Khoirudin - 4123600060"
        )
        msg.setText(credit_text)
        
        # Opsional: Mengatur ikon di Title Bar
        msg.setWindowIcon(QtGui.QIcon("D:\\Me\\Akademik\\Teknik Mekatronika\\Mata Kuliah\\Semester 5\\Pemrograman Sistem Mekatronik\\DOBOT ROBOT\\LOGO\\DOBOT_ROBOT.png")) 

        msg.exec_()
        self.update_view("Menampilkan Credit.")
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_calibration(self):
        self.pushButton_calibration.setEnabled(False)
        gcode_command = 'G28\r\n'
        self.serial.write(gcode_command.encode())
        print(gcode_command)
        self.textEdit_vew.append(gcode_command)
        self.label_status.setText("Robot sedang kalibrasi")

        # Set tanda_kalibrasi menjadi True saat kalibrasi ditekan
        self.tanda_kalibrasi = True
        self.tanda_motor = True

        self.pushButton_start.setEnabled(True)
        self.pushButton_pause.setEnabled(True)
        self.pushButton_stop.setEnabled(True)

        self.pushButton_motor_ONOFF.setChecked(True)
        self.pushButton_fan.setChecked(True)
        self.pushButton_motor_ONOFF.setText("MOTOR ON")
        self.pushButton_fan.setText("FAN ON")

        # Buat timer untuk batas waktu 40 detik
        self.homing_timer = QTimer()
        self.homing_timer.setSingleShot(True)  # Timer hanya berjalan sekali
        self.homing_timer.timeout.connect(self.homing_timeout)  # Panggil fungsi jika timeout
        self.homing_timer.start(30000)  # 30 detik
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_motor_ONOFF(self):
        if self.pushButton_motor_ONOFF.isChecked():
            self.update_view("MOTOR ON")
            self.pushButton_motor_ONOFF.setText("MOTOR ON")
            gcode_command = 'M17\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
            self.pushButton_fan.setChecked(True)
            self.fungsi_pushButton_fan()
            self.tanda_motor = True
        else:
            self.update_view("MOTOR OFF")
            self.pushButton_motor_ONOFF.setText("MOTOR OFF")
            self.update_view("FAN OFF dalam 30 detik")
            gcode_command = 'M18\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
            self.pushButton_fan.setChecked(False)
            self.fungsi_pushButton_fan()
            self.tanda_motor = False
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_fan(self):
        if self.pushButton_fan.isChecked():
            self.update_view("FAN ON")
            self.pushButton_fan.setText("FAN ON")
            gcode_command = 'M106\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
        else:
            self.update_view("Fan OFF dalam 30 detik")
            self.pushButton_fan.setText("FAN OFF")
            gcode_command = 'M107\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)

# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_cek_posisi(self):
        gcode_command = 'M114\r\n'
        self.serial.write(gcode_command.encode())
        print(gcode_command)
        self.textEdit_vew.append(gcode_command)
# ----------------------------------------------------------------------------------------------
    def homing_timeout(self):
        """Dipanggil jika homing tidak selesai dalam 40 detik"""
        self.label_status.setText("DONE (Timeout)")
        self.buka_tombol_slide_dan_spinbox()
        self.fungsi_pushButton_cek_posisi()
# ----------------------------------------------------------------------------------------------
    def parse_current_position(self, line):
        import re  # Untuk ekstraksi angka
        # Ekstrak angka dari format "X:0.00 Y:216.90 Z:138.00 E:0.00"
        match = re.search(r'X:(-?\d+\.\d+)\s+Y:(-?\d+\.\d+)\s+Z:(-?\d+\.\d+)\s+E:(-?\d+\.\d+)', line)
        if match:
            x, y, z, e = map(float, match.groups())  # Konversi ke float
            # ✅ Set nilai spin box
            self.doubleSpinBox_X.setDecimals(2)
            self.doubleSpinBox_Y.setDecimals(2)
            self.doubleSpinBox_Z.setDecimals(2)
            self.doubleSpinBox_E.setDecimals(2)

            self.doubleSpinBox_X.setValue(x)
            self.doubleSpinBox_Y.setValue(y)
            self.doubleSpinBox_Z.setValue(z)
            self.doubleSpinBox_E.setValue(e)
# ----------------------------------------------------------------------------------------------
    def parse_current_position_servo(self, line):
        import re  # Untuk ekstraksi angka
        # Ekstrak angka dari format "X:0.00 Y:216.90 Z:138.00 E:0.00"
        match = re.search(r"MIN (\d+) MAX (\d+)", line)
        if match:
            MIN = int(match.group(1))  # Menyimpan nilai MIN
            MAX = int(match.group(2))  # Menyimpan nilai MAX
            
            # Memperbarui nilai pada doubleSpinBox dan horizontalSlider
            self.doubleSpinBox_gripper_servoB.setMinimum(MIN)
            self.doubleSpinBox_gripper_servoB.setMaximum(MAX)
            self.doubleSpinBox_gripper_servoB.setProperty("value", MAX)  # Update dengan nilai MAX atau nilai default
            
            self.horizontalSlider_gripper_servoB.setMinimum(MIN)
            self.horizontalSlider_gripper_servoB.setMaximum(MAX)
            self.horizontalSlider_gripper_servoB.setProperty("value", MAX)  # Update dengan nilai MAX atau nilai default
# ----------------------------------------------------------------------------------------------    
    def buka_tombol_slide_dan_spinbox(self):
        self.horizontalSlider_X.setEnabled(True)
        self.horizontalSlider_Y.setEnabled(True)
        self.horizontalSlider_Z.setEnabled(True)
        self.horizontalSlider_speed.setEnabled(True)
        self.horizontalSlider_gripper_servo.setEnabled(True)
        self.horizontalSlider_gripper_servoB.setEnabled(True)

        self.doubleSpinBox_X.setEnabled(True)
        self.doubleSpinBox_Y.setEnabled(True)
        self.doubleSpinBox_Z.setEnabled(True)
        self.doubleSpinBox_speed.setEnabled(True)
        self.doubleSpinBox_gripper_servo.setEnabled(True)
        self.doubleSpinBox_gripper_servoB.setEnabled(True)
        
        if self.status_rail_on_off:
            self.horizontalSlider_E.setEnabled(True)
            self.doubleSpinBox_E.setEnabled(True)
        else:
            self.horizontalSlider_E.setEnabled(False)
            self.doubleSpinBox_E.setEnabled(False)    
# ----------------------------------------------------------------------------------------------

    def tutup_tombol_slide_dan_spinbox(self):
        self.horizontalSlider_X.setEnabled(False)
        self.horizontalSlider_Y.setEnabled(False)
        self.horizontalSlider_Z.setEnabled(False)
        self.horizontalSlider_E.setEnabled(False)
        self.horizontalSlider_speed.setEnabled(False)
        self.horizontalSlider_gripper_servo.setEnabled(False)
        self.horizontalSlider_gripper_servoB.setEnabled(False)

        self.doubleSpinBox_X.setEnabled(False)
        self.doubleSpinBox_Y.setEnabled(False)
        self.doubleSpinBox_Z.setEnabled(False)
        self.doubleSpinBox_E.setEnabled(False)
        self.doubleSpinBox_speed.setEnabled(False)
        self.doubleSpinBox_gripper_servo.setEnabled(False)
        self.doubleSpinBox_gripper_servoB.setEnabled(False)

        self.doubleSpinBox_gripper_servo.setProperty("value", 90)

        self.listWidget_save.blockSignals(False)
# ----------------------------------------------------------------------------------------------

    def check_ready_calibration(self):
        """
        Fungsi yang dijalankan oleh QTimer untuk mengecek apakah "READY CALIBRATION" sudah muncul.
        Jika belum muncul dalam batas waktu tertentu, tampilkan pesan ke pengguna.
        """
        elapsed_time = self.calibration_start_time.msecsTo(
            QtCore.QTime.currentTime())

        if self.ready_calibration_detected:
            self.calibration_timer.stop()  # Hentikan pengecekan jika sudah ditemukan
            print("READY CALIBRATION ditemukan, lanjutkan proses.")
            return

        if elapsed_time > self.calibration_timeout:
            self.calibration_timer.stop()
            print("Timeout: READY CALIBRATION tidak ditemukan!")
            self.update_view(
                "Silahkan cabut USB ke robot lalu matikan robot, nyalakan ulang robot dan pasang kembali USB.")

            if hasattr(self, 'serial') and self.serial is not None and self.serial.isOpen():
                self.pushButton_connect.setText("CONNECT")
                self.label_status.setText(":(")
                self.pushButton_calibration.setEnabled(False)
                self.frame_bawahutama.setEnabled(False)
                self.pushButton_start.setEnabled(False)
                self.pushButton_pause.setEnabled(False)
                self.pushButton_stop.setEnabled(False)
                self.tutup_tombol_slide_dan_spinbox()

                self.blink_timer.start(500)  # Mulai kedipan setiap 500ms

                self.pushButton_motor_ONOFF.setChecked(False)
                self.pushButton_fan.setChecked(False)

                self.pushButton_motor_ONOFF.setText("MOTOR OFF")
                self.pushButton_fan.setText("FAN OFF")

                self.pushButton_gripper_servo.setChecked(False)
                self.pushButton_gripper_servo.setText("SERVO OFF")
                self.pushButton_gripper_vacum.setChecked(False)
                self.pushButton_gripper_vacum.setText("VACUM OFF")
                self.pushButton_LG1.setChecked(False)
                self.pushButton_LG1.setText("LG1 OFF")
                self.pushButton_LG2.setChecked(False)
                self.pushButton_LG2.setText("LG2 OFF")
                self.pushButton_LG3.setChecked(False)
                self.pushButton_LG3.setText("LG3 OFF")                

                self.serial.close()
                self.serial = None  # Reset objek serial

                self.pushButton_connect.setChecked(False)
# ----------------------------------------------------------------------------------------------

    def start_ready_calibration_check(self, timeout=5000):
        """
        Memeriksa apakah pesan "READY CALIBRATION" diterima dalam `timeout` milidetik.
        Jika tidak terdeteksi dalam waktu tersebut, tampilkan pesan kepada pengguna.
        """
        self.ready_calibration_detected = False  # Reset status
        self.calibration_timer = QtCore.QTimer(self)
        self.calibration_timer.setInterval(100)  # Periksa setiap 500 ms
        self.calibration_timer.timeout.connect(self.check_ready_calibration)

        self.calibration_start_time = QtCore.QTime.currentTime()
        self.calibration_timeout = timeout
        self.calibration_timer.start()  # Mulai pengecekan asinkron
# ----------------------------------------------------------------------------------------------

    def fungsi_pushButton_save_move(self):
        self.update_button_save_move()
        self.blink_timer_move.stop()
        # Ambil nilai doubleSpinBox X Y Z E F
        x_value = self.doubleSpinBox_X.text()
        y_value = self.doubleSpinBox_Y.text()
        z_value = self.doubleSpinBox_Z.text()
        e_value = self.doubleSpinBox_E.text()
        f_value = self.doubleSpinBox_speed.text()

        # ✅ Cek apakah doubleSpinBox_E sedang disabled
        if not self.doubleSpinBox_E.isEnabled():
            gcode_command = f'G0 X{x_value} Y{y_value} Z{z_value} F{f_value}'
        else:
            gcode_command = f'G0 X{x_value} Y{y_value} Z{z_value} E{e_value} F{f_value}'

        # Cek apakah ada item yang dipilih di listWidget_save
        selected_items = self.listWidget_save.selectedItems()
        if selected_items:
            # Ganti teks item yang dipilih dengan G-code yang baru
            selected_items[0].setText(gcode_command)
        else:
            # Jika tidak ada item yang dipilih, tambahkan item baru
            self.listWidget_save.addItem(gcode_command)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_save_move_servo(self):
        self.update_button_save_move_servo()
        self.blink_timer_move_servo.stop()
        # Ambil nilai doubleSpinBox X Y Z E F
        a_value = self.doubleSpinBox_gripper_servo.text()
        b_value = self.doubleSpinBox_gripper_servoB.text()

        gcode_command = f'G100 A{a_value} B{b_value}'

        # Cek apakah ada item yang dipilih di listWidget_save
        selected_items = self.listWidget_save.selectedItems()
        if selected_items:
            # Ganti teks item yang dipilih dengan G-code yang baru
            selected_items[0].setText(gcode_command)
        else:
            # Jika tidak ada item yang dipilih, tambahkan item baru
            self.listWidget_save.addItem(gcode_command)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_clear(self):
        # Membuat popup konfirmasi
        self.listWidget_save.blockSignals(False)
        reply = QMessageBox.question(self, 'Konfirmasi', 'Apakah Anda yakin ingin menghapus semua item?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("Item dihapus")
            self.textEdit_vew.append("Item dihapus")
            self.listWidget_save.clear()
        else:
            print("Penghapusan dibatalkan")
            self.textEdit_vew.append("Penghapusan dibatalkan")
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_start(self):
        self.listWidget_save.blockSignals(False)
        """Memulai atau melanjutkan pengiriman G-code dalam mode LOOPING (Ulang Otomatis)."""

        self.is_looping_mode = True # Mode Looping diaktifkan
        
        if hasattr(self, 'paused') and self.paused:
            # Logika Resume (Looping)
            self.paused = False
            self.stop_sending = False
            print(f"Melanjutkan pengiriman dari baris {self.current_line_index + 1}.")
            self.send_next_line()
            return

        # --- Aksi saat START baru ditekan ---
        # Disable KONTROL UTAMA
        self.pushButton_save_servo.setEnabled(False)
        self.pushButton_save_LG.setEnabled(False)
        self.pushButton_save_move.setEnabled(False)
        self.pushButton_save_manual.setEnabled(False)
        self.pushButton_LG4.setEnabled(False)
        self.pushButton_edit.setEnabled(False)
        self.pushButton_new.setEnabled(False)
        self.pushButton_delete.setEnabled(False)
        self.pushButton_clear.setEnabled(False)
        self.pushButton_up.setEnabled(False)
        self.pushButton_down.setEnabled(False)
        self.pushButton_home.setEnabled(False)
        self.pushButton_save_servo_seld.setEnabled(False)
        self.pushButton_calibration.setEnabled(False)

        # Nonaktifkan tombol run dan tombol single run
        self.pushButton_start.setEnabled(False)
        self.pushButton_single_run.setEnabled(False) # KUNCI SINGLE RUN
        self.pushButton_pause.setEnabled(True)
        self.pushButton_stop.setEnabled(True)
        
        # Nonaktifkan interaksi list
        self.listWidget_save.itemDoubleClicked.disconnect()
        self.listWidget_save.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidget_save.clearSelection()
        
        self.stop_sending = False
        self.paused = False

        self.baris = [self.listWidget_save.item(i).text() for i in range(self.listWidget_save.count())]

        if not self.baris:
            print("Program tidak ada.")
            self.pushButton_start.setEnabled(True)
            self.pushButton_single_run.setEnabled(True) 
            return

        self.current_line_index = 0
        self.ok_received = False
        self.send_next_line()
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_single_run(self):
        self.listWidget_save.blockSignals(False)
        """Memulai pengiriman G-code dalam mode SINGLE RUN (1x Putaran)."""
        
        self.is_looping_mode = False # Mode Single Run diaktifkan

        # Logika single run mengabaikan mode pause, selalu mulai dari awal
        
        # Disable KONTROL UTAMA
        self.pushButton_save_servo.setEnabled(False)
        self.pushButton_save_LG.setEnabled(False)
        self.pushButton_save_move.setEnabled(False)
        self.pushButton_save_manual.setEnabled(False)
        self.pushButton_LG4.setEnabled(False)
        self.pushButton_edit.setEnabled(False)
        self.pushButton_new.setEnabled(False)
        self.pushButton_delete.setEnabled(False)
        self.pushButton_clear.setEnabled(False)
        self.pushButton_up.setEnabled(False)
        self.pushButton_down.setEnabled(False)
        self.pushButton_home.setEnabled(False)
        self.pushButton_save_servo_seld.setEnabled(False)
        self.pushButton_calibration.setEnabled(False)
        
        # Nonaktifkan tombol run dan tombol single run
        self.pushButton_start.setEnabled(False)        # START (Loop) Nonaktif
        self.pushButton_single_run.setEnabled(False)    # SINGLE RUN Nonaktif DIRI SENDIRI SEMENTARA
        self.pushButton_pause.setEnabled(False)         # PAUSE TIDAK RELEVAN DI SINGLE RUN
        self.pushButton_stop.setEnabled(True)
        
        # Nonaktifkan interaksi list
        self.listWidget_save.itemDoubleClicked.disconnect()
        self.listWidget_save.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidget_save.clearSelection()

        self.stop_sending = False
        self.paused = False 

        self.baris = [self.listWidget_save.item(i).text() for i in range(self.listWidget_save.count())]

        if not self.baris:
            print("Program kosong, tidak bisa dimulai.")
            self.pushButton_start.setEnabled(True)
            self.pushButton_single_run.setEnabled(True) 
            return

        self.current_line_index = 0
        self.ok_received = False 
        self.send_next_line()
# ----------------------------------------------------------------------------------------------
    def send_next_line(self):
        """ Mengirim satu baris dari listWidget_save dan menunggu balasan 'ok'. """
        if self.stop_sending:
            print("Pengiriman dihentikan oleh pengguna.")
            return

        # Pastikan masih ada baris yang harus dikirim
        if self.current_line_index < len(self.baris):
            baris_terpilih = self.baris[self.current_line_index].strip()
            #/////////////////////////////////////////////////////////////////////////////////
            if baris_terpilih:
                # Ekstrak nilai X, Y, Z, E, F, A, dan B dari G-code yang dikirim    
                match = re.search(r'X(-?\d+\.?\d*)|Y(-?\d+\.?\d*)|Z(-?\d+\.?\d*)|E(-?\d+\.?\d*)|F(-?\d+\.?\d*)|A(-?\d+\.?\d*)|B(-?\d+\.?\d*)', baris_terpilih)
                if match:
                    # Ekstrak nilai untuk X, Y, Z, E, F
                    x = self.extract_gcode_value(baris_terpilih, 'X', self.doubleSpinBox_X.value())
                    y = self.extract_gcode_value(baris_terpilih, 'Y', self.doubleSpinBox_Y.value())
                    z = self.extract_gcode_value(baris_terpilih, 'Z', self.doubleSpinBox_Z.value())
                    e = self.extract_gcode_value(baris_terpilih, 'E', self.doubleSpinBox_E.value())
                    f = self.extract_gcode_value(baris_terpilih, 'F', self.doubleSpinBox_speed.value())

                    # Ekstrak nilai untuk A dan B
                    a = self.extract_gcode_value(baris_terpilih, 'A', self.doubleSpinBox_gripper_servo.value())
                    b = self.extract_gcode_value(baris_terpilih, 'B', self.doubleSpinBox_gripper_servoB.value())

                    # Update nilai spin box
                    self.doubleSpinBox_X.setValue(x)
                    self.doubleSpinBox_Y.setValue(y)
                    self.doubleSpinBox_Z.setValue(z)
                    self.doubleSpinBox_E.setValue(e)
                    self.doubleSpinBox_speed.setValue(f)

                    self.doubleSpinBox_gripper_servo.setValue(a)
                    self.doubleSpinBox_gripper_servoB.setValue(b)

                # Cek apakah perintah M3 atau M5 ada dalam baris
                if "SERVO ON" in baris_terpilih:
                    self.pushButton_gripper_servo.setChecked(True)
                    self.pushButton_gripper_servo.setText("SERVO ON")
                    self.fungsi_pushButton_gripper_servo()

                if "SERVO OFF" in baris_terpilih:
                    self.pushButton_gripper_servo.setChecked(False)
                    self.pushButton_gripper_servo.setText("SERVO OFF")
                    self.fungsi_pushButton_gripper_servo()

                if "VACUM ON" in baris_terpilih:
                    self.pushButton_gripper_vacum.setChecked(True)
                    self.pushButton_gripper_vacum.setText("VACUM ON")
                    
                    self.pushButton_LG3.setChecked(True)
                    self.pushButton_LG3.setText("LG3 ON")

                    self.pushButton_LG2.setChecked(False)
                    self.pushButton_LG2.setText("LG2 OFF")

                if "VACUM OFF" in baris_terpilih:
                    self.pushButton_gripper_vacum.setChecked(False)
                    self.pushButton_gripper_vacum.setText("VACUM OFF")

                    self.pushButton_LG3.setChecked(False)
                    self.pushButton_LG3.setText("LG3 OFF")

                if "LG1 ON" in baris_terpilih:
                    self.pushButton_LG1.setChecked(True)
                    self.pushButton_LG1.setText("LG1 ON")
                    
                if "LG1 OFF" in baris_terpilih:
                    self.pushButton_LG1.setChecked(False)
                    self.pushButton_LG1.setText("LG1 OFF") 

                if "LG2 ON" in baris_terpilih:
                    self.pushButton_LG2.setChecked(True)
                    self.pushButton_LG2.setText("LG2 ON") 

                if "LG2 OFF" in baris_terpilih:
                    self.pushButton_LG2.setChecked(False)
                    self.pushButton_LG2.setText("LG2 OFF")

                if "LG3 ON" in baris_terpilih:
                    self.pushButton_LG3.setChecked(True)
                    self.pushButton_LG3.setText("LG3 ON") 

                if "LG3 OFF" in baris_terpilih:
                    self.pushButton_LG3.setChecked(False)
                    self.pushButton_LG3.setText("LG3 OFF")

            #/////////////////////////////////////////////////////////////////////////////////
                # Fungsi untuk mengirim perintah ke serial
                gcode_line = f"{baris_terpilih}\r\n"
                print(f"Mengirim: {gcode_line.strip()} (Baris {self.current_line_index + 1})")
                self.serial.write(gcode_line.encode())
                self.serial.flush()

                self.highlight_current_line()

                # Reset flag OK sebelum menunggu respons
                self.ok_received = False

                # Set up timer untuk memeriksa balasan OK
                self.timer_ok_received = QTimer(self)
                self.timer_ok_received.timeout.connect(self.check_ok_received)
                self.timer_ok_received.start(100)  # Cek setiap 100ms

            else:
                self.current_line_index += 1
                self.send_next_line()  # Lewati baris kosong
        else:
            print("Semua baris telah dikirim.")
      
            # <<< START LOGIKA PERULANGAN BARU >>>
            if self.is_looping_mode:
                # Mode Looping (Tombol START)
                self.textEdit_vew.append("Program Loop: Mengulang dari awal...")
                self.current_line_index = 0 # Reset index
                self.send_next_line() # Kirim ulang dari baris pertama
            else:
                # Mode Single Run (Tombol SINGLE RUN)
                self.textEdit_vew.append("--- Eksekusi Single Run Selesai ---")
                
                # Menggunakan fungsi STOP untuk mereset semua UI dan mengaktifkan kembali tombol
                self.fungsi_pushButton_stop() 
                
                # Tambahan penting untuk memastikan tombol RUN kembali aktif:
                # self.pushButton_start.setEnabled(True)
                # self.pushButton_single_run.setEnabled(True)
            # <<< AKHIR LOGIKA PERULANGAN BARU >>>
# ----------------------------------------------------------------------------------------------
    def check_ok_received(self):
        """ Memeriksa apakah balasan OK sudah diterima. """
        if self.ok_received:
            self.current_line_index += 1  # Pindah ke baris berikutnya
            self.timer_ok_received.stop()  # Hentikan timer setelah berhasil
            self.send_next_line()  # Kirim baris berikutnya
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_stop(self):
        self.blink_timer_move.stop()
        self.blink_timer_move_servo.stop()
        """Menghentikan pengiriman sepenuhnya dan mereset semua status ke keadaan awal (standby)."""
        
        # Reset visual pause
        self.pushButton_pause.setText("PAUSE")
        self.update_pushButton_pause_defult()

        # Aktifkan kembali SEMUA KONTROL UTAMA
        self.pushButton_save_servo.setEnabled(True)
        self.pushButton_save_LG.setEnabled(True)
        self.pushButton_save_move.setEnabled(True)
        self.pushButton_save_manual.setEnabled(True)
        self.pushButton_LG4.setEnabled(True)
        self.pushButton_edit.setEnabled(True)
        self.pushButton_new.setEnabled(True)
        self.pushButton_delete.setEnabled(True)
        self.pushButton_clear.setEnabled(True)
        self.pushButton_up.setEnabled(True)
        self.pushButton_down.setEnabled(True)
        self.pushButton_home.setEnabled(True)
        self.pushButton_save_servo_seld.setEnabled(True)
        self.pushButton_calibration.setEnabled(True)
        
        # AKTIFKAN KEMBALI KEDUA tombol RUN hanya jika robot sudah dikalibrasi (self.tanda_kalibrasi)
        if self.tanda_kalibrasi:
            self.pushButton_start.setEnabled(True)
            self.pushButton_single_run.setEnabled(True) # Diaktifkan jika robot sudah siap
        else:
            # Jika belum dikalibrasi, tombol RUN tetap mati, hanya tombol kalibrasi yang nyala
            self.pushButton_start.setEnabled(False)
            self.pushButton_single_run.setEnabled(False)

        self.pushButton_pause.setEnabled(False)
        self.pushButton_stop.setEnabled(False)
        
        # Reset flag eksekusi
        self.stop_sending = True
        self.paused = False
        self.is_looping_mode = False

        # Kembalikan fungsi double click dan mode seleksi
        try:
            self.listWidget_save.itemDoubleClicked.connect(self.edit_item2)
        except TypeError:
            pass 
        
        self.listWidget_save.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_save.clearSelection()
        
        # Reset variabel list dan highlight
        self.baris = []
        self.current_line_index = 0
        for i in range(self.listWidget_save.count()):
            item = self.listWidget_save.item(i)
            item.setForeground(QColor("#FFFFFF"))
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_pause(self):
        """Menghentikan atau melanjutkan pengiriman G-code"""
        self.blink_timer_move.stop()
        self.blink_timer_move_servo.stop()
        if hasattr(self, 'paused') and self.paused:  
            # Jika sedang pause, lanjutkan pengiriman
            self.pushButton_pause.setText("PAUSE")
            self.update_pushButton_pause_defult()
            self.paused = False
            self.stop_sending = False
            print(f"Melanjutkan pengiriman dari baris {self.current_line_index + 1}.")
            self.send_next_line()
            self.listWidget_save.clearSelection() 
            # Tambahkan ini untuk mematikan double click
            self.listWidget_save.itemDoubleClicked.disconnect()

            # Tambahkan ini untuk nonaktifkan seleksi
            self.listWidget_save.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.listWidget_save.clearSelection()
            
        else:
            # Jika tidak pause, hentikan pengiriman sementara
            self.pushButton_pause.setText("RESUME")
            self.update_pushButton_pause_merah()
            self.paused = True
            self.stop_sending = True
            print(f"Pengiriman dijeda di baris {self.current_line_index + 1}.")
            if hasattr(self, 'timer_ok_received'):
                self.timer_ok_received.stop()  # Hentikan timer agar tidak melanjutkan

            # Kembalikan fungsi double click saat pause
            self.listWidget_save.itemDoubleClicked.connect(self.edit_item2)

            # Kembalikan mode seleksi saat pause
            self.listWidget_save.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)   

            self.listWidget_save.clearSelection() 

    def extract_gcode_value(self, gcode_line, key, default_value):
        """
        Mengekstrak nilai X, Y, Z, atau F dari perintah G-code.
        Jika tidak ditemukan, gunakan nilai default sebelumnya.
        """
        match = re.search(rf'{key}(-?\d+\.?\d*)', gcode_line)
        return float(match.group(1)) if match else default_value   
    
# ----------------------------------------------------------------------------------------------
    def highlight_current_line(self):
        # Reset semua warna ke default
        for i in range(self.listWidget_save.count()):
            item = self.listWidget_save.item(i)
            item.setForeground(QColor("#FFFFFF"))

        # Tandai item yang sedang dikirim dengan warna kuning
        current_item = self.listWidget_save.item(self.current_line_index)
        current_item.setForeground(QColor("#FFD700"))  # Warna teks hitam
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_save_as(self):
        # Menampilkan jendela dialog untuk memilih lokasi dan nama file
        file_name, _ = QFileDialog.getSaveFileName(self, "Simpan File G-code", "", "G-code Files (*.gcode);;All Files (*)")
        
        # Jika pengguna tidak memilih file (membatalkan), keluar dari fungsi
        if not file_name:
            print("Penyimpanan dibatalkan.")
            self.textEdit_vew.append("Penyimpanan dibatalkan.")
            return

        # Jika pengguna memilih nama file, simpan file tersebut
        self.write_to_file(file_name)
    
    def write_to_file(self, file_name):
        # Periksa apakah listWidget_save kosong (untuk keperluan contoh)
        if self.listWidget_save.count() == 0:
            print("Program kosong, tidak ada yang disimpan.")
            self.textEdit_vew.append("Program kosong, tidak ada yang disimpan.")
            return  # Keluar dari fungsi jika kosong

        # Membuka file dengan mode tulis
        with open(file_name, "w") as file:
            # Menulis header dari file
            file.write("// File ini dihasilkan secara otomatis\n")
            file.write("// DOBOTROBOT_V1\n")


            # Loop melalui item di listWidget_save dan tulis ke file
            for i in range(self.listWidget_save.count()):
                item_text = self.listWidget_save.item(i).text()
                if i == self.listWidget_save.count() - 1:  # Jika ini adalah elemen terakhir
                    file.write(f'    "{item_text}"\n')  # Tidak ada koma
                else:
                    file.write(f'    "{item_text}",\n')  # Tambahkan koma
        
        print(f"Item telah disimpan ke file {file_name}")
        self.textEdit_vew.append(f"Item telah disimpan ke file {file_name}")
# ----------------------------------------------------------------------------------------------
    def load_h_file_to_list(self):
        # Membuka dialog untuk memilih file
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Pilih File G-code", 
            "", 
            "G-code Files (*.gcode *.nc);;Header Files (*.h);;All Files (*)"
        )
        
        if not file_name:
            print("Tidak ada file yang dipilih.")
            return  # Keluar jika tidak ada file yang dipilih
        
        self.listWidget_save.clear()  # Bersihkan list sebelum memuat data baru

        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

            for line in lines:
                line = line.strip()  # Hapus spasi di awal/akhir
                
                # Abaikan baris kosong dan komentar
                if not line or line.startswith("//"):
                    continue  
                
                # Hapus tanda kutip dan koma dari setiap baris
                cleaned_line = line.strip('" ,')

                if cleaned_line:  # Pastikan hanya menambahkan baris yang valid
                    self.listWidget_save.addItem(cleaned_line)

            print(f"Item telah dimuat dari file {file_name}")
            self.textEdit_vew.append(f"Item telah dimuat dari file {file_name}")

        except FileNotFoundError:
            print(f"File {file_name} tidak ditemukan.")
            self.textEdit_vew.append(f"File {file_name} tidak ditemukan.")

# ----------------------------------------------------------------------------------------------
    def eventFilter(self, source, event):
        # Periksa apakah listWidget_save masih ada
        if not sip.isdeleted(self.listWidget_save):
            # Periksa event hanya jika objek masih valid
            if (
                source == self.listWidget_save.viewport()
                and event.type() == event.MouseButtonPress
            ):
                item = self.listWidget_save.itemAt(event.pos())
                if item is None:
                    self.listWidget_save.clearSelection()
        return super().eventFilter(source, event)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_gripper_servo(self):
        if self.pushButton_gripper_servo.isChecked():
            self.update_view("SERVO ON")
            self.pushButton_gripper_servo.setText("SERVO ON")
            gcode_command = 'M5\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
        else:
            self.update_view("SERVO OFF")
            self.pushButton_gripper_servo.setText("SERVO OFF")
            gcode_command = 'M3\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_gripper_vacum(self):
        if self.pushButton_gripper_vacum.isChecked():
            self.update_view("VACUM ON")
            self.pushButton_gripper_vacum.setText("VACUM ON")
            gcode_command = 'M209\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)

            self.pushButton_LG3.setChecked(True)
            self.pushButton_LG3.setText("LG3 ON")

            self.pushButton_LG2.setChecked(False)
            self.pushButton_LG2.setText("LG2 OFF")

        else:
            self.update_view("VACUM OFF")
            self.pushButton_gripper_vacum.setText("VACUM OFF")
            gcode_command = 'M230\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)

            self.pushButton_LG3.setChecked(False)
            self.pushButton_LG3.setText("LG3 OFF")

# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_LG1(self):
        if self.pushButton_LG1.isChecked():
            self.pushButton_LG1.setText("LG1 ON")
            gcode_command = 'LG1 ON\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
        else:
            self.pushButton_LG1.setText("LG1 OFF")
            gcode_command = 'LG1 OFF\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_LG2(self):
        if self.pushButton_LG2.isChecked():
            self.pushButton_LG2.setText("LG2 ON")
            gcode_command = 'LG2 ON\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
        else:
            self.pushButton_LG2.setText("LG2 OFF")
            gcode_command = 'LG2 OFF\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_LG3(self):
        if self.pushButton_LG3.isChecked():
            self.pushButton_LG3.setText("LG3 ON")
            gcode_command = 'LG3 ON\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
        else:
            self.pushButton_LG3.setText("LG3 OFF")
            gcode_command = 'LG3 OFF\r\n'
            self.serial.write(gcode_command.encode())
            print(gcode_command)
            self.textEdit_vew.append(gcode_command)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_save_LG(self):
        # Tampilkan dialog pilihan gripper
        dialog = GripperChoiceDialog_LG(self)
        if dialog.exec_() == QDialog.Accepted:
            pilihan = dialog.selected
        else:
            return  # Jika batal, keluar dari fungsi

        # Tentukan command berdasarkan pilihan dan status tombol
        command_list = []  # List untuk menyimpan lebih dari satu command

        if pilihan == "LG1":
            if self.pushButton_LG1.isChecked():
                command_list = ["LG1 ON"]
            else:
                command_list = ["LG1 OFF"]
        elif pilihan == "LG2":
            if self.pushButton_LG2.isChecked():
                command_list = ["LG2 ON"]  # Simpan dua command
            else:
                command_list = ["LG2 OFF"]  # Simpan dua command dalam urutan berbeda
        elif pilihan == "LG3":
            if self.pushButton_LG3.isChecked():
                command_list = ["LG3 ON"]  # Simpan dua command
            else:
                command_list = ["LG3 OFF"]  # Simpan dua command dalam urutan berbeda        

        # Cek apakah ada item yang dipilih di listWidget_save
        selected_items = self.listWidget_save.selectedItems()

        if selected_items:
            # Jika ada item yang dipilih, timpa item tersebut dengan yang baru
            for i, cmd in enumerate(command_list):
                if i < len(selected_items):
                    selected_items[i].setText(cmd)
                else:
                    # Jika command_list lebih panjang dari selected_items, tambahkan item baru
                    self.listWidget_save.addItem(cmd)
        else:
            # Jika tidak ada item yang dipilih, tambahkan semua item dari command_list sebagai item baru
            for cmd in command_list:
                self.listWidget_save.addItem(cmd)

        # Tampilkan pesan notifikasi
        self.update_view(f"Command {', '.join(command_list)} disimpan.")
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_save_servo(self):
        # Tampilkan dialog pilihan gripper
        dialog = GripperChoiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            pilihan = dialog.selected
        else:
            return  # Jika batal, keluar dari fungsi

        # Tentukan command berdasarkan pilihan dan status tombol
        command_list = []  # List untuk menyimpan lebih dari satu command

        if pilihan == "Servo":
            if self.pushButton_gripper_servo.isChecked():
                command_list = ["SERVO ON"]
            else:
                command_list = ["SERVO OFF"]
        elif pilihan == "VACUM":
            if self.pushButton_gripper_vacum.isChecked():
                command_list = ["VACUM ON"]  # Simpan dua command
            else:
                command_list = ["VACUM OFF"]  # Simpan dua command dalam urutan berbeda

        # Cek apakah ada item yang dipilih di listWidget_save
        selected_items = self.listWidget_save.selectedItems()

        if selected_items:
            # Jika ada item yang dipilih, timpa item tersebut dengan yang baru
            for i, cmd in enumerate(command_list):
                if i < len(selected_items):
                    selected_items[i].setText(cmd)
                else:
                    # Jika command_list lebih panjang dari selected_items, tambahkan item baru
                    self.listWidget_save.addItem(cmd)
        else:
            # Jika tidak ada item yang dipilih, tambahkan semua item dari command_list sebagai item baru
            for cmd in command_list:
                self.listWidget_save.addItem(cmd)

        # Tampilkan pesan notifikasi
        self.update_view(f"Command {', '.join(command_list)} disimpan.")
# ----------------------------------------------------------------------------------------------
    def edit_item2(self, item):
        # Ambil teks lama
        old_text = item.text()

        # Buat dialog input secara manual agar bisa diatur lebarnya
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Edit Command")
        dialog.setTextValue(old_text)  # Isi dengan teks lama
        dialog.setFixedWidth(500)  # Lebarkan dialog
        dialog.resize(400, 100)  # Bisa diatur sesuai kebutuhan
        dialog.setStyleSheet("""
                            /* Background utama dialog */
                            QDialog {
                                background-color: rgba(20, 20, 20, 0.92); /* Warna gelap dengan transparansi */
                                border-radius: 12px; /* Sudut melengkung */
                                padding: 15px; /* Jarak dalam */
                            }

                            /* Label dalam dialog */
                            QLabel {
                                color: #E5E9F0; /* Warna teks */
                                font-size: 16px;
                            }

                            /* Tombol dalam dialog */
                            QPushButton {
                                background-color: #3B4252;
                                color: #D8DEE9;
                                border: 2px solid #81A1C1;
                                border-radius: 8px;
                                padding: 8px 12px;
                                font-size: 14px;
                                transition: all 0.3s ease-in-out;
                            }

                            QPushButton:hover {
                                background-color: #4C566A;
                                border: 2px solid #88C0D0;
                                box-shadow: 0px 0px 12px rgba(136, 192, 208, 0.6); /* Glow efek hover */
                            }

                            /* Input box */
                            QLineEdit {
                                background-color: #3B4252;
                                color: #D8DEE9;
                                border: 2px solid #1B5E20;
                                border-radius: 8px;
                                font-size: 18px;
                                padding: 6px;
                                selection-background-color: #81A1C1;
                                selection-color: #2E3440;
                            }

                            QLineEdit:hover {
                                border: 2px solid #81A1C1;
                            }

                            QLineEdit:focus {
                                border: 2px solid #88C0D0;
                                background-color: #434C5E;
                            }
                        """)
        dialog.setWindowIcon(QtGui.QIcon("logo.png"))
        self.set_title_bar_color(dialog)
        # Tampilkan dialog
        if dialog.exec_() == QDialog.Accepted:
            new_text = dialog.textValue().strip().upper()  # Ambil teks baru
            if new_text:  # Pastikan tidak kosong
                item.setText(new_text)  # Simpan perubahan
# ----------------------------------------------------------------------------------------------
    def S1_ON(self):
        self.pushButton_S1.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #BF616A ; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 14px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}")
    def S1_OFF(self):
        self.pushButton_S1.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #9575CD ; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 14px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}")    
# ----------------------------------------------------------------------------------------------
    def S2_ON(self):
        self.pushButton_S2.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #BF616A ; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 14px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}")
    def S2_OFF(self):
        self.pushButton_S2.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #9575CD ; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 14px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}")
# ----------------------------------------------------------------------------------------------
    def S3_ON(self):
        self.pushButton_S3.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #BF616A ; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 14px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}")
    def S3_OFF(self):
        self.pushButton_S3.setStyleSheet("QPushButton {\n"
                                         "    background-color: #2E3440; /* Warna latar belakang tombol */\n"
                                         "    color: #ECEFF4; /* Warna teks */\n"
                                         "    border: 2px solid #9575CD ; /* Warna border */\n"
                                         "    border-radius: 6px; /* Sudut tombol yang melengkung */\n"
                                         "    padding: 5px; /* Padding di dalam tombol */\n"
                                         "    font-size: 14px; /* Ukuran font */\n"
                                         "    font-weight: bold; /* Ketebalan font */\n"
                                         "}")
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_tunggu(self):
        tunggu_value = self.doubleSpinBox.value() 
        new_item = f'G4 S{tunggu_value}'
        
        # Cek apakah ada item yang dipilih di listWidget
        selected_items = self.listWidget_save.selectedItems()
        if selected_items:
            # Ganti teks item yang dipilih dengan G-code yang baru
            selected_items[0].setText(new_item)
        else:
            # Jika tidak ada item yang dipilih, tambahkan item baru di baris terakhir
            self.listWidget_save.addItem(new_item)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_new(self):
        selected_items = self.listWidget_save.selectedItems()

        if not selected_items:  # Jika tidak ada item yang dipilih
            self.listWidget_save.addItem("")  # Tambahkan item baru di akhir
        else:  # Jika ada item yang dipilih
            indeks_terpilih = self.listWidget_save.row(selected_items[0])  # Dapatkan index item yang dipilih
            self.listWidget_save.insertItem(indeks_terpilih + 1, "")  # Tambahkan item kosong di bawahnya
            self.listWidget_save.setCurrentRow(indeks_terpilih + 1)  # Pilih item baru yang ditambahkan

# ----------------------------------------------------------------------------------------------
    def update_spinboxes_from_selected_item(self):
        self.listWidget_save.blockSignals(False)
        # Ambil item yang dipilih
        selected_items = self.listWidget_save.selectedItems()
        
        if not selected_items:
            return  # Tidak ada item yang dipilih
            
        current_item_text = selected_items[0].text()
        
        # Fungsi untuk ekstrak nilai dari G-code
        def extract_value(key, default):
            match = re.search(rf'{key}(-?\d+\.?\d*)', current_item_text)
            return float(match.group(1)) if match else default
        
        try:
            # Update nilai spin box
            self.doubleSpinBox_X.setValue(extract_value('X', self.doubleSpinBox_X.value()))
            self.doubleSpinBox_Y.setValue(extract_value('Y', self.doubleSpinBox_Y.value()))
            self.doubleSpinBox_Z.setValue(extract_value('Z', self.doubleSpinBox_Z.value()))
            self.doubleSpinBox_E.setValue(extract_value('E', self.doubleSpinBox_E.value()))
            self.doubleSpinBox_speed.setValue(extract_value('F', self.doubleSpinBox_speed.value()))
            self.doubleSpinBox_gripper_servo.setValue(extract_value('A', self.doubleSpinBox_gripper_servo.value()))
            self.doubleSpinBox_gripper_servoB.setValue(extract_value('B', self.doubleSpinBox_gripper_servoB.value()))
        except ValueError:
            pass  # Handle error jika format tidak valid
        
        if self.tanda_kalibrasi:  # Hanya kirim jika kalibrasi selesai
            # Kirim perintah berdasarkan item yang dipilih
            selected_items = self.listWidget_save.selectedItems()
            if selected_items:
                current_item = selected_items[0].text()
                if current_item.startswith('G0'):
                    self.send_gcode_command_pilih()

                if current_item.startswith('G100'):
                    self.send_gcode_command_servo()

                if "VACUM ON" in current_item:
                    self.pushButton_gripper_vacum.setChecked(True)
                    self.pushButton_gripper_vacum.setText("VACUM ON")
                    
                    self.pushButton_LG3.setChecked(True)
                    self.pushButton_LG3.setText("LG3 ON")

                    self.pushButton_LG2.setChecked(False)
                    self.pushButton_LG2.setText("LG2 OFF")

                    self.fungsi_pushButton_gripper_vacum()

                if "VACUM OFF" in current_item:
                    self.pushButton_gripper_vacum.setChecked(False)
                    self.pushButton_gripper_vacum.setText("VACUM OFF")

                    self.pushButton_LG3.setChecked(False)
                    self.pushButton_LG3.setText("LG3 OFF")

                    self.fungsi_pushButton_gripper_vacum()

                if "LG1 ON" in current_item:
                    self.pushButton_LG1.setChecked(True)
                    self.pushButton_LG1.setText("LG1 ON")
                    self.fungsi_pushButton_LG1()
                    
                if "LG1 OFF" in current_item:
                    self.pushButton_LG1.setChecked(False)
                    self.pushButton_LG1.setText("LG1 OFF") 
                    self.fungsi_pushButton_LG1()

                if "LG2 ON" in current_item:
                    self.pushButton_LG2.setChecked(True)
                    self.pushButton_LG2.setText("LG2 ON") 
                    self.fungsi_pushButton_LG2()

                if "LG2 OFF" in current_item:
                    self.pushButton_LG2.setChecked(False)
                    self.pushButton_LG2.setText("LG2 OFF")
                    self.fungsi_pushButton_LG2()

                if "LG3 ON" in current_item:
                    self.pushButton_LG3.setChecked(True)
                    self.pushButton_LG3.setText("LG3 ON") 
                    self.fungsi_pushButton_LG3()

                if "LG3 OFF" in current_item:
                    self.pushButton_LG3.setChecked(False)
                    self.pushButton_LG3.setText("LG3 OFF") 
                    self.fungsi_pushButton_LG3()   
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_home(self):
        self.doubleSpinBox_X.setProperty("value", 0)
        self.horizontalSlider_X.setProperty("value", 0)

        self.doubleSpinBox_Y.setProperty("value", 217)
        self.horizontalSlider_Y.setProperty("value", 217)

        self.doubleSpinBox_Z.setProperty("value", 138)
        self.horizontalSlider_Z.setProperty("value", 138)

        self.doubleSpinBox_E.setProperty("value", 0)
        self.horizontalSlider_E.setProperty("value", 0)

        self.doubleSpinBox_gripper_servo.setProperty("value", 90)
        self.horizontalSlider_gripper_servo.setProperty("value", 90)
        
        if self.tanda_kalibrasi:  # Hanya kirim jika kalibrasi selesai
            self.send_gcode_command()
            self.send_gcode_command_servo()
            self.update_button_save_move()
            self.blink_timer_move.stop()
            self.update_button_save_move_servo()
            self.blink_timer_move_servo.stop()
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_delete(self):
        # Blokir sinyal selectionChanged sementara
        self.listWidget_save.blockSignals(True)

        selected_items = self.listWidget_save.selectedItems()
        if not selected_items:
            self.textEdit_vew.append("Pilih item yang akan dihapus")
            return  # Tidak ada item yang dipilih
        
        # Ambil item pertama yang dipilih
        item = selected_items[0]
        # Dapatkan indeks baris dari item yang dipilih
        indeks = self.listWidget_save.row(item)
        # Hapus item berdasarkan indeks
        self.listWidget_save.takeItem(indeks)
        self.textEdit_vew.append("Item dihapus")
        self.listWidget_save.clearSelection()  # Membersihkan seleksi setelah penghapusan

        # Aktifkan kembali sinyal
        self.listWidget_save.blockSignals(False)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_up(self):
        # Blokir sinyal selectionChanged sementara
        self.listWidget_save.blockSignals(True)
        
        # Simpan posisi scroll vertikal
        scroll_position = self.listWidget_save.verticalScrollBar().value()
        
        # Dapatkan indeks item yang dipilih
        selected_items = self.listWidget_save.selectedItems()
        if not selected_items:
            self.textEdit_vew.append("Pilih item yang akan dipindahkan")
            return
        indeks_terpilih = self.listWidget_save.row(selected_items[0])
            
        if indeks_terpilih > 0:
            item = self.listWidget_save.takeItem(indeks_terpilih)
            self.listWidget_save.insertItem(indeks_terpilih - 1, item)
            self.listWidget_save.setCurrentRow(indeks_terpilih - 1)

        # Kembalikan posisi scroll
        self.listWidget_save.verticalScrollBar().setValue(scroll_position)
        
        # Aktifkan kembali sinyal
        self.listWidget_save.blockSignals(False)

# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_down(self):
        # Blokir sinyal selectionChanged sementara
        self.listWidget_save.blockSignals(True)
        
        # Simpan posisi scroll vertikal
        scroll_position = self.listWidget_save.verticalScrollBar().value()
        
        # Dapatkan indeks item yang dipilih
        selected_items = self.listWidget_save.selectedItems()
        if not selected_items:
            self.textEdit_vew.append("Pilih item yang akan dipindahkan")
            return
        indeks_terpilih = self.listWidget_save.row(selected_items[0])
            
        if indeks_terpilih < self.listWidget_save.count() - 1:
            item = self.listWidget_save.takeItem(indeks_terpilih)
            self.listWidget_save.insertItem(indeks_terpilih + 1, item)
            self.listWidget_save.setCurrentRow(indeks_terpilih + 1)

        # Kembalikan posisi scroll
        self.listWidget_save.verticalScrollBar().setValue(scroll_position)
        
        # Aktifkan kembali sinyal
        self.listWidget_save.blockSignals(False)
# ----------------------------------------------------------------------------------------------
# --- Definisikan di luar setupUi dan retranslateUi, sejajar dengan fungsi lainnya ---

    def fungsi_pushButton_gripper_01_toggle(self):
        """Mengatur posisi Gripper antara 10 (Menutup) dan 50 (Membuka)."""
        
        # 1. Tentukan Nilai Target
        if self.pushButton_gripper_01.isChecked():
            # Status: ON (Menutup)
            target_value = 10.00
            status_text = "Gripper Menutup (10.00)"
        else:
            # Status: OFF (Membuka)
            target_value = 50.00
            status_text = "Gripper Membuka (50.00)"

        # 2. Update Slider/Spin Box GUI
        self.doubleSpinBox_gripper_servoB.setValue(target_value)
        # Slider B akan otomatis mengikuti karena sudah terhubung di retranslateUi
        
        # 3. Kirim Perintah ke Robot (Hanya jika terhubung)
        if hasattr(self, 'serial') and self.serial and self.serial.isOpen():
            # Ambil nilai A saat ini (servo utama)
            a_value = self.doubleSpinBox_gripper_servo.text()
            
            # Buat perintah G-code untuk Gripper (G100 AXX BXX)
            gcode_command = f'G100 A{a_value} B{target_value:.2f}\r' # .2f agar format sesuai
            
            self.serial.write(gcode_command.encode())
            self.update_view(f"Kirim: {gcode_command.strip()}")
            print(f"Kirim: {gcode_command.strip()}")
        
        self.update_view(status_text)
# ----------------------------------------------------------------------------------------------
    def fungsi_pushButton_save_manual(self):
        # Ambil teks dari lineEdit
        input_text = self.lineEdit.text().upper()  # Simpan dalam teks besar

        # Cek apakah ada item yang dipilih di listWidget_save
        selected_item = self.listWidget_save.selectedItems()

        if selected_item:
            if input_text:  # Pastikan lineEdit tidak kosong
                # Jika ada item yang dipilih, ganti teks item yang dipilih dengan teks dari lineEdit
                selected_item[0].setText(input_text)
                self.lineEdit.clear()  # Bersihkan lineEdit setelah mengganti item
            else:
                print("Teks kosong, tidak ada yang diubah!")
                self.textEdit_vew.append("Teks kosong, tidak ada yang diubah!")
        else:
            # Jika tidak ada item yang dipilih, tambahkan teks ke listWidget_save
            if input_text:  # Pastikan input tidak kosong
                self.listWidget_save.addItem(input_text)
                self.lineEdit.clear()  # Bersihkan lineEdit setelah menambahkan ke listWidget_save
            else:
                print("Teks kosong, tidak ada yang ditambahkan!")
                self.textEdit_vew.append("Teks kosong, tidak ada yang ditambahkan!")
# ----------------------------------------------------------------------------------------------
    def send_serial_data_input_manual(self):
        data = self.lineEdit.text()
        data_with_cr = f"{data}\r"  # Menambahkan '\r' ke data yang dikirim
        print(f"Kirim: {data_with_cr}")
        message = f"Kirim: {data_with_cr}"
        self.textEdit_vew.append(message)
        self.serial.write(data_with_cr.encode())  # Kirim data ke serial
        self.lineEdit.clear()
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Kelas Dialog Kustom
class GripperChoiceDialog_LG(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        parent.setWindowIcon(QtGui.QIcon("D:\Me\Akademik\Teknik Mekatronika\Mata Kuliah\Semester 5\Pemrograman Sistem Mekatronik\DOBOT ROBOT\DOBOTROBOT.ico"))
        self.selected = None  # Variabel untuk menyimpan pilihan pengguna

        self.setWindowTitle("Pilih Output ")
        self.setFixedSize(220, 220)  # Atur ukuran dialog

        # Layout vertikal untuk menyusun tombol
        layout = QVBoxLayout(self)

       
        self.lg1_button = QPushButton("SAVE LG1")
        layout.addWidget(self.lg1_button)
        self.lg1_button.clicked.connect(self.lg1)

  
        self.lg2_button = QPushButton("SAVE LG2")
        layout.addWidget(self.lg2_button)
        self.lg2_button.clicked.connect(self.lg2)

        self.lg3_button = QPushButton("SAVE LG3")
        layout.addWidget(self.lg3_button)
        self.lg3_button.clicked.connect(self.lg3)

        # Tombol Batal
        self.cancel_button = QPushButton("BATAL")
        layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.reject)  # Menutup dialog tanpa memilih

        # Aktifkan Dark Mode
        self.enable_dark_mode()
        self.set_title_bar_color()

    def lg1(self):
        self.selected = "LG1"
        self.accept()  # Menutup dialog dengan status Accepted

    def lg2(self):
        self.selected = "LG2"
        self.accept()  # Menutup dialog dengan status Accepted

    def lg3(self):
        self.selected = "LG3"
        self.accept()  # Menutup dialog dengan status Accepted    

    def enable_dark_mode(self):
        dark_stylesheet = """
            QWidget { 
                background-color: #1D293D;  /* Warna latar belakang lebih modern */
                color: #E0E0E0; /* Warna teks lebih soft */
                font-size: 14px; 
            }

            QPushButton { 
                background-color: #252525; 
                border: 2px solid #1B5E20; 
                padding: 10px; 
                border-radius: 10px;  /* Membuat tombol melengkung */
                transition: all 0.3s ease-in-out;  /* Animasi smooth */
            }

            QPushButton:hover { 
                background-color: #333333; 
                box-shadow: 0px 0px 10px rgba(0, 122, 204, 0.5); /* Glow efek hover */
            }

            QPushButton:checked { 
                background-color: #007ACC; 
                color: white; 
                border-radius: 10px;  
            }

            QListWidget { 
                background-color: #252525; 
                border: 2px solid #333; 
                border-radius: 10px;  
                padding: 5px; 
            }

            QListWidget::item { 
                padding: 8px; 
                border-radius: 6px;  
            }

            QListWidget::item:selected { 
                background-color: #007ACC; 
                color: white; 
                border-radius: 6px;  
            }

            QInputDialog QLabel { 
                color: white; 
            }

            QLineEdit { 
                background-color: #2E2E2E; 
                color: white; 
                border: 2px solid #007ACC; 
                border-radius: 8px;  
                padding: 5px;
            }

            QMessageBox { 
                background-color: #222222; 
                border-radius: 10px;  
            }

            QDialog { 
                background-color: #222222; 
                border-radius: 10px;  
            }

            QDialog QPushButton { 
                background-color: #252525; 
                border-radius: 8px;  
                padding: 6px; 
            }

            QDialog QPushButton:hover { 
                background-color: #333333; 
                box-shadow: 0px 0px 8px rgba(0, 122, 204, 0.5); 
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def set_title_bar_color(self):
        hwnd = self.winId().__int__()
        value = ctypes.c_int(1)  # Enable dark mode title bar
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        ) 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Kelas Dialog Kustom
class GripperChoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        parent.setWindowIcon(QtGui.QIcon("D:\Me\Akademik\Teknik Mekatronika\Mata Kuliah\Semester 5\Pemrograman Sistem Mekatronik\DOBOT ROBOT\LOGO\DOBOT_ROBOT.png"))
        self.selected = None  # Variabel untuk menyimpan pilihan pengguna

        self.setWindowTitle("Pilih Gripper ")
        self.setFixedSize(220, 170)  # Atur ukuran dialog

        # Layout vertikal untuk menyusun tombol
        layout = QVBoxLayout(self)

        # Tombol Vacum
        self.vacum_button = QPushButton("SAVE VACUM")
        layout.addWidget(self.vacum_button)
        self.vacum_button.clicked.connect(self.select_vacum)

        # Tombol Servo
        self.servo_button = QPushButton("    ")
        layout.addWidget(self.servo_button)
        self.servo_button.clicked.connect(self.select_servo)
        self.servo_button.setEnabled(False)

        # Tombol Batal
        self.cancel_button = QPushButton("BATAL")
        layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.reject)  # Menutup dialog tanpa memilih

        # Aktifkan Dark Mode
        self.enable_dark_mode()
        self.set_title_bar_color()

    def select_servo(self):
        self.selected = "Servo"
        self.accept()  # Menutup dialog dengan status Accepted

    def select_vacum(self):
        self.selected = "VACUM"
        self.accept()  # Menutup dialog dengan status Accepted

    def enable_dark_mode(self):
        dark_stylesheet = """
            QWidget { 
                background-color: #181818;  /* Warna latar belakang lebih modern */
                color: #E0E0E0; /* Warna teks lebih soft */
                font-size: 14px; 
            }

            QPushButton { 
                background-color: #252525; 
                border: 2px solid #1B5E20; 
                padding: 10px; 
                border-radius: 10px;  /* Membuat tombol melengkung */
                transition: all 0.3s ease-in-out;  /* Animasi smooth */
            }

            QPushButton:hover { 
                background-color: #333333; 
                box-shadow: 0px 0px 10px rgba(0, 122, 204, 0.5); /* Glow efek hover */
            }

            QPushButton:checked { 
                background-color: #007ACC; 
                color: white; 
                border-radius: 10px;  
            }

            QListWidget { 
                background-color: #252525; 
                border: 2px solid #333; 
                border-radius: 10px;  
                padding: 5px; 
            }

            QListWidget::item { 
                padding: 8px; 
                border-radius: 6px;  
            }

            QListWidget::item:selected { 
                background-color: #007ACC; 
                color: white; 
                border-radius: 6px;  
            }

            QInputDialog QLabel { 
                color: white; 
            }

            QLineEdit { 
                background-color: #2E2E2E; 
                color: white; 
                border: 2px solid #007ACC; 
                border-radius: 8px;  
                padding: 5px;
            }

            QMessageBox { 
                background-color: #222222; 
                border-radius: 10px;  
            }

            QDialog { 
                background-color: #222222; 
                border-radius: 10px;  
            }

            QDialog QPushButton { 
                background-color: #252525; 
                border-radius: 8px;  
                padding: 6px; 
            }

            QDialog QPushButton:hover { 
                background-color: #333333; 
                box-shadow: 0px 0px 8px rgba(0, 122, 204, 0.5); 
            }

            QPushButton:disabled {
                background-color: #222222;  /* Warna abu-abu */
                color: #333333;
                border: 2px solid #333333;
            }
        """
        self.setStyleSheet(dark_stylesheet)

    def set_title_bar_color(self):
        hwnd = self.winId().__int__()
        value = ctypes.c_int(1)  # Enable dark mode title bar
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
              
   
#===============================================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # === 🎯 TAMPILKAN LOADING SCREEN PERTAMA ===
    splash = LoadingScreen()
    splash.show()
    
    # === 🎯 SIMULASIKAN PROSES LOADING ===
    for i in range(101):
        splash.update_progress(i, f"Loading DOBOT ROBOT System...")
        time.sleep(0.02)  # Hapus atau kurangi di production
    
    # === 🎯 BUAT MAIN WINDOW ===
    DOBOTROBOT_V1 = QtWidgets.QMainWindow()
    ui = Ui_DOBOTROBOT_V1()
    ui.setupUi(DOBOTROBOT_V1)
    
    # === 🎯 TUTUP SPLASH DAN TAMPILKAN MAIN WINDOW ===
    splash.finish(DOBOTROBOT_V1)
    DOBOTROBOT_V1.show()
    
    sys.exit(app.exec_())
    


    