import sys
import os
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QThread
from PySide2.QtCore import Signal as pyqtSignal
os.environ['QT_MAC_WANTS_LAYER'] = '1'
from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QMainWindow, QWidget, QPushButton, QLabel, QListWidget,
    QFileDialog, QFrame, QMessageBox
)
#from emat_mfl_combined.applications.pdw_upload.analysis_tools.path2proj import Path2ProjAnomaliesGeneral
import pathlib
import os
import pandas as pd
from tabulate import tabulate


class MyThread(QThread):

    update_progress = pyqtSignal(int)
    thread_finished = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    # IMPORTANT
    # Define the relevant code, which should executed in the
    # separate QThread-process.
    # Remember: the important variables, which should be used from
    # the main-class has to be defined inside the main-class itself,
    # look inside the function create_df_of_features!
        self.patch_dir_glob = None
        self.path_project_anomalies_dirs = None
        self.df_tmp = {}
        self.region_number_tmp = []
        self.region_number_df = {}
        self.project_number_tmp = []
        self.project_number_df = {}
        self.lineshort_name_tmp = []
        self.lineshort_name_df = {}
        self.counts_anom_types_tmp = []
        self.counts_anom_types_df = {}
        self.exchange_file_anom_types = {}
        self.df_final = pd.DataFrame()
        # self.list_info = None
        self.current_csv_path = None
        self.filtered_exchange_file = None
        self.exchange_file = None
        self.counts_anom_types = 0
        self.counts_exchange_file_anom_types_tmp = []
        # str_exec_val = "Lines have been executed"
        # QMessageBox.information(self, "Done!", str_exec_val)
        # QMessageBox.information(self, "Done!", str_val)

    def run(self) -> None:

        self.patch_dir_glob = [x.split('/anomalies')[0] for x in self.anomaly_dirs]
        root_path = '//linfile1/groups/emat_evaluation_data/combevaldatawarehouse/'
        self.path_project_anomalies_dirs = [os.path.join(root_path, x) for x in self.patch_dir_glob]

        for tmp_lines in self.path_project_anomalies_dirs[:]:

            self.current_csv_path = pathlib.Path(tmp_lines) / "CE/Feature/exchange_with_anomcenter.csv"

            if not self.current_csv_path.exists():
                continue

            p = Path2ProjAnomaliesGeneral(tmp_lines)

            # self.region_number_tmp.append(p.region_number)
            # self.region_number_df = pd.DataFrame(self.region_number_tmp)
            # self.project_number_tmp.append(p.project_number)
            # self.project_number_df = pd.DataFrame(self.project_number_tmp)

            displayed_string = r'Loading the csv-file of {}: '.format(p.lineshort_name)
            print('displayed_String: ', displayed_string)
            cur_val = self.path_project_anomalies_dirs.index(tmp_lines) + 1

            leng = len(self.path_project_anomalies_dirs)

            displayed_string_2 = r'[{}] of [{}]'.format(str(cur_val), str(leng))

            self.written_line_of_features_info.addItem(displayed_string + displayed_string_2)

            # self.written_line_of_features_info.repaint() # it seems, that his is not necessary!
            print('current_csv_path: ', self.current_csv_path)
            self.exchange_file = pd.read_csv(self.current_csv_path)
            self.filtered_exchange_file = self.exchange_file
            self.filtered_exchange_file = self.filtered_exchange_file.reset_index()

            if "TYPE" in self.exchange_file.columns:
                self.exchange_file = self.exchange_file.rename(columns={'TYPE': 'type'})

            elif "type" in self.exchange_file.columns:
                self.exchange_file = self.exchange_file.rename(columns={'type': 'type'})
            else:
                raise ValueError("csv-File does not contain a 'TYPE' or 'type' namend column")

            # self.exchange_file_anom_types = list(self.exchange_file["type"].unique())

            # self.exchange_file_anom_types_df = pd.DataFrame(self.exchange_file_anom_types)

            self.counts_anom_types = self.exchange_file["type"].value_counts()
            self.df_tmp = pd.DataFrame()
            self.df_tmp['ctn'] = self.counts_anom_types.values
            self.df_tmp['feature'] = self.counts_anom_types.index
            self.df_tmp['lineshort'] = [p.lineshort_name] * len(self.df_tmp['ctn'])
            self.df_tmp['project_number'] = [p.project_number] * len(self.df_tmp['ctn'])
            self.df_tmp['region'] = [p.region_number] * len(self.df_tmp['ctn'])

            self.df_final = self.df_final.append(self.df_tmp)
            # self.exchange_file_anom_types = pd.DataFrame(self.counts_anom_types.index)
            # self.counts_exchange_file_anom_types_tmp = list(self.counts_anom_types)
            # self.counts_anom_types_df = pd.DataFrame(self.counts_exchange_file_anom_types_tmp)
            # self.lineshort_name_tmp.append(p.lineshort_name)
            # self.lineshort_name_df = pd.DataFrame(self.lineshort_name_tmp)
            # self.df_tmp = pd.concat([
            #    self.region_number_df, self.project_number_df, self.lineshort_name_df, self.exchange_file_anom_types,
            #    self.counts_anom_types_df], axis=1
            # )
            # print('df_tmp: ', self.df_tmp)
            # self.df_tmp.columns = ['region', 'project_number', 'lineshort', 'feature', 'ctn']
            # self.df_tmp['region'] = p.region_number
            # self.df_tmp['project_number'] = p.project_number
            # self.df_tmp['lineshort'] = p.lineshort_name

            #self.df_final = pd.concat([self.df_final, self.df_tmp])
            print('debug end')
        self.df_final = self.df_final[['region', 'project_number', 'lineshort', 'feature', 'ctn']]
        print(tabulate(self.df_final, headers='keys', tablefmt="psql"))
        self.thread_finished.emit('Lines have been finished')

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class WindowScanDir(QMainWindow):
    def __init__(self, x_pos_parent_window, y_pos_parent_window, width_parent_window):
        super().__init__()

        self.x_pos_parent_window = x_pos_parent_window
        self.y_pos_parent_window = y_pos_parent_window
        self.width_parent_window = width_parent_window

        self.move(self.x_pos_parent_window, self.y_pos_parent_window)
        self.setFixedWidth(self.width_parent_window)
        self.setWindowTitle("Scan directories V0.5 - Manual edition!")

        ###################################################
        # Define the layout !!
        ###################################################

        # Create the complete_layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen logo
        self.label_pic_layout = QHBoxLayout()

        # Define labels for header and Rosen_logo
        self.lbl_scan_dir = QLabel("Scan directories")
        self.lbl_scan_dir.setStyleSheet("font-size: 16px;" "color: green")
        self.lbl_rosen_logo = QLabel("Rosen logo")
        self.lbl_rosen_logo.setPixmap(QPixmap("rosen_logo.png"))
        self.lbl_rosen_logo.setScaledContents(False)

        # Fill the label_pic_layout
        self.label_pic_layout.addWidget(self.lbl_scan_dir)
        self.label_pic_layout.addStretch()               # Distribute the widgets equidistant
        self.label_pic_layout.addWidget(self.lbl_rosen_logo)

        # Layout for buttons and listwidgets area - different to qgrid!
        self.btn_and_listwidget_layout = QHBoxLayout()

        # Define buttons and the layout - should be arranged vertically
        self.btn_layout = QVBoxLayout()

        self.btn_add_anomaly_dir = QPushButton("Add directory ...")
        self.btn_create_df = QPushButton("Create df of available features ...")
        self.btn_save_list_of_anomaly_dirs = QPushButton("Save list of anomaly dirs ...")
        self.btn_chose_csv_file = QPushButton("Choose csv_file for saving ...")
        self.btn_write_anomaly_dirs_to_csv = QPushButton("Write csv_file ...")

        # Fill the btn_layout with buttons
        self.btn_layout.addWidget(self.btn_add_anomaly_dir)
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.btn_create_df)
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.btn_save_list_of_anomaly_dirs)
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.btn_chose_csv_file)
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.btn_write_anomaly_dirs_to_csv)

        # Define layout for horizontal line
        self.hor_line_1_layout = QHBoxLayout()
        self.hor_line_1_layout.addWidget(QHLine())
        #self.btn_layout.addLayout(self.hor_line_1_layout)

        # Next group of buttons for dealing with the pdw!
        self.btn_load_uploaded_ctns_from_pdw = QPushButton("Load uploaded features from PDW ...")
        self.btn_layout.addStretch(1)
        self.btn_layout.addWidget(self.btn_load_uploaded_ctns_from_pdw)
        self.btn_write_df_complete_to_pdw = QPushButton("Write df complete to PDW ...")
        self.btn_layout.addStretch(1)

        self.btn_layout.addWidget(self.btn_write_df_complete_to_pdw)
        # Define QListWidgets and the layout - should be arranged vertically
        self.list_widget_layout = QVBoxLayout()

        self.text_anomaly_dirs = QListWidget()
        self.text_anomaly_dirs.addItem("anomaly text 1 for check")
        self.text_anomaly_dirs.addItem("anomaly text 2 for check")

        self.written_line_of_features_info = QListWidget()

        # Fill the list_widget_layout with listwidgets
        self.list_widget_layout.addWidget(self.text_anomaly_dirs)
        # list_widget_layout.addStretch()
        self.list_widget_layout.addWidget(self.written_line_of_features_info)

        # Arrange btn_layout and list_widgets_layout in horizontal layout
        self.btn_and_listwidget_layout.addLayout(self.btn_layout)
        self.btn_and_listwidget_layout.addLayout(self.list_widget_layout)

        # Place the layouts in the desired manner
        self.complete_layout.addLayout(self.label_pic_layout)
        # complete_layout.addStretch()
        self.complete_layout.addLayout(self.btn_and_listwidget_layout)

        # Set the hand-made complete_layout in a superordinate QWidget called dummy_widget
        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(self.dummy_widget)

        ###################################################
        # END of definition of the layout !!
        ###################################################

        # Definition of relevant/required variables
        self.anomaly_dirs = []
        self.current_dir = None
        self.saved_file_name = ""
        self.saved_csv_file = ""
        self.choosen_aomaly_dir = ""
        self.path_csv_file = None
        self.patch_dir = None
        self.saved_anomaly_list = None
        self.clicked_value = 0
        self.df_final = pd.DataFrame()
        self.thread = None

        self.text_anomaly_dirs.clear()
        [self.text_anomaly_dirs.addItem(str(x)) for x in self.anomaly_dirs]

        # Define the actions, when Buttons are clicked
        self.btn_add_anomaly_dir.clicked.connect(self.add_anomaly_dir)
        self.btn_create_df.clicked.connect(self.create_df_of_features)
        self.btn_save_list_of_anomaly_dirs.clicked.connect(self.save_list_of_anomaly_dirs)
        self.btn_chose_csv_file.clicked.connect(self.choose_csv_file)
        self.btn_write_anomaly_dirs_to_csv.clicked.connect(self.save_to_csv_file)

        self.current_dir = os.path.dirname(__file__)
        # print('self.current_dir: ', self.current_dir)
        os.chdir(self.current_dir)
        self.saved_file_name = os.path.join(self.current_dir, 'saved_anomaly_list.txt')

    def add_anomaly_dir(self):

        if not self.anomaly_dirs:
            with open(self.saved_file_name) as f:
                self.anomaly_dirs = f.read().splitlines()

        self.patch_dir = QFileDialog.getExistingDirectory(
            parent=None,
            caption="Select additional directory for scanning (AP-dir)",
            directory="",
        )

        if self.patch_dir == "":
            return

            # self.saved_anomaly_list = open('saved_anomaly_list.txt', 'r')
            # for line in self.saved_anomaly_list:
            #     self.anomaly_dirs.read(line + "\n")
            # self.saved_anomaly_list.close()

        tmp_anomaly_dir = self.patch_dir.strip('H:/') + '/anomalies'
        self.anomaly_dirs.append(tmp_anomaly_dir)

        self.anomaly_dirs = list(set(self.anomaly_dirs))
        print('len: ', len(self.anomaly_dirs))
        self.anomaly_dirs = list(filter(None, self.anomaly_dirs))
        # print('self.anomaly_dirs: ', self.anomaly_dirs)
        self.text_anomaly_dirs.clear()
        [self.text_anomaly_dirs.addItem(str(x)) for x in sorted(self.anomaly_dirs)]
        str_val = "Anomaly dirs have been loaded!"
        QMessageBox.information(self, "Done!", str_val)

    def create_df_of_features(self):
        self.thread = MyThread()
        # Now: Definition of the relevant variables for the thread class.
        # Here is the same logic as compared in the ._uploaded-py-File line 303ff !!!! IMPORTANT!

        self.thread.anomaly_dirs = self.anomaly_dirs
        self.thread.written_line_of_features_info = self.written_line_of_features_info
        self.thread.start()
        # self.thread.finished.connect(self.print_message)
        # self.thread.thread_finished.connect(self.print_message)
        # str_val = 'Lines have been executed'
        self.thread.thread_finished.connect(self.print_message)
        # self.thread.thread_finished.connect(QMessageBox.information(self, "Done !"))
        # self.thread.update_progress.connect(self.evt_update_progress)

    def save_list_of_anomaly_dirs(self):
        self.saved_anomaly_list = open(self.saved_file_name, 'w')
        for line in self.anomaly_dirs:
            self.saved_anomaly_list.write(line + "\n")
        self.saved_anomaly_list.close()
        self.short_file_name = self.saved_file_name.split('\\')[-1]

        msg = r'List of anomaly dirs have been saved under {}'.format(self.short_file_name)
        self.print_message(msg)

    def choose_csv_file(self):

        os.chdir(os.getcwd())

        self.path_csv_file = QFileDialog.getSaveFileName(self, "Open file for saving", dir=os.getcwd())

        print('self.path_csv_file: ', self.path_csv_file[0])

    def save_to_csv_file(self):
        self.df_final = self.thread.df_final
        self.saved_csv_file = self.path_csv_file[0]

        print('df_final: ', self.df_final)

        print('self.saved_file: ', self.saved_csv_file)

        self.df_final.to_csv(self.saved_csv_file)
        msg = r'csv-file of anomalies have been saved under {}'.format(self.saved_csv_file.split('/')[-1])
        self.print_message(msg)

    def print_message(self, str_val):
        print('str_val: ', str_val)
        QMessageBox.information(self, "Done!", str_val)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowScanDir(200, 330, 800)
    window.show()
    sys.exit(app.exec_())
