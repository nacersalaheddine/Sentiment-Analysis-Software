#!/usr/bin/python3 
#python version 3.7.0
# -*- coding: utf-8 -*-
import sys,json
from PyQt5.QtWidgets import QApplication, QWidget
from main_window import QTMainWindow


window_title = 'Sentiment Analysis'
strings_lang = 'assets/strings_english.json'
graphic_res = 'assets/resources.json'

#docs site
#https://doc.qt.io/qt-5/qtextedit.html
if __name__ == '__main__':
    
    with open(strings_lang) as f:
        strings_lang_json = json.load(f)
    # the result is a JSON string:
    #print(strings_lang_json)
    
    app = QApplication(sys.argv)
    ex = QTMainWindow(strings_lang_json)
    sys.exit(app.exec_())
   