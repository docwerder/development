import sys
import os
from typing import Optional, Dict, List
import pathlib
import json


from PySide2.QtCore import Signal as pyqtSignal
# import progressbar_QThread

from PySide2 import QtCore
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QListWidget,
    QPushButton, QCheckBox, QFrame, QScrollArea,
    QWidget, QMainWindow, QLineEdit, QLabel, QFileDialog, QMessageBox
)

# Important: the next two lines have to be imported after the Pyside2 imports.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# import xarray as xr  # important: has to be imported after FigureCanvas-import
import pandas as pd


from emat_mfl_combined.applications.pdw_upload.analysis_tools.path2proj import Path2ProjAnomaliesGeneral
from emat_mfl_combined.applications.pdw_upload.analysis_tools.pdw_tools import joerg_pdw_py_wc
# from pdw_py.data.datacubes import DataCubeError
# from emat_mfl_combined.applications.pdw_upload.gui_utils.dlgWindow import show_dialog as show_dialog

# Define the import of own-written functions
from emat_mfl_combined.applications.pdw_upload.pdw.pdw_manual_edition.utilities_functions.load_and_normalize_df import (
    load_and_normalize_df

)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class WindowShowFeatureSignals(QMainWindow):
    def __init__(self, x_pos_parent_window, y_pos_parent_window, width_parent_window):
        super().__init__()
        self.x_pos_parent_window = x_pos_parent_window
        self.y_pos_parent_window = y_pos_parent_window
        self.width_pos_parent_window = width_parent_window
        # self.setFixedWidth(600)
        self.setWindowTitle("My Layout of Show feature signals manual edition!")
        self.move(200, 20)
        self.resize(2000, 1150)

        self.patch_dir = None
        # #############################################
        #  Define the layout
        # #############################################

        # Create the complete layout
        self.complete_layout = QVBoxLayout()

        # Layout for label and Rosen_logo
        self.label_pic_layout = QHBoxLayout()

        # Define label for header and Rosen_logo
        self.lbl_feature_overview = QLabel("Show Feature Signals - Manual edition! edited")
        self.lbl_feature_overview.setStyleSheet("font-size: 18px;" "color: rgb(44, 44, 126);")
        self.lbl_rosen_logo = QLabel("Rosen logo")
        self.pixmap = QPixmap("rosen_logo.png")
        print('size of picturew: ', self.lbl_rosen_logo.size() / 2)
        scaled = self.pixmap.scaled(self.lbl_rosen_logo.size() / 4, QtCore.Qt.KeepAspectRatio)
        self.lbl_rosen_logo.setPixmap(scaled)
        self.lbl_rosen_logo.setScaledContents(False)

        # Fill the label_pic_layout
        self.label_pic_layout.addWidget(self.lbl_feature_overview)
        self.label_pic_layout.addStretch()
        self.label_pic_layout.addWidget(self.lbl_rosen_logo)

        # Define layout for horizontal line
        self.hor_line_1_layout = QHBoxLayout()
        self.hor_line_1_layout.addWidget(QHLine())

        # Define layout for load_btn
        self.load_xarray_btn_layout = QHBoxLayout()

        # Define widgets
        self.btn_load_anomalies_dir = QPushButton("Load xarray")
        self.lbl_anomalies_dir = QLineEdit("...")

        # Fill the layout with the widgets
        self.load_xarray_btn_layout.addWidget(self.btn_load_anomalies_dir)
        self.load_xarray_btn_layout.addWidget(self.lbl_anomalies_dir)

        # Define layout for horizontal line
        self.hor_line_2_layout = QHBoxLayout()
        self.hor_line_2_layout.addWidget(QHLine())

        # Define the label for chosen anomaly_dir:
        self.lbl_chosen_anomaly_dir_layout = QHBoxLayout()

        # Define the widgets within layout
        lineshort_name = ""  # TODO: Define the correct variable for lineshort_name
        self.lbl_chosen_anomaly_dir = QLabel("Available anomalies within the line: " + lineshort_name)
        self.lbl_chosen_anomaly_dir.setStyleSheet("font-size: 16px;" "color: rgb(44, 44, 126);")
        # Fill the layout with the widget
        self.lbl_chosen_anomaly_dir_layout.addWidget(self.lbl_chosen_anomaly_dir)

        # Define layout for horizontal line
        self.hor_line_3_layout = QHBoxLayout()
        self.hor_line_3_layout.addWidget(QHLine())

        self.general_vbox_layout = QVBoxLayout()
        # Define the layout, in which teh QFrame, nc-display and feature_signal are located
        self.qframe_nc_signals_display_layout = QHBoxLayout()

        self.layout_frame_left = QVBoxLayout()
        self.btn_show_anom_types = QPushButton("Show anomalies...")
        self.layout_left = QHBoxLayout()

        # Define layout for apply and cancel buttons
        self.btn_bar_layout = QHBoxLayout()
        self.evaluate_button = QPushButton("Apply/Evaluate...")
        self.cancel_button = QPushButton("Cancel...")

        # Fill the layout
        self.btn_bar_layout.addWidget(self.evaluate_button)
        self.btn_bar_layout.addWidget(self.cancel_button)

        self.layout_frame_right = QVBoxLayout()
        self.btn_show_all_features = QPushButton("Window of ALL feature signals")
        self.lbl_all_features_of_line = QLabel("Features of line: ")
        self.list_single_features = QListWidget()

        # Locate the QFrame and nc_display into the left layout
        # self.qframe = QFrame()
        # self.frame_for_scrollarea_left = MyFrame()
        # self.frame_total_left = self.frame_for_scrollarea_left.vbox
        # self.frame_for_scrollarea_left.setLayout(self.frame_total_left)

        self.frame_for_scrollarea = None
        self.scrolling_area_left = QScrollArea()
        self.scrolling_area_left.setWidgetResizable(True)
        # self.layout_left.addWidget(self.scrolling_area_left)

        # Define the right site
        # self.frame_for_scrollarea_right = MyFrame()
        # self.frame_total_right = self.frame_for_scrollarea_right.vbox
        # self.frame_for_scrollarea_right.setLayout(self.frame_total_right)
        # self.scrolling_area_right = QScrollArea()
        # self.scrolling_area_right.setWidgetResizable(True)

        # self.frame_for_scrollarea_right = QFrame() # orig
        # self.frame_for_scrollarea_right.setStyleSheet('background-color: grey;') # orig

        self.layout_frame_right.addWidget(self.btn_show_all_features)
        self.layout_frame_right.addWidget(self.lbl_all_features_of_line)
        self.layout_frame_right.addWidget(self.list_single_features)

        self.layout_frame_left.addWidget(self.btn_show_anom_types)
        self.layout_frame_left.addWidget(self.scrolling_area_left, stretch=1)
        self.layout_frame_left.addLayout(self.btn_bar_layout)

        # Define layout for horizontal line
        self.hor_line_4_layout = QHBoxLayout()
        self.hor_line_4_layout.addWidget(QHLine())

        self.layout_frame_left.addLayout(self.hor_line_4_layout)
        self.layout_frame_left.addLayout(self.layout_frame_right, stretch=1)

        # self.layout_right.addWidget(self.frame_for_scrollarea_right, stretch=1) # orig
        # self.layout_right.addWidget(self.scrolling_area_right)

        self.btn_show_anom_types.clicked.connect(self.show_frame_left)

        # Define the right side for displaying the feature signals.
        # self.layout_right = QHBoxLayout() # orig

        self.layout_right = QGridLayout()

        self.qwidget_echof = QWidget()
        self.qwidget_echof.setStyleSheet('background-color: rgb(44, 44, 126);')
        self.layout_echof = QVBoxLayout()
        self.layout_echof.addWidget(self.qwidget_echof)

        self.qwidget_echot = QWidget()
        self.qwidget_echot.setStyleSheet('background-color: rgb(44, 44, 126);')
        self.layout_echot = QVBoxLayout()
        self.layout_echot.addWidget(self.qwidget_echot)

        self.qwidget_tranf = QWidget()
        self.qwidget_tranf.setStyleSheet('background-color: rgb(44, 44, 126);')
        self.layout_tranf = QVBoxLayout()
        self.layout_tranf.addWidget(self.qwidget_tranf)

        self.qwidget_pth = QWidget()
        self.qwidget_pth.setStyleSheet('background-color: rgb(44, 44, 126);')
        self.layout_pth = QVBoxLayout()
        self.layout_pth.addWidget(self.qwidget_pth)

        # Fill the QGridLayout
        self.layout_right.addWidget(self.qwidget_echof, 0, 0)
        self.layout_right.addWidget(self.qwidget_echot, 0, 1)
        self.layout_right.addWidget(self.qwidget_tranf, 1, 0)
        self.layout_right.addWidget(self.qwidget_pth, 1, 1)

        # Define an fill the left and right layout into the complete layout..
        self.qframe_nc_signals_display_layout.addLayout(self.layout_frame_left, stretch=20)
        self.qframe_nc_signals_display_layout.addLayout(self.layout_frame_right, stretch=20)
        self.qframe_nc_signals_display_layout.addLayout(self.layout_right, stretch=100)

        # Locate the QFrame and nc_display into the left layout
        # self.nc_display = QPlainTextEdit()

        # Fill the complete_layout
        self.complete_layout.addLayout(self.label_pic_layout)
        self.complete_layout.addLayout(self.hor_line_1_layout)
        self.complete_layout.addLayout(self.load_xarray_btn_layout)
        self.complete_layout.addLayout(self.hor_line_2_layout)
        self.complete_layout.addLayout(self.lbl_chosen_anomaly_dir_layout)
        self.complete_layout.addLayout(self.hor_line_3_layout)
        self.complete_layout.addLayout(self.qframe_nc_signals_display_layout)
        # Define the overall layout in which the nc-files and signals are pasted..
        # As part of the vbox layout....

        # Set the hand-made complete layout in a superordinate QWidget called dummy_widget
        dummy_widget = QWidget()

        dummy_widget.setLayout(self.complete_layout)
        self.setCentralWidget(dummy_widget)

        # #############################################
        #  End of Definition the layout
        # #############################################

        # #############################################
        #  Define signals and slots
        # #############################################

        self.btn_load_anomalies_dir.clicked.connect(self.load_level_anomaly)
        self.btn_show_all_features.clicked.connect(self.show_window_all_feature_signals)
        self.list_single_features.itemClicked.connect(self.single_feature_clicked)

        # #############################################
        #  End of Definition of signals and slots
        # #############################################

    def load_level_anomaly(self):

        self.patch_dir = QFileDialog.getExistingDirectory(
            parent=None,
            caption="Select Patch save directory (xarray-dir)",
            directory="",
        )

        if self.patch_dir == "":
            return

        self.exchange_file, self.filtered_exchange_file = load_and_normalize_df(self.patch_dir)

        self.exchange_file_anom_types = list(self.exchange_file["type"].unique())
        print('loaded anom_types: ', self.exchange_file_anom_types)
        self.counts_anom_types = self.exchange_file["type"].value_counts()

        self.current_nc_index = 0
        self.current_filtered_index = 0
        self.max_number_of_features = len(self.filtered_exchange_file)
        # self.anom_type_filter_frame.enabling_mapping = None
        p = Path2ProjAnomaliesGeneral(self.patch_dir)

        self.text_string_csv_file = f"" \
                                    f"exchange_with_anomcenter.csv file for \n " \
                                    f"{p.lineshort_name} has been loaded  has been loaded!"

        self.path_anomaly_label = pathlib.Path(self.patch_dir) / "anomalies"
        self.path_project_anomalies_dir = self.path_anomaly_label
        self.level_anomalies_label = '.'.join(
            ['combeval_dwh', p.region_number, p.project_number, p.lineshort_name, 'anomalies']
        )

        self.lbl_anomalies_dir.setText(self.patch_dir)
        msg = r'anom_types of of line {} have been loaded!'.format(p.lineshort_name)

        self.show_anomalies_within_dir_new()
        self.print_message(msg)

    def print_message(self, str_val):
        QMessageBox.information(self, "Done!", str_val)

    def show_anomalies_within_dir_new(self):

        self.len_anomalies = [
            len(files) for root, dirs, files in os.walk(self.path_project_anomalies_dir, topdown=False)
        ]
        self.anomalies = [dirs for root, dirs, files in os.walk(self.path_project_anomalies_dir)]

        self.max_count_anomalies = len(self.len_anomalies) - 1
        self.anomalies_list = [x.lower() for x in self.anomalies[0]]

        self.anomalies_list_immutable = []
        self.anomalies_list_immutable = tuple(self.anomalies_list)

        p = Path2ProjAnomaliesGeneral(self.patch_dir)
        self.lbl_chosen_anomaly_dir.setText('Available features within the line:' + p.lineshort_name)

    def show_frame_left(self):

        if self.frame_for_scrollarea is None:

            self.frame_for_scrollarea = AnomTypeFilterFrame_for_scrollarea(parent=self)
            self.frame_for_scrollarea.filter_anom_types_signal.connect(self.set_filtered_exchange_file)
            self.evaluate_button.clicked.connect(self.frame_for_scrollarea.display_chosen_anom_types)
            # self.frame_for_scrollarea.show()
            self.frame_for_scrollarea.set_existing_anom_types(self.exchange_file_anom_types)
            self.frame_for_scrollarea.counts_anom_types = self.counts_anom_types
            self.frame_for_scrollarea.path_anomaly_label = self.path_anomaly_label
            self.frame_for_scrollarea.patch_dir = self.patch_dir
            # self.frame_for_scrollarea.level_anomalies_label = self.level_anomalies_label
            # self.frame_for_scrollarea.chose_pdw_server = self.chose_pdw_server
            # self.frame_for_scrollarea.output_terminal = self.output_terminal
            # self.frame_for_scrollarea.calculation_terminal = self.calculation_terminal
            self.frame_for_scrollarea.init_ui()
            # self.layout = self.frame_for_scrollarea.layout
            # self.frame_for_scrollarea.setLayout(self.layout)
            self.gorgo = self.frame_for_scrollarea.anom_types_layout
            self.frame_for_scrollarea.setLayout(self.gorgo)

            self.scrolling_area_left.setWidget(self.frame_for_scrollarea)

        else:
            self.frame_for_scrollarea.hide()
            self.frame_for_scrollarea = None

    def set_filtered_exchange_file(self, chosen_anom_types: List[str]) -> None:

        # self.list_single_features.clear()
        print('Debug NEW...')
        server = "https://pdw-lin.roseninspection.net/pdw-emat"  # the adress of the server
        self.pdw = joerg_pdw_py_wc.connect(server)
        print('chosen_anom_types: ', chosen_anom_types)

        self.list_single_features.clear()
        for level_anom_type in chosen_anom_types:
            tmp_level_single_anomaly = ".".join([self.level_anomalies_label, level_anom_type])

            if not self.pdw.levels.exists(tmp_level_single_anomaly):
                continue
            else:

                tmp_chosen_single_feature_list = self.pdw.get_level_list(tmp_level_single_anomaly)
                tmp_list_single_features = [x.split(".")[-1] for x in tmp_chosen_single_feature_list]

                self.list_single_features.addItem('== ' + level_anom_type + ' ==')

                self.list_single_features.setStyleSheet('color: green;')
                [self.list_single_features.addItem(x) for x in tmp_list_single_features]
                self.list_single_features.setStyleSheet('color: blue;')

        """Reduces the loaded exchange file to the current chosen anomaly types"""

        self.filtered_exchange_file = self.exchange_file[self.exchange_file["type"].isin(chosen_anom_types)]
        self.filtered_exchange_file = self.filtered_exchange_file.reset_index()
        self.max_number_of_features = len(self.filtered_exchange_file)

    # def pdw_server_changed(self):
    #     self.actual_chosen_pdw_server = "https://pdw-lin.roseninspection.net/pdw-emat"
    #     print('self.actual_chosen_pdw_server: ', self.actual_chosen_pdw_server)

    def single_feature_clicked(self, item):
        # ?? Think about a new function??
        # First: Implement the code within this function...

        self.single_feature = item.text()
        print('Clicked self.single_feature: ', self.single_feature)

        server = "https://pdw-lin.roseninspection.net/pdw-emat"  # the adress of the server
        pdw = joerg_pdw_py_wc.connect(server)
        df_cat = pdw.catalog.find(f"filetype eq datacube and startswith(filename,'{self.single_feature}_')")
        if len(df_cat) == 0:
            print('no corresponding level found')
            return ''

        parts = list(set(df_cat['dirname']))[0].split(".")[:-1]
        self.level_single_anomaly = '.'.join(parts)

        self.clicked_level_single_feature = ".".join([self.level_single_anomaly, self.single_feature])

        self.props_clicked_single_feature = pdw.levels.get_props(self.clicked_level_single_feature)

        new_attr = {}
        for lf in self.props_clicked_single_feature.keys():
            value = self.props_clicked_single_feature[lf]
            try:
                obj = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                obj = value
            new_attr[lf] = obj

        temp = []
        dictList = []
        for key, value in new_attr.items():
            temp = [key, value]
            dictList.append(temp)

        # flatten of the two-dimensional list:
        self.flat_list = [c for sublist in dictList for c in sublist]
        # print('self.flat_list: ', self.flat_list)
        # self.attributes_single_feature.clear()
        # [self.attributes_single_feature.addItem(str(x)) for x in self.flat_list]

        p = Path2ProjAnomaliesGeneral(self.patch_dir)
        self.returned_datacube_echof = pdw.datacubes.get(self.clicked_level_single_feature,
                                                         self.clicked_level_single_feature.split('.')[-1] + '_echof'
                                                         )

        self.logdistance = pdw.datacubes.get(self.clicked_level_single_feature,
                                             self.clicked_level_single_feature.split('.')[-1] + '_logdistance'
                                             )

        self.z_axis = pdw.datacubes.get(self.level_anomalies_label, p.lineshort_name + '_z_axis')

        self.data_echof = self.returned_datacube_echof[:]
        self.data_logdistance = self.logdistance[:]
        self.data_z_axis = self.z_axis[:]

        # ECHOT
        self.returned_datacube_echot = pdw.datacubes.get(self.clicked_level_single_feature,
                                                         self.clicked_level_single_feature.split('.')[-1] + '_echot'
                                                         )
        self.z_axis_echot = pdw.datacubes.get(self.level_anomalies_label, p.lineshort_name + '_z_axis_echot')

        self.data_echot = self.returned_datacube_echot[:]
        self.data_z_axis_echot = self.z_axis_echot[:]

        # TRANF

        self.returned_datacube_tranf = pdw.datacubes.get(self.clicked_level_single_feature,
                                                         self.clicked_level_single_feature.split('.')[-1] + '_tranf'
                                                         )

        self.data_tranf = self.returned_datacube_tranf[:]

        # PTH
        if pdw.datacubes.exists(self.clicked_level_single_feature,
                                self.clicked_level_single_feature.split('.')[-1]
                                + '_pth_offset_corrected'):
            self.returned_datacube_pth = pdw.datacubes.get(self.clicked_level_single_feature,
                                                           self.clicked_level_single_feature.split('.')[-1]
                                                           + '_pth_offset_corrected')
            self.logdistance_pth_offset_corrected = \
                pdw.datacubes.get(self.clicked_level_single_feature,
                                  self.clicked_level_single_feature.split('.')[-1]
                                  + '_logdistance_pth_offset_corrected')
            self.angle_pth_offset_corrected = \
                pdw.datacubes.get(self.clicked_level_single_feature,
                                  self.clicked_level_single_feature.split('.')[-1]
                                  + '_angle_pth_offset_corrected')

            # self.returned_datacube_pth = pdw.datacubes.get('combeval_dwh.proj0.15990.30160jam.anomalies.plin.625044', '625044_pth_offset_corrected')
            # self.pth_logd_axis = pdw.datacubes.get('combeval_dwh.proj0.15990.30160jam.anomalies.plin.625044', '625044_pth-logd-axis')
            # self.pth_circ_axis = pdw.datacubes.get('combeval_dwh.proj0.15990.30160jam.anomalies.plin.625044', '625044_pth-circ-axis')

            self.data_pth = self.returned_datacube_pth[:]
            self.data_logdistance_pth_offset_corrected = self.logdistance_pth_offset_corrected[:]
            self.data_angle_pth_offset_corrected = self.angle_pth_offset_corrected[:]

        self.signal_dict = {}

        # Filling the signal_dict....
        self.signal_dict['ECHOF'] = (self.data_echof, self.data_logdistance, self.data_z_axis)
        self.signal_dict['ECHOT'] = (self.data_echot, self.data_logdistance, self.data_z_axis_echot)
        self.signal_dict['TRANF'] = (self.data_tranf, self.data_logdistance, self.data_z_axis)
        if pdw.datacubes.exists(self.clicked_level_single_feature,
                                self.clicked_level_single_feature.split('.')[-1] + '_pth_offset_corrected'):
            self.signal_dict['PTH_OFFSET_CORRECTED'] = (
                self.data_pth, self.data_logdistance_pth_offset_corrected, self.data_angle_pth_offset_corrected
            )
        self.show_window_all_feature_signals(self.signal_dict, self.single_feature)
        print('END: Debug function...?!')

    def show_window_all_feature_signals(self, signal_dict, actual_value):

        self.create_layout_echof(signal_dict, actual_value)
        self.create_layout_echot(signal_dict, actual_value)
        self.create_layout_tranf(signal_dict, actual_value)
        self.create_layout_pth(signal_dict, actual_value)

    def create_layout_echof(self, signal_dict, actual_value):
        if self.qwidget_echof.layout():
            QWidget().setLayout(self.qwidget_echof.layout())

        self.layout_echof = QGridLayout()
        # Code below not necessary, because the with the self.qwidget_echof.layout()
        # ONLY the subwidget layout of the qwidet_echof is deleted, not the qwidget itself!!
        # self.qwidget_echof = QWidget()
        self.fig_tmp_echof = plt.Figure()
        self.canvas = FigureCanvas(self.fig_tmp_echof)
        ax1f1_echof = self.fig_tmp_echof.add_subplot(111)
        data_echof = signal_dict['ECHOF'][0]
        data_logd_axis = signal_dict['ECHOF'][1]
        data_z_axis = signal_dict['ECHOF'][2]
        ax1f1_echof.grid(color='w')
        self.echof_plot = ax1f1_echof.imshow(data_echof[::-1, :], cmap='jet', aspect='auto', interpolation='bicubic',
                                             extent=[data_logd_axis[0], data_logd_axis[-1], data_z_axis[0],
                                                     data_z_axis[-1]])

        self.fig_tmp_echof.colorbar(self.echof_plot)
        title_string_echof = str(actual_value) + ' - ECHOF signal'
        ax1f1_echof.set_title(title_string_echof)

        self.layout_echof.addWidget(self.canvas)
        self.qwidget_echof.setLayout(self.layout_echof)

        # below Code serves as an example
        # import random
        # ax1f1_echof = self.fig_tmp_echof.add_subplot(111)
        # t = np.arange(0.0, 1.0, 0.01)
        # s = np.sin(2 * np.pi * t + random.random())
        # ax1f1_echof.plot(t, s, lw=2)
        # ax1f1_echof.grid(color='k')

    def create_layout_echot(self, signal_dict, actual_value):
        if self.qwidget_echot.layout():
            QWidget().setLayout(self.qwidget_echot.layout())

        self.layout_echot = QGridLayout()
        # Code below not necessary, because the with the self.qwidget_echof.layout()
        # ONLY the subwidget layout of the qwidet_echof is deleted, not the qwidget itself!!
        # self.qwidget_echof = QWidget()
        self.fig_tmp_echot = plt.Figure()
        self.canvas = FigureCanvas(self.fig_tmp_echot)
        ax1f1_echot = self.fig_tmp_echot.add_subplot(111)

        data_echot = signal_dict['ECHOT'][0]
        data_logd_axis = signal_dict['ECHOT'][1]
        data_echot_z_axis = signal_dict['ECHOT'][2]

        ax1f1_echot.grid(color='w')
        #self.echot_plot = ax1f1_echot.imshow(data_echot.T[::-1, :], cmap='jet', aspect='auto', interpolation='bicubic',
        #                                     extent=[data_logd_axis[0], data_logd_axis[-1], data_echot_z_axis[0],
        #                                             data_echot_z_axis[-1]])
        self.echot_plot = ax1f1_echot.imshow(data_echot[::-1, :], cmap='jet', aspect='auto', interpolation='bicubic',
                                             extent=[data_logd_axis[0], data_logd_axis[-1], data_echot_z_axis[0],
                                                     data_echot_z_axis[-1]])

        self.fig_tmp_echot.colorbar(self.echot_plot)
        title_string_echot = str(actual_value) + ' - ECHOT signal'
        ax1f1_echot.set_title(title_string_echot)
        self.layout_echot.addWidget(self.canvas)
        self.qwidget_echot.setLayout(self.layout_echot)
        # import random
        # ax1f1_echot = self.fig_tmp_echot.add_subplot(111)
        # t = np.arange(0.0, 1.0, 0.01)
        # s = np.sin(2 * np.pi * t + random.random())
        # ax1f1_echot.plot(t, s, lw=2)
        # ax1f1_echot.grid(color='y')

    def create_layout_tranf(self, signal_dict, actual_value):
        if self.qwidget_tranf.layout():
            QWidget().setLayout(self.qwidget_tranf.layout())

        self.layout_tranf = QGridLayout()
        # Code below not necessary, because the with the self.qwidget_echof.layout()
        # ONLY the subwidget layout of the qwidet_echof is deleted, not the qwidget itself!!
        # self.qwidget_echof = QWidget()
        self.fig_tmp_tranf = plt.Figure()
        self.canvas = FigureCanvas(self.fig_tmp_tranf)
        ax1f1_tranf = self.fig_tmp_tranf.add_subplot(111)

        data_tranf = signal_dict['TRANF'][0]
        data_logd_axis = signal_dict['TRANF'][1]
        data_z_axis = signal_dict['TRANF'][2]

        ax1f1_tranf.grid(color='w')
        # self.tranf_plot = ax1f1_tranf.imshow(data_tranf.T[::-1, :], cmap='jet', aspect='auto', interpolation='bicubic', extent=[data_logd_axis[0], data_logd_axis[-1], data_z_axis[0], data_z_axis[-1]])
        self.tranf_plot = ax1f1_tranf.imshow(data_tranf[::-1, :], cmap='jet', aspect='auto', interpolation='bicubic',
                                             extent=[data_logd_axis[0], data_logd_axis[-1], data_z_axis[0],
                                                     data_z_axis[-1]])

        self.fig_tmp_tranf.colorbar(self.tranf_plot)
        title_string_tranf = str(actual_value) + ' - TRANF signal'
        ax1f1_tranf.set_title(title_string_tranf)

        self.layout_tranf.addWidget(self.canvas)
        self.qwidget_tranf.setLayout(self.layout_tranf)

    def create_layout_pth(self, signal_dict, actual_value):
        if self.qwidget_pth.layout():
            QWidget().setLayout(self.qwidget_pth.layout())

        self.layout_pth = QGridLayout()

        # Code below not necessary, because the with the self.qwidget_echof.layout()
        # ONLY the subwidget layout of the qwidet_echof is deleted, not the qwidget itself!!
        # self.qwidget_echof = QWidget()
        self.fig_tmp_pth = plt.Figure()
        if "PTH_OFFSET_CORRECTED" in signal_dict.keys():
            self.canvas = FigureCanvas(self.fig_tmp_pth)
            ax1f1_pth = self.fig_tmp_pth.add_subplot(111)

            ax1f1_pth.grid(color='b')

            data_pth = signal_dict['PTH_OFFSET_CORRECTED'][0]
            data_pth_logd_axis = signal_dict['PTH_OFFSET_CORRECTED'][1]
            data_circ_logd_axis = signal_dict['PTH_OFFSET_CORRECTED'][2]
            #self.pth_plot = ax1f1_pth.imshow(data_pth.T[::-1, :], cmap='jet', aspect='auto',
            #                                 extent=[data_pth_logd_axis[0], data_pth_logd_axis[-1],
            #                                         data_circ_logd_axis[0], data_circ_logd_axis[-1]])

            self.pth_plot = ax1f1_pth.imshow(data_pth[::-1, :], cmap='jet', aspect='auto',
                                             extent=[data_pth_logd_axis[0], data_pth_logd_axis[-1],
                                                     data_circ_logd_axis[0], data_circ_logd_axis[-1]])

            self.fig_tmp_pth.colorbar(self.pth_plot)
            title_string_pth = str(actual_value) + ' - PTH_OFFSET_CORRECTED signal'
            ax1f1_pth.set_title(title_string_pth)
            self.layout_pth.addWidget(self.canvas)
            self.qwidget_pth.setLayout(self.layout_pth)
        else:
            self.canvas = FigureCanvas(self.fig_tmp_pth)
            ax1f1_pth = self.fig_tmp_pth.add_subplot(111)
            ax1f1_pth.set_title('No AFD Data available!!!')
            self.layout_pth.addWidget(self.canvas)
            self.qwidget_pth.setLayout(self.layout_pth)

        self.layout_pth.addWidget(self.canvas)
        self.qwidget_pth.setLayout(self.layout_pth)


