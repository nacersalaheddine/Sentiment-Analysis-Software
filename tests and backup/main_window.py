import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QHBoxLayout,QLineEdit,QFormLayout, 
QVBoxLayout,QToolTip,QAction,QMenu,QRadioButton,QLabel,QStackedWidget,QGridLayout,qApp,QMessageBox,QMainWindow,QDesktopWidget,QListWidget)
from PyQt5.QtGui import QIcon,QFont


class QTMainWindow(QMainWindow):
    __lang_strings = None
    
    def __init__(self,lang_strings):
        super().__init__()
        
        self.__lang_strings = lang_strings
        self.initUI()
        
    def createMenuBar(self):
        exitAct = QAction(QIcon(self.__lang_strings['menuBarItems']['exit']['iconPath']), 
        self.__lang_strings['menuBarItems']['exit']['name'], self)        
        exitAct.setShortcut(self.__lang_strings['menuBarItems']['exit']['mnemonic'])
        exitAct.setStatusTip(self.__lang_strings['menuBarItems']['exit']['statusTip'])
        exitAct.triggered.connect(qApp.quit)
        
        newAct = QAction(QIcon(self.__lang_strings['menuBarItems']['new']['iconPath']),
        self.__lang_strings['menuBarItems']['new']['name'], self) 
        newAct.setShortcut(self.__lang_strings['menuBarItems']['new']['mnemonic'])
        newAct.setStatusTip(self.__lang_strings['menuBarItems']['new']['statusTip'])
        
        impMenu = QMenu(self.__lang_strings['menuBarItems']['import']['name'], self)
  
        impTrainData = QAction('Import traning data', self) 
        impTestData = QAction('Import test data', self) 
        
        impMenu.addAction(impTrainData)
        impMenu.addAction(impTestData)
        
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu(self.__lang_strings['menuBar']['file']['name'])
        
        #tool bar
        self.createToolBar(exitAct)

        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        fileMenu.addAction(exitAct)
    
    def createToolBar(self,exitAct):
        self.toolbar = self.addToolBar(self.__lang_strings['menuBarItems']['exit']['name'])
        self.toolbar.addAction(exitAct)
        
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip(self.__lang_strings['mainWindow']['toolTip'])
        #print(type(self.__lang_strings['mainWindow']['width']))

        self.setWindowTitle(self.__lang_strings['mainWindow']['windowTitle'])
        self.setWindowIcon(QIcon(self.__lang_strings['mainWindow']['windowIcon']))
        
        self.createMenuBar()

        #Creating the status bar
        self.statusBar().showMessage(self.__lang_strings['statusBar']['msg'])
        
        #To Center the window
        self.center()
        
        #Button
        btn = self.createButton('Button',50,50,'Push to <b>Button</b> widget')
        #Quit Button
        qbtn = self.createButton(self.__lang_strings['buttons']['quitButton']['name']
        ,100,100,self.__lang_strings['buttons']['quitButton']['toolTip'])
        
        #Setting events
        qbtn.clicked.connect(QApplication.instance().quit)
        '''
        #Creating layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(qbtn)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox) 
        '''
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Contact' )
        self.leftlist.insertItem(1, 'Personal' )

        self.central_widget = QWidget()               # define central widget
        self.setCentralWidget(self.central_widget)    # set QMainWindow.centralWidget

        self.stack1 = QWidget()
        self.stack2 = QWidget()

        self.stack1UI()
        self.stack2UI()

        self.Stack = QStackedWidget (self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        grid = QGridLayout()
        self.centralWidget().setLayout(grid)# add the layout to the central widget
        grid.addWidget(self.leftlist,0,0)
        grid.addWidget(self.Stack,0,1)

        self.leftlist.currentRowChanged.connect(self.display)                   
        
        
        
        self.setGeometry(300, 300, self.__lang_strings['mainWindow']['width'],
        self.__lang_strings['mainWindow']['height'])
        self.show()
        
    def stack1UI(self):
        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        layout.addRow("Address",QLineEdit())
        self.stack1.setLayout(layout)

    def stack2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"),sex)
        layout.addRow("Date of Birth",QLineEdit())

        self.stack2.setLayout(layout)
    def display(self,i):
        self.Stack.setCurrentIndex(i)
        
    def createButton(self,title,x,y,toolTip):
        b = QPushButton(title, self)
        b.setToolTip(toolTip)
        #b.move(x, y) 
        #b.resize(b.sizeHint())
        return b
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, self.__lang_strings['closeEventMsgBox']['title'],
            self.__lang_strings['closeEventMsgBox']['msg'], QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  