import os
import pandas as pd
from functools import reduce
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('ProteoSelector')

        # Create a central widget
        centralWidget = QtWidgets.QWidget(self)
        centralWidget.setFixedSize(800, 600)
        self.setCentralWidget(centralWidget)




        # Add a label for input directory selection
        label = QtWidgets.QLabel('Select input directory:', centralWidget)
        label.setStyleSheet("font-size: 12px")
        label.setGeometry(20, 20, 200, 30)

        # Add a line edit for input directory
        self.inputDirLineEdit = QtWidgets.QLineEdit(centralWidget)
        self.inputDirLineEdit.setStyleSheet("background-color: #fff")
        self.inputDirLineEdit.setGeometry(20, 50, 600, 30)

        # Add a browse button for input directory
        browseButton = QtWidgets.QPushButton('Browse', centralWidget)
        browseButton.setGeometry(680, 50, 100, 50)
        browseButton.clicked.connect(self.browseInputDir)
        browseButton.setStyleSheet("color: #fff  ;"
                                   "background-color: #4169e1;"
                                   "  border-radius: 8px;"
                                   " font-size: 12px;margin-bottom: 20px;")


        # Add a label for column selection
        label = QtWidgets.QLabel('Select column names:', centralWidget)
        label.setStyleSheet("font-size: 12px")
        label.setGeometry(20, 100, 200, 30)

        # Add a widget for column selection
        columnWidget = QtWidgets.QWidget(centralWidget)
        columnWidget.setStyleSheet("background-color: #fff")
        columnWidget.setGeometry(20, 130, 750, 350)

        # Add a scroll area for column selection
        scrollArea = QtWidgets.QScrollArea(columnWidget)
        scrollArea.setGeometry(0, 0, 750, 350)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidget = QtWidgets.QWidget()
        scrollArea.setWidget(scrollAreaWidget)

        # Add a checkbox for each column name
        self.columnCheckBoxes = []
        self.columnNames = set()
        self.allColumns = QtWidgets.QCheckBox('Select All Columns', scrollAreaWidget)
        self.allColumns.setGeometry(10, 10, 200, 30)
        self.allColumns.setChecked(False)
        self.allColumns.stateChanged.connect(self.selectAllColumns)

        # Add a layout for the checkbox widgets
        scrollAreaLayout = QtWidgets.QVBoxLayout(scrollAreaWidget)
        scrollAreaLayout.addWidget(self.allColumns)

        # Add a label for file type selection
        label = QtWidgets.QLabel('File type:', centralWidget)
        label.setStyleSheet("font-size: 18px")
        label.setGeometry(20, 500, 150, 30)

        # Add a checkbox for file type selection
        self.fileTypeCheckBox = QtWidgets.QCheckBox('CSV', centralWidget)
        self.fileTypeCheckBox.setGeometry(20, 530, 100, 30)
        self.fileTypeCheckBox.setStyleSheet("font-size: 12px")
        self.fileTypeCheckBox.setChecked(False)

        # Add a button to load files
        loadButton = QtWidgets.QPushButton('Load Files', centralWidget)
        loadButton.setGeometry(250, 95, 100, 50)
        loadButton.setStyleSheet("color: #fff  ;"
                                   "background-color: #4169e1 ;"
                                   "  border-radius: 8px;"
                                   " font-size: 12px;margin-bottom: 20px;")
        loadButton.clicked.connect(self.loadFiles)

        # Add a button to run the code
        button = QtWidgets.QPushButton('Run', centralWidget)
        button.setGeometry(680, 530, 100, 50)
        button.clicked.connect(self.runCode)
        button.setStyleSheet("color: #fff  ;"
                                   "background-color: #4682b4 ;"
                                   "  border-radius: 8px;"
                                   " font-size: 12px;margin-bottom: 20px;")

    def browseInputDir(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.inputDirLineEdit.setText(dialog.selectedFiles()[0])

    def selectAllColumns(self, state):
        for checkBox in self.columnCheckBoxes:
            checkBox.setChecked(state)

    def loadFiles(self):
        inputDir = self.inputDirLineEdit.text()
        fileType = 'csv' if self.fileTypeCheckBox.isChecked() else 'txt'
        self.columnNames = set()

        # Iterate over all files in the input directory
        for file in os.listdir(inputDir):
            filePath = os.path.join(inputDir, file)

            # Check if file is a CSV or TSV file
            if os.path.isfile(filePath) and filePath.lower().endswith('.' + fileType):

                # Read the file into a pandas data frame
                ReportContent = pd.read_csv(filePath, sep='\t' if not self.fileTypeCheckBox.isChecked() else ',')

                # Update the set of column names
                self.columnNames.update(ReportContent.columns.tolist())

        # Sort the column names and add a checkbox for each column
        self.columnNames = sorted(list(self.columnNames))
        for columnName in self.columnNames:
            checkBox = QtWidgets.QCheckBox(columnName, self.scrollAreaLayout)
            checkBox.setGeometry(10, len(self.columnCheckBoxes)*30 + 50, 200, 30)
            checkBox.setChecked(True)
            self.columnCheckBoxes.append(checkBox)

    def runCode(self):
        # Get the input directory path, selected columns, and file type
        inputDir = self.inputDirLineEdit.text()
        selectedColumns = [checkBox.text() for checkBox in self.columnCheckBoxes if checkBox.isChecked()]
        fileType = 'csv' if self.fileTypeCheckBox.isChecked() else 'txt'

        # Initialize a list to store data frames from all input files
        AllSubReportContent = []

        # Iterate over all files in the input directory
        for file in os.listdir(inputDir):
            filePath = os.path.join(inputDir, file)

            # Check if file is a CSV or TSV file
            if os.path.isfile(filePath) and filePath.lower().endswith('.' + fileType):

                # Read the file into a pandas data frame
                ReportContent = pd.read_csv(filePath, sep='\t' if not self.fileTypeCheckBox.isChecked() else ',')

                # Get the file name without extension
                filename = os.path.splitext(file)[0]

                # Select only the columns that the user has selected
                SelectedColumnsData = ReportContent[selectedColumns]

                # Create a header for the selected columns in the output file, including the filename as a prefix for each column
                header = [filename + '->' + col for col in selectedColumns]

                # Update the column names in the selected data frame
                SelectedColumnsData.columns = header

                # Append the selected data frame to the list of data frames
                AllSubReportContent.append(SelectedColumnsData)

        # Merge the data frames from all input files based on the selected columns
        if AllSubReportContent:
            AllSubReportContent = reduce(lambda df1, df2: pd.merge(df1, df2, left_index=True, right_index=True), AllSubReportContent)

            # Sort the columns in the merged data frame
            AllSubReportContent = AllSubReportContent[sorted(AllSubReportContent.columns)]

            # Create the output file path and header
            OutputPath = os.path.join(inputDir, 'OutputData.csv')
            header = list(AllSubReportContent.columns)

            # Write the merged data frame to the output file
            AllSubReportContent.to_csv(OutputPath, index=False, columns=header)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()