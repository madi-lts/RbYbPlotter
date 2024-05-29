import sys
import io
from PyQt6.QtCore import Qt, QMimeData
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget,
    QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QLineEdit, QMessageBox, QTabWidget
)
from mpl_backend import *
import datetime

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, fig):
        super(MplCanvas, self).__init__(fig)

class ClickableGraphicsView(QGraphicsView):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.metadata_str = ''
        self.fig = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click(flag='left')
        elif event.button() == Qt.MouseButton.RightButton:
            self.on_click(flag='right')
        super().mousePressEvent(event)

    def on_click(self,flag='left'):
        clipboard = QApplication.clipboard()
        if flag=='left':
            buffer = io.BytesIO()
            self.fig.savefig(buffer)
            data_to_clipboard = QMimeData()
            data_to_clipboard.setText(self.metadata_str)
            data_to_clipboard.setImageData(QtGui.QImage.fromData(buffer.getvalue()))
            clipboard.setMimeData(data_to_clipboard)
        elif flag=='right':
            clipboard.setText(self.metadata_str)

        QMessageBox.information(self, "Clipboard", "Text copied to clipboard!")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ryj = RbYbJupyter()
        self.fig_list = []
        self.setWindowTitle("RbYb Plotter")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main vertical layout for the central widget
        self.main_vertical_layout = QVBoxLayout(self.central_widget)

        # Create the tab widget and add two tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Python Code")
        self.tabs.addTab(self.tab2, "Plots")

        self.main_vertical_layout.addWidget(self.tabs)

        # Initialize layouts for both tabs
        self.grid_layout_code = QGridLayout()
        self.grid_layout_plots = QGridLayout()

        # Set up the first tab
        self.setup_tab(self.tab1, self.grid_layout_code)
        # Set up the second tab
        self.setup_tab(self.tab2, self.grid_layout_plots)

        # Track the widgets added to each tab
        self.widgets_tab1 = []
        self.widgets_tab2 = []


    def update_ryj_params(self, base_path_edit, seq_name_edit, date_edit):
        self.ryj._base_path = base_path_edit.text()
        self.ryj._date = date_edit.text()
        self.ryj._seq_name = seq_name_edit.text()
        self.ryj.init_paths(self.ryj._base_path)

    def setup_tab(self, tab, layout):
        tab_layout = QVBoxLayout(tab)


        # Create the layout for row, col, colspan, and rowspan QLineEdit objects
        if tab == self.tab1: 
            base_path_edit = QLineEdit()
            base_path_edit.setText(r'/home/madi/RbYbTweezers/Data/2024/05/2024-05-15-Rb_slow_MOT_ramp')
            tab_layout.addWidget(QLabel('Base path:'))
            tab_layout.addWidget(base_path_edit)

            ryj_params_layout = QHBoxLayout()
            # Sequence name
            ryj_params_layout.addWidget(QLabel('Sequence name:'))
            seq_name_edit = QLineEdit()
            seq_name_edit.setText('Rb_slow_MOT_ramp')
            ryj_params_layout.addWidget(seq_name_edit)
            # Date
            ryj_params_layout.addWidget(QLabel('Date:'))
            date_edit = QLineEdit()
            date_edit.setText(str(datetime.date.today()).replace('-','/'))
            ryj_params_layout.addWidget(date_edit)
            tab_layout.addLayout(ryj_params_layout)

            self.update_ryj_button = QPushButton('Update MPL Params')
            self.update_ryj_button.clicked.connect(lambda: self.update_ryj_params(base_path_edit,seq_name_edit,date_edit))
            tab_layout.addWidget(self.update_ryj_button)

            span_layout = QHBoxLayout()
            row_edit = QLineEdit()
            col_edit = QLineEdit()
            col_span_edit = QLineEdit()
            row_span_edit = QLineEdit()
            span_layout.addWidget(QLabel("Row:"))
            span_layout.addWidget(row_edit)
            span_layout.addWidget(QLabel("Col:"))
            span_layout.addWidget(col_edit)
            span_layout.addWidget(QLabel("Colspan:"))
            span_layout.addWidget(col_span_edit)
            span_layout.addWidget(QLabel("Rowspan:"))
            span_layout.addWidget(row_span_edit)
            tab_layout.addLayout(span_layout)   

            # Add button to add widget
            self.add_plot_button = QPushButton("Add Plot")
            self.add_plot_button.clicked.connect(lambda: self.add_widget(tab, layout, row_edit, col_edit, col_span_edit, row_span_edit))
            tab_layout.addWidget(self.add_plot_button)

            self.run_code_button = QPushButton('Run Code')
            self.run_code_button.clicked.connect(lambda: self.run_plot_code())
            tab_layout.addWidget(self.run_code_button)

        # Add the grid layout to the tab layout
        tab_layout.addLayout(layout)

        tab.setLayout(tab_layout)

    def add_widget(self, tab, layout, row_edit, col_edit, col_span_edit, row_span_edit):
        row_text = row_edit.text()
        col_text = col_edit.text()
        col_span_text = col_span_edit.text()
        row_span_text = row_span_edit.text()

        try:
            row = int(row_text) if row_text else 0
            col = int(col_text) if col_text else 0
            colspan = int(col_span_text) if col_span_text else 1
            rowspan = int(row_span_text) if row_span_text else 1
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid integer values for row, col, colspan, and rowspan.")
            return

        self.add_graphics_view_to_layout(layout, row, col, rowspan, colspan)
        self.widgets_tab2.append((row, col, rowspan, colspan))
        self.update_tab(self.tab1, self.grid_layout_code, self.widgets_tab1, self.widgets_tab2)

        self.add_plain_text_edit_to_layout(layout, row, col, rowspan, colspan)
        self.widgets_tab1.append((row, col, rowspan, colspan))
        self.update_tab(self.tab2, self.grid_layout_plots, self.widgets_tab2, self.widgets_tab1)

    def add_plain_text_edit_to_layout(self, layout, row, col, rowspan, colspan):
        plain_text_edit = QPlainTextEdit()
        plain_text_edit.setPlainText("Write your Python code here...")
        layout.addWidget(plain_text_edit, row, col, rowspan, colspan)

    def add_graphics_view_to_layout(self, layout, row, col, rowspan, colspan):
        graphics_view = ClickableGraphicsView()
        scene = QGraphicsScene()
        scene.addText("Hello, QGraphicsScene!")
        graphics_view.setScene(scene)
        layout.addWidget(graphics_view, row, col, rowspan, colspan)

    def update_tab(self, tab, layout, widgets_source, widgets_target):
        # Clear existing widgets
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)
        
        # Add widgets to target tab
        for widget in widgets_source:
            row, col, rowspan, colspan = widget
            if tab == self.tab1:
                self.add_plain_text_edit_to_layout(layout, row, col, rowspan, colspan)
            elif tab == self.tab2:
                self.add_graphics_view_to_layout(layout, row, col, rowspan, colspan)

    def run_plot_code(self):
        self.update_ryj_button.click()
        self.fig_list = []
        for i in range(self.grid_layout_code.count()):
            print(i)
            plot_cell_code = self.grid_layout_code.itemAt(i).widget().toPlainText()
            
            local_variables = {}
            exec(plot_cell_code, {'self': self}, local_variables)
            canvas = MplCanvas(local_variables['fig'])
            self.fig_list.append(canvas)
            graphics_view = self.grid_layout_plots.itemAt(i).widget()
            graphics_view.fig = local_variables['fig']
            scene = graphics_view.scene()
            scene.addWidget(self.fig_list[-1])
            self.grid_layout_plots.itemAt(i).widget().show()
            graphics_view.metadata_str = local_variables['metadata']




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

"""
x = 'manual_scan'
y = 'Rb_MOT_time'
scans = [31,32,33,34,35,36,37,38,39]
plot_var_list = ['Andor_image_SHOT_LYSE__ODT_amp_fit']
metadata_var_list = ['Rb_MOT_current_zgrad']
metadata, fig = self.ryj.plot(scans, [x,y], plot_var_list, metadata_var_list, figsize=(6,4))
"""