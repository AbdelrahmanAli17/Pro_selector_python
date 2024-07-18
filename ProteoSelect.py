import os
import pandas as pd
from functools import reduce
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('ProteoSelector')
        self.setStyleSheet("background-color:#F0F8FF ;")

        # Create a central widget
        centralWidget = QtWidgets.QWidget(self)
        centralWidget.setFixedSize(800, 600)
        self.setCentralWidget(centralWidget)


        # Add a label
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


        # Create a widget for column selection
        columnWidget = QtWidgets.QWidget(centralWidget)
        columnLayout = QtWidgets.QVBoxLayout()
        columnWidget.setLayout(columnLayout)
        columnWidget.setStyleSheet("background-color: #fff")
        columnWidget.setGeometry(20, 130, 750, 350)
        #layout.addWidget(columnWidget)

        # Add a scroll area for column selection
        scrollArea = QtWidgets.QScrollArea(columnWidget)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidget = QtWidgets.QWidget(columnWidget)
        scrollAreaLayout = QtWidgets.QVBoxLayout(scrollAreaWidget)
        scrollArea.setWidget(scrollAreaWidget)
        columnLayout.addWidget(scrollArea)

        # Add a checkbox for each column name
        self.columnCheckBoxes = []
        self.columnNames = set()
        self.allColumns = QtWidgets.QCheckBox('Select All Columns')
        self.allColumns.setChecked(True)
        self.allColumns.stateChanged.connect(self.selectAllColumns)
        self.scrollAreaWidget = QtWidgets.QWidget(columnWidget)
        self.scrollAreaWidget.setLayout(QtWidgets.QVBoxLayout())
        self.scrollAreaWidget.layout().addWidget(self.allColumns)
        scrollArea.setWidget(self.scrollAreaWidget)

        # Add a label for file type selection
        label = QtWidgets.QLabel('File type:', centralWidget)
        label.setStyleSheet("font-size: 18px")
        label.setGeometry(20, 500, 150, 30)

        # Add a checkbox for file type selection
        self.fileTypeCheckBox = QtWidgets.QCheckBox('csv', centralWidget)
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

        # Add an image of the hospital
        imageLabel = QtWidgets.QLabel(centralWidget)
        pixmap = QPixmap('57357.png')
        imageLabel.setPixmap(pixmap)
        imageLabel.setGeometry(200, 500,200,100)
        imageLabel.setScaledContents(True)

        # Add an image of the lab
        imageLabel = QtWidgets.QLabel(centralWidget)
        pixmap = QPixmap('log.jpg')
        imageLabel.setPixmap(pixmap)
        imageLabel.setGeometry(400, 500, 100, 100)
        imageLabel.setScaledContents(True)

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

        # Check if the input directory exists
        if not os.path.isdir(inputDir):
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid input directory.")
            return

        # Iterate over files in the input directory
        try:
            for file in os.listdir(inputDir):
                filePath = os.path.join(inputDir, file)

                # Check if the file is of the supported type
                if os.path.isfile(filePath) and filePath.lower().endswith('.' + fileType):
                    try:
                        if fileType == "txt":
                            # Read the file into a pandas data frame
                            ReportContent = pd.read_csv(filePath,sep='\t' )
                        if fileType == "csv":
                            # Read the file into a pandas data frame
                            ReportContent = pd.read_csv(filePath)

                        # Update the set of column names
                        self.columnNames.update(ReportContent.columns.tolist())

                    except pd.errors.ParserError:
                        QtWidgets.QMessageBox.warning(self, "Warning",
                                                      f"Error reading file: {file}. Skipping the file.")

        except OSError:
            QtWidgets.QMessageBox.critical(self, "Error", "Error accessing files in the input directory.")
            return

        # Check if any files were found and processed
        if not self.columnNames:
            QtWidgets.QMessageBox.warning(self, "Warning",
                                          "No files of the specified type found in the input directory.")
            return

        # Sort and display the column names
        self.columnNames = sorted(list(self.columnNames))
        for columnName in self.columnNames:
            checkBox = QtWidgets.QCheckBox(columnName)
            checkBox.setChecked(True)
            self.columnCheckBoxes.append(checkBox)
            self.scrollAreaWidget.layout().addWidget(checkBox)

    def runCode(self):
        # Get the input directory path, selected columns, and file type
        inputDir = self.inputDirLineEdit.text()
        selectedColumns = [checkBox.text() for checkBox in self.columnCheckBoxes if checkBox.isChecked()]
        fileType = 'csv' if self.fileTypeCheckBox.isChecked() else 'txt'

        if not selectedColumns:
            QtWidgets.QMessageBox.warning(self, "Error",
                                          "Please select at least one column.")
            return
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
                header = [selectedColumns[0]] + [filename + '_' + col for col in selectedColumns[1:]]

                # Update the column names in the selected data frame
                SelectedColumnsData.columns = header

                # Append the selected data frame to the list of data frames
                AllSubReportContent.append(SelectedColumnsData)

        # Merge the data frames from all input files based on the selected columns
        if AllSubReportContent:
            if selectedColumns[0] == "Main Accession":
                AllSubReportContent = reduce(lambda df1, df2: pd.merge(df1, df2, on="Main Accession"),AllSubReportContent)

            if selectedColumns[0] == "Accessions":
                AllSubReportContent = reduce(lambda df1, df2: pd.merge(df1, df2, on="Accessions" ),AllSubReportContent)

            else:
                QtWidgets.QMessageBox.warning(self, "Error",
                                              "Please ,Select the Main Accession or Accessions in case of proteinpilot at First.")
            # Create the output file path and header
            OutputPath = os.path.join(inputDir, 'OutputData.csv')
            header = list(AllSubReportContent.columns)

            # Write the merged data frame to the output file
            AllSubReportContent.to_csv(OutputPath, index=False, columns=header ,mode='w+' )

            messageBox = QtWidgets.QMessageBox(self)
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setWindowTitle("ProteoSelector")
            messageBox.setText("The program has finished running.")
            messageBox.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()