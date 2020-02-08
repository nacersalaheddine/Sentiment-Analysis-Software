import sys

from PyQt5.QtWidgets import (QApplication,QWidget,QComboBox,QPushButton,QHBoxLayout,QLineEdit,QFormLayout, 
QVBoxLayout,QToolTip,QAction,QMenu,QRadioButton,QLabel,QTextEdit,QStackedWidget,QGridLayout,qApp,QMessageBox,QMainWindow,QDesktopWidget,QListWidget)
from PyQt5.QtGui import QIcon,QFont

#learning models
from svm.svm_model import SvmModel
from textblobclassifier.textblb import TextBlbClsfr


class QTMainWindow(QMainWindow):
    __models_set = ['SVM (Support Vector Machine)','Textblob->sentiments->NaiveBayesAnalyzer','Textblob->sentiments->PatternAnalyzer']
    __lang_strings = None
    __svmModel = None
    __textBlbClfr = None
    __current_selected_model = None
    def __init__(self,lang_strings):
        super().__init__()
        self.__lang_strings = lang_strings
        self.__current_selected_model = self.__models_set[0]
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
        QToolTip.setFont(QFont('SansSerif', 15))
        self.setFont(QFont('cairo', 12))
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
        btn = self.createButton(self.__lang_strings['buttons']['analyseButton']['name'],
        50,50,self.__lang_strings['buttons']['analyseButton']['name'])
        #Quit Button
        qbtn = self.createButton(self.__lang_strings['buttons']['quitButton']['name']
        ,100,100,self.__lang_strings['buttons']['quitButton']['toolTip'])
        
        #Quit Button
        loadModelBtn = self.createButton(self.__lang_strings['buttons']['loadModelBtn']['name']
        ,100,100,self.__lang_strings['buttons']['loadModelBtn']['toolTip'])
        
        #Setting events
        qbtn.clicked.connect(QApplication.instance().quit)
        btn.clicked.connect(self.analizeButtonClicked)
        loadModelBtn.clicked.connect(self.loadModelButtonClicked)

        self.central_widget = QWidget()               # define central widget
        self.setCentralWidget(self.central_widget)    # set QMainWindow.centralWidget

        combo = QComboBox(self)
        combo.addItem(self.__models_set[0])
        combo.addItem(self.__models_set[1])
        combo.addItem(self.__models_set[2])
        '''
        combo.addItem("Desision Tree")
        combo.addItem("Tokenizer")
        combo.addItem("RNN (Recurrent Neural Network)")
        combo.addItem("CNN (Convolutional Neural Network)")
        '''         
        self.resultEdit = QTextEdit()
        self.inputTextEdit = QTextEdit()
        review = QLabel(self.__lang_strings['textLabels']['review'])
        resultLbl = QLabel(self.__lang_strings['textLabels']['result'])
        #Creating layout
        hboxCombo = QHBoxLayout()
        hboxCombo.addStretch(1)
        hboxCombo.addWidget(combo)
        hboxCombo.addWidget(loadModelBtn)
        combo.activated[str].connect(self.onActivated) 
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(qbtn)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hboxCombo)
        vbox.addWidget(review)
        vbox.addWidget(self.inputTextEdit)
        vbox.addWidget(resultLbl)
        vbox.addWidget(self.resultEdit)
        #vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.centralWidget().setLayout(vbox) 
        
        
        self.setGeometry(300, 300, self.__lang_strings['mainWindow']['width'],
        self.__lang_strings['mainWindow']['height'])
        self.show()
        '''
        
        '''
    def onActivated(self, text):   
        #self.lbl.setText(text)
        #self.lbl.adjustSize() 
        self.__current_selected_model = text
        self.statusBar().showMessage(text + ' was selected')        
        
    def analizeButtonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        text = self.inputTextEdit.toPlainText()
        if(len(text) > 5):
            if(self.__current_selected_model == self.__models_set[0]):
                if(self.__svmModel):
                    res = self.__svmModel.analyse_sentiment(text)
                    print("==>",res)
                    self.resultEdit.setText(str(res))
                else:
                    print("Load a Model First")
            elif(self.__current_selected_model == self.__models_set[1]):
                if(self.__textBlbClfr):
                    blob = self.__textBlbClfr.blob_sentiment_analyzer(text,"PatternAnalyzer")
                    print("==>",blob)
                    self.resultEdit.setText(str(blob.sentiment))
                        
            elif(self.__current_selected_model == self.__models_set[2]):
                if(self.__textBlbClfr):
                    blob = self.__textBlbClfr.blob_sentiment_analyzer(text,"NaiveBayesAnalyzer")
                    print("==>",blob)
                    self.resultEdit.setText(str(blob.sentiment))
            else:
                print("error")
        else:
            print("provide text first >5")
        
    def loadModelButtonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        if(self.__current_selected_model == self.__models_set[0]):
            print("Loading SVM")
            if(not(self.__svmModel)):
                self.__svmModel  = SvmModel("svm/train_data1/train.csv","svm/test_data1/test.csv","svm/pkl_dump1/vectorizer.sav","svm/pkl_dump1/classifier.sav")
            
            print("SVM Loaded")
        elif(self.__current_selected_model == self.__models_set[1]):
            print("Loading TextBlob NaiveBayesAnalyzer")
            if(not(self.__textBlbClfr)):
                self.__textBlbClfr = TextBlbClsfr()
                
                
        elif(self.__current_selected_model == self.__models_set[2]):
            print("Loading TextBlob PatternAnalyzer")
            if(not(self.__textBlbClfr)):
                self.__textBlbClfr = TextBlbClsfr()
            
            
        else:
            print("ERROR")
        
        
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