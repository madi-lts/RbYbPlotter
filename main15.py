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
        self.setup_tab(self.tab1, "Tab 1")
        # Set up the second tab
        self.setup_tab(self.tab2, "Tab 2")

    def setup_tab(self, tab, tab_name):
        tab_layout = QVBoxLayout(tab)

        # Create the layout for row, col, colspan and rowspan QLineEdit objects
        span_layout = QHBoxLayout()
        self.row_edit = QLineEdit()
        self.col_edit = QLineEdit()
        self.col_span_edit = QLineEdit()
        self.row_span_edit = QLineEdit()

        span_layout.addWidget(QLabel("Row:"))
        span_layout.addWidget(self.row_edit)
        span_layout.addWidget(QLabel("Col:"))
        span_layout.addWidget(self.col_edit)
        span_layout.addWidget(QLabel("Colspan:"))
        span_layout.addWidget(self.col_span_edit)
        span_layout.addWidget(QLabel("Rowspan:"))
        span_layout.addWidget(self.row_span_edit)
        tab_layout.addLayout(span_layout)

        # Create the grid layout for QGraphicsView widgets
        graphics_layout = QGridLayout()
        button = QPushButton("Add QGraphicsView")
        button.clicked.connect(lambda: self.add_graphics_view(graphics_layout, graphics_layout_2, self.row_edit, self.col_edit, self.col_span_edit, self.row_span_edit))
        tab_layout.addWidget(button)

        # Add the grid layout to the tab layout
        tab_layout.addLayout(graphics_layout)

        tab.setLayout(tab_layout)

        if tab_name == "Tab 1":
            self.graphics_layout_1 = graphics_layout
        elif tab_name == "Tab 2":
            self.graphics_layout_2 = graphics_layout

    def add_graphics_view(self, layout1, layout2, row_edit, col_edit, col_span_edit, row_span_edit):
        row_text = row_edit.text()
        col_text = col_edit.text()
        col_span_text = col_span_edit.text()
        row_span_text = row_span_edit.text()

        try:
            row = int(row_text) if row_text else 0
            col = int(col_text) if col_text else max(layout1.columnCount(), layout2.columnCount())
            colspan = int(col_span_text) if col_span_text else 1
            rowspan = int(row_span_text) if row_span_text else 1
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid integer values for row, col, colspan, and rowspan.")
            return

        self.add_graphics_view_to_layout(layout1, row, col, rowspan, colspan)
        self.add_graphics_view_to_layout(layout2, row, col, rowspan, colspan)

    def add_graphics_view_to_layout(self, layout, row, col, rowspan, colspan):
        graphics_view = QGraphicsView()
        scene = QGraphicsScene()
        scene.addText("Hello, QGraphicsView!")
        graphics_view.setScene(scene)
        layout.addWidget(graphics_view, row, col, rowspan, colspan)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
