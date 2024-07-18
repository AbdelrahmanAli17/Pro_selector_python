import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QComboBox, QMessageBox
import pandas as pd


class ExcelSheetExtractor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Sheet Extractor")
        self.setGeometry(100, 100, 400, 250)

        self.folder_label = QLabel("Select folder directory:", self)
        self.folder_label.setGeometry(20, 20, 200, 30)

        self.select_folder_button = QPushButton("Select Folder", self)
        self.select_folder_button.setGeometry(220, 20, 100, 30)
        self.select_folder_button.clicked.connect(self.select_folder)

        self.loading_label = QLabel("Loading sheets...", self)
        self.loading_label.setGeometry(20, 60, 300, 30)
        self.loading_label.show()

        self.sheet_label = QLabel("Select sheet to extract:", self)
        self.sheet_label.setGeometry(20, 100, 200, 30)

        self.sheet_combo = QComboBox(self)
        self.sheet_combo.setGeometry(220, 100, 150, 30)

        self.extract_button = QPushButton("Extract Sheet", self)
        self.extract_button.setGeometry(120, 160, 160, 40)
        self.extract_button.clicked.connect(self.extract_sheet)

    def select_folder(self):
        folder_dialog = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folder_path = folder_dialog

        self.load_sheet_combo()

    def load_sheet_combo(self):
        self.sheet_combo.clear()
        #self.loading_label.show()

        try:
            files = os.listdir(self.folder_path)
            sheet_names = set()
            for file in files:
                if file.endswith(".xlsx") or file.endswith(".xls"):
                    file_path = os.path.join(self.folder_path, file)
                    try:
                        df = pd.read_excel(file_path, sheet_name=None)
                        sheets = df.keys()
                        sheet_names.update(sheets)
                    except Exception as e:
                        print(f"Error reading file {file}: {str(e)}")

            self.sheet_combo.addItems(sorted(sheet_names))
        except Exception as e:
            print(f"Error loading sheets: {str(e)}")

        #self.loading_label.hide()

    def extract_sheet(self):
        selected_sheet = self.sheet_combo.currentText()

        files = os.listdir(self.folder_path)
        for file in files:
            if file.endswith(".xlsx") or file.endswith(".xls"):
                file_path = os.path.join(self.folder_path, file)
                try:
                    df = pd.read_excel(file_path, sheet_name=selected_sheet)
                    csv_file_name = os.path.splitext(file)[0] + "_" + selected_sheet + ".csv"
                    csv_file_path = os.path.join(self.folder_path, csv_file_name)
                    df.to_csv(csv_file_path, index=False)
                except Exception as e:
                    print(f"Error processing file {file}: {str(e)}")

        QMessageBox.information(self, "Extraction Complete", "Sheet extraction is complete.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelSheetExtractor()
    window.show()
    sys.exit(app.exec_())