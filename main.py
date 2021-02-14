import json
import os
import sys
import qdarkstyle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pygame import mixer

play_song = []
song_cur = []
loop = False

if not os.path.isfile('settings.json'):
    open('settings.json', 'a').close()
    with open('settings.json', 'w') as jFile:
        a = {"volume":50}
        json_string = json.dumps(a, default=lambda o: o.__dict__, sort_keys=True, indent=2)
        jFile.write(json_string)
with open('settings.json', 'r') as jFile:
    jdata = json.load(jFile)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Music Player")
        MainWindow.resize(640, 480)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.song_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.song_progress.setProperty("value", 0)
        self.song_progress.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.song_progress.setObjectName("song_progress")
        self.gridLayout_2.addWidget(self.song_progress, 1, 0, 1, 3)
        self.stop_but = QtWidgets.QPushButton(self.centralwidget)
        self.stop_but.setObjectName("stop_but")
        self.gridLayout_2.addWidget(self.stop_but, 0, 2, 1, 1)
        self.backward_b = QtWidgets.QPushButton(self.centralwidget)
        self.backward_b.setObjectName("backward")
        self.gridLayout_2.addWidget(self.backward_b, 0, 0, 1, 1)
        self.cont_pau = QtWidgets.QPushButton(self.centralwidget)
        self.cont_pau.setObjectName("cont_pau")
        self.gridLayout_2.addWidget(self.cont_pau, 0, 1, 1, 1)
        self.loop_single = QtWidgets.QCheckBox(self.centralwidget)
        self.loop_single.setObjectName("loop_single")
        self.gridLayout_2.addWidget(self.loop_single, 0, 4, 1, 1)
        self.forward_b = QtWidgets.QPushButton(self.centralwidget)
        self.forward_b.setObjectName("forward")
        self.gridLayout_2.addWidget(self.forward_b, 0, 3, 1, 1)
        self.time_remain = QtWidgets.QLabel(self.centralwidget)
        self.time_remain.setObjectName("time_remain")
        self.gridLayout_2.addWidget(self.time_remain, 1, 3, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.volume = QtWidgets.QLabel(self.centralwidget)
        self.volume.setAlignment(QtCore.Qt.AlignCenter)
        self.volume.setObjectName("volume")
        self.verticalLayout_2.addWidget(self.volume)
        self.volume_ctrl = QtWidgets.QSlider(self.centralwidget)
        self.volume_ctrl.setOrientation(QtCore.Qt.Horizontal)
        self.volume_ctrl.setObjectName("volume_ctrl")
        self.volume_ctrl.setValue(jdata["volume"])
        self.volume_ctrl.setMinimum(0)
        self.volume_ctrl.setMaximum(100)
        self.volume_ctrl.setSingleStep(1)
        self.verticalLayout_2.addWidget(self.volume_ctrl)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 4, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.playing = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.playing.setFont(font)
        self.playing.setAlignment(QtCore.Qt.AlignCenter)
        self.playing.setObjectName("playing")
        self.playing.setScaledContents(True)
        self.playing.setWordWrap(True)
        self.verticalLayout.addWidget(self.playing)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.song_list = ListWidget(self.centralwidget)
        self.song_list.setMinimumSize(QtCore.QSize(183, 0))
        self.song_list.setAcceptDrops(True)
        self.song_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.song_list.setObjectName("song_list")
        self.verticalLayout_3.addWidget(self.song_list)
        self.delete_song_q = QtWidgets.QPushButton(self.centralwidget)
        self.delete_song_q.setObjectName("delete_song_q")
        self.verticalLayout_3.addWidget(self.delete_song_q)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionLisence_Information = QtWidgets.QAction(MainWindow)
        self.actionLisence_Information.setObjectName("actionLisence_Information")
        self.menuFile.addAction(self.actionOpen)
        self.menuAbout.addAction(self.actionLisence_Information)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 5, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.event_timer = QTimer()

        self.info = QMessageBox()
        self.info.setWindowTitle("License Information")
        self.info.setText("MIT License\n\nCopyright (c) 2021 Marganotvke")

        mixer.music.set_volume(jdata["volume"]/100)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionLisence_Information.triggered.connect(lambda: self.info.exec_())
        self.cont_pau.clicked.connect(lambda: self.cur_playing())
        self.volume_ctrl.valueChanged[int].connect(lambda: self.change_vol())
        self.volume_ctrl.sliderReleased.connect(lambda: self.vol_write())
        self.stop_but.clicked.connect(lambda: self.stop_playing())
        self.forward_b.clicked.connect(lambda: self.forward())
        self.backward_b.clicked.connect(lambda: self.backward())
        self.song_list.dropped.connect(lambda e: self.start_play(e))
        self.song_list.itemDoubleClicked.connect(lambda: self.jump_start(self.song_list.currentRow()))
        self.song_list.model().rowsAboutToBeMoved.connect(lambda e,f,g,h,i: self.test(f,i))
        self.delete_song_q.clicked.connect(lambda: self.delete_q(self.song_list.currentRow()))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music Player"))
        self.song_progress.setFormat(_translate("MainWindow", "%p%"))
        self.stop_but.setText(_translate("MainWindow", "■"))
        self.backward_b.setText(_translate("MainWindow", "Backward"))
        self.cont_pau.setText(_translate("MainWindow", "Load Song"))
        self.loop_single.setText(_translate("MainWindow", "Loop"))
        self.forward_b.setText(_translate("MainWindow", "Forward"))
        self.time_remain.setText(_translate("MainWindow", "Time"))
        self.volume.setText(_translate("MainWindow", f"Volume: {jdata['volume']} "))
        self.playing.setText(_translate("MainWindow", "Currently playing: None"))
        self.delete_song_q.setText(_translate("MainWindow", "Delete Selected Song Queue"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionLisence_Information.setText(_translate("MainWindow", "License Information"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

    def test(self, e = None,f = None):
        f -= 1 if self.song_list.count() == f else 0
        play_song.insert(f,play_song.pop(e))
        print(f"rearr: {play_song}")

    def jump_start(self,index = None):
        global song_cur
        if index is None:
            pass
        else:
            mixer.music.stop()
            mixer.music.unload()
            mixer.music.load(play_song[index][1])
            self.playing.setText(f"Currently playing: {play_song[index][0]}")
            mixer.music.play()
            self.time_remain.setText(f"0/{int(play_song[index][2] / 1000)}(s)")
            song_cur = play_song[index]
            self.cont_pau.setText("||")

    def reset(self):
        mixer.music.unload()
        self.playing.setText(f"Currently playing: None")
        self.cont_pau.setText("Load Song")
        self.time_remain.setText("Time")
        self.song_progress.setProperty("value", 0)

    def start_play(self, a = None):
        global play_song
        global song_cur
        print("Emitted from drop event:", a)
        if not mixer.music.get_busy() and play_song:
            mixer.music.load(play_song[0][1])
            self.playing.setText(f"Currently playing: {play_song[0][0]}")
            mixer.music.play()
            self.time_remain.setText(f"0/{int(play_song[0][2] / 1000)}(s)")
            song_cur = play_song[0]
            self.cont_pau.setText("||")
            self.event_timer.timeout.connect(self.handleTimer)
            self.event_timer.start(500)

    def play_next(self):
        global song_cur
        mixer.music.unload()
        self.song_list.takeItem(0)
        if play_song:
            play_song.pop(0)
            mixer.music.load(play_song[0][1])
            song_cur = play_song[0]
            self.playing.setText(f"Currently playing: {song_cur[0]}")
            mixer.music.play()
        else:
            mixer.music.unload()
            self.event_timer.stop()
            self.reset()

    def stop_playing(self):
        global play_song
        global song_cur
        mixer.music.stop()
        play_song = []
        song_cur = []
        for i in range(self.song_list.count()):
            self.song_list.takeItem(0)
        self.reset()

    def cur_playing(self):
        if not play_song:
            self.open_file()
        else:
            if mixer.music.get_busy():
                mixer.music.pause()
                self.cont_pau.setText("▶")
            else:
                mixer.music.unpause()
                self.cont_pau.setText("||")

    def forward(self):
        if play_song:
            mixer.music.stop()
            self.play_next()
        else:
            mixer.music.stop()
            self.reset()

    def backward(self):
        if play_song:
            mixer.music.stop()
            mixer.music.play()
        else:
            pass

    def open_file(self):
        filename = QFileDialog.getOpenFileName(None, 'Open File', filter="*.mp3;;*.wav;;*.ogg;;All files(*)")
        if filename != ('', ''):
            song = os.path.basename(filename[0])
            play_song.append([song.split(".")[0],filename[0],int(mixer.Sound(filename[0]).get_length()*1000)])
            self.song_list.addItem(play_song[0][0])
            self.start_play()

    def delete_q(self, i):
        global play_song
        if i != -1:
            if i == 0:
                self.song_list.takeItem(i)
                self.play_next()
            else:
                play_song.pop(i)
                self.song_list.takeItem(i)
        else:
            pass

    def change_vol(self):
        vol = self.volume_ctrl.value()
        mixer.music.set_volume(vol/100)
        self.volume.setText(f"Volume: {vol}")

    def vol_write(self):
        vol = self.volume_ctrl.value()
        jdata["volume"] = vol
        mixer.music.set_volume(vol/100)
        with open('settings.json', 'w') as jFile:
            json_string = json.dumps(jdata, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            jFile.write(json_string)

    def handleTimer(self):
        if song_cur:
            t = ((mixer.music.get_pos()/song_cur[2]))
            self.song_progress.setProperty("value",t*100)
            self.time_remain.setText(f"{int(mixer.music.get_pos()/1000)}/{int(song_cur[2]/1000)}(s)")
            if t<0:
                if self.loop_single.isChecked():
                    mixer.music.play()
                elif not self.loop_single.isChecked():
                    self.play_next()

class ListWidget(QtWidgets.QListWidget):
    dropped = QtCore.pyqtSignal(str)
    
    def __init__(self, parent):
        super(ListWidget, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setAlternatingRowColors(True)
        self.setWordWrap(True)

    def dragEnterEvent(self,e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            super().dragEnterEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            super().dragMoveEvent(e)


    def dropEvent(self,e):
        if e.mimeData().hasUrls():
            global play_song
            foo = e.mimeData().text()
            foo = foo.split("///")
            song = os.path.basename(foo[1])
            song = song.split(".")
            if song[1] in ["mp3","wav","ogg"]:
                self.addItem(song[0])
                play_song.append([song[0],foo[1],int(mixer.Sound(foo[1]).get_length()*1000)])
                self.dropped.emit(song[0])
        else:
            super().dropEvent(e)

if __name__ == "__main__":
    mixer.init()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
