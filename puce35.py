import PyOrigin
import sys, os, codecs, math
#Stores the path of the actual OriginLab file being used.
origin_path = PyOrigin.LT_get_str('system.PATH.ORIGIN')
#PyQt4 is stored locally and then loaded into the current OriginLab session. This eliminates the need to have PyQt installed to the OriginLab python.
py_ext_path = origin_path+"/Python35/Lib/site-packages"
if py_ext_path not in sys.path:
    sys.path.append(py_ext_path)
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat

vernum = "0.1.0"

class mainwin(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(mainwin, self).__init__()
        self.initUI()
        
        
    def initUI(self):
        self.mainwinwidget = mainwidget()
        self.setCentralWidget(self.mainwinwidget)
        
        exitAction = QtWidgets.QAction(QtGui.QIcon(origin_path+'/images/exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        
        openFile = QtWidgets.QAction(QtGui.QIcon(origin_path+'/images/openfile.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new Files')
        openFile.triggered.connect(self.showDialog)
        
        self.statusBar().showMessage('Ready')
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)
        
        self.resize(1000, 500)
        self.center()
        global vernum
        self.setWindowTitle('PUCE35 '+str(vernum))  
        self.setWindowIcon(QtGui.QIcon(origin_path+'/images/ico.png'))   
        self.show()
        
    def showDialog(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open files', origin_path)
        self.mainwinwidget.mainfilelist._populate(files)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        
        reply = QtWidgets.QMessageBox.question(self, ' ',
            "Are you sure you want to quit?", QtWidgets.QMessageBox.Yes | 
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    

class mainwidget(QtWidgets.QWidget):
    def __init__(self):
        super(mainwidget, self).__init__()
        self.initUI()
    def initUI(self):
        ''' Define all subwidgets which will be used '''
        self.mainfilelist = filelist()
        self.mainfilelist.setFixedWidth(607)
        self.textdisplay = LineNumberedText()
        self.textdisplay.setReadOnly(True)
        self.runOriginButton = QtWidgets.QPushButton("Export to Origin")
        self.runButton = QtWidgets.QPushButton("Export to file")
        self.loadButton = QtWidgets.QPushButton("Load Data")
        self.openButton = QtWidgets.QPushButton("Open files")
        self.applyButton = QtWidgets.QPushButton("Apply to all")
        label_data = QtWidgets.QLabel("Raw Data")
        label_data.setAlignment(QtCore.Qt.AlignLeft)
        label_files = QtWidgets.QLabel("Opened Files")
        label_files.setAlignment(QtCore.Qt.AlignLeft)
        label_lines = QtWidgets.QLabel("Header Lines")
        label_area = QtWidgets.QLabel("Cell Area (cm<sup>2</sup>)")
        label_meas = QtWidgets.QLabel("Measurement Type")
        label_resist = QtWidgets.QLabel("Resistance Output")
        label_cols = QtWidgets.QLabel("Columns")
        label_v1 = QtWidgets.QLabel("V1")
        label_v1.setFixedWidth(300)
        label_v2 = QtWidgets.QLabel("V2")
        label_v2.setFixedWidth(300)
        label_i1 = QtWidgets.QLabel("I1")
        label_i1.setFixedWidth(300)
        label_i2 = QtWidgets.QLabel("I2")
        label_i2.setFixedWidth(300)
        self.line_lines = QtWidgets.QLineEdit()
        self.line_lines.setFixedWidth(300)
        self.line_area = QtWidgets.QLineEdit()
        self.line_area.setFixedWidth(300)
        self.line_v1 = QtWidgets.QLineEdit()
        self.line_v1.setFixedWidth(300)
        self.line_v2 = QtWidgets.QLineEdit()
        self.line_v2.setFixedWidth(300)
        self.line_v2.setEnabled(False)
        self.line_i1 = QtWidgets.QLineEdit()
        self.line_i1.setFixedWidth(300)
        self.line_i2 = QtWidgets.QLineEdit()
        self.line_i2.setFixedWidth(300)
        self.line_i2.setEnabled(False)
        self.combo_meas = QtWidgets.QComboBox()
        self.combo_meas.setFixedWidth(300)
        self.combo_meas.addItem("Single I/V")
        self.combo_meas.addItem("Double I/V")
        self.combo_resist = QtWidgets.QComboBox()
        self.combo_resist.setFixedWidth(300)
        self.combo_resist.addItem("None")
        self.combo_resist.addItem("Text only")
        self.combo_resist.addItem("Text + Tangent")
        self.check_delimiter = QtWidgets.QCheckBox("Other Delimiter than Whitespace")
        self.check_delimiter.setFixedWidth(300)
        self.line_delimiter = QtWidgets.QLineEdit()
        self.line_delimiter.setFixedWidth(300)
        self.line_delimiter.setEnabled(False)
        self.check_valsur = QtWidgets.QCheckBox("Values Surrounded")
        self.check_valsur.setFixedWidth(300)
        self.line_valsur = QtWidgets.QLineEdit()
        self.line_valsur.setFixedWidth(300)
        self.line_valsur.setEnabled(False)
        
        ''' Create main HBox which contains two vboxes as columns left and right'''
        hbox_main = QtWidgets.QHBoxLayout()
        
        ''' Create two columns '''
        vbox1 = QtWidgets.QVBoxLayout()
        vbox2 = QtWidgets.QVBoxLayout()
        
        ''' Filling right column '''
        vbox2.addWidget(label_data)
        vbox2.addWidget(self.textdisplay)
        hbox2_1 = QtWidgets.QHBoxLayout()
        hbox2_1.addStretch(1)
        hbox2_1.addWidget(self.runButton)
        hbox2_1.addWidget(self.runOriginButton)
        vbox2.addLayout(hbox2_1)
        
        ''' Filling left column '''
        hbox1_0 = QtWidgets.QHBoxLayout()
        hbox1_0.addWidget(self.openButton)
        hbox1_0.addStretch(1)
        vbox1.addLayout(hbox1_0)
        vbox1.addWidget(label_files)
        vbox1.addWidget(self.mainfilelist)
        hbox1_1 = QtWidgets.QHBoxLayout()
        hbox1_1.addWidget(self.loadButton)
        hbox1_1.addWidget(self.applyButton)
        hbox1_1.addStretch(1)
        vbox1.addLayout(hbox1_1)
        hbox1_2 = QtWidgets.QHBoxLayout()
        hbox1_2.addWidget(label_lines)
        hbox1_2.addStretch(1)
        hbox1_2.addWidget(self.line_lines)
        vbox1.addLayout(hbox1_2)
        hbox1_10 = QtWidgets.QHBoxLayout()
        hbox1_10.addWidget(self.check_delimiter)
        hbox1_10.addStretch(1)
        hbox1_10.addWidget(self.line_delimiter)
        vbox1.addLayout(hbox1_10)
        hbox1_11 = QtWidgets.QHBoxLayout()
        hbox1_11.addWidget(self.check_valsur)
        hbox1_11.addStretch(1)
        hbox1_11.addWidget(self.line_valsur)
        vbox1.addLayout(hbox1_11)
        hbox1_3 = QtWidgets.QHBoxLayout()
        hbox1_3.addWidget(label_area)
        hbox1_3.addStretch(1)
        hbox1_3.addWidget(self.line_area)
        vbox1.addLayout(hbox1_3)
        hbox1_4 = QtWidgets.QHBoxLayout()
        hbox1_4.addWidget(label_meas)
        hbox1_4.addWidget(self.combo_meas)
        vbox1.addLayout(hbox1_4)
        hbox1_5 = QtWidgets.QHBoxLayout()
        hbox1_5.addWidget(label_resist)
        hbox1_5.addWidget(self.combo_resist)
        vbox1.addLayout(hbox1_5)
        vbox1.addWidget(label_cols)
        hbox1_6 = QtWidgets.QHBoxLayout()
        hbox1_6.addWidget(label_v1)
        hbox1_6.addStretch(1)
        hbox1_6.addWidget(label_i1)
        vbox1.addLayout(hbox1_6)
        hbox1_7 = QtWidgets.QHBoxLayout()
        hbox1_7.addWidget(self.line_v1)
        hbox1_7.addStretch(1)
        hbox1_7.addWidget(self.line_i1)
        vbox1.addLayout(hbox1_7)
        hbox1_8 = QtWidgets.QHBoxLayout()
        hbox1_8.addWidget(label_v2)
        hbox1_8.addStretch(1)
        hbox1_8.addWidget(label_i2)
        vbox1.addLayout(hbox1_8)
        hbox1_9 = QtWidgets.QHBoxLayout()
        hbox1_9.addWidget(self.line_v2)
        hbox1_9.addStretch(1)
        hbox1_9.addWidget(self.line_i2)
        vbox1.addLayout(hbox1_9)
        
        ''' Add left and right columns to main hbox '''
        v1_widget = QtWidgets.QWidget()
        v1_widget.setLayout(vbox1)
        v1_widget.setFixedWidth(625)
        v2_widget = QtWidgets.QWidget()
        v2_widget.setLayout(vbox2)
        hbox_main.addWidget(v1_widget)
        hbox_main.addWidget(v2_widget)
        
        ''' Set layout of main widget '''
        self.setLayout(hbox_main)
            
        ''' Triggers '''
        self.loadButton.clicked.connect(self.loadFileCont)
        self.applyButton.clicked.connect(self.applytoall)
        self.line_area.textEdited.connect(self.sync_line_area)
        self.line_lines.textEdited.connect(self.sync_line_lines)
        self.combo_meas.currentIndexChanged.connect(self.sync_combo_meas)
        self.combo_resist.currentIndexChanged.connect(self.sync_combo_resist)
        self.line_v1.textEdited.connect(self.sync_line_v1)
        self.line_v2.textEdited.connect(self.sync_line_v2)
        self.line_i1.textEdited.connect(self.sync_line_i1)
        self.line_i2.textEdited.connect(self.sync_line_i2)
        self.openButton.clicked.connect(self.showDialog)
        self.runOriginButton.clicked.connect(self.exportToOrigin)
        self.runButton.clicked.connect(self.exportToFile)
        self.check_delimiter.stateChanged.connect(self.sync_check_delimiter)
        self.check_valsur.stateChanged.connect(self.sync_check_valsur)
        self.line_delimiter.textEdited.connect(self.sync_line_delimiter)
        self.line_valsur.textEdited.connect(self.sync_line_valsur)

    def loadFileCont(self):
        if sel_filePath:
            with open(sel_filePath,"rt") as file:
                self.textdisplay.setPlainText(file.read())
    def applytoall(self):
        try:
            for i in range(self.mainfilelist.count()):
                self.mainfilelist.item(i).headerLines = int(self.line_lines.text())
                self.mainfilelist.item(i).cellarea = float(self.line_area.text())
                self.mainfilelist.item(i).meastype = self.combo_meas.currentIndex()
                self.mainfilelist.item(i).resisttype = self.combo_resist.currentIndex()
                self.mainfilelist.item(i).colv1 = int(self.line_v1.text())
                self.mainfilelist.item(i).coli1 = int(self.line_i1.text())
                self.mainfilelist.item(i).colv2 = int(self.line_v2.text())
                self.mainfilelist.item(i).coli2 = int(self.line_i2.text())
                self.mainfilelist.item(i).delimiter_state = self.check_delimiter.checkState()
                self.mainfilelist.item(i).delimiter_val = str(self.line_delimiter.text())
                self.mainfilelist.item(i).valsur_state =  self.check_valsur.checkState()
                self.mainfilelist.item(i).valsur_chars = str(self.line_valsur.text())
            self.mainfilelist.setCurrentRow(0)
        except:
            altertbox = QtWidgets.QMessageBox.warning(self, '','Error occured, check if inputted values are valid.')
    def sync_line_area(self):
        if self.mainfilelist.currentItem():
            try:
                self.mainfilelist.currentItem().cellarea = float(self.line_area.text())
            except:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Input must be a float')
    def sync_line_lines(self):
        if self.mainfilelist.currentItem():
            try:
                self.mainfilelist.currentItem().headerLines = int(self.line_lines.text())
            except:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Input must be an integer')
    def sync_combo_meas(self):
        if self.mainfilelist.currentItem():
            self.mainfilelist.currentItem().meastype = self.combo_meas.currentIndex()
        if self.combo_meas.currentIndex() == 1:
            self.line_v2.setEnabled(True)
            self.line_i2.setEnabled(True)
        elif self.combo_meas.currentIndex() == 0:
            self.line_v2.setEnabled(False)
            self.line_i2.setEnabled(False)
    def sync_combo_resist(self):
        if self.mainfilelist.currentItem():
            self.mainfilelist.currentItem().resisttype = self.combo_resist.currentIndex()
    def sync_line_v1(self):
        if self.mainfilelist.currentItem():
            try:
                self.mainfilelist.currentItem().colv1 = int(self.line_v1.text())
            except:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Input must be an integer')
    def sync_line_v2(self):
        if self.mainfilelist.currentItem():
            try:
                self.mainfilelist.currentItem().colv2 = int(self.line_v2.text())
            except:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Input must be an integer')
    def sync_line_i1(self):
        if self.mainfilelist.currentItem():
            try:
                self.mainfilelist.currentItem().coli1 = int(self.line_i1.text())
            except:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Input must be an integer')
    def sync_line_i2(self):
        if self.mainfilelist.currentItem():
            try:
                self.mainfilelist.currentItem().coli2 = int(self.line_i2.text())
            except:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Input must be an integer')
    def sync_check_delimiter(self):
        if self.mainfilelist.currentItem():
            self.mainfilelist.currentItem().delimiter_state = self.check_delimiter.checkState()
        if self.check_delimiter.checkState() == 2:
            self.line_delimiter.setEnabled(True)
        elif self.check_delimiter.checkState() == 0:
            self.line_delimiter.setEnabled(False)
    def sync_check_valsur(self):
        if self.mainfilelist.currentItem():
            self.mainfilelist.currentItem().valsur_state = self.check_valsur.checkState()
        if self.check_valsur.checkState() == 2:
            self.line_valsur.setEnabled(True)
        elif self.check_valsur.checkState() == 0:
            self.line_valsur.setEnabled(False)
    def sync_line_delimiter(self):
        if self.mainfilelist.currentItem():
            self.mainfilelist.currentItem().delimiter_val = str(self.line_delimiter.text())
    def sync_line_valsur(self):
        if self.mainfilelist.currentItem():
            if len(str(self.line_valsur.text())) <= 2:
                self.mainfilelist.currentItem().valsur_chars = str(self.line_valsur.text())
            else:
                altertbox = QtWidgets.QMessageBox.warning(self, '','Please input only two characters.')
    def exportToFile(self):
        global vernum
        rawsavelocation = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', origin_path+'/output', 'Text file (*.txt)')
        savelocation = rawsavelocation[0]
        if savelocation:
            with open(savelocation,'w',encoding='utf-8') as outPutFileHeaderLines:
                outPutFileHeaderLines.write('Evaluated using PUCE35 Version: '+str(vernum)+'\n'+'Evaluation Parameters'+'\n'+'File'+'\t'+'Header lines'+'\t'+'Other delimiter checked'+'\t'+'Other delimiter value'+'\t'+'Values surrounded checked'+'\t'+'Values surrounded value'+'\t'+'Measurement type'+'\t'+'Resistance output'+'\t'+'V1'+'\t'+'I1'+'\t'+'V2'+'\t'+'I2'+'\n')
                outPutFileHeaderLines.close()
            for i in range(self.mainfilelist.count()):
                writeOutputFileHeaders(savelocation,self.mainfilelist.item(i))
            with open(savelocation,'a',encoding='utf-8') as outPutFile:
                for i in range(self.mainfilelist.count()):
                    curItem = self.mainfilelist.item(i)
                    evaluatedFileResults = evaluateEternalFile(0,curItem.filePath,curItem.headerLines,curItem.delimiter_state,curItem.delimiter_val,curItem.valsur_state,curItem.valsur_chars,curItem.cellarea,curItem.meastype,curItem.resisttype,curItem.colv1,curItem.coli1,curItem.colv2,curItem.coli2,curItem)
                    for idx,result in enumerate(evaluatedFileResults):
                        if not curItem.resisttype == 0:
                            outPutFile.write(str(os.path.basename(self.mainfilelist.item(i).filePath))+'\t'+str(result[4])+'\t'+str(result[-1])+'\t'+str(idx+1)+'\t'+str(result[1])+'\t'+str(result[0])+'\t'+str(result[2])+'\t'+str(result[3])+'\t'+str(result[5])+'\t'+str(result[6]/1000)+'\n')
                        else:
                            outPutFile.write(str(os.path.basename(self.mainfilelist.item(i).filePath))+'\t'+str(result[4])+'\t'+str(result[-1])+'\t'+str(idx+1)+'\t'+str(result[1])+'\t'+str(result[0])+'\t'+str(result[2])+'\t'+str(result[3])+'\n')
            outPutFile.close()
        else:
            pass
    def showDialog(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open files', origin_path)
        self.mainfilelist._populate(files)
    def exportToOrigin(self):
        global vernum
        if not os.path.exists(os.path.join(os.path.dirname(origin_path),'log\\')):
            os.makedirs(os.path.join(os.path.dirname(origin_path),'log\\'))
        for i in range(self.mainfilelist.count()):
            curItem = self.mainfilelist.item(i)
            savelocation = os.path.join(os.path.dirname(origin_path), 'log\\'+str(os.path.basename(curItem.filePath).split('.')[0])+'.txt') 
            with open(savelocation,'w',encoding='utf-8') as outPutFileHeaderLines:
                outPutFileHeaderLines.write('Evaluated using PUCE35 Version: '+str(vernum)+'\n'+'Evaluation Parameters'+'\n'+'File'+'\t'+'Header lines'+'\t'+'Other delimiter checked'+'\t'+'Other delimiter value'+'\t'+'Values surrounded checked'+'\t'+'Values surrounded value'+'\t'+'Measurement type'+'\t'+'Resistance output'+'\t'+'V1'+'\t'+'I1'+'\t'+'V2'+'\t'+'I2'+'\n')
                outPutFileHeaderLines.close()
            writeOutputFileHeaders(savelocation,curItem)
            evaluatedFileResults = evaluateEternalFile(1,curItem.filePath,curItem.headerLines,curItem.delimiter_state,curItem.delimiter_val,curItem.valsur_state,curItem.valsur_chars,curItem.cellarea,curItem.meastype,curItem.resisttype,curItem.colv1,curItem.coli1,curItem.colv2,curItem.coli2,curItem)
            if PyOrigin.LT_execute("pe_cd /main_folder/cell_char_data/") == 0: #switch to cell_char_data folder in origin if it exists, if not make it (this if query will trigger an error in origin, unavoidable)
                PyOrigin.LT_execute("pe_cd /main_folder/cell_char_data/")
            else:
                PyOrigin.LT_execute("pe_mkdir /main_folder/cell_char_data/")
                PyOrigin.LT_execute("pe_cd /main_folder/cell_char_data/")
            if PyOrigin.LT_execute("win -a cellvals") == 0: #check if cellvals worksheet exists, if not make it and make it active
                PyOrigin.LT_execute("win -a cellvals")
                cellValsSheet = PyOrigin.WorksheetPages('cellvals').Layers(0)
            else:
                PyOrigin.LT_execute('newbook name:="cellvals" option:=lsname')
                PyOrigin.LT_execute("win -a cellvals")
                PyOrigin.LT_execute('wks.name$ = "Cell Values"') #fill in the sheet name and fill all the column data
                PyOrigin.LT_execute('wks.ncols = 9')
                PyOrigin.LT_execute("wks.col1.lname$ = File")
                PyOrigin.LT_execute("wks.col2.lname$ = Cell area")
                PyOrigin.LT_execute("wks.col2.unit$ = cm\+(2)")
                PyOrigin.LT_execute("wks.col3.lname$ = Scan direction")
                PyOrigin.LT_execute("wks.col4.lname$ = Measurement stage")
                PyOrigin.LT_execute("wks.col6.lname$ = Voltage")
                PyOrigin.LT_execute("wks.col6.unit$ = V")
                PyOrigin.LT_execute("wks.col5.lname$ = Current density")
                PyOrigin.LT_execute("wks.col5.unit$ = mA/cm\+(2)")
                PyOrigin.LT_execute("wks.col7.lname$ = Fill factor")
                PyOrigin.LT_execute("wks.col7.unit$ = %")
                PyOrigin.LT_execute("wks.col8.lname$ = PCE")
                PyOrigin.LT_execute("wks.col8.unit$ = %")
                PyOrigin.LT_execute("wks.col9.lname$ = Version number")
                PyOrigin.LT_execute("wks.col9.comment$ = Version of PUCE used to evaluate data")
                cellValsSheet = PyOrigin.WorksheetPages('cellvals').Layers(0)
                cellValsSheet.SetData([str(vernum)],-1,8)
            for idx,result in enumerate(evaluatedFileResults): #add evaluated file data to the cellvals sheet
                cellValsSheet.SetData([str(os.path.basename(self.mainfilelist.item(i).filePath))+'_'+str(idx+1)],-1,0)
                cellValsSheet.SetData([str(result[4])],-1,1)
                cellValsSheet.SetData([str(result[-1])],-1,2)
                cellValsSheet.SetData([str(idx+1)],-1,3)
                cellValsSheet.SetData([str(result[0])],-1,4)
                cellValsSheet.SetData([str(result[1])],-1,5)
                cellValsSheet.SetData([str(result[2])],-1,6)
                cellValsSheet.SetData([str(result[3])],-1,7)
                CurSheet = PyOrigin.WorksheetPages('cellvals').Layers(0)
                if PyOrigin.LT_execute("win -a cellcharacteristics") == 0:
                    char_graph = PyOrigin.Pages("cellcharacteristics")
                else:
                    char_graph = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, 'cellcharacteristics', 'char_cells', 1)
                gp = PyOrigin.Pages(str(char_graph)) # Get graph page by name
                gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
                gp.LT_execute("layer2.x.opposite = 1;layer2.y.opposite = 1;")
                gp.LT_execute("layer3.x.opposite = 1;layer3.y.opposite = 1;")
                gp.LT_execute("layer4.x.opposite = 1;layer4.y.opposite = 1;")
                gl = gp.Layers(0) 
                rng = PyOrigin.NewDataRange()  # Create data range.
                rng.Add('X', CurSheet, 0, 0, -1, 0) # Add worksheet's 1st col as X.
                rng.Add('Y', CurSheet, 0, 4, -1, 4) # Add worksheet's 2nd col as Y.
                dp = gl.AddPlot(rng, 201)
                rng.Destroy()
                gl = gp.Layers(1) 
                rng = PyOrigin.NewDataRange()  # Create data range.
                rng.Add('X', CurSheet, 0, 0, -1, 0) # Add worksheet's 1st col as X.
                rng.Add('Y', CurSheet, 0, 5, -1, 5) # Add worksheet's 2nd col as Y.
                dp = gl.AddPlot(rng, 201)
                rng.Destroy()
                gl = gp.Layers(2) 
                rng = PyOrigin.NewDataRange()  # Create data range.
                rng.Add('X', CurSheet, 0, 0, -1, 0) # Add worksheet's 1st col as X.
                rng.Add('Y', CurSheet, 0, 6, -1, 6) # Add worksheet's 2nd col as Y.
                dp = gl.AddPlot(rng, 201)
                rng.Destroy()
                gl = gp.Layers(3) 
                rng = PyOrigin.NewDataRange()  # Create data range.
                rng.Add('X', CurSheet, 0, 0, -1, 0) # Add worksheet's 1st col as X.
                rng.Add('Y', CurSheet, 0, 7, -1, 7) # Add worksheet's 2nd col as Y.
                dp = gl.AddPlot(rng, 201)
                rng.Destroy()
class filelist(QtWidgets.QListWidget):
    def __init__(self):
        super(filelist, self).__init__()
        self.currentItemChanged.connect(self.list_change)
    def _populate(self, rawfiles):
        self.clear()
        files = rawfiles[0]
        for file in files:
            cellarea = findCellArea(file)
            item = fileitem(file, cellarea)
            self.addItem(item)
            item.setText(os.path.basename(file))
        self.setCurrentRow(0)
    def list_change(self):
        if self.currentItem():
            global sel_filePath
            sel_filePath = self.currentItem().filePath
            win.mainwinwidget.line_lines.setText(str(self.currentItem().headerLines))
            win.mainwinwidget.line_area.setText(str(self.currentItem().cellarea))
            win.mainwinwidget.combo_meas.setCurrentIndex(self.currentItem().meastype)
            win.mainwinwidget.combo_resist.setCurrentIndex(self.currentItem().resisttype)
            win.mainwinwidget.line_v1.setText(str(self.currentItem().colv1))
            win.mainwinwidget.line_i1.setText(str(self.currentItem().coli1))
            win.mainwinwidget.line_v2.setText(str(self.currentItem().colv2))
            win.mainwinwidget.line_i2.setText(str(self.currentItem().coli2))
            win.mainwinwidget.check_delimiter.setChecked(self.currentItem().delimiter_state)
            win.mainwinwidget.check_valsur.setChecked(self.currentItem().valsur_state)
            win.mainwinwidget.line_delimiter.setText(str(self.currentItem().delimiter_val))
            win.mainwinwidget.line_valsur.setText(str(self.currentItem().valsur_chars))

class fileitem(QtWidgets.QListWidgetItem):
    def __init__(self, filePath, cellarea):
        super(fileitem, self).__init__()
        self.cellarea = cellarea
        self.headerLines = 1
        self.colv1 = 2
        self.coli1 = 3
        self.colv2 = 0
        self.coli2 = 0
        self.meastype = 0
        self.resisttype = 0
        self.filePath = filePath
        self.delimiter_state = 0
        self.delimiter_val = ","
        self.valsur_state = 0
        self.valsur_chars = '""'
class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class LineNumberedText(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
        
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
def evaluateEternalFile(originOrFile,filePath, headerLines, otherDelimChecked, otherDelimValue, valSurChecked, valSurChars, cellArea, measType, resistType, colV1, colI1, colV2, colI2,curItem):
    '''Takes arguments of how to evaluate the given file and returns the results of the scans found in the form of a list containing jsc,voc,fillFactor,efficiency,cellArea,scan direction'''
    rawFileValues = []  #rawFileValues should contain list of lists in this fashion [[voltageLine1,currentLine1],[voltageLine2,currentLine2],...]
    with open(filePath,'r') as inputFile:
        for lineNumber, line in enumerate(inputFile):
            if lineNumber > (int(headerLines)-1):
                if otherDelimChecked == 0:
                    splitLineContent = line.split()
                elif otherDelimChecked == 2:
                    splitLineContent = line.split(str(otherDelimValue))
                if valSurChecked == 2:
                    for i,content in enumerate(splitLineContent):
                        if (content[0] == valSurChars[0]) and (content[-1] == valSurChars[-1]):
                            splitLineContent[i] = splitLineContent[i][1:-1]
                rawFileValues.append([splitLineContent[int(colV1)-1],splitLineContent[int(colI1)-1]])
        if measType == 1:
            with open(filePath,'r') as inputFile:
                for lineNumber, line in enumerate(inputFile):
                    if lineNumber > (int(headerLines)-1):
                        if otherDelimChecked == 0:
                            splitLineContent = line.split()
                        elif otherDelimChecked == 2:
                            splitLineContent = line.split(str(otherDelimValue))
                        if valSurChecked == 2:
                            for i,content in enumerate(splitLineContent):
                                if (content[0] == valSurChars[0]) and (content[-1] == valSurChars[-1]):
                                    splitLineContent[i] = splitLineContent[i][1:-1]
                        rawFileValues.append([splitLineContent[int(colV2)-1],splitLineContent[int(colI2)-1]])
    temporaryVoltages = []
    temporaryCurrents = []
    scanResults = []
    measurementStage = 1
    skipOne = False #skipOne is used so that if you have a file with two reverse measurements or two forward measurement after another, it won'T get hung up at the jumping point
    for idx, volCurPair in enumerate(rawFileValues): #finds segments of scans inside file and then sends each "cut" of the files to the getScanResults
        voltage = float(volCurPair[0].replace(',','.'))
        current = float(volCurPair[1].replace(',','.'))
        nextVoltage = None
        nextCurrent = None
        perviousVoltage = None
        previousCurrent = None
        temporaryVoltages.append(float(voltage))
        temporaryCurrents.append(float(current))
        if skipOne == False:
            if idx > 0:
                perviousVoltage = float(rawFileValues[idx-1][0].replace(',','.'))
                previousCurrent = float(rawFileValues[idx-1][1].replace(',','.'))
            if idx < (len(rawFileValues)-1):
                nextVoltage = float(rawFileValues[idx+1][0].replace(',','.'))
                nextCurrent = float(rawFileValues[idx+1][1].replace(',','.'))
            elif idx == (len(rawFileValues)-1):
                if (temporaryVoltages[0] > temporaryVoltages[len(temporaryVoltages)-1] and temporaryCurrents[0] > temporaryCurrents[len(temporaryCurrents)-1]) or (temporaryVoltages[0] < temporaryVoltages[len(temporaryVoltages)-1] and temporaryCurrents[0] < temporaryCurrents[len(temporaryCurrents)-1]): #checks if the file was recorded using reversed polarity of the cell, if it was, fix it by flipping the sign of the current
                    temporaryCurrents = [-temporaryCurrent for temporaryCurrent in temporaryCurrents]
                scanResult = getScanResults(temporaryVoltages,temporaryCurrents,cellArea,curItem)
                if (voltage > perviousVoltage):
                    scanResult.append("forward")
                elif (voltage < perviousVoltage):
                    scanResult.append("reverse")
                scanResults.append(scanResult)
                if originOrFile == 1:
                    createIVWorkbook(temporaryVoltages,temporaryCurrents,curItem,measurementStage,scanResult)
                measurementStage += 1
                temporaryVoltages = []
                temporaryCurrents = []
            if nextVoltage and perviousVoltage:
                if ((voltage > perviousVoltage) and (voltage > nextVoltage)) or ((voltage < perviousVoltage) and (voltage < nextVoltage)):
                    skipOne = True
                    if (temporaryVoltages[0] > temporaryVoltages[len(temporaryVoltages)-1] and temporaryCurrents[0] > temporaryCurrents[len(temporaryCurrents)-1]) or (temporaryVoltages[0] < temporaryVoltages[len(temporaryVoltages)-1] and temporaryCurrents[0] < temporaryCurrents[len(temporaryCurrents)-1]): #checks if the file was recorded using reversed polarity of the cell, if it was, fix it by flipping the sign of the current
                        temporaryCurrents = [-temporaryCurrent for temporaryCurrent in temporaryCurrents]
                    scanResult = getScanResults(temporaryVoltages,temporaryCurrents,cellArea,curItem)
                    if (voltage > perviousVoltage):
                        scanResult.append("forward")
                    elif (voltage < perviousVoltage):
                        scanResult.append("reverse")
                    scanResults.append(scanResult)
                    if originOrFile == 1:
                        createIVWorkbook(temporaryVoltages,temporaryCurrents,curItem,measurementStage,scanResult)
                    measurementStage += 1
                    temporaryVoltages = []
                    temporaryCurrents = []
        elif skipOne == True:
            skipOne = False
    return(scanResults)
def getScanResults(voltages,currents,cellArea,curItem):
    '''Takes voltages,currents and cellArea as arguments and returns a list of scan results containing jsc,voc,fillFactor,efficiency,cellArea'''
    powers = [voltage*current for voltage,current in zip(voltages,currents)]
    for idx, voltage in enumerate(voltages):#finds the crossover point of the voltage with zero and adds some values into variables with which linear regression will be done in order to find a precise value for Isc
        if idx > 0 and ((voltage < 0 and voltages[idx-1] > 0) or (voltage > 0 and voltages[idx-1] < 0)):
            f0 = currents[idx]
            x0 = voltages[idx]
            f1 = currents[idx-1]
            x1 = voltages[idx-1]
            isc = f0 + (((f1-f0)/(x1-x0))*(0-x0))
    for idx, current in enumerate(currents):#does the same as above for Voc
        if (idx > 0) and ((current < 0 and currents[idx-1] >= 0) or (current > 0 and currents[idx-1] <= 0)):
            f0 = voltages[idx]
            x0 = current
            f1 = voltages[idx-1]
            x1 = currents[idx-1]
            voc = f0 + (((f1-f0)/(x1-x0))*(0-x0))
    jsc = (isc / cellArea)*1000
    fillFactor = (max(powers)/(isc*voc))*100 #the times 100 gives you fillfactor in percent
    efficiency = (jsc*voc*fillFactor)/100 #because FF is already in percent the efficiency is also in percent
    if not curItem.resisttype == 0:
        vols_ohmic_voc=[]
        curs_ohmic_voc=[]
        for idx, vol_rev in enumerate(voltages):
            if (vol_rev >= voc - 0.1) and (vol_rev <= voc + 0.1):
                vols_ohmic_voc.append(vol_rev)
                curs_ohmic_voc.append(currents[idx])
        avg_vols_ohmic_voc = sum(vols_ohmic_voc) / float(len(vols_ohmic_voc))
        avg_curs_ohmic_voc = sum(curs_ohmic_voc) / float(len(curs_ohmic_voc))
        vols_ohmic_min_avg_voc = [x - avg_vols_ohmic_voc for x in vols_ohmic_voc]
        curs_ohmic_min_avg_voc = [x - avg_curs_ohmic_voc for x in curs_ohmic_voc]
        vols_min_avg_times_curs_min_avg_voc = [x * y for x,y in zip(vols_ohmic_min_avg_voc,curs_ohmic_min_avg_voc)]
        vols_ohmic_min_avg_sqr_voc = [x**2 for x in vols_ohmic_min_avg_voc]
        curs_ohmic_min_avg_sqr_voc = [x**2 for x in curs_ohmic_min_avg_voc]
        pearson_r_voc = sum(vols_min_avg_times_curs_min_avg_voc)/math.sqrt(sum(vols_ohmic_min_avg_sqr_voc)*sum(curs_ohmic_min_avg_sqr_voc))
        stand_div_curs_voc = math.sqrt(sum(curs_ohmic_min_avg_sqr_voc)/(float(len(curs_ohmic_voc))-1))
        stand_div_vols_voc = math.sqrt(sum(vols_ohmic_min_avg_sqr_voc)/(float(len(vols_ohmic_voc))-1))
        ohm_slope_voc = pearson_r_voc * (stand_div_curs_voc/stand_div_vols_voc)
        ohm_res_voc = -1/ohm_slope_voc
        intercept_ohmic_voc = avg_curs_ohmic_voc - (ohm_slope_voc*avg_vols_ohmic_voc)
        vols_ohmic_isc=[]
        curs_ohmic_isc=[]
        for idx, cur_rev in enumerate(currents):
            if (cur_rev >= (isc) - 0.0005) and (cur_rev <= (isc) + 0.0005):
                curs_ohmic_isc.append(cur_rev)
                vols_ohmic_isc.append(voltages[idx])
        avg_vols_ohmic_isc = sum(vols_ohmic_isc) / float(len(vols_ohmic_isc))
        avg_curs_ohmic_isc = sum(curs_ohmic_isc) / float(len(curs_ohmic_isc))
        vols_ohmic_min_avg_isc = [x - avg_vols_ohmic_isc for x in vols_ohmic_isc]
        curs_ohmic_min_avg_isc = [x - avg_curs_ohmic_isc for x in curs_ohmic_isc]
        vols_min_avg_times_curs_min_avg_isc = [x * y for x,y in zip(vols_ohmic_min_avg_isc,curs_ohmic_min_avg_isc)]
        vols_ohmic_min_avg_sqr_isc = [x**2 for x in vols_ohmic_min_avg_isc]
        curs_ohmic_min_avg_sqr_isc = [x**2 for x in curs_ohmic_min_avg_isc]
        pearson_r_isc = sum(vols_min_avg_times_curs_min_avg_isc)/math.sqrt(sum(vols_ohmic_min_avg_sqr_isc)*sum(curs_ohmic_min_avg_sqr_isc))
        stand_div_curs_isc = math.sqrt(sum(curs_ohmic_min_avg_sqr_isc)/(float(len(curs_ohmic_isc))-1))
        stand_div_vols_isc = math.sqrt(sum(vols_ohmic_min_avg_sqr_isc)/(float(len(vols_ohmic_isc))-1))
        ohm_slope_isc = pearson_r_isc * (stand_div_curs_isc/stand_div_vols_isc)
        ohm_res_isc = -1/ohm_slope_isc
        intercept_ohmic_isc = avg_curs_ohmic_isc - (ohm_slope_isc*avg_vols_ohmic_isc)
    if not curItem.resisttype == 0:
        return([jsc,voc,fillFactor,efficiency,cellArea,ohm_res_voc,ohm_res_isc,ohm_slope_voc,intercept_ohmic_voc,vols_ohmic_voc,vols_ohmic_isc,ohm_slope_isc,intercept_ohmic_isc])
    else:
        return([jsc,voc,fillFactor,efficiency,cellArea])
def writeOutputFileHeaders(savelocation, listitem):
    with open(savelocation,'a',encoding='utf-8') as outPutFileHeaderLines:
        outPutFileHeaderLines.write(str(os.path.basename(listitem.filePath))+'\t'+str(listitem.headerLines)+'\t')
        if listitem.delimiter_state == 0:
            outPutFileHeaderLines.write('No'+'\t')
        elif listitem.delimiter_state == 2:
            outPutFileHeaderLines.write('Yes'+'\t')
        outPutFileHeaderLines.write(str(listitem.delimiter_val)+'\t')
        if listitem.valsur_state == 0:
            outPutFileHeaderLines.write('No'+'\t')
        elif listitem.valsur_state == 2:
            outPutFileHeaderLines.write('Yes'+'\t')
        outPutFileHeaderLines.write(str(listitem.valsur_chars)+'\t')
        if listitem.meastype == 0:
            outPutFileHeaderLines.write('Single I/V'+'\t')
        elif listitem.meastype == 1:
            outPutFileHeaderLines.write('Double I/V'+'\t')
        if listitem.resisttype == 0:
            outPutFileHeaderLines.write('None'+'\t')
        elif listitem.resisttype == 1:
            outPutFileHeaderLines.write('Text only'+'\t')
        elif listitem.resisttype == 2:
            outPutFileHeaderLines.write('Text + Tangent'+'\t')
        outPutFileHeaderLines.write(str(listitem.colv1)+'\t'+str(listitem.coli1)+'\t'+str(listitem.colv2)+'\t'+str(listitem.coli2)+'\n')
        outPutFileHeaderLines.write('Results'+'\n'+'File'+'\t'+'Cell area'+'\t'+'Scan direction'+'\t'+'Measurement stage'+'\t'+'Voc [V]'+'\t'+'Jsc [mA]'+'\t'+'FF [%]'+'\t'+'Efficiency [%]'+'\t'+'Series Resistance [Ohm]'+'\t'+'Shunt Resistance [kOhm]'+'\n')
    outPutFileHeaderLines.close()
def findCellArea(filePath):
    foundCellArea = "0.4" #sets a default cell area in case none is found
    with open(filePath,'r') as inputFile:
        for line in inputFile:
            if ('cell' and 'area' in line.lower().split()) or ('cell' and 'area:' in line.lower().split()):
                foundCellArea = line.split()[-1]
    if len(foundCellArea.split(",")) == 2:
        foundCellArea = foundCellArea.split(",")[0]+"."+foundCellArea.split(",")[1]
    try:
        return(float(foundCellArea))
    except:
        return(0.4)
def createIVWorkbook(voltages,currents,curItem,measurementStage,scanResult):
    if PyOrigin.LT_execute("pe_cd /main_folder/iv_curves/") == 0: #switch to iv_curves folder in origin if it exists, if not make it (this if query will trigger an error in origin, unavoidable)
        PyOrigin.LT_execute("pe_cd /main_folder/iv_curves/")
    else:
        PyOrigin.LT_execute("pe_mkdir /main_folder/iv_curves/")
        PyOrigin.LT_execute("pe_cd /main_folder/iv_curves/")
    j=1
    while True: #creates a new worksheet with shortname ivcurve1, ivcurve2, ... for every file, giving each file a unique worksheet even if previous ones exist, and give them a longname equal to the file name
        if PyOrigin.LT_execute("win -a ivcurve"+str(j)) == 0: #check if ivcurvex worksheet exists, if not make it and make it active
            j += 1
        else:
            break
    PyOrigin.LT_execute('newbook name:="ivcurve'+str(j)+'" option:=lsname')
    PyOrigin.LT_execute("win -a ivcurve"+str(j))
    PyOrigin.LT_execute('page.longname$ = "'+str(os.path.basename(curItem.filePath).split('.')[0])+'_'+str(measurementStage)+'"')
    PyOrigin.LT_execute('page.title = 1;') #makes it so long name is shown as title
    if curItem.resisttype == 2: #setup the worksheets of the IV workbook
        PyOrigin.LT_execute("wks.ncols = 6")
    else:
        PyOrigin.LT_execute("wks.ncols = 2")
    PyOrigin.LT_execute("wks.name$ = Rev. Scan")
    PyOrigin.LT_execute("wks.col1.lname$ = Voltage")
    PyOrigin.LT_execute("wks.col1.unit$ = V")
    PyOrigin.LT_execute("wks.col2.comment$ = "+str(scanResult[-1]).title()+" scan")
    PyOrigin.LT_execute("wks.col2.lname$ = Current density")
    PyOrigin.LT_execute("wks.col2.unit$ = mA/cm\+(2)")
    if curItem.resisttype == 2:
        PyOrigin.LT_execute("wks.col3.comment$ = Series resistance rev.")
        PyOrigin.LT_execute("wks.col3.lname$ = Series res. V")
        PyOrigin.LT_execute("wks.col3.unit$ = V")
        PyOrigin.LT_execute("wks.col3.type = 4")
        PyOrigin.LT_execute("wks.col4.comment$ = Series resistance rev.")
        PyOrigin.LT_execute("wks.col4.lname$ = Series res. I")
        PyOrigin.LT_execute("wks.col4.unit$ = mA/cm\+(2)")
        PyOrigin.LT_execute("wks.col5.comment$ = Shunt resistance rev.")
        PyOrigin.LT_execute("wks.col5.lname$ = Shunt res. V")
        PyOrigin.LT_execute("wks.col5.unit$ = V")
        PyOrigin.LT_execute("wks.col5.type = 4")
        PyOrigin.LT_execute("wks.col6.comment$ = Shunt resistance rev.")
        PyOrigin.LT_execute("wks.col6.lname$ = Shunt res. I")
        PyOrigin.LT_execute("wks.col6.unit$ = mA/cm\+(2)")
    PyOrigin.LT_execute("wks.name$ = Rev. Scan")
    CurPage = PyOrigin.LT_get_str('page.name')
    CurSheet = PyOrigin.WorksheetPages(CurPage).Layers(0)
    if curItem.resisttype == 2:
        CurSheet.SetData([voltages,[x *(1000/(float(curItem.cellarea))) for x in currents],[scanResult[9][0], scanResult[9][-1]],[((scanResult[7]*scanResult[9][0])+scanResult[8])*(1000/(float(curItem.cellarea))),((scanResult[7]*scanResult[9][-1])+scanResult[8])*(1000/(float(curItem.cellarea)))],[scanResult[10][0],scanResult[10][-1]],[((scanResult[11]*(scanResult[10][0]))+scanResult[12])*(1000/(float(curItem.cellarea))),((scanResult[11]*(scanResult[10][-1]))+scanResult[12])*(1000/(float(curItem.cellarea)))]],0,0)
    else:
        CurSheet.SetData([voltages,[x *(1000/(float(curItem.cellarea))) for x in currents]],0,0) #adds IV data to worksheet
    if curItem.resisttype == 2:
        iv_graph = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "ivgraph"+str(j), "iv_curve_2", 1) #creates graph with template iv_curve_2
    else:
        iv_graph = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "ivgraph"+str(j), "iv_curve", 1) #creates graph with template iv_curve
    PyOrigin.LT_execute("win -a ivgraph"+str(j))
    PyOrigin.LT_execute('page.longname$ = "'+str(os.path.basename(curItem.filePath).split('.')[0])+'_'+str(measurementStage)+'"')
    PyOrigin.LT_execute('page.title = 1;') #makes it so long name is shown as title
    gp = PyOrigin.Pages(str(iv_graph)) # Get graph page by name
    gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
    gl = gp.Layers(0) 
    rng = PyOrigin.NewDataRange()  # Create data range.
    rng.Add('X', CurSheet, 0, 0, -1, 0) # Add worksheet's 1st col as X (0,0,-1,0) mean the data is from row 0, colum 0 in the worksheet to row -1, colum 0 in the worksheet.
    rng.Add('Y', CurSheet, 0, 1, -1, 1) # Add worksheet's 2nd col as Y.
    dp = gl.AddPlot(rng, 200)
    if curItem.resisttype == 2:
        rng.Destroy()
        rng = PyOrigin.NewDataRange()  # Create data range.
        rng.Add('X', CurSheet, 0, 2, -1, 2) # Add worksheet's 3rd col as X.
        rng.Add('Y', CurSheet, 0, 3, -1, 3) # Add worksheet's 4th col as Y.
        dp = gl.AddPlot(rng, 200)
        rng.Destroy()
        rng = PyOrigin.NewDataRange()  # Create data range.
        rng.Add('X', CurSheet, 0, 4, -1, 4) # Add worksheet's 5th col as X.
        rng.Add('Y', CurSheet, 0, 5, -1, 5) # Add worksheet's 6th col as Y.
        dp = gl.AddPlot(rng, 200)
    PyOrigin.LT_execute("layer.x.from = "+str(min(voltages)))
    PyOrigin.LT_execute("layer.x.to = "+str(max(voltages)))
    PyOrigin.LT_execute("layer.x.inc = 0.1")
    PyOrigin.LT_execute("layer.y.from = "+str(min(currents)*(1000/(float(curItem.cellarea)))))
    PyOrigin.LT_execute("layer.y.to = "+str(max(currents)*(1000/(float(curItem.cellarea)))))
    PyOrigin.LT_execute("layer.y.inc = 1")
    rng.Destroy()
    if curItem.resisttype == 1 or curItem.resisttype == 2:
        PyOrigin.LT_execute('label -sa -d 1500 2200 \p40(J\-(sc)[mA/cm\+(2)])\n\p40(V\-(oc)[V])\n\p40(FF[%])\n\p40(PCE[%])\n\p40(R\-(S)[Ohm])\n\p40(R\-(SH)[kOhm]);')
        PyOrigin.LT_execute('label -sa -d 2000 1980 \p40('+str(scanResult[-1]).title()+')\n\p40('+str(round(scanResult[0],2))+')\n\p40('+str(round(scanResult[1],2))+')\n\p40('+str(round(scanResult[2],2))+')\n\p40('+str(round(scanResult[3],2))+')\n\p40('+str(round(scanResult[5],2))+')\n\p40('+str(round((scanResult[6]/1000),2))+');')
    else:
        PyOrigin.LT_execute('label -sa -d 1500 2200 \p40(J\-(sc)[mA/cm\+(2)])\n\p40(V\-(oc)[V])\n\p40(FF[%])\n\p40(PCE[%]);')
        PyOrigin.LT_execute('label -sa -d 2000 1980 \p40('+str(scanResult[-1]).title()+')\n\p40('+str(round(scanResult[0],2))+')\n\p40('+str(round(scanResult[1],2))+')\n\p40('+str(round(scanResult[2],2))+')\n\p40('+str(round(scanResult[3],2))+');')
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    global win
    win = mainwin()
    app.exec_()
    
if __name__ == '__main__':
    main()