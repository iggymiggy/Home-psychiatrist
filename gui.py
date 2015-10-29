# -*- coding: iso-8859-1 -*-

import sys
from PyQt4 import QtGui, QtCore
from shrink import Shrink
from user import User
from text import Text
import random

WIDTH = 800
HEIGHT = 100
DEBUG_MIN_WIDTH = 100
DEBUG_MIN_HEIGHT = 100
PHOTO = "photo.jpg"

class Gui(QtGui.QWidget):
    
    def __init__(self, shrink, text, user,ai,keywords, transformations, syno, output):
        super(Gui, self).__init__()
         
        self.shrink = shrink
        self.text = text
        self.user = user
        self.ai = ai
        self.keywords = keywords
        self.transformations = transformations
        self.syno = syno
        self.output = output
        self.first_bool = False
        self.debug_counter = 0
        self.patience_color = QtGui.QColor(65,105,225)
        self.shrink_color = QtGui.QColor(0,205,205)
        self.initUI()
        
    def initUI(self):
        
        patience = QtGui.QLabel('Patience')
        patience.setToolTip('You')
        conversation = QtGui.QLabel('Conversation')
        self.patienceEdit = QtGui.QLineEdit()
        self.connect(self.patienceEdit, QtCore.SIGNAL("returnPressed()"),self.answer_button_pressed)
        self.patienceEdit.setToolTip('Write your answer here')
        self.text.write_file(self.output, None, None)
        begin = self.shrink.response(None, self.keywords, self.transformations, self.syno, "")
        begin = str(begin)
        self.conversationEdit = QtGui.QTextEdit()
        self.conversationEdit.setTextColor(self.shrink_color)
        self.conversationEdit.append("Home psychiatrist: " + begin)
        self.conversationEdit.setReadOnly(True)
        self.conversationEdit.setToolTip('Conversation between Home psychiatrist and Patience')
        grid = QtGui.QGridLayout()
        grid.setSpacing(15)
        grid.addWidget(patience, 7, 0)
        grid.addWidget(self.patienceEdit, 7, 1, 1,1)
        grid.addWidget(conversation, 0, 0)
        grid.addWidget(self.conversationEdit, 0, 1, 5, 1)
        self.debug_button = QtGui.QPushButton("Debug", self)
        self.debug_button.setToolTip('Debug-mode ON/OFF')
        grid.addWidget(self.debug_button, 0,2,1,1)
        self.debugEdit = QtGui.QTextEdit()
        grid.addWidget(self.debugEdit, 0,3,2,2)
        self.debug_button.clicked.connect(self.debug_button_pressed)
        self.debugEdit.setDisabled(True)
        self.debugEdit.setReadOnly(True)
        self.debugEdit.setMinimumSize(DEBUG_MIN_WIDTH, DEBUG_MIN_HEIGHT)
        self.debugEdit.setToolTip('Answers of the Home psychiatrist is based on the following details:\n\n'+
                                  'Keyword: word or words that is or are recognised.\n'+
                                  'Useful part: rest of the sentence after the keyword.\n'+
                                  'Response: random response that matches the keyword founded in the ai.txt file.\n\n'+
                                  'The answer of the Home psychiatrist is formed on the following matter:\n'+
                                  "1) If the response has a letter '*', the answer is response plus useful part on the place where the star is.\n"+
                                  "2) Else the answer is the response.")
        self.quit_button = QtGui.QPushButton('Quit', self)
        self.quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.quit_button.resize(self.quit_button.sizeHint())
        self.quit_button.setToolTip('Quit the program')
        self.quit_button.setMaximumSize(50, 100)
        grid.addWidget(self.quit_button, 7,3,1,1)
        self.button = QtGui.QPushButton("Answer", self)
        self.button.setAutoDefault(False)
        self.button.clicked.connect(self.answer_button_pressed)
        self.button.setToolTip('Answer')
        grid.addWidget(self.button, 7,2,1,1)
        pic = QtGui.QLabel()
        pic.setPixmap(QtGui.QPixmap(PHOTO))
        pic.resize(50, 50)
        grid.addWidget(pic, 2,3,1,1)
        self.setLayout(grid) 
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setWindowTitle('Home psychiatrist')    
        self.show()
    
    def debug_button_pressed(self):
        if self.debug_counter % 2 == 1:
            self.debugEdit.setDisabled(True)
            self.debugEdit.clear()
        else:
            self.debugEdit.setDisabled(False)
            self.debugEdit.setText("Keyword: " + self.shrink.get_keyword()+ "\n\nUseful part: " + 
                                   self.shrink.get_useful_part()+
                                   "\n\nResponse: " + self.shrink.get_response_from_list())
        self.debug_counter = self.debug_counter +1
        
    def answer_button_pressed(self):
        text = self.patienceEdit.text()
        self.conversationEdit.setTextColor(self.patience_color)
        self.conversationEdit.append("Patience: " + text)
        self.conversationEdit.append("")
        text = str(text)
        text_array = self.user.read(text)
        self.text.write_file(self.output, text, self.shrink.get_response())
        
        #if it's a beginning of session
        if self.first_bool == False:
            self.first_bool = True
            self.shrink.add_name(text)
            
        if self.shrink.is_over(text) == True:
            self.patienceEdit.setReadOnly(True)
            self.patienceEdit.setDisabled(True)
            self.button.setDisabled(True)
            self.button.setAutoDefault(True)
            self.shrink.response(text_array, self.keywords, self.transformations, self.syno, text)
            self.text.write_file(self.output, None, self.shrink.get_response())
        self.shrink.response(text_array, self.keywords, self.transformations, self.syno, text)
        self.conversationEdit.setTextColor(self.shrink_color)
        self.conversationEdit.append("Home psychiatrist: "+ self.shrink.get_response())
        self.patienceEdit.clear()
        
        if self.debug_counter % 2 == 1:
            self.debugEdit.setText("Keyword: " + self.shrink.get_keyword()+ "\n\nUseful part: "+ 
                                   self.shrink.get_useful_part()+
                                   "\n\nResponse: "+ self.shrink.get_response_from_list())
  
def main():
    try:
        shrink= Shrink()
        text = Text()
        user = User()
        try:
            ai = open('ai.txt', 'r')
            keywords = text.get_keywords(ai)
        except IOError:
            print "ERROR in reading file ai.txt"
            return
        try: 
            transform_text = open('transform.txt', 'r')
            transformations = text.get_transformations(transform_text)
        except IOError:
            print "ERROR reading file transform.txt"
            return
        try:
            synonymes = open('syno.txt', 'r')
            syno = text.get_synonymes(synonymes)
        except IOError:
            print "ERROR reading file syno.txt"
            return
        synonymes = open('syno.txt', 'r')
        syno = text.get_synonymes(synonymes)
        ai.close()
        transform_text.close()
        synonymes.close()
        app = QtGui.QApplication(sys.argv)
        if len(sys.argv) > 2:
            sys.exit("Two many arguments.\n\nFirst argument is shrink.py\n\nSecond argument is optional file name if "+
                     "you want to save your conversation to a text file. For example file.txt\n")  
        #saving conversation to file
        if len(sys.argv) == 2:  
            output = open(sys.argv[1], 'a')
        else:
            output = None
        ex = Gui(shrink, text, user,ai,keywords, transformations, syno, output)
        sys.exit(app.exec_())
        
    except not SystemExit:
        print "Unexpected error:", sys.exc_info()[0]
        
if __name__ == '__main__':
    main()
