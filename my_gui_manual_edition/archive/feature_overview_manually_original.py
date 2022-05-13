import sys
import os
import datetime
from tabulate import tabulate
os.environ['QT_MAC_WANTS_LAYER'] = '1'

from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2 import QtWidgets

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout,
    QMessageBox, QPushButton, QListWidget,
    QFrame, QWidget, QMainWindow, QLineEdit, QLabel
)

# Important: the next two lines have to be imported after the Pyside2 imports.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# seaborn has to be imported after the matplotlib modules
import seaborn as sns
import pandas as pd

#from emat_mfl_combined.applications.pdw_upload.analysis_tools.pdw_tools import joerg_pdw_py_wc
#from emat_mfl_combined.applications.pdw_upload.analysis_tools.tools import show_values_on_bars_v2
#from emat_mfl_combined.applications.pdw_upload.pdw.gui_scanning_directories \
#    import window_scanning_directories_for_feature_overview as scanning_window

#from emat_mfl_combined.applications.pdw_upload.pdw.pdw_manual_edition import (
#scan_directories_manually as scanning_window
#)

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.HVine)
        self.setFrameShadow(QFrame.Sunken)


class WindowShowFeatureOverview(QMainWindow):
    def __init__(self, x_pos_parent_window, y_pos_parent_window, width_parent_window):
        super().__init__()
        self.x_pos_parent_window = x_pos_parent_window
        print('self.x_pos_parent_window: ', self.x_pos_parent_window)
        self.y_pos_parent_window = y_pos_parent_window
        print('self.y_pos_parent_window: ', self.y_pos_parent_window)
        self.width_parent_window = width_parent_window
        print('self.width_parent_window: ', self.width_parent_window)
        print('width of feature_overview_window: ', self.width())
        print('height of feature_overview_window: ', self.height())

        self.move(self.x_pos_parent_window + self.width_parent_window, self.y_pos_parent_window)
        # self.setFixedWidth(self.width_parent_window)

        self.setWindowTitle('Feature overview V 0.5 - Manual edition!')
        self.level_counts = []
        self.level_names = []
        self.region_number_db = []
        self.project_number_db = []
        self.lineshot_name_db = []
        self.feature_list_db = []
        ###########################################################
        # Definition of the layout
        ###########################################################

        # Create the complete layout as a vertical box layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen logo
        self.label_pic_layout = QHBoxLayout()

        # Define the label for header and Rosen-logo
        self.lbl_feature_overview = QLabel("PDW: Feature overview")
        self.lbl_feature_overview.setStyleSheet("font-size: 18px;" "color: rgb(44, 44, 126,255);")
        self.lbl_rosen_logo = QLabel("Rosen_logo")
        self.pixmap = QPixmap("rosen_logo.png")
        self.scaled_picture = self.pixmap.scaled(self.lbl_rosen_logo.size() / 4, QtCore.Qt.KeepAspectRatio)
        self.lbl_rosen_logo.setPixmap(self.scaled_picture)
        self.lbl_rosen_logo.setScaledContents(True)

        # Fill the label_picture_layout
        self.label_pic_layout.addWidget(self.lbl_feature_overview)
        self.label_pic_layout.addStretch()                          # Distribute the widgets equidistant
        self.label_pic_layout.addWidget(self.lbl_rosen_logo)

        # layout for load and display the csv-file
        self.btn_and_display_csv_file_layout = QHBoxLayout()
        self.btn_load_csv_file = QPushButton("Load csv-file ...")
        self.show_path_csv_file = QLineEdit()
        self.btn_and_display_csv_file_layout.addWidget(self.btn_load_csv_file)
        self.btn_and_display_csv_file_layout.addWidget(self.show_path_csv_file)

        # Define layout for a horizontal line...
        self.hor_line_3_layout = QHBoxLayout()
        self.hor_line_3_layout.addWidget(QHLine())

        # Layout for the buttons - now it's a QHBox
        self.btn_layout = QHBoxLayout()

        # Define the buttons ...
        self.btn_load_features_for_overview = QPushButton("Load features for overview")
        self.btn_1_dummy = QPushButton("Dummy button 1")
        self.btn_2_dummy = QPushButton("Dummy button 2")

        self.btn_layout.addWidget(self.btn_load_features_for_overview)
        self.btn_layout.addWidget(self.btn_1_dummy)
        self.btn_layout.addWidget(self.btn_2_dummy)

        # Define layout for a horizontal line...
        self.hor_line_1_layout = QHBoxLayout()
        self.hor_line_1_layout.addWidget(QHLine())

        # Define layout for a horizontal line...
        self.hor_line_2_layout = QHBoxLayout()
        self.hor_line_2_layout.addWidget(QHLine())

        # Define layout for the QListWidget for the lines
        self.lbl_lines_layout = QVBoxLayout()

        self.lbl_line = QLabel('Available lines')
        self.list_of_lines = QListWidget()
        # self.list_of_lines.setFixedWidth(140)

        # Search for the maximum length of the line
        # max_length_of_elements = max(list_lines_tmp, key=len)
        # self.max_element = QLabel(max_length_of_elements)
        # max_width_of_line_list = self.max_element.fontMetrics().width(max_length_of_elements)
        # self.list_of_lines.setFixedWidth(max_width_of_line_list*2)
        self.lbl_lines_layout.addWidget(self.lbl_line)
        self.lbl_lines_layout.addWidget(self.list_of_lines)

        # Define the layout-place for the canvas
        self.canvas_layout = QVBoxLayout()

        # Now, its getting complicated...
        # Create two additional layouts for later deleting inside
        # the remove-function
        self.canvas_layout_available_features = QVBoxLayout()
        self.canvas_layout_uploaded_features = QVBoxLayout()

        self.fig_1 = plt.Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_feature_overview = FigureCanvas(self.fig_1)
        self.fig_1.text(0.2, 0.5, "Displaying the available features of the lines", fontsize=14)

        # The Code below is for the testing of the canvas.
        # self.figure_feature_overview = self.fig_1.add_subplot(111)
        # self.figure_feature_overview.clear()
        # self.figure_feature_overview.set_ylabel('Volts')
        # self.figure_feature_overview.set_title('A sinus wave')
        # t = np.arange(0.0, 1.0, 0.01)
        # s = np.sin(2 * np.pi * t)
        # line = self.figure_feature_overview.plot(t, s, lw=2)

        # With the command below, the plot will be shown
        self.canvas_layout_available_features.addWidget(self.canvas_feature_overview)

        # Second plot below
        self.fig_2 = plt.Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas_feature_overview_uploaded_features = FigureCanvas(self.fig_2)
        self.fig_2.text(0.2, 0.5, "Displaying the uploaded features of the lines", fontsize=14)

        # The Code below is for the testing of the canvas.
        # self.figure_overview_uploaded_features = self.fig_2.add_subplot(111)
        # self.figure_overview_uploaded_features.clear()

        # self.figure_overview_uploaded_features.set_ylabel('Volts')
        # self.figure_overview_uploaded_features.set_title('A cosinus wave')
        # t = np.arange(0.0, 1.0, 0.01)
        # c = np.cos(2 * np.pi * t)
        # line = self.figure_overview_uploaded_features.plot(t, c, lw=2)

        # With the command below, the plot will be shown
        # self.canvas_layout.addWidget(self.canvas_feature_overview_uploaded_features)
        self.canvas_layout_uploaded_features.addWidget(self.canvas_feature_overview_uploaded_features)

        # Referring to the creating of the layout self.canvas_layout..
        self.canvas_layout.addLayout(self.canvas_layout_available_features)
        self.canvas_layout.addLayout(self.canvas_layout_uploaded_features)

        # Define layout for canvas AND line display, it horizontal layout
        self.canvas_and_line_layout = QHBoxLayout()

        self.canvas_and_line_layout.addLayout(self.canvas_layout)
        self.canvas_and_line_layout.addLayout(self.lbl_lines_layout)

        # NOW: Build the complete layouts together...
        self.complete_layout.addLayout(self.label_pic_layout)
        self.complete_layout.addLayout(self.hor_line_1_layout)
        self.complete_layout.addLayout(self.btn_and_display_csv_file_layout)
        self.complete_layout.addLayout(self.hor_line_2_layout)
        self.complete_layout.addLayout(self.btn_layout)
        self.complete_layout.addLayout(self.hor_line_3_layout)
        self.complete_layout.addLayout(self.canvas_and_line_layout)

        # Set the complete_layout into a superordinate QWidget called dummy widget

        dummy_widget = QWidget()
        dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(dummy_widget)

        ###########################################################
        # End of definition of the layout
        ###########################################################

        # Define the signals and slots
        self.btn_load_csv_file.clicked.connect(self.load_csv_file)
        self.btn_load_features_for_overview.clicked.connect(self.get_uploaded_features)
        self.list_of_lines.itemClicked.connect(self.clicked_single_line)

    ################################################################
    # Define the functions for handling the data
    ################################################################

    # Removing the figures, or canvas respectively...

    def remove_figure_available_feature_window(self,):
        for i in reversed(range(self.canvas_layout_available_features.count())):
            self.canvas_layout_available_features.itemAt(i).widget().deleteLater()

    def remove_figure_uploaded_feature_window(self):
        for i in reversed(range(self.canvas_layout_uploaded_features.count())):
            self.canvas_layout_uploaded_features.itemAt(i).widget().deleteLater()

    # Define the function for the "re-drawing" of the figure
    # mostly, when an item is clicked this functions will be executed

    # First: For the upper figure...
    def add_figure_available_features_window(self, fig):
        self.canvas_feature_overview = FigureCanvas(fig)
        self.canvas_layout_available_features.addWidget(self.canvas_feature_overview)

    # Second: For the lower figure...
    def add_figure_uploaded_features_window(self, fig):
        self.canvas_uploaded_feature_overview = FigureCanvas(fig)
        self.canvas_layout_uploaded_features.addWidget(self.canvas_uploaded_feature_overview)

    def load_csv_file(self):
        current_dir_part_1 = r'c:\users\jwingbermuehle\Repos\EmatMflCombined\emat_mfl_combined'
        current_dir_part_2 = r'\applications\pdw_upload\pdw\gui_feature_overview'
        os.chdir(current_dir_part_1 + current_dir_part_2)
        self.path_csv_file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select csv-file",
            "*.csv",
        )
        if isinstance(self.path_csv_file, tuple):

            self.show_path_csv_file.setText(self.path_csv_file[0])
            self.overview_available_features = pd.read_csv(self.path_csv_file[0]).drop(['Unnamed: 0'], axis=1)
            self.overview_available_features['project_number'] = \
                self.overview_available_features['project_number'].astype(str)
            self.overview_available_features['feature'] = self.overview_available_features['feature'].str.lower()
            [self.list_of_lines.addItem(x) for x in self.overview_available_features['lineshort'].unique()]
            self.figure_handle_db = self.overview_available_features['lineshort'].unique()
            # Search for the maximum length of the line
            max_length_of_elements = max(self.overview_available_features['lineshort'].unique(), key=len)
            self.max_element = QLabel(max_length_of_elements)
            max_width_of_line_list = self.max_element.fontMetrics().width(max_length_of_elements)
            self.list_of_lines.setFixedWidth(max_width_of_line_list * 4)

        else:

            str(self.path_csv_file)

    def get_uploaded_features(self):
        time_1 = datetime.datetime.now()
        print(time_1.strftime("time_1: %H-%M-%S"))

        server = "https://pdw-lin.roseninspection.net/pdw-emat"
        pdw = joerg_pdw_py_wc.connect(server)

        w = scanning_window.WindowScanDir(self.x_pos_parent_window, self.y_pos_parent_window, self.width_parent_window)

        # original: if w.anomaly_dire == []
        if not w.anomaly_dirs:
            with open(w.saved_file_name) as f:
                w.anomaly_dirs = f.read().splitlines()

        self.anomaly_dirs = w.anomaly_dirs

        print('anomaly_dirs from scanning window...', self.anomaly_dirs)

        self.level_names = []
        self.level_counts = []
        self.feature_name_tmp = []
        self.feature_nr_tmp = []
        self.features = []
        self.feature_ctns = []
        self.features_db = {}
        self.feat_db = {}
        self.ctns_db = {}
        self.feat_ctn_db_all = pd.DataFrame()
        self.df_features_and_counts_single_lineshort = pd.DataFrame()
        self.lineshot_db = []

        for lf1 in self.anomaly_dirs[:]:
            self.feature_list = []
            self.region_number = lf1.split('/')[0]
            self.project_number = lf1.split('/')[1]
            self.lineshot_name = lf1.split('/')[2].lower()
            self.lineshot_db.append(self.lineshot_name)
            self.run_number = lf1.split('/')[3]

            self.path_to_feature_level = '.'.join(
                ['combeval_dwh', self.region_number, self.project_number, self.lineshot_name, 'anomalies'])

            if pdw.levels.exists(self.path_to_feature_level):

                self.df_dcs_all_tmp = pd.DataFrame()
                self.df_feature_counts = pd.DataFrame()
                self.ctns_db = pd.DataFrame()
                self.feat_db = pd.DataFrame()
                self.feature_name_tmp = []
                self.feature_nr_tmp = []
                self.lf_comp = []

                self.df_dcs_all_tmp = pdw.get_pdw_datacubes_catalog(pdw, self.path_to_feature_level)
                print('self.path_to_feature_level: ', self.path_to_feature_level)
                # IMPORTANT: Usage of list comprehension reduces the time from 3-4min to several seconds...!!!

                self.lf_comp = [x for x in self.df_dcs_all_tmp['dirname'] if len(x.split('.')) > 5]
                self.feature_name_tmp = [x.split('.')[-2] for x in self.lf_comp]
                self.feature_nr_tmp = [x.split('.')[-1] for x in self.lf_comp]
                self.feat_db = pd.DataFrame((self.feature_name_tmp))
                self.ctns_db = pd.DataFrame((self.feature_nr_tmp))
                self.df_feature_counts = pd.concat([self.ctns_db, self.feat_db], axis=1)
                self.df_feature_counts.columns = list(['uploaded_ctns', 'features'])
                self.feature_list = list(self.df_feature_counts.features.unique())

                self.feature_counts = pd.DataFrame(
                    self.df_feature_counts.groupby(["features"], sort=False)["uploaded_ctns"].nunique())
                self.uploaded_counts = list(self.feature_counts['uploaded_ctns'])

                self.df_features_and_counts_single_lineshort = pd.DataFrame(
                    {'lineshort': self.lineshot_name, 'feature': self.feature_list, 'uploaded_ctn': self.uploaded_counts})

                self.feat_ctn_db_all = pd.concat([self.feat_ctn_db_all, self.df_features_and_counts_single_lineshort])

        # time_2 = datetime.datetime.now()
        # print(time_2.strftime("time_2: %H-%M-%S"))

        self.uploaded_feature_df = self.feat_ctn_db_all

        # print(tabulate(self.overview_available_features, headers='keys', tablefmt='psql'))

        for self.index_uploaded_feature_df, self.row_uploaded_feature_df in self.uploaded_feature_df.iterrows():
            for self.index_overview, self.row_overview in self.overview_available_features.iterrows():
                if (self.row_overview['lineshort'] == self.row_uploaded_feature_df['lineshort']) & (
                        self.row_overview['feature'] == self.row_uploaded_feature_df['feature']):
                    self.overview_available_features.loc[self.index_overview, 'uploaded_ctn'] = self.row_overview['ctn']

        self.overview_available_features = self.overview_available_features.fillna(0)
        print(tabulate(self.overview_available_features, headers='keys', tablefmt='psql'))
        self.overview_available_features.to_csv('overview_available_features.csv')
        # self.uploaded_feature_df.to_csv('uploaded_feature_df.csv')
        # self.overview_available_features.to_csv('overview_available_features.csv')
        # Now, the dataframe self.overview_available_features contains also
        # an additional column named "uploaded_ctn", which contained the uploaded counts of
        # every single feature, which have been read from the PDW directly...

        time_6 = datetime.datetime.now()
        print(time_6.strftime("time_6: %H-%M-%S"))

        self.print_message('Features for overview loaded')

    # Define the function, which will be executed, when a single line of the QListWidget is clicked
    def clicked_single_line(self, item):

        self.single_line_clicked = item.text()
        print('clicked line: ', self.single_line_clicked)
        self.remove_figure_available_feature_window()

        # Create a figure-handle for plotting...
        sns.set_style("darkgrid")
        self.figure_tmp_available_features = plt.Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1),
                                                        edgecolor=(0, 0, 0))
        self.add_figure_available_features_window(self.figure_tmp_available_features)
        self.axf1 = self.figure_tmp_available_features.add_subplot(111)

        # Filling the figure with the relevant informations...
        # That means: Configure the upper plot!

        self.counts = self.overview_available_features[self.overview_available_features['lineshort']
                                                       == self.single_line_clicked]['ctn']
        self.selected_features = self.overview_available_features[self.overview_available_features['lineshort']
                                                                  == self.single_line_clicked]['feature']
        clrs = ['lime' if (x != 0) else 'grey' for x in self.overview_available_features[
            self.overview_available_features['lineshort'] == self.single_line_clicked]['uploaded_ctn']]
        self.axf1.barh(self.selected_features, self.counts, color=clrs)
        self.max_of_counts = max(self.counts)
        self.max_x_lim = self.max_of_counts * 1.1
        self.axf1.set_xlim(0, self.max_x_lim)
        print('self.max of counts: \n', self.max_of_counts)
        print('self.max_x_lim: \n', self.max_x_lim)
        show_values_on_bars_v2(self.axf1, 'h', 0, self.max_of_counts, + 0.45)
        self.axf1.set_title(self.single_line_clicked)

        # Filling the figure with the relevant informations...
        # That means: Configure the lower plot!

        self.remove_figure_uploaded_feature_window()
        self.figure_tmp_uploaded_features = plt.Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1),
                                                       edgecolor=(0, 0, 0))
        self.add_figure_uploaded_features_window(self.figure_tmp_uploaded_features)
        self.axf2 = self.figure_tmp_uploaded_features.add_subplot(111)
        sns.set_style('darkgrid')

        self.uploaded_features_not_zero = self.overview_available_features[(self.overview_available_features[
            'lineshort'] == self.single_line_clicked) & (
                self.overview_available_features['uploaded_ctn'] != 0)]['feature']

        self.counts_not_zero = self.overview_available_features[(self.overview_available_features[
            'lineshort'] == self.single_line_clicked) & (
            self.overview_available_features['uploaded_ctn'] != 0)]['uploaded_ctn']

        if self.counts_not_zero.empty & self.uploaded_features_not_zero.empty:
            self.title_string = self.single_line_clicked + ' NO uploaded features'
            self.axf2.set_title(self.title_string)
            self.axf2.barh(0, 0, color=clrs)
            print(self.single_line_clicked, 'has no uploaded features')
        else:
            self.axf2.barh(self.uploaded_features_not_zero, self.counts_not_zero, color='lime')
            self.max_of_counts_not_zero = max(self.counts_not_zero)
            self.axf2.set_xlim(0, self.max_of_counts_not_zero * 1.1)
            self.title_string = 'Uploaded features into pdw of line ' + self.single_line_clicked
            self.axf2.set_title(self.title_string)
            show_values_on_bars_v2(self.axf2, 'h', 0, self.max_of_counts_not_zero, +0.45)

    def print_message(self, str_val):
        print('str_val: ', str_val)
        QMessageBox.information(self, "Done!", str_val)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowShowFeatureOverview()
    window.show()
    sys.exit(app.exec_())
