import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, 
    QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QMessageBox, QTabWidget
)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Qt GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main vertical layout for the central widget
        self.main_vertical_layout = QVBoxLayout(self.central_widget)

        # Create the tab widget and add two tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        self.main_vertical_layout.addWidget(self.tabs)

        # Set up the first tab
        self.setup_tab(self.tab1)
        # Set up the second tab
        self.setup_tab(self.tab2)

    def setup_tab(self, tab):
        tab_layout = QVBoxLayout(tab)

        # Create the layout for row, col, colspan and rowspan QLineEdit objects
        span_layout = QHBoxLayout()
        row_label = QLabel("Row:")
        self.row_edit = QLineEdit()
        col_label = QLabel("Col:")
        self.col_edit = QLineEdit()
        col_span_label = QLabel("Colspan:")
        self.col_span_edit = QLineEdit()
        row_span_label = QLabel("Rowspan:")
        self.row_span_edit = QLineEdit()
        span_layout.addWidget(row_label)
        span_layout.addWidget(self.row_edit)
        span_layout.addWidget(col_label)
        span_layout.addWidget(self.col_edit)
        span_layout.addWidget(col_span_label)
        span_layout.addWidget(self.col_span_edit)
        span_layout.addWidget(row_span_label)
        span_layout.addWidget(self.row_span_edit)
        tab_layout.addLayout(span_layout)

        # Create the grid layout for QGraphicsView widgets
        self.graphics_layout = QGridLayout()
        self.button = QPushButton("Add QGraphicsView")
        self.button.clicked.connect(self.add_graphics_view)
        tab_layout.addWidget(self.button)

        self.graphics_views = []  # List to hold added QGraphicsView widgets

        # Add the grid layout to the tab layout
        tab_layout.addLayout(self.graphics_layout)

        tab.setLayout(tab_layout)

    def add_graphics_view(self):
        graphics_view = QGraphicsView()
        scene = QGraphicsScene()
        scene.addText("Hello, QGraphicsView!")
        graphics_view.setScene(scene)

        # Get user-input values for row, col, colspan and rowspan
        row_text = self.row_edit.text()
        col_text = self.col_edit.text()
        col_span_text = self.col_span_edit.text()
        row_span_text = self.row_span_edit.text()

        # Determine row, col, colspan and rowspan, with default values
        try:
            row = int(row_text) if row_text else len(self.graphics_views)
            col = int(col_text) if col_text else 0
            colspan = int(col_span_text) if col_span_text else 1
            rowspan = int(row_span_text) if row_span_text else 1
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid integer values for row, col, colspan, and rowspan.")
            return

        self.graphics_layout.addWidget(graphics_view, row, col, rowspan, colspan)
        self.graphics_views.append(graphics_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