class AnomTypeFilterFrame_for_scrollarea(QFrame):
    """Overlay frame to set the current anomaly types to filter the exchange file on.

    Parameters
    ----------
    parent
        Parent widget in which this widget may be embedded into.
    """

    filter_anom_types_signal = pyqtSignal(list)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        style = """AnomTypeFilterFrame_for_scrollarea {
            border: 1px solid;
            background-color: white;
        }
        """
        self.setStyleSheet(style)

        self.existing_anom_types: List[str] = []
        self.chosen_anom_types: List[str] = []
        self.counts_anom_types = None

        self.checkboxes = []
        self.level_anomalies_label = None
        self.df_dcs = None
        # self.apply_button = QtWidgets.QPushButton("Apply/Eval...")
        # self.write_button = QtWidgets.QPushButton("Write...")
        # self.cancel_button = QtWidgets.QPushButton("Cancel ")
        # Optional[List[int]] <=> Union[List[int], None]
        # >> Mapping of my example: Optional[Dict[str, bool]] <=> Union[Dict[str, bool], None]
        # Default value has to be None, than the nomenclature Optional can be used!!

        self.enabling_mapping: Optional[Dict[str, bool]] = None

    def init_ui(self) -> None:
        """Initialize the ui."""
        # Reparent layout to create the new layout without any issues

        if self.layout():
            QWidget().setLayout(self.layout())

        if self.enabling_mapping is None:
            self.enabling_mapping = {}

            for anom_type in ["All"] + self.existing_anom_types:
                self.enabling_mapping[anom_type] = True

            self.enabling_mapping["None"] = False

        self.checkboxes = []

        self.layout = QVBoxLayout()
        self.anom_types_layout = QVBoxLayout()

        # load the corresponding level in the PDW
        # and display the levels (== anomalies) and counts
        # get the anomalies and counts in the dataframe: pdw_all_anom_with_ctns

        p = Path2ProjAnomaliesGeneral(self.patch_dir)

        self.level_anomalies_label = '.'.join(
            ['combeval_dwh', p.region_number, p.project_number, p.lineshort_name, 'anomalies'])

        server = "https://pdw-lin.roseninspection.net/pdw-emat"  # the adress of the server

        self.pdw = joerg_pdw_py_wc.connect(server)

        # no_levels_available = 0

        if not self.pdw.levels.exists(self.level_anomalies_label):

            # pdw_all_anom_with_ctns = pd.DataFrame(
            # {'pdw_anom': self.existing_anom_types, 'pdw_ctn': self.counts_anom_types}
            # )
            pdw_all_anom_with_ctns = pd.DataFrame(
                {'pdw_anom': self.existing_anom_types, 'pdw_ctn': 0}
            )
            print('pdw_all_anom_with_ctn_0: \n', pdw_all_anom_with_ctns)

        else:

            # = counts_in_level(
            #    self.pdw.get_level_list(self.level_anomalies_label, recursive=True)
            # )

            dirname_column_lineshot_tmp = self.pdw.get_pdw_datacubes_catalog(self.pdw, self.level_anomalies_label)
            dirname_column_lineshot = sorted(dirname_column_lineshot_tmp['dirname'].unique())
            keys_lineshot = set([".".join(v.split(".")[:-1]) for v in dirname_column_lineshot])
            dict_lineshot = {k: [] for k in sorted(keys_lineshot)}
            for level in dirname_column_lineshot:
                parts = level.split(".")
                key = ".".join(parts[:-1])
                value = parts[-1]
                dict_lineshot[key].append(value)

            count_lineshot = {k: len(dict_lineshot[k]) for k in dict_lineshot}
            count_lineshot.values()

            pdw_level_list_with_ctns = [list(count_lineshot.values())[1:], list(count_lineshot.keys())[1:]]

            print('pdw_level_list_with_ctns: ', pdw_level_list_with_ctns)
            print('type...:', type(pdw_level_list_with_ctns))
            pdw_anom_list = [lf.split(".")[-1].upper() for lf in pdw_level_list_with_ctns[1]]
            pdw_anom_list = ['pLS-IND' if lf == 'PLS-IND' else lf for lf in pdw_anom_list]
            pdw_anom_list = ['LS-pLIN' if lf == 'LS-PLIN' else lf for lf in pdw_anom_list]
            pdw_anom_list = ['pLIN' if lf == 'PLIN' else lf for lf in pdw_anom_list]

            print('pdw_anom_list: ', pdw_anom_list)

            pdw_all_anom_with_ctns = pd.DataFrame({'pdw_anom': pdw_anom_list, 'pdw_ctn': pdw_level_list_with_ctns[0]})

        print('after first pdw')
        # level_not_complete_with_datacubes = 0

        ################################################

        # Write the anomalies and counts of the linfile1-anomalies folder in a dataframe

        ctn_all = []

        for anom_type in ["All", "None"] + self.existing_anom_types:

            if anom_type == "All":
                ctn = sum(self.counts_anom_types)
                ctn_all.append(ctn)

            elif anom_type == "None":
                pass
            else:
                ctn = self.counts_anom_types[anom_type]
                ctn_all.append(ctn)

        all_anomalies_with_ctns = pd.DataFrame(
            {'lfile1_anom': ['All'] + self.existing_anom_types, 'lfile1_ctn': ctn_all})

        df_merged = all_anomalies_with_ctns.merge(pdw_all_anom_with_ctns, "outer", left_on="lfile1_anom",
                                                  right_on="pdw_anom")
        df_merged['pdw_ctn'] = df_merged['pdw_ctn'].fillna(0).astype(int)
        df_merged['pdw_anom'] = df_merged['pdw_anom'].fillna("")
        del (df_merged['pdw_anom'])
        df_merged.columns = ['anom', 'lfile1_ctn', 'pdw_ctn']
        # print('df_merged: \n ', df_merged)
        df_merged.to_dict("records")
        df_merged['uploaded'] = df_merged['pdw_ctn'].apply(lambda x: x > 0)
        df_uploaded_anom = dict(zip(df_merged['anom'], df_merged['uploaded']))
        print('df_uploaded_anom: \n', df_uploaded_anom)
        #####################################################

        # ctn_all = []

        self.df_dcs = self.pdw.get_pdw_datacubes_catalog(self.pdw, self.level_anomalies_label)
        # level_not_complete = []
        level_not_fully_complete = []

        for my_anom_type in ["All", "None"] + self.existing_anom_types:
            if (my_anom_type != "All") & (my_anom_type != "None"):
                level_single_anomaly = '.'.join([self.level_anomalies_label, my_anom_type.lower()])

                if self.pdw.levels.exists(level_single_anomaly):
                    level_single_feature = self.pdw.get_level_list(level_single_anomaly)

                    for single_feature in level_single_feature:
                        dcs_in_single_feature = self.df_dcs[self.df_dcs["dirname"] == single_feature]
                        ctn_complete = len(dcs_in_single_feature)

                        if (ctn_complete != 13) & (ctn_complete != 9):
                            level_not_fully_complete.append(single_feature)

        # print('dcs_in_level_db: ', level_not_complete)

        for anom_type in ["All", "None"] + self.existing_anom_types:

            if anom_type == "All":
                ctn = sum(self.counts_anom_types)
                ctn_label = " (CTN = " + str(ctn) + ")"
            elif anom_type == "None":
                ctn_label = ""
            else:
                ctn = self.counts_anom_types[anom_type]
                ctn_label = " (CTN = " + str(ctn) + ")"

            anom_type_checkbox = QCheckBox(anom_type + ctn_label)

            checkbox_content = anom_type_checkbox.text().split(" ")[0]
            print('checkbox_content: ', checkbox_content)

            if (checkbox_content == "None") or (checkbox_content == "All"):
                anom_type_checkbox.setStyleSheet("color: green")

            elif not df_uploaded_anom[checkbox_content]:
                anom_type_checkbox.setStyleSheet("color: red")

            elif df_uploaded_anom[checkbox_content]:
                dcs_not_complete = any(
                    [lf for lf in level_not_fully_complete if f".anomalies.{checkbox_content}.".lower() in lf.lower()]
                )
                print('dcs_not_complete:', dcs_not_complete)

                if dcs_not_complete:
                    anom_type_checkbox.setStyleSheet("color: orange")
                else:
                    anom_type_checkbox.setStyleSheet("color: green")

            anom_type_checkbox.setChecked(self.enabling_mapping[anom_type])
            anom_type_checkbox.clicked.connect(self.toggle_anom_type)
            self.anom_types_layout.addWidget(anom_type_checkbox)
            self.checkboxes.append(anom_type_checkbox)

        self.layout.addLayout(self.anom_types_layout)
        # button_layout = QHBoxLayout()
        # Definition of Buttons will be inside the __init__ function of the class
        # NO!!! Above line leads to an error during the additional call of the frame!!
        # Therefore the definition is here!
        self.evaluate_button = QPushButton("Evaluate...")
        self.write_button = QPushButton("Write...")
        self.cancel_button = QPushButton("Cancel ")
        # self.apply_button.clicked.connect(self.emit_chosen_anom_types)

        self.evaluate_button.clicked.connect(self.display_chosen_anom_types)
        self.write_button.clicked.connect(self.write_to_pdw_function)
        self.cancel_button.clicked.connect(self.cancel_to_pdw_function)
        # button_layout.addWidget(self.evaluate_button)
        # button_layout.addWidget(self.write_button)
        # button_layout.addWidget(self.cancel_button)

        # layout.addLayout(button_layout)
        self.setLayout(self.layout)
        self.setMinimumHeight(25 * (2 + len(self.existing_anom_types)) + 30)
        # print('Debug after self.existing_anom_types')
        mm = []

        for lf in self.existing_anom_types:
            mm.append(len(lf))
        self.setMinimumWidth(25 * (max(mm)) + 10)

        self.show()

    def set_existing_anom_types(self, anom_types: List[str]) -> None:
        """Sets the existing anomaly types for this frame. The input will be sorted.

        Parameters
        ----------
        anom_types
            List of anomaly types, e.g. ["LIN", "MIFE"]
        """
        self.existing_anom_types = sorted(anom_types)
        print('self.existing_anom_types: ', self.existing_anom_types)

    def emit_chosen_anom_types(self) -> None:
        """Emits the chosen anomaly types"""
        self.hide()

        self.chosen_anom_types: List[str] = []

        for anom_type in ["All", "None"] + self.existing_anom_types:
            is_checked = self.enabling_mapping[anom_type]

            if is_checked and anom_type not in {"All", "None"}:
                self.chosen_anom_types.append(anom_type)

        self.filter_anom_types_signal.emit(self.chosen_anom_types)

    def display_chosen_anom_types(self) -> None:
        """Emits the chosen anomaly types"""
        # self.hide()
        print('going into the NEW display_chose_anom_types function!!!!')
        self.chosen_anom_types: List[str] = []

        for anom_type in ["All", "None"] + self.existing_anom_types:
            is_checked = self.enabling_mapping[anom_type]

            if is_checked and anom_type not in {"All", "None"}:
                self.chosen_anom_types.append(anom_type)

        print('chosen_anom_types: \n', self.chosen_anom_types)
        self.ctn_total = sum(self.counts_anom_types[self.chosen_anom_types])
        print('ctn_total = ', str(self.ctn_total))
        self.filter_anom_types_signal.emit(self.chosen_anom_types)

        print('end apply/eval function...')

    def write_to_pdw_function(self) -> None:
        """Writes the single features of the chosen single anomalies into pdw"""
        self.hide()

        self.chosen_anom_types: List[str] = []

        for anom_type in ["All", "None"] + self.existing_anom_types:
            is_checked = self.enabling_mapping[anom_type]

            if is_checked and anom_type not in {"All", "None"}:
                self.chosen_anom_types.append(anom_type)

        self.filter_anom_types_signal.emit(self.chosen_anom_types)

        print('chosen_anom_types within the write_to_pdw_function: \n', self.chosen_anom_types)

    def cancel_to_pdw_function(self) -> None:
        self.hide()

    def toggle_anom_type(self, state: bool) -> None:
        """Check or uncheck the clicked checkbox and update other checkboxes if needed.

        Since there is an "All" and a "None" checkbox, there is some update logic needed to
        check or uncheck other checkboxes.

        Parameters
        ----------
        state
            True if the checkbox has been checked, False otherwise
        """
        print('before clicked ....')
        clicked_anom_type = self.sender().text().split(" ")[0]
        print('clicked .. ', clicked_anom_type)

        if clicked_anom_type == "All":
            ctn = sum(self.counts_anom_types)
            print('ctn: ', ctn)
        elif clicked_anom_type == "None":
            ctn = 0
            print('ctn: ', str(ctn))

        else:
            print('ctn: ', self.counts_anom_types[clicked_anom_type])

        if state is True:
            if clicked_anom_type == "All":
                for anom_type in ["All"] + self.existing_anom_types:
                    self.enabling_mapping[anom_type] = True

                self.enabling_mapping["None"] = False

            elif clicked_anom_type == "None":
                for anom_type in ["All"] + self.existing_anom_types:
                    self.enabling_mapping[anom_type] = False

                self.enabling_mapping["None"] = True

            else:
                self.enabling_mapping[clicked_anom_type] = True

                all_enabled = True

                for anom_type in self.existing_anom_types:
                    if self.enabling_mapping[anom_type] is False:
                        all_enabled = False
                        break

                self.enabling_mapping["All"] = all_enabled
                self.enabling_mapping["None"] = False

        elif state is False:
            if clicked_anom_type == "All":
                for anom_type in ["All"] + self.existing_anom_types:
                    self.enabling_mapping[anom_type] = False

                self.enabling_mapping["None"] = True
            elif clicked_anom_type == "None":
                for anom_type in ["All"] + self.existing_anom_types:
                    self.enabling_mapping[anom_type] = True

                self.enabling_mapping["None"] = False
            else:
                self.enabling_mapping[clicked_anom_type] = False
                self.enabling_mapping["All"] = False

                none_enabled = True

                for anom_type in self.existing_anom_types:
                    if self.enabling_mapping[anom_type] is True:
                        none_enabled = False
                        break

                self.enabling_mapping["None"] = none_enabled

        else:
            raise ValueError(f"State {state} is not valid.")

        for anom_type, checkbox in zip(["All", "None"] + self.existing_anom_types, self.checkboxes):
            is_checked = self.enabling_mapping[anom_type]
            checkbox.setChecked(is_checked)

        if self.enabling_mapping["None"] is True:
            self.evaluate_button.setEnabled(False)
        else:
            self.evaluate_button.setEnabled(True)


class MyFrame(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        style = """MyFrame {
            border: 1px solid;
            background-color: green;
            }
            """
        self.setStyleSheet(style)
        self.vbox = QVBoxLayout()
        # self.frame_total = QVBoxLayout()
        # self.frame_total.addLayout(self.vbox)
        for i in range(1, 50):
            object = QCheckBox("Label inside Class")
            self.vbox.addWidget(object)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowShowFeatureSignals(200, 500, 1000)
    window.show()
    sys.exit(app.exec_())
