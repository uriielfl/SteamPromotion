from PySide2 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
from readstyle import readStyle
from newmain import AddIt, CheckIt, RemoveIt
from functools import partial
from time import sleep


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowIcon(QtGui.QIcon('img/globalheader_logo.png'))
        self.resize(400, 500)
        self.setWindowTitle('Steam Promotion')
        self.setStyleSheet(readStyle())
        self.start()

    def start(self):
        self.logo = QtWidgets.QLabel()
        self.logo.setPixmap(QtGui.QPixmap('img/globalheader_logo.png'))
        self.logo.setScaledContents(True)
        self.logo.setMaximumSize(200, 220)
        self.pesquisa = QtWidgets.QLineEdit()
        self.pesquisa.setPlaceholderText('Insira a URL')
        self.botao1 = QtWidgets.QPushButton('Adicionar Jogo a lista')
        self.botao1.clicked.connect(partial(AddIt, master=self))
        self.botao1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao2 = QtWidgets.QPushButton('Checar promoções')
        self.botao2.clicked.connect(partial(CheckIt, master=self))
        self.botao2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.notification = QtWidgets.QListWidget()
        self.notification.setMinimumHeight(200)
        self.remove = QtWidgets.QPushButton('Remover')
        self.remove.setVisible(False)
        self.remove.clicked.connect(partial(RemoveIt, master=self))
        self.grade = QtWidgets.QGridLayout(self)
        self.grade.addWidget(self.logo, 0, 0, QtCore.Qt.AlignHCenter)
        self.grade.addWidget(self.pesquisa, 1, 0, QtCore.Qt.AlignLeft)
        self.grade.addWidget(self.botao1, 1, 0, QtCore.Qt.AlignRight)
        self.grade.addWidget(self.botao2)
        self.grade.addWidget(self.notification)
        self.grade.addWidget(self.remove)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    form = MyWidget()
    form.show()
    app.exec_()